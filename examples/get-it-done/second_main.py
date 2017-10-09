'''
For this example we need to add a few lines of code
'''

from flask import Flask, request, redirect, render_template
'''
First we need to import SQLAlchemy so we have access to it's tools
'''
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True

'''
We then need to add some config parameters to our already created Flask app named app
We are telling our flask app:
        what type of database it is
        the username and password
        the server it's located on (localhost in this case)
        the port
        and finally the DB name
We are also telling our app to print out some nice statements when we use SQLAlchemy from our app
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:root@localhost:3306/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True

'''
We then need to create a database object (named db)
from the SQLAlchemy code we imported above
'''
db = SQLAlchemy(app)

'''
Now we need to create a class for each table in the DB we wish to use from this app
We only have one table for this example named Task
It should be noted that if we had more tables we would need more classes to map them to
'''
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

tasks = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)

    return render_template('todos.html',title="Get It Done!", tasks=tasks)

if __name__ == '__main__':
    app.run()