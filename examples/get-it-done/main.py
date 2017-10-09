# Don't forget to include session, and flash as imports!
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:root@localhost:3306/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
# add a secret_key to our app
app.secret_key = 'y337kGcys&zP3B'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    # We had to create a new column that holds a FK to the owner table
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # We also set our constructor to accept another argument, that sets the owner
    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        # That happened here!
        self.owner = owner

'''
We need to create a new class to map to our DB
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    # We had to create relationship between the User table and the Task table, and set the backref (what it's called in this app)
    tasks = db.relationship('Task', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

'''
We need to create a new route for what the applicaiotn does before it handles every request
'''
# Before every request we want to first check to see if they are requesting a page in the whitelist
# Those pages are login, register, register_post, and login_post !!! Note these are the names of the python functions, not the routes themselves!
# If the user requests a white page just let them through every time
# Second, if the user doesn't request a white page, let's make sure they have actually logged in by checking the session['email']
# If they have logged in, let them access whatever they are trying to access, if not, redirect them to login
@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'register_post', 'login_post']
    if request.endpoint in allowed_routes:
        pass
    else:
        if 'email' not in session:
            return redirect("/login")

'''
We need to create a new login route
'''
# Route that handles a GET request to /login, it serves up the webform
@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html", title="Login")

# Route that handles a POST method to /login (form from login.html),
# It checks to see if the user exists in the DB
# It checks to make sure the entered password matches the password for the User in the DB
# It redirects the user to the main page, if the first two checks pass
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    # If user.query.filter_by(email=email).first() doesn't find anything it sets user = None
    if user and user.password == password:
        session['email'] = email
        # Use the flask flash message, so we can pass information between html templates
        flash("Logged in", "success")
        return redirect('/')
    else:
        # Another flash message
        flash("User pasword incorrect, or user does not exist.", 'error')

    return render_template("login.html", title="Login")

'''
We need to create a new register route
'''
# Route that handles a GET request to /register, it serves up the webform
@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html", title="Register")

# Route that handles a POST method to /register (form from register.html),
# It verifies the passwords match from the form
# It checks to see if a user is already registered with this email address
# Finally it writes the new user to the DB assuming the first two checks pass
@app.route('/register', methods=['POST'])
def register_post():
    email = request.form['email']
    password = request.form['password']
    verify_password = request.form['verify']

    # TODO: Validate user

    existing_user = User.query.filter_by(email=email).first()
    # If user is not in DB, create an object and add them
    if existing_user == None:
        new_user = User(email, password)
        db.session.add(new_user)
        db.session.commit()
        # Another flash message
        flash("{} User created".format(email), "success")
        session['email'] = email
        return redirect('/')
    # Else if user is in DB, reload the page and give them a message that the user exists
    else:
        flash("User already exists.", "error")
        return render_template("register.html", title="Register")
    return render_template("register.html", title="Register")


@app.route('/logout', methods=['GET'])
def logout():
    del session['email']
    return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():

    # we need to get the owner that is saved in the session so we can set the owner_id when creating a new task!
    owner = User.query.filter_by(email=session['email']).first()

    # If the method is POST, we need to write this task to the DB!
    if request.method == 'POST':
        # save the form results in a variable named task_name
        task_name = request.form['task']
        # create a new Task object
        new_task = Task(task_name, owner)
        # add the task to a db session and then commit it!
        db.session.add(new_task)
        db.session.commit()

    # When we query tasks, we need to also check to make sure they are for the associated owner, so one person's tasks don't come up on another person's page!
    tasks = Task.query.filter_by(completed=False, owner=owner).all()
    completed_tasks = Task.query.filter_by(completed=True, owner=owner).all()
    return render_template("todos.html", title="Get it done!", tasks=tasks, completed_tasks=completed_tasks)

# We need a route that will allow the user to mark their task as completed
@app.route('/delete-task', methods=['POST'])
def delete_task():
    # get the task_id from the form
    task_id = int(request.form['task-id'])
    # get the task record from the DB
    task = Task.query.get(task_id)
    # mark the task as completed in the DB
    task.completed = True
    # add the change to a DB session, and commit it!
    db.session.add(task)
    db.session.commit()
    
    # finally redirect the user to the same page
    return redirect('/')




if __name__ == '__main__':
    app.run()