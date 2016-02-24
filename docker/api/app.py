from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def status():
    """
    Provides the current status of the address parsing service
    """

    status = {
        "status": "DENIED!",
    }

    return jsonify(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
