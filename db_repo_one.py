import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CLUSTER = os.getenv("DB_CLUSTER")


class Database(pymongo.database.Database):

    def __init__(self, username=DB_USERNAME, password=DB_PASSWORD, database="repository_db", cluster=DB_CLUSTER):
        self.username = username
        self.password = password
        self.database = database
        self.cluster = cluster
        mongo = pymongo.MongoClient(
            f"mongodb+srv://{self.username}:{self.password}@{self.cluster}.4fryz.mongodb.net/{self.database}?retryWrites=true&w=majority",
            connect=False,
            tlsAllowInvalidCertificates=True
        )
        super().__init__(mongo, self.database)

    def put(self, oid, size):
        put_dict = {"oid": oid,
                    "size": size}
        response = self.arbi_repo.insert_one(put_dict)
        return response

    def get(self, oid):
        get_resp = self.arbi_repo.find_one({"oid": oid, }, {"_id": False})
        return get_resp

    def delete(self, oid):
        del_resp = self.arbi_repo.delete_one({"oid": oid, })
        return del_resp


db_repo_one = Database()
