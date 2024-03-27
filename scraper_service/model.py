import copy
from datetime import datetime


def __init__(self, github_user=None, mongo_document=None):
    if github_user:
        self.login = github_user.login
        self.avatar_url = github_user.avatar_url
        self.bio = github_user.bio
        self.blog = github_user.blog
        self.company = github_user.company
        self.created_at = github_user.created_at
        self.email = github_user.email
        self.events_url = github_user.events_url
        self.followers = github_user.followers
        self.following = github_user.following
        self.gists_url = github_user.gists_url
        self.gravatar_id = github_user.gravatar_id
        self.hireable = github_user.hireable
        self.html_url = github_user.html_url
        self.id = github_user.id
        self.location = github_user.location
        self.name = github_user.name
        self.node_id = github_user.node_id
        self.organizations_url = github_user.organizations_url
        self.public_gists = github_user.public_gists
        self.public_repos = github_user.public_repos
        self.received_events_url = github_user.received_events_url
        self.repos_url = github_user.repos_url
        self.site_admin = github_user.site_admin
        self.starred_url = github_user.starred_url
        self.subscriptions_url = github_user.subscriptions_url
        self.twitter_username = github_user.twitter_username
        self.type = github_user.type
        self.updated_at = github_user.updated_at
        self.raw_data = copy.deepcopy(github_user.raw_data) if github_user.raw_data else None
        self.raw_headers = copy.deepcopy(github_user.raw_headers) if github_user.raw_headers else None
        self.insert_ts = datetime.utcnow()
        self.update_ts = datetime.utcnow()
    elif mongo_document:
        self.login = mongo_document.get('login')
        self.avatar_url = mongo_document.get('avatar_url')
        self.bio = mongo_document.get('bio')
        self.blog = mongo_document.get('blog')
        self.company = mongo_document.get('company')
        self.created_at = mongo_document.get('created_at')
        self.email = mongo_document.get('email')
        self.events_url = mongo_document.get('events_url')
        self.followers = mongo_document.get('followers')
        self.following = mongo_document.get('following')
        self.gists_url = mongo_document.get('gists_url')
        self.gravatar_id = mongo_document.get('gravatar_id')
        self.hireable = mongo_document.get('hireable')
        self.html_url = mongo_document.get('html_url')
        self.id = mongo_document.get('id')
        self.location = mongo_document.get('location')
        self.name = mongo_document.get('name')
        self.node_id = mongo_document.get('node_id')
        self.organizations_url = mongo_document.get('organizations_url')
        self.public_gists = mongo_document.get('public_gists')
        self.public_repos = mongo_document.get('public_repos')
        self.received_events_url = mongo_document.get('received_events_url')
        self.repos_url = mongo_document.get('repos_url')
        self.site_admin = mongo_document.get('site_admin')
        self.starred_url = mongo_document.get('starred_url')
        self.subscriptions_url = mongo_document.get('subscriptions_url')
        self.twitter_username = mongo_document.get('twitter_username')
        self.type = mongo_document.get('type')
        self.updated_at = mongo_document.get('updated_at')
        self.raw_data = copy.deepcopy(mongo_document.get('raw_data')) if mongo_document.get('raw_data') else None
        self.raw_headers = copy.deepcopy(mongo_document.get('raw_headers')) if mongo_document.get('raw_headers') else None
        self.insert_ts = mongo_document.get('insert_ts')
        self.update_ts = mongo_document.get('update_ts')

    def to_mongo_dict(self):
        # Dynamically convert all attributes to a dictionary
        result = {}
        for key, value in self.__dict__.items():
            # Handle special cases, like converting datetime to strings or handling other non-serializable types
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

