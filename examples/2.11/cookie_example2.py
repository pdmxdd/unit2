from flask import Flask, request, make_response, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    count = int(request.cookies.get('visit-count', 0))
    count += 1

    # showing how we can use render_template with make_response
    resp = make_response(render_template("home.html", visits=count))
    resp.set_cookie('visit-count', str(count))
    return resp


if __name__ == '__main__':
    app.run()