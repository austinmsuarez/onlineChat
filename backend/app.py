from flask import Flask, request, render_template, g, jsonify,Response
from flask_basicauth import BasicAuth
import json
import sqlite3
import time, datetime


app = Flask(__name__)

# Sets the path of the database
DATABASE = './data.db'

# Connects to the database
def get_db():
  db = getattr(g, '_database', None)
  if db is None:
       db = g._database = sqlite3.connect(DATABASE)
  return db

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d

#initializes the data base using flask
def init_db():
  with app.app_context():
      db = get_db()
      with app.open_resource('init.sql', mode='r') as f:
          db.cursor().executescript(f.read())
      db.commit()
  print("*********************\nDATABASE INITALIZED\n*********************")

#connects to DB
def get_connections():
  conn = get_db()
  conn.row_factory = dict_factory
  cur = conn.cursor()
  return cur

init_db()

#########################################
# myAuthorizor:
# param: takes in BasicAuth
# uses:  used to override the check_credentials to check the Database
# for authorized users
#########################################

class myAuthorizor(BasicAuth):
  def check_credentials(self, username, password):
    valid = False
    conn = get_connections()
    data = conn.execute('SELECT * FROM auth_users').fetchall()
    for entry in data:
      if entry["username"] == username and entry["password"] == password:
        valid = True
    return valid
    
def valid_username(newUsername):
  conn = get_connections()
  data = conn.execute('SELECT * FROM auth_users').fetchall()
  validNewUser = True
  for user in data:
    if user["username"] == newUsername:
      validNewUser = False
  return validNewUser


#########################################
# GETs
#########################################
@app.route("/messageList",methods=['GET'])
def getMessageList():
    b_auth = myAuthorizor()
    db = get_db()
    db.row_factory = dict_factory
    conn = db.cursor()

    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']

    if b_auth.check_credentials(username, password):
      myMessageList = conn.execute('SELECT * FROM message_list WHERE userSender = ? OR userRecieve = ?', (username,username))
      print(myMessageList)
      #returns a success response
      return jsonify(myMessageList)


@app.route("/messageList/<username>/<messageID>", methods=['GET'])
def getMessages(username,messageID):
    b_auth = myAuthorizor()
    db = get_db()
    db.row_factory = dict_factory
    conn = db.cursor()

    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']

    if b_auth.check_credentials(username, password):
        myMessageList = conn.execute('SELECT * FROM messages WHERE messageID = ?', (messageID))

#########################################
# POSTs
#########################################
@app.route("/signup", methods=['POST'])
def addUser():
    db = get_db()
    db.row_factory = dict_factory
    conn = db.cursor()

    req_data = request.get_json()
    newUser = req_data['username']
    newPass = req_data['password']

    if valid_username(newUser):
      conn.execute('INSERT INTO auth_users(username,password) VALUES(\''+newUser+'\',\''+ newPass+'\')')
      db.commit()
      #returns a success response
      response = Response("HTTP 201 Created",201,mimetype = 'application/json')
    else:
      #returns a success response
      response = Response("HTTP 409 Conflict if username already exists\n",409,mimetype = 'application/json')
    return response

@app.route("/messageList/<username>",methods=['POST'])
def newMessageList(username):
    
    b_auth = myAuthorizor()
    db = get_db()
    db.row_factory = dict_factory
    conn = db.cursor()

    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']

    convoTitle = req_data['convoTitle']
    convoPreview = req_data['convoPreview']
    timeUpdate = req_data['timeUpdate']
    userSender = req_data['userSender']
    userFrom = req_data['userFrom']
    
    #checks to see if user has proper auth
    if b_auth.check_credentials(username, password):
      conn.execute('INSERT INTO message_list(convoTitle, convoPreview, timeUpdate, userSender, userFrom) VALUES(?,?,?,?)',(convoTitle,convoPreview,timeUpdate,userSender,userFrom))
      db.commit()
      #returns a success response
      response = Response("HTTP 201 Created",201,mimetype = 'application/json')
    
    else:
      #returns a success response
      response = Response("HTTP 409 Conflict if username already exists\n",409,mimetype = 'application/json')
    
    return response

@app.route("/messageList/<username>/<messageID>", methods=['POST'])
def newMessage(username,messageID):
    
    b_auth = myAuthorizor()
    db = get_db()
    db.row_factory = dict_factory
    conn = db.cursor()

    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']

    msg = req_data['msg']
    messageID = req_data['msgID']
    # Create the timestamp
    ts = time.time()
    time_stamp = st = datetime.datetime.fromtimestamp(ts).strftime('%a, %d %b %Y %H:%M:%S %Z')
    tmp = time_stamp + "GMT"
    time_stamp = datetime.datetime.strptime(tmp,'%a, %d %b %Y %H:%M:%S %Z')
    #checks to see if user has proper auth
    if b_auth.check_credentials(username, password):
       conn.execute('INSERT INTO messages(msg, msgID, timeUpdate) VALUES(?,?,?)',(msg, messageID,time_stamp))
       db.commit()
       response = Response("HTTP 201 Created\n", 201, mimetype = 'application/json')
    else:
          invalMsg = "HTTP 401 Not Authorized"
          response = Response(invalMsg, 404, mimetype = 'application/json')

@app.route("/login",methods=['POST'])
def getUserVerified():
    b_auth = myAuthorizor()
    db = get_db()
    db.row_factory = dict_factory
    conn = db.cursor()

    req_data = request.get_json()
    print(req_data)
    username = request.authorization['username']
    password = request.authorization['password']

    if b_auth.check_credentials(username, password):
        response = Response("HTTP 202 Accepted",202,mimetype = 'application/json')

    else:
        response = Response("HTTP 403 Forbidden",403,mimetype = 'application/json')
    return response

if __name__ == "__main__":
  app.run(debug=True)
