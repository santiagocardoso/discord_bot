import os
from flask import Flask
from threading import Thread
import logging

app = Flask('')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
    return "Wafflinho está rodando!"

def run():
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

def server():
    t = Thread(target=run, daemon=True)
    t.start()