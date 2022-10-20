
from flask import Flask, make_response, request
import dbhelpers as dh
import apihelper as a
import json
import dbcreds as d
from uuid import uuid4

new_token = uuid4()

app = Flask(__name__)

@app.post('/api/login')

def login():
    valid_check=a.check_endpoint_info(request.json, ['email', 'password'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)

    result = dh.run_statement('CALL validate_id(?,?)', [request.json('email'), request.json('password')])
    if (type(result) == list):
        return new_token
        # return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

    





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