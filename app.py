
from flask import Flask, make_response, request
import dbhelpers as dh
import apihelper as a
import json
import dbcreds as d
from uuid import uuid4



app = Flask(__name__)

@app.post('/api/login')

def login():
    valid_check=a.check_endpoint_info(request.json, ['email', 'password'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL validate_id(?,?)', [request.json.get('email'), request.json.get('password')])
    if (type(result) == list and len(result) == 1):
        token = uuid4().hex
        login_result = dh.run_statement('CALL client_log_session(?,?)', [result[0][0], token])
        if(type(login_result) == list and login_result[0][0] == 1):
            return make_response(json.dumps(token, default=str), 200)
        else:
            return make_response(json.dumps("sorry, there was an internal server error"), 400)
    else:
        return make_response(json.dumps("sorry, bad login attempt"), 400)

    





if(d.production_mode == True):
    print("Running in Production Mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)