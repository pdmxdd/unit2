from flask import Flask, request
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

form = """
<!doctype html>
<html>
<body>
    <form action="/hello" method="post">
        <label for="f-name">First Name:</label>
        <input type="text" id="f-name" name="fname" />
        <input type="submit" />
    </form>
</body>
</html>
"""


@app.route("/", methods=['GET'])
def index():
    return form

@app.route("/hello", methods=['POST'])
def hello():
    first_name = request.form['fname']
    # we are using cgi.escape(INPUT_FROM_FORM) to sanitize any injected HTML, or JavaScript
    return "Hi " + cgi.escape(first_name)

app.run()