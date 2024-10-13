from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
import socketio

sio = socketio.server()
app = sockettio.WSGIApp(sio, static_file={ '/': './public/'
})

@sio.event
def connect(sid, environ):
    print(sid, 'connected')

@sio.event
def disconnect(sid):
    print(sid, 'disconnected')
    
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
def home():
    return render_template('index.html')
