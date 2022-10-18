import json
import secrets
from typing import Dict
from flask_restful import reqparse

repo_put_args = reqparse.RequestParser()
# All the arguments are needed to input
repo_put_args.add_argument("size", type=int, required=True)


def put_action(args: Dict, repo_obj: object) -> Dict:
    # setting up the ret_dict in a josn file to get rid of redundancy,
    # by default it will have empty value, the values in this dict will change during runtime
    ret_dict = json.load(open("ret_dict.json", "r"))
    args = repo_put_args.parse_args()

    # As we have only one key to consider here, we are checking if after parsing, the dictionary is empty or not,
    # For multiple arguments we can check if the key exists or not in the resulting dict
    if not args:
        ret_dict["message"] = "Invalid arguments passed!"
        ret_dict["code"] = 400
    else:
        # Generating 64 char hex oid value defined in the task description
        oid = secrets.token_hex(32)
        repo_obj.put(oid=oid, size=args["size"])
        ret_dict["message"] = args
        ret_dict["code"] = 201
    return ret_dict



