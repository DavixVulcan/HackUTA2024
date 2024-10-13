from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_socketio import SocketIO, send
import device
import json

app = Flask(__name__,
    template_folder='BASE HTML'
    )

# Initialize Flask-SocketIO
socketio = SocketIO(app)

def heartrate_mon():
    while True:
        if device.get_heartrate() > 100:
            device.alert()
            socketio.emit('alert', {'datatype': 'heartrate', 'data':str(device.get_heartrate())}, broadcast=True)
        time.sleep(1)

@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")
    messagesplit = message.split(':')
    socketio.emit('alert', {'datatype':f'{messagesplit[0]}', 'data': f'{messagesplit[1]}'})

@socketio.on('stream')
def handle_stream(message):
    print(f"Received message: {message}")
    socketio.emit('stream', json.loads(message))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('Status.html')


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


##EDITING BACKEND