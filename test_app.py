import unittest
import requests
from db_repo_one import db_repo_one


class testEndPoints(unittest.TestCase):
    def setUp(self):
        # this part does all the setup before the test is run
        self.valid_put_dict = {
            # unique size as there should not a file of size 0 that should exist
            "size": 0
        }
        self.bad_put_req = {
            "siz": 345
        }

        self.base_url = "http://localhost:8282/"

    def test_a_root(self):
        root_response = requests.get(self.base_url)
        self.assertEqual(root_response.status_code, 200)

    def test_b_put(self):
        # testing with valid request body
        valid_put_resp = requests.put(f"{self.base_url}data/db_repo_one", self.valid_put_dict)
        self.assertEqual(valid_put_resp.status_code, 201)

        # testing with invalid request body
        bad_put_resp = requests.put(f"{self.base_url}data/db_repo_one", self.bad_put_req)
        self.assertEqual(bad_put_resp.status_code, 400)

        # testing with invalid repo
        bad_repo_name = requests.put(f"{self.base_url}data/non_existing_repo", self.valid_put_dict)
        self.assertEqual(bad_repo_name.status_code, 404)

    def test_c_get(self):
        # testing with valid oid, namely, the same one inserted in the put test,
        # query is done directly here just to get the oid as with size value as a query arg as it is unique
        valid_oid = db_repo_one.arbi_repo.find_one({"size": 0, }, {"_id": False})["oid"]
        valid_get_req = requests.get(f"{self.base_url}data/db_repo_one/{valid_oid}")
        self.assertEqual(valid_get_req.status_code, 200)

        # testing with an invalid oid
        bad_oid = "21323fgsd56sbfhbsdahg"
        bad_get_req = requests.get(f"{self.base_url}data/db_repo_one/{bad_oid}")
        self.assertEqual(bad_get_req.status_code, 404)

    def test_d_delete(self):
        # testing with valid oid, namely, the same one inserted in the put test,
        # the data inserted in an earlier test is being deleted from here, as it does not need to exist after the test has been performed
        valid_oid = db_repo_one.arbi_repo.find_one({"size": 0, }, {"_id": False})["oid"]
        valid_del_req = requests.delete(f"{self.base_url}data/db_repo_one/{valid_oid}")
        self.assertEqual(valid_del_req.status_code, 200)

        # we can use the same oid here as now, it will be invalid as the data has already been deleted, it will return a 404 error
        invalid_del_req = requests.delete(f"{self.base_url}data/db_repo_one/{valid_oid}")
        self.assertEqual(invalid_del_req.status_code, 404)
