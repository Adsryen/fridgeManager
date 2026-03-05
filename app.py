# -*- coding: utf-8 -*-
from flask import *
import json
import os
import sqlite3
import uuid
import secrets
from dataclasses import dataclass
from datetime import datetime
from auth import hash_password, verify_password, login_required, get_current_user_id, get_current_username

def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)

def _to_iso_z(dt: any) -> str | None:
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    raise TypeError(f'Unsupported date type: {type(dt)}')

@dataclass
class _InsertOneResult:
    inserted_id: str

@dataclass
class _UpdateResult:
    modified_count: int

@dataclass
class _DeleteResult:
    deleted_count: int

class _Admin:
    def command(self, name: str) -> dict[str, any]:
        if name == 'ping':
            return {'ok': 1}
        raise ValueError(f'Unsupported command: {name}')

class SQLiteCollection:
    def __init__(self, conn: sqlite3.Connection, table: str):
        self._conn = conn
        self._table = table

    def _row_to_doc(self, row: sqlite3.Row) -> dict[str, any]:
        doc = {'_id': row['_id']}
        for key in row.keys():
            if key != '_id':
                doc[key] = row[key]
        return doc

    def _build_where(self, query: dict[str, any] | None) -> tuple[str, list[any]]:
        if not query:
            return '', []

        clauses: list[str] = []
        params: list[any] = []
 
        for k, v in query.items():
            if isinstance(v, dict):
                if '$regex' in v:
                    pattern = str(v['$regex'])
                    clauses.append(f"{k} LIKE ?")
                    params.append(f"%{pattern}%")
                elif '$gte' in v:
                    clauses.append(f"{k} >= ?")
                    params.append(_to_iso_z(v['$gte']))
                elif '$lt' in v:
                    clauses.append(f"{k} < ?")
                    params.append(_to_iso_z(v['$lt']))
                else:
                    raise ValueError(f'Unsupported query operator for {k}: {v}')
            else:
                clauses.append(f"{k} = ?")
                params.append(v)

        if not clauses:
            return '', []
        return ' WHERE ' + ' AND '.join(clauses), params

    def find(self, query: dict[str, any] | None = None) -> list[dict[str, any]]:
        where, params = self._build_where(query)
        cur = self._conn.execute(
            f"SELECT * FROM {self._table}{where}",
            params,
        )
        rows = cur.fetchall()
        return [self._row_to_doc(r) for r in rows]

    def find_one(self, query: dict[str, any]) -> dict[str, any] | None:
        where, params = self._build_where(query)
        cur = self._conn.execute(
            f"SELECT * FROM {self._table}{where} LIMIT 1",
            params,
        )
        row = cur.fetchone()
        return self._row_to_doc(row) if row else None

    def insert_one(self, doc: dict[str, any]) -> _InsertOneResult:
        _id = doc.get('_id')
        if not _id:
            _id = uuid.uuid4().hex
        
        # 动态构建插入语句
        fields = ['_id']
        values = [_id]
        placeholders = ['?']
        
        for k, v in doc.items():
            if k == '_id':
                continue
            fields.append(k)
            
            # 特殊处理日期和数字
            if k == 'ExpireDate':
                v = _to_iso_z(v)
            elif k == 'Num':
                try:
                    v = int(v) if v is not None else None
                except Exception:
                    pass
            
            values.append(v)
            placeholders.append('?')
        
        sql = f"INSERT INTO {self._table} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
        self._conn.execute(sql, values)
        self._conn.commit()
        return _InsertOneResult(inserted_id=_id)

    def update_one(self, query: dict[str, any], update: dict[str, any]) -> _UpdateResult:
        if '$set' not in update:
            raise ValueError('Only $set update is supported')
        fields: Dict[str, Any] = update['$set']

        sets: list[str] = []
        params: list[any] = []
        for k, v in fields.items():
            if k == 'ExpireDate':
                v = _to_iso_z(v)
            if k == 'Num':
                try:
                    v = int(v) if v is not None else None
                except Exception:
                    pass
            sets.append(f"{k} = ?")
            params.append(v)

        where, where_params = self._build_where(query)
        params.extend(where_params)

        cur = self._conn.execute(
            f"UPDATE {self._table} SET {', '.join(sets)}{where}",
            params,
        )
        self._conn.commit()
        return _UpdateResult(modified_count=cur.rowcount)

    def delete_one(self, query: dict[str, any]) -> _DeleteResult:
        doc = self.find_one(query)
        if not doc:
            return _DeleteResult(deleted_count=0)

        cur = self._conn.execute(
            f"DELETE FROM {self._table} WHERE _id = ?",
            (doc['_id'],),
        )
        self._conn.commit()
        return _DeleteResult(deleted_count=cur.rowcount)

    def delete_many(self, query: dict[str, any] | None = None) -> _DeleteResult:
        where, params = self._build_where(query)
        cur = self._conn.execute(
            f"DELETE FROM {self._table}{where}",
            params,
        )
        self._conn.commit()
        return _DeleteResult(deleted_count=cur.rowcount)

