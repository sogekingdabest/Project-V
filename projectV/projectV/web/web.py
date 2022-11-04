from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/")
def loadMain():
    return render_template('main.html')

@app.route("/auth/register", methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        user = request.form['username'],
        password = request.form['password']
        print(user, password)
        return render_template('/auth/login.html', error=error)

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    

    return render_template("./auth/register.html")
    
@app.route("/auth/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        pass
    return render_template("./auth/login.html")

