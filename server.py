from flask import Flask
from threading import Thread

app = Flat(' ')

@app.route('/')
def ping():
    return "w"

def run():
    app.run(host='0.0.0.0',port=0000)

def server():
    t = Thread(target=run)
    t.start()