from flask import Flask, redirect

app = Flask(__name__)
app.config['DEBUG'] = True

# We are creating a decorator, and handler for /home
@app.route("/home", methods=['GET'])
def home():
    return "Welcome to the <b>Home</b> page!"

# We are creating a decorator and handler for /
@app.route("/", methods=['GET'])
def index():
    return redirect("/home")



app.run()