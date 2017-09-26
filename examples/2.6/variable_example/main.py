from flask import Flask, request, redirect
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def redir():
    return redirect('/validate-time')

@app.route('/validate-time')
def index():
    template = jinja_env.get_template('time_form.html')
    return template.render()

def is_integer(str_num):
    try:
        int(str_num)
        return True
    except ValueError:
        return False

@app.route('/validate-time', methods=['POST'])
def validate_time():
    hours = request.form['hours']
    minutes = request.form['minutes']

    hours_error = ''
    minutes_error = ''

    if not is_integer(hours):
        hours_error = 'Not a valid integer'
        hours = ''
    else:
        hours = int(hours)
        if hours < 0 or hours > 23:
            hours_error = 'Hour value out of range (0-23)'
    if not is_integer(minutes):
        minutes_error = 'Not a valid integer'
        minutes = ''
    else:
        minutes = int(minutes)
        if minutes < 0 or minutes > 59:
            minutes_error = 'Minute value out of range (0-59)'

    if minutes_error == '' and hours_error == '':
        template = jinja_env.get_template('success_time.html')
        return template.render(hours=hours, minutes=minutes)
    else:
        # We need to create and render a template here
        template = jinja_env.get_template('time_form.html')
        return template.render(hours_error=hours_error,
            minutes_error=minutes_error,
            hours=hours,
            minutes=minutes)
        

app.run()