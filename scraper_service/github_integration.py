from github import Github
import os
from model import Developer

github_token = os.environ.get("GITHUB_TOKEN")
github = Github(github_token)


def full_scan(db):
    for github_user in github.get_users():
        db.developers.insert_one(github_user.__dict__)


def scan_by_country(db, country):
    users = github.search_users(query=f"location:{country}")
    for user in users:
        if user.email and user.email.strip():
            dev = Developer(user)
            db.developers.insert_one(dev.to_mongo_dict())