class SQLiteDatabase:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self.item = SQLiteCollection(conn, 'item')
        self.user = SQLiteCollection(conn, 'user')

class SQLiteMongoLikeClient:
    def __init__(self, db_dir: str):
        self._db_dir = db_dir
        self._connections: dict[str, sqlite3.Connection] = {}
        self.admin = _Admin()

    def _db_path(self, db_name: str) -> str:
        filename = f'{db_name}.db'
        return os.path.join(self._db_dir, filename)

    def _get_connection(self, db_name: str) -> sqlite3.Connection:
        path = self._db_path(db_name)
        if path in self._connections:
            return self._connections[path]

        _ensure_parent_dir(path)
        conn = sqlite3.connect(path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        
        # 创建 item 表
        conn.execute(
            "CREATE TABLE IF NOT EXISTS item ("
            "_id TEXT PRIMARY KEY, "
            "user_id TEXT NOT NULL, "
            "Name TEXT, "
            "ExpireDate TEXT, "
            "Place TEXT, "
            "Num INTEGER, "
            "Type TEXT"
            ")"
        )
        
        # 创建 user 表
        conn.execute(
            "CREATE TABLE IF NOT EXISTS user ("
            "_id TEXT PRIMARY KEY, "
            "username TEXT UNIQUE NOT NULL, "
            "email TEXT UNIQUE NOT NULL, "
            "password_hash TEXT NOT NULL, "
            "salt TEXT NOT NULL, "
            "created_at TEXT NOT NULL"
            ")"
        )
        
        # 创建索引
        conn.execute("CREATE INDEX IF NOT EXISTS idx_item_user_id ON item(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_item_expire ON item(ExpireDate)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_user_username ON user(username)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_user_email ON user(email)")
        
        conn.commit()
        self._connections[path] = conn
        return conn

    def __getattr__(self, name: str) -> SQLiteDatabase:
        conn = self._get_connection(name)
        return SQLiteDatabase(conn)

    def close(self) -> None:
        for conn in list(self._connections.values()):
            try:
                conn.close()
            except Exception:
                pass
        self._connections.clear()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return _to_iso_z(o)
        return json.JSONEncoder.default(self, o)

_DEFAULT_DB_DIR = os.environ.get(
    'SQLITE_DB_DIR',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'),
)
client = SQLiteMongoLikeClient(db_dir=_DEFAULT_DB_DIR)
_ = client.fridge

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

@app.route('/')
@login_required
def index():
    return render_template('template.html', username=get_current_username())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    if not username or not email or not password:
        return jsonify({'error': '所有字段都必须填写'}), 400
    
    db = client.fridge
    
    # 检查用户名是否已存在
    if db.user.find_one({'username': username}):
        return jsonify({'error': '用户名已存在'}), 400
    
    # 检查邮箱是否已存在
    if db.user.find_one({'email': email}):
        return jsonify({'error': '邮箱已被注册'}), 400
    
    # 创建用户
    password_hash, salt = hash_password(password)
    user = {
        '_id': uuid.uuid4().hex,
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'salt': salt,
        'created_at': datetime.now().isoformat()
    }
    
    db.user.insert_one(user)
    
    # 自动登录
    session['user_id'] = user['_id']
    session['username'] = username
    
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    db = client.fridge
    user = db.user.find_one({'username': username})
    
    if not user or not verify_password(password, user['password_hash'], user['salt']):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    session['user_id'] = user['_id']
    session['username'] = user['username']
    
    next_url = request.args.get('next')
    if next_url:
        return redirect(next_url)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/insert', methods = ['POST'])
@login_required
def insert():
    db = client.fridge
    user_id = get_current_user_id()
    try:
        date = request.values['itemDate']
        date = date.replace('-', '')
        ITEM = {
            "_id": uuid.uuid4().hex,
            "user_id": user_id,
            "Name": request.values['itemName'],
            "ExpireDate": datetime.strptime(date, "%Y%m%d"),
            "Place": request.values['itemPlace'],
            "Num": request.values['itemNum'],
            "Type": request.values['itemType'],
        }
        db.item.insert_one(ITEM)
    except Exception:
        pass
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    searchbox = request.form.get('text')
    user_id = get_current_user_id()
    db = client.fridge
    if not searchbox:
        ITEM = db.item.find({'user_id': user_id})
    else:
        ITEM = db.item.find({'user_id': user_id, 'Name': {'$regex': searchbox}})
    return jsonify(list(ITEM))

@app.route('/stateok/<time>', methods=['GET', 'POST'])
@login_required
def stateok(time):
    db = client.fridge
    user_id = get_current_user_id()
    date = datetime.fromtimestamp(int(time)/1000.0)
    y = date.year
    m = date.month
    d = date.day
    ITEM = db.item.find({'user_id': user_id, 'ExpireDate': {"$gte": datetime(y,m,d)}})
    return jsonify(list(ITEM))

@app.route('/statebad/<time>', methods=['GET', 'POST'])
@login_required
def statebad(time):
    db = client.fridge
    user_id = get_current_user_id()
    date = datetime.fromtimestamp(int(time)/1000.0)
    y = date.year
    m = date.month
    d = date.day
    ITEM = db.item.find({'user_id': user_id, 'ExpireDate': {"$lt": datetime(y,m,d)}})
    return jsonify(list(ITEM))

@app.route('/cold', methods=['GET', 'POST'])
@login_required
def cold():
    db = client.fridge
    user_id = get_current_user_id()
    ITEM = db.item.find({'user_id': user_id, 'Place': 'cold'})
    return jsonify(list(ITEM))

@app.route('/frozer', methods=['GET', 'POST'])
@login_required
def frozer():
    db = client.fridge
    user_id = get_current_user_id()
    ITEM = db.item.find({'user_id': user_id, 'Place': 'frozer'})
    return jsonify(list(ITEM))

@app.route('/tag/<tagName>', methods=['GET', 'POST'])
@login_required
def tag(tagName):
    db = client.fridge
    user_id = get_current_user_id()
    ITEM = db.item.find({'user_id': user_id, 'Type': tagName})
    return jsonify(list(ITEM))

@app.route('/total', methods=['GET', 'POST'])
@login_required
def total():
    db = client.fridge
    user_id = get_current_user_id()
    ITEM = db.item.find({'user_id': user_id})
    return jsonify(list(ITEM)) 

@app.route("/delete/<_id>", methods=['POST'])
@login_required
def delete(_id):
    db = client.fridge
    user_id = get_current_user_id()
    db.item.delete_one({'_id': _id, 'user_id': user_id})
    return '', 200

@app.route('/getone/<_id>', methods=['GET', 'POST'])
@login_required
def getone(_id):
    db = client.fridge
    user_id = get_current_user_id()
    ITEM = db.item.find({'_id': _id, 'user_id': user_id})
    return jsonify(list(ITEM)) 

@app.route("/edit/<_id>", methods=['POST'])
@login_required
def edit(_id):
    db = client.fridge
    user_id = get_current_user_id()
    try:
        date = request.values['itemDate']
        date = date.replace('-', '')
        update = {
            'Name': request.values['itemName'],
            "ExpireDate": datetime.strptime(date, "%Y%m%d"),
            "Place": request.values['itemPlace'],
            "Num": request.values['itemNum'],
            "Type": request.values['itemType'],
        }
        db.item.update_one({'_id': _id, 'user_id': user_id}, {'$set': update})
    except Exception:
        pass
    return redirect(url_for('index'))

if __name__ == "__main__":
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '8080'))
    debug = os.environ.get('DEBUG', '').lower() in ('1', 'true', 'yes', 'y')
    app.run(host=host, debug=debug, port=port)