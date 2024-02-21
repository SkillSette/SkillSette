import logging
import requests
from github import Github
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# GitHub setup
github_token = os.environ.get("GITHUB_TOKEN")
github = Github(github_token)


def init_db(uri=None):
    if uri is None:
        exit("No URI provided")
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client


def send_dev(username):
    # The URL for your endpoint
    url = 'http://localhost:5000/scan_developer'

    # The JSON payload with the username you want to scan
    data = {'username': username}

    # Make a POST request
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code in [200, 201]:
        # The request was successful; you can process the response further
        print(f"Success! Status code: {response.status_code}")
        print("Response data:", response.json())
    else:
        # The request failed; handle errors accordingly
        print(f"Failed! Status code: {response.status_code}")
        print("Response message:", response.json().get('message'))


def main():
    existing_devs = client_db_source.codespread.developers.find()
    for dev in existing_devs:
        dev_username = dev["login"]
        logging.info(f"Sending {dev_username} to the scan_developer endpoint")
        send_dev(dev_username)


if __name__ == '__main__':
    client_db_source = init_db(uri=os.environ.get("MONGO_URI_SOURCE"))
    main()
