from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def status():
    """
    Root resource with no authN or authZ required
    """

    resp = {
        "message": "So what!  Anybody can get here!",
        "meta": {
            "headers" : [header for header in request.headers]
        }
    }

    return jsonify(resp)

@app.route('/secure', methods=['GET'])
def secure():
    """
    Requires authN, but not authZ
    """

    resp = {
        "message": "Wow.  You must be...somebody!",
        "meta": {
            "headers": [header for header in request.headers]
        }
    }

    return jsonify(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
