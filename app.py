import json
from flask import Flask, Response, request
from put_action import put_action
from get_action import get_action
from delete_action import del_action
from db_repo_one import db_repo_one

app = Flask(__name__)

# TODO: Explanation, we can have multiple repositories. In that case We can also have an abstract repo that the repositories can inherit from.
#    In this below dict, we can choose from existing repo objects and do the actions necessary, these can be different available endpoints for
#    different repos in the system, example: data/person, data/company etc. I am using an arbitrary name just to demonstrate.

repo_obj_dict = {"db_repo_one": db_repo_one}

# setting up the response in a json file to get rid of redundancy, by default it will be a 404 error as when data is found, the values in this dict will change
error_resp = {"message": "The repository does not exist",
              "code": 404}


@app.route('/', methods=['GET'])
def root():
    root_details = {"service": "Interview-task api",
                    "version": "1",
                    "status": "online"}
    byte_format = json.dumps(root_details)
    return Response(byte_format, status=200, mimetype='application/json')


@app.route('/data/<repo>', methods=['PUT'])
def put(repo: str):
    if repo in repo_obj_dict.keys():
        resp = put_action(args=request.args, repo_obj=repo_obj_dict[repo])
    else:
        resp = error_resp
    byte_format = json.dumps(resp["message"])
    return Response(byte_format, status=resp["code"], mimetype='application/json')


@app.route('/data/<repo>/<oid>', methods=['GET', 'DELETE'])
def get_delete(repo: str, oid: str):
    if repo in repo_obj_dict.keys():
        if request.method == 'GET':
            resp = get_action(oid=oid, repo_obj=repo_obj_dict[repo])
        elif request.method == 'DELETE':
            resp = del_action(oid=oid, repo_obj=repo_obj_dict[repo])
    else:
        resp = error_resp
    byte_format = json.dumps(resp["message"])
    return Response(byte_format, status=resp["code"], mimetype='application/json')


if __name__ == '__main__':
    app.run(port=8282, debug=True)
