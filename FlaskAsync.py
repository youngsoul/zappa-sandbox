from zappa.async import task, get_async_response
from flask import Flask, make_response, abort, url_for, redirect, request, jsonify
from time import sleep

app = Flask(__name__)

@app.route('/payload')
def payload():
    print("payload called...")
    # Make sure this delay is LESS than the lambda timeout.
    delay = request.args.get('delay', 50)
    x = longrunner(int(delay))

    return redirect(url_for('response', response_id=x.response_id))

@app.route('/async-response/<response_id>')
def response(response_id):
    response = get_async_response(response_id)
    if response is None:
        abort(404)

    if response['status'] == 'complete':
        return jsonify(response['response'])

    sleep(5)

    print("returning from response")
    return "Not yet ready. Redirecting.", 302, {
        'Content-Type': 'text/plain; charset=utf-8',
        'Location': url_for('response', response_id=response_id, backoff=5),
        'X-redirect-reason': "Not yet ready.",
    }

@task(capture_response=True)
def longrunner(delay):
    print(f"FlaskAsync  longrunner sleeping...: {delay}")
    sleep(delay)
    print("FlaskAsync longrunner returning....")
    return {'MESSAGE': "It took {} seconds to generate this.".format(delay)}
