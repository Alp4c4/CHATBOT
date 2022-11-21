from flask import Flask



app =Flask(__name__)

@app.route('/')
def name():
    return "ออกเถอะ"

if __name__ == ' __name__':
    app.run()