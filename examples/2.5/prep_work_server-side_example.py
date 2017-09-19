from flask import Flask, request

app = Flask(__name__)
app.config['DEBUG'] = True

# The example we saw in our prep work has us creating a form, for getting the time from the user.
time_form = """
<style>
    .error {{ color: red; }}
</style>
<h1>Validate Time</h1>
<form method="POST">
    <label>Hours (24-hour format)
        <input name="hours" type="text" value="{hours}" />
    </label>
    <p class="error">{hours_error}</p>
    <label>Minutes
        <input name="minutes" type="text" value="{minutes}" />
    </label>
    <p class="error">{minutes_error}</p>
    <input type="submit" value="Validate" />
</form>
"""


@app.route('/validate-time')
def index():
    return time_form.format(hours='', hours_error='', minutes='', minutes_error='')

def is_integer(str_num):
    # return True if it can be converted to int
    # return False if it can't be converted to int
    print("IN INTEGER FOR", str_num)
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

    # Validate steps
    # We are expecting integers, did they give us integers
    # Are the integers in the correct range
    

    # is the hour input an integer?
    if not is_integer(hours):
        hours_error = 'Not a valid integer'
        # their input was invalid, so let's wipe it out for them
        hours = ''
    else:
        # is the hour in the range of 0-24
        hours = int(hours)
        if hours < 0 or hours > 23:
            hours_error = 'Hour value out of range (0-23)'
    # is the minute input an integer?
    if not is_integer(minutes):
        minutes_error = 'Not a valid integer'
        # their input was invalid, so let's wipe it out for them
        minutes = ''
    else:
        # is the minute in the range of 0-59
        minutes = int(minutes)
        if minutes < 0 or minutes > 59:
            minutes_error = 'Minute value out of range (0-59)'

    # now that we have created the code that validates if hours & minutes are integers
    # and validates that hours & minutes are in the correct range
    # we can now serve up the HTTP Response

    # didn't catch any errors in the form, so we need to send a success message
    if minutes_error == '' and hours_error == '':
        # success message
        return "SUCCESS"
    else:
        return time_form.format(hours_error=hours_error,
            minutes_error=minutes_error,
            hours=hours,
            minutes=minutes)
        

app.run()