from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)


# python dict. store connected users. Key is  socket id, value is username and avtar url

users = {}

@app.route('/')
def index():
    return render_template('index.html')


# we are listening for the connect event
@socketio.on("connect")
def handle_connect():
    username = f"User_{random.randint(1000, 9999)}"
    # username = f"User_(random.randomint(1000, 9999))"
    gender = random.choice(["adventurer", "bottts", "micah"])
    
    avtar_url = f"https://api.dicebear.com/7.x/{gender}/svg?seed=User_123"
    
    users[request.sid] = {"username": username, "avtar": avtar_url}
    
    emit("user_joined", {"username": username, "avtar": avtar_url}, broadcast=True)
    
    emit("set_username", {"username": username})
    
    
    
@socketio.on("disconnect")
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        emit("user_left", {"username": user["username"]}, broadcast=True)
        
@socketio.on("send_message")
def handle_message(data):
    user = users.get(request.sid)
    if user:
        emit("new_message", {
            "username": user["username"],
            "avtar": user["avtar"],
            "message": data["message"]
        }, broadcast=True)
        
@socketio.on("update_username")
def handle_update_username(data):
    old_username = users[request.sid]["username"]
    new_username = data["username"]
    users[request.sid]["username"] = new_username
    
    emit("username_updated", {
        "old_username": old_username,
        "new_username": new_username
    }, broadcast=True)       
    
    
if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug=True)
