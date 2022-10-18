import json
from typing import Dict


def del_action(oid: str, repo_obj: object) -> Dict:
    # setting up the ret_dict in a josn file to get rid of redundancy,
    # by default it will have empty value, the values in this dict will change during runtime
    ret_dict = json.load(open("ret_dict.json", "r"))
    del_resp = repo_obj.delete(oid=oid)
    deleted_count = del_resp.deleted_count
    if deleted_count == 0:
        ret_dict["message"] = "The object id is invalid!"
        ret_dict["code"] = 404
    else:
        ret_dict["message"] = f"Object deletion successful with message {del_resp} "
        ret_dict["code"] = 200
    return ret_dict
