#
# keep_alive.py
#
# Reference: https://qiita.com/Erytheia/items/2f64c06d6d8a4f802390
#

from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def index():
    return "Service is alive."

def run():
    app.run(host="0.0.0.0", port=5000)

def keep_alive():
    t = Thread(target=run)
    t.start()
