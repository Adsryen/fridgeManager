from flask import *
from pymongo import MongoClient
import uuid
from bson.objectid import ObjectId
from datetime import datetime
import pprint
from functools import wraps

client = MongoClient(host="localhost", port=27017)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/insert', methods = ['POST'])
def insert():
    db = client.fridge
    date = request.values['itemDate']
    date =date.replace('-', '')
    ITEM = {"_id": uuid.uuid4().hex, "Name": request.values['itemName'], "ExpireDate": datetime.strptime(date,"%Y%m%d"),"Place": request.values['itemPlace'], "Num": request.values['itemNum'],"Type": request.values['itemType']}
    db.item.insert_one(ITEM)
    # return jsonify(ITEM), 200
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    searchbox = request.form.get('text')
    db = client.fridge
    ITEM = db.item.find({'Name': {'$regex': searchbox}})
    return jsonify(list(ITEM))

@app.route('/stateok/<time>', methods=['GET', 'POST'])
def stateok(time):
    db = client.fridge
    date = datetime.fromtimestamp(int(time)/1000.0)
    y = date.year
    m = date.month
    d = date.day
    ITEM = db.item.find({'ExpireDate': {"$gte": datetime(y,m,d)}})
    return jsonify(list(ITEM))

@app.route('/statebad/<time>', methods=['GET', 'POST'])
def statebad(time):
    db = client.fridge
    date = datetime.fromtimestamp(int(time)/1000.0)
    y = date.year
    m = date.month
    d = date.day
    ITEM = db.item.find({'ExpireDate': {"$lt": datetime(y,m,d)}})
    return jsonify(list(ITEM))

@app.route('/cold', methods=['GET', 'POST'])
def cold():
    db = client.fridge
    ITEM = db.item.find({'Place': 'cold'})
    return jsonify(list(ITEM))

@app.route('/frozer', methods=['GET', 'POST'])
def frozer():
    db = client.fridge
    ITEM = db.item.find({'Place': 'frozer'})
    return jsonify(list(ITEM))

@app.route('/tag/<tagName>', methods=['GET', 'POST'])
def tag(tagName):
    db = client.fridge
    ITEM = db.item.find({'Type': tagName})
    return jsonify(list(ITEM))

@app.route('/total', methods=['GET', 'POST'])
def total():
    db = client.fridge
    ITEM = db.item.find()
    return jsonify(list(ITEM)) 

@app.route("/delete/<_id>", methods=['POST'])
def delete(_id):
    db = client.fridge
    db.item.delete_one({'_id': _id})

@app.route('/getone/<_id>', methods=['GET', 'POST'])
def getone(_id):
    db = client.fridge
    ITEM = db.item.find({'_id': _id})
    return jsonify(list(ITEM)) 


@app.route("/edit/<_id>", methods=['POST'])
def edit(_id):
    _id = _id
    db = client.fridge
    date = request.values['itemDate']
    date =date.replace('-', '')
    update = {'Name': request.values['itemName'], "ExpireDate": datetime.strptime(date,"%Y%m%d"), "Place": request.values['itemPlace'], "Num": request.values['itemNum'],"Type": request.values['itemType']}
    db.item.update_one({'_id': _id}, {'$set': update})
    # return 'id ' + str(_id) +  ' Name '+ request.values['itemName']+ " ExpireDate "+request.values['itemDate'] + " Num " + request.values['itemNum'] + " Type "+ request.values['itemType']
    return redirect(url_for('index'))

if __name__ == "__main__":

    app.run(host="127.0.0.1", debug=True, port=8080)