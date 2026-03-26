import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Oie, estou on!"

def run():
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

def server():
    t = Thread(target=run)
    t.start()