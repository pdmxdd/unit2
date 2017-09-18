# Import statements, we've seen Flask (that's the class we are using to build our app object)
# request is an additional library in flask that allows us to access, and handle additional information from the client
# Flask - request documentation: http://flask.pocoo.org/docs/0.12/api/#flask.Request (it's using a fragment!)
from flask import Flask, request

# Creating the app, out of the Flask class we imported from the flask library
app = Flask(__name__)
# setting our app to run in debug mode, which gives us some additional powers (printing out HTTP Request, and Response statements)
app.config['DEBUG'] = True

# creating the form we wish to display to the user, it's HTML saved in a python variable
form = '''
<!doctype html>
<html>
    <body>
        <form action="/hello">
            <label for="first-name">First name</label>
            <input id="first-name" type="text" name="first_name" />
            <input type="submit" />
        </form>
    </body>
</html>
'''

# Creating a decorator that tells our server how to handle this path (/) HTTP request
@app.route("/")
def index():
    # We are having the server send the client the HTML file we created and saved in the variable form
    return form

# The form we created has action="/hello" so when it is submitted it will redirect them to the /hello path, and pass information from the form

# Creating a decorator that tells our server how to handle this path (/hello) HTTP request HANDLER FOR FORM SAVED IN FORM VARIABLE
@app.route("/hello")
def hello():
    '''Documentation Example'''
    #print("Request.args:", request.args)
    #print("Request.form:", request.form)
    #print("Request.data:", request.data)
    # Accessing the Flask - request library to get the user input associated with the form where the name == 'first_name'
    name = request.args.get('first_name')
    # return a statement that will be turned into HTML that just says "Hi " + whatever name they gave us with the form they filled out
    return "Hi " + name


# Telling our app to run when main.py is run from the command line
app.run()