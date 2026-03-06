# -*- coding: utf-8 -*-
"""数据库工具模块"""
import os
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime


def _ensure_parent_dir(path: str) -> None:
    """确保父目录存在"""
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)


def _to_iso_z(dt: any) -> str | None:
    """转换日期为 ISO 格式"""
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
    """SQLite 集合（表）操作类"""
    
    def __init__(self, conn: sqlite3.Connection, table: str):
        self._conn = conn
        self._table = table

    def _row_to_doc(self, row: sqlite3.Row) -> dict[str, any]:
        """将数据库行转换为字典"""
        doc = {'_id': row['_id']}
        for key in row.keys():
            if key != '_id':
                doc[key] = row[key]
        return doc

    def _build_where(self, query: dict[str, any] | None) -> tuple[str, list[any]]:
        """构建 WHERE 子句"""
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
        """查询多条记录"""
        where, params = self._build_where(query)
        cur = self._conn.execute(
            f"SELECT * FROM {self._table}{where}",
            params,
        )
        rows = cur.fetchall()
        return [self._row_to_doc(r) for r in rows]

    def find_one(self, query: dict[str, any]) -> dict[str, any] | None:
        """查询单条记录"""
        where, params = self._build_where(query)
        cur = self._conn.execute(
            f"SELECT * FROM {self._table}{where} LIMIT 1",
            params,
        )
        row = cur.fetchone()
        return self._row_to_doc(row) if row else None

    def insert_one(self, doc: dict[str, any]) -> _InsertOneResult:
        """插入一条记录"""
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
        """更新一条记录"""
        if '$set' not in update:
            raise ValueError('Only $set update is supported')
        fields = update['$set']

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
        """删除一条记录"""
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
        """删除多条记录"""
        where, params = self._build_where(query)
        cur = self._conn.execute(
            f"DELETE FROM {self._table}{where}",
            params,
        )
        self._conn.commit()
        return _DeleteResult(deleted_count=cur.rowcount)


class SQLiteDatabase:
    """SQLite 数据库类"""
    
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self.item = SQLiteCollection(conn, 'item')
        self.user = SQLiteCollection(conn, 'user')
        self.settings = SQLiteCollection(conn, 'settings')


class SQLiteMongoLikeClient:
    """类 MongoDB 的 SQLite 客户端"""
    
    def __init__(self, db_dir: str):
        self._db_dir = db_dir
        self._connections: dict[str, sqlite3.Connection] = {}
        self.admin = _Admin()

    def _db_path(self, db_name: str) -> str:
        """获取数据库文件路径"""
        filename = f'{db_name}.db'
        return os.path.join(self._db_dir, filename)

    def _get_connection(self, db_name: str) -> sqlite3.Connection:
        """获取数据库连接"""
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
            "created_at TEXT NOT NULL, "
            "is_admin INTEGER DEFAULT 0, "
            "is_active INTEGER DEFAULT 1"
            ")"
        )
        
        # 创建 settings 表
        conn.execute(
            "CREATE TABLE IF NOT EXISTS settings ("
            "_id TEXT PRIMARY KEY, "
            "user_id TEXT NOT NULL, "
            "notify_expiring INTEGER DEFAULT 1, "
            "notify_days INTEGER DEFAULT 3, "
            "items_per_page INTEGER DEFAULT 20, "
            "default_view TEXT DEFAULT 'all', "
            "profile_public INTEGER DEFAULT 0"
            ")"
        )
        
        # 创建索引
        conn.execute("CREATE INDEX IF NOT EXISTS idx_item_user_id ON item(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_item_expire ON item(ExpireDate)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_user_username ON user(username)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_user_email ON user(email)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_settings_user_id ON settings(user_id)")
        
        conn.commit()
        self._connections[path] = conn
        return conn

    def __getattr__(self, name: str) -> SQLiteDatabase:
        """动态获取数据库"""
        conn = self._get_connection(name)
        return SQLiteDatabase(conn)

    def close(self) -> None:
        """关闭所有连接"""
        for conn in list(self._connections.values()):
            try:
                conn.close()
            except Exception:
                pass
        self._connections.clear()
