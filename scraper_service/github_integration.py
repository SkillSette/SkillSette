from github import Github
import os
from model import Developer
from db import init_db
import datetime
github_token = os.environ.get("GITHUB_TOKEN")
github = Github(github_token)
db = init_db()


def full_scan():
    for github_user in github.get_users():
        db.developers.insert_one(github_user.__dict__)


def scan_by_filters(filters):
    query_github = ""
    for k, v in filters.items():
        query_github += k + ":" + v
    users = github.search_users(query=query_github)
    for user in users:
        if user.email and user.email.strip():
            dev = Developer(user)
            db.developers.insert_one(dev.to_mongo_dict())
def update_exitsing():
    developers = db.developers.find({"update_ts": {"$lt": datetime.utcnow()}})
    for developer in developers:
        user = github.get_user(developer['login'])
        dev = Developer(user)
        updated_data = dev.to_mongo_dict()
        # Important: Ensure to refresh the update timestamp
        updated_data['update_ts'] = datetime.utcnow().isoformat()
        db.developers.update_one({"login": developer['login']}, {"$set": updated_data}, upsert=True)
