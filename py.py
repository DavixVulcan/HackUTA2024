from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "Hello"
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
def home():
    return render_template('HTML.html')
if __name__ == "__main__":
    app.run(debug=True)