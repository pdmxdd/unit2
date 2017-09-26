from flask import Flask, request, escape
import cgi
import html

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
form2 = """
<!doctype html>
<html>
<body>
    <form action="/hello-test" method="post">
        <label for="f-name">First Name:</label>
        <input type="text" id="f-name" name="fname" />
        <input type="submit" />
    </form>
</body>
</html>
"""
form3 = """
<!doctype html>
<html>
<body>
    <form action="/hello-test" method="post">
        <label for="f-name">First Name:</label>
        <input type="text" id="f-name" name="fname" />
        <input type="submit" />
    </form>
</body>
</html>
"""


@app.route("/", methods=['GET'])
def index():
    return "<h1>Using the CGI library</h1>" + form

@app.route("/hello", methods=['POST'])
def hello():
    first_name = request.form['fname']
    # we are using cgi.escape(INPUT_FROM_FORM) to sanitize any injected HTML
    return "Hi " + cgi.escape(first_name)

@app.route("/test", methods=['GET'])
def test():
    return "<h1>Using the HTML library</h1>" + form2

@app.route("/hello-test", methods=['POST'])
def hello_test():
    first_name = request.form['fname']
    # we are using html.escape(INPUT_FROM_USER) to sanitize any injected HTML
    # after looking at the documentation for CGI library in Python, cgi.escape() is deprecated, and the supported way is using the html library
    return "Hi " + html.escape(first_name)

@app.route("/test2", methods=['GET'])
def test2():
    return "<h1>Using the flask escape library</h1>" + form3

@app.route("/hello-test2", methods=['POST'])
def test3():
    first_name = request.form['fname']
    # we are using escape() built into flask for sanitizing HTML tags
    # after digging even deeper into the documentation I've found a third tool that will solve the problem, and it doesn't require anything outside of Flask!
    # It should be noted, you only need to use one of the HTML escape methods: cgi.escape(), html.escape(), or flask.escape()
    return "Hi " + escape(first_name)
app.run()