from flask import Flask, request, jsonify
from github import Github
from celery import Celery
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from model.developers import Developer

app = Flask(__name__)


def init_db():
    # MongoDB setup
    # uri = os.environ.get("MONGO_URI")
    uri = "mongodb://localhost:27017"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    connect_db = client.developers
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return connect_db

# GitHub setup
github_token = os.environ.get("GITHUB_TOKEN")
github = Github(github_token)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)



# Celery task for full scan
@celery.task
def full_scan():
    for github_user in github.get_users():
        # Process and save to DB
        db.developers.insert_one(github_user.__dict__)

# @celery.task

@celery.task
def scan_by_country(country):
    # Search for users based on location
    users = github.search_users(query=f"location:{country}")
    for user in users:
        # Attempt to get user's email
        # Note: Most users do not have a publicly visible email address due to privacy settings
        if user.email and user.email.strip():
            dev = Developer(user)
            db.developers.insert_one(dev.to_mongo_dict())
    return None

@app.route('/scan_by_country', methods=['POST'])
def scan_by_country_route():

    country = request.json.get('country')
    # country = "Israel"

    if not country:
        return jsonify({"message": "Country is required"}), 400
    # scan_by_country.delay(country)
    scan_by_country(country)
    return jsonify({"message": "Full scan initiated"}), 202


@app.route('/full_scan', methods=['POST'])
def trigger_full_scan():
    full_scan.delay()
    # full_scans()
    return jsonify({"message": "Full scan initiated"}), 202


@app.route('/scan_developer', methods=['POST'])
def scan_developer():
    username = request.json.get('username')
    if not username:
        return jsonify({"message": "Username is required"}), 400

    # Attempt to get the GitHub user
    try:
        github_user = github.get_user(username)
    except Exception as e:
        # Handle exceptions, e.g., user not found or API errors
        return jsonify({"message": str(e)}), 500

    # Prepare the developer information
    dev = Developer(github_user).__dict__

    # Update the document if exists, otherwise insert a new one
    result = db.developers.update_one(
        {"username": username},  # Query criteria
        {"$set": dev},  # Update document
        upsert=True  # Insert a new document if one doesn't exist
    )

    # Check if a new document was inserted or an existing was updated
    if result.upserted_id:
        return jsonify(dev), 201  # Return 201 CREATED if a new document was inserted
    else:
        return jsonify(dev), 200  # Return 200 OK if an existing document was updated


if __name__ == '__main__':
    db = init_db()
    app.run(debug=True)
