from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "Bot läuft!"

def run():
    app.run(host='0.0.0.0', port=80)

t = threading.Thread(target=run)
t.start()