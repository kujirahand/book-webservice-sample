from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

# Socket.ioのセットアップ --- (※1)
socketio = SocketIO(app)

# MongoDBの接続先設定 --- (※2)
mongo_uri = "mongodb+srv://<接続文字列>"
client = MongoClient(mongo_uri)
db = client["SNS"]
messages_collection = db["messages"]

@app.route("/")
def index():
    return render_template("index.html")

# メッセージの読み込み --- (※3)
@socketio.on('load messages')
def load_messages():
    messages = messages_collection.find().sort('_id', -1).limit(10)
    messages = list(messages)[::-1]
    messages_return = [message['message'] for message in messages]
    # メッセージをクライアントへ送信 --- (※4)
    emit('load all messages', messages_return)

# メッセージの登録 --- (※5)
@socketio.on('send message')
def send_message(message):
    messages_collection.insert_one({'message': message})
    # メッセージをクライアントへ送信 --- (※6)
    emit('load one message', message, broadcast=True)


if __name__ == "__main__":
    # Socket.ioサーバーの起動 --- (※7)
    socketio.run(app, debug=True)
