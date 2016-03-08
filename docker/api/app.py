from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def status():
    """
    Provides the current status of the address parsing service
    """

    headers = request.headers

    status = {
        "status": "You made it!",
        "meta": {
            "headers" : [header for header in headers]
        }
    }

    return jsonify(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
