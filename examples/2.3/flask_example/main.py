from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return "Hello from Flask"

@app.route("/home")
def home():
    return "Welcome to the home page."

@app.route("/python")
def python_route():
    return '<p style="color: red">PYTHON IS THE BEST!!<p>'

app.run()