import json

from flask import Flask, jsonify, make_response, render_template, request
from pusher import Pusher

app = Flask(__name__)

# configure pusher object


pusher = Pusher(
  app_id='978882',
  key='89df329c2036ddf6c93b',
  secret='a7ee958929bf53affb94',
  cluster='us2',
  ssl=True
)

##end point for main landing page with posting button
@app.route("/")
def home():
    return render_template("index.html")


##feed = {
#    event1= {"title": 'an event', "id": 1234, "description": 'something really cool'},
#    event2= { "title": 'another event', id: 5678, "description": 'something even cooler'}
#}

@app.route("/feed")
def feed():
    res = make_response(jsonify(feed))
    return res

# endpoint for storing todo item
@app.route('/add-todo', methods = ['POST'])
def addTodo():
    data = json.loads(request.data) # load JSON data from request
    pusher.trigger('todo', 'item-added', data) # trigger `item-added` event on `todo` channel
    return jsonify(data)

# endpoint for deleting todo item
@app.route('/remove-todo/<item_id>')
def removeTodo(item_id):
  data = {'id': item_id }
  pusher.trigger('todo', 'item-removed', data)
  return jsonify(data)

# endpoint for updating todo item
@app.route('/update-todo/<item_id>', methods = ['POST'])
def updateTodo(item_id):
  data = {
    'id': item_id,
    'completed': json.loads(request.data).get('completed', 0)
  }
  pusher.trigger('todo', 'item-updated', data)
  return jsonify(data)

# run Flask app in debug mode
app.run(debug=True)
    


#@app.route("/event")
#def event():
#    return render_template("event.hbs")
