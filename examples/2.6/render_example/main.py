from flask import Flask, render_template
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def home():
    #template = jinja_env.get_template('example.html')
    return render_template('example.html', title='example', the_list=['Trees', 'Cars', 'Python'])
    #return template.render(title='EXAMPLE', the_list=['Trees', 'Cars', 'Python'])

app.run()