from flask import Flask, request, jsonify
from pymongo import MongoClient
from github import Github
from celery import Celery
import os

app = Flask(__name__)

# MongoDB setup
mongo_uri = "mongodb://localhost:27017"
client = MongoClient(mongo_uri)
db = client.developers

# GitHub setup
github_token = os.environ.get("GITHUB_TOKEN")
github = Github(github_token)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


class Developer:
    # Class to model developer data
    def __init__(self, github_user):
        self.username = github_user.login
        self.email = github_user.email
        # Add more attributes as needed


# Celery task for full scan
@celery.task
def full_scan():
    for github_user in github.get_users():
        print(github_user)
        dev = Developer(github_user)
        # Process and save to DB
        db.developers.insert_one(dev.__dict__)
        exit(1)


@app.route('/full_scan', methods=['GET'])
def trigger_full_scan():
    full_scan.delay()
    return jsonify({"message": "Full scan initiated"}), 202


@app.route('/scan_developer', methods=['POST'])
def scan_developer():
    username = request.json.get('username')
    github_user = github.get_user(username)
    dev = Developer(github_user)
    db.developers.insert_one(dev.__dict__)
    return jsonify(dev.__dict__), 200


if __name__ == '__main__':
    app.run(debug=True)
