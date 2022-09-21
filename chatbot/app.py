from flask import Flask,request,render_template,url_for

app=Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello,World!'


    app.run()