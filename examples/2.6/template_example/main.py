from flask import Flask, request
import cgi
import os
import jinja2

# The following line creates a variable that contains the directory of our templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#print(template_dir)
# The following line creates a jinja2 Environment which contains a loader, and an attribute called autoescape
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/", methods=['GET'])
def index():
    # We need to first create a template from an HTML file
    template = jinja_env.get_template('hello_form.html')
    # We need to then render the template
    return template.render()

@app.route("/hello", methods=['POST'])
def hello():
    # We need to first create a template from an HTML file
    template = jinja_env.get_template('hello_greeting.html')
    # We need to get the user input from the form
    first_name = request.form['fname']
    # We need to render the template, and also pass the template the variable we need it to display
    return template.render(name=first_name)


app.run()