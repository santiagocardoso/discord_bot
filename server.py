from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Oie, estou on!"

def run():
    app.run(host='0.0.0.0', port=8000)

def server():
    t = Thread(target=run)
    t.start()
