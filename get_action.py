import json
from typing import Dict


def get_action(oid: str, repo_obj: object) -> Dict:
    # setting up the ret_dict in a josn file to get rid of redundancy,
    # by default it will have empty value, the values in this dict will change during runtime
    ret_dict = json.load(open("ret_dict.json", "r"))
    get_resp = repo_obj.get(oid=oid)

    if not get_resp:
        ret_dict["message"] = "The object id is invalid!"
        ret_dict["code"] = 404
    else:
        ret_dict["message"] = get_resp
        ret_dict["code"] = 200
    return ret_dict
