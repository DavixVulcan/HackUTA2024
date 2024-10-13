from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_socketio import SocketIO, send
import device

app = Flask(__name__)

# Initialize Flask-SocketIO
socketio = SocketIO(app)

def heartrate_mon():
    while True:
        if device.get_heartrate() > 100:
            device.alert()
            socketio.emit('alert', {'datatype': 'heartrate', 'data':str(device.get_heartrate())}, broadcast=True)
        time.sleep(1)

def bloodpressure_mon():
    while True:
        if device.get_bloodpressure() > 120:
            device.alert()
            socketio.emit('alert', {'datatype': 'bloodpressure', 'data':str(device.get_bloodpressure())}, broadcast=True)
        time.sleep(1)

def bloodoxy_mon():
    while True:
        if device.get_bloodoxygen() < 90:
            device.alert()
            socketio.emit('alert', {'datatype': 'bloodoxy', 'data':str(device.get_bloodoxygen())}, broadcast=True)
        time.sleep(1)

@app.route('/')
def home():
    return render_template('test.html')

@app.route('/login')
def login():
    return render_template('Status.html')

@app.before_first_request
def main_looper():
    device.initialize_gpio()
    thread1 = Thread(target=heartrate_mon)
    thread1.start()
    thread2 = Thread(target=bloodpressure_mon)
    thread2.start()
    thread3 = Thread(target=bloodoxy_mon)
    thread3.start()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


##EDITING BACKEND