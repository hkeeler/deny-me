from flask import Flask, jsonify, request
from werkzeug.exceptions import Forbidden

app = Flask(__name__)

def build_response(request, message):
    resp = {
        "message": message,
        "meta": {
            "headers": {h[0]: h[1] for h in request.headers}
        }
    }

    return resp


username_header = 'Remote-User'
authz_header = 'Employeetype'
authz_admin = 'System Administrator'
idp_header = 'Shib-Identity-Provider'
valid_idps = set(
    'https://hkeeler-sso-dev-ed.my.salesforce.com',
)

def auth_n(request):
    url = request.url
    method = request.method
    username = request.headers.get(username_header, '**UNKNOWN**')

    print('DEBUG: Authentication request {} {} by {} starting...'.format(method, url, username))

    try:
        idp = request.headers[idp_header]
        if idp in valid_idps:
            print('DEBUG: Authentication request {} {} by {} successful.'.format(method, url, username))
        else:
            print('ERROR: Authentication request {} {} by {} failed. IdP "{}" is not valid.  Must be one of : {}'.format(
                method, url, username, idp, valid_idps))

            return username

    except KeyError:
        print('WARN:  Authentication request {} {} by {} failed.  IdP request header {} not present'.format(
            method, url, username, idp_header))

    raise Forbidden('Not authenticated')


def auth_z(request, role):
    username = auth_n(request)
    method = request.method
    url = request.url

    print('DEBUG: Authorization request {} {} by {} starting...'.format(method, url, username))
        
    try:
        request.headers[authz_header] == role
        print('DEBUG: Authorization request {} {} by {} successful.'.format(method, url, username))

        return True
    except KeyError:
        print('WARN:  Authorization request {} {} by {} failed.  User not in {} role.'.format(
            method, url, username, authz_value))
        
    return Forbidden('Not authorized to access this resource')


@app.route('/', methods=['GET'])
def status():
    """
    Root resource with no authN or authZ required
    """
    return jsonify(build_response(request, 'Big deal.  Anyone can get here!'))


@app.route('/secure', methods=['GET'])
def secure():
    """
    Requires authN, but not authZ
    """
    auth_n(request)
    return jsonify(build_response(request, "Huh.  You must be...somebody!"))

@app.route('/secure/admin', methods=['GET'])
def admin():
    """
    Requires authN, AND authZ via specified headers
    """
    auth_z(request, authz_admin)
    return jsonify(build_response(request, "Wow!  A real life admin!?"))


def gen_error_json(message, code):
    """
    Builds standard JSON error message
    """
    resp = build_response(request, message)
    resp['statusCode'] = code

    return jsonify(resp), code

# Register all Flask error handlers
@app.errorhandler(404)
def not_found_error(error):
    return gen_error_json('Resource not found', 404)

#@app.errorhandler(Forbidden)
@app.errorhandler(403)
def forbidden_error(error):
    print("Yep, you're in the Forbidden error hander!")
    return gen_error_json(error.description, 403)

@app.errorhandler(Exception)
def default_error(error):
    app.logger.exception('Internal server error')
    return gen_error_json('Internal server error', 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
