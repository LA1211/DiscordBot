import os
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=80)

def keep_alive():
    threading.Thread(target=run).start()

if __name__ == '__main__':
    keep_alive()