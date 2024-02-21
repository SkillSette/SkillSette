import json


def modify_dict(source):
    # Initialize the target dictionary structure
    print(source.get("user_id", {}))
    target = {
            "first_name": source.get("first_name", ""),
            "last_name": source.get("last_name", ""),
            "user_id": source.get("user_id", ""),
            "date_of_birth": source.get("date_of_birth", ""),  # Assuming you have a date_of_birth field to fill
            "country": source.get("country", ""),
            "email": source.get("email", ""),
            "token": source.get("token", ""),  # Assuming you have a token field to fill
            "score": int(source.get("github_rate", 0)),
            "verified": source.get("verified", False),
            "skills": {}
        }

    # Extracting skills from github_code_level
    if source.get("github_code_level"):
        for skill, details in source.get("github_code_level", {}).items():
            target["skills"][skill] = {
                "type": "programming",  # Assuming all github_code_level skills are programming, adjust as necessary
                "level": int(details["github_score"] // 10)  # Simplified conversion, adjust the calculation as needed
            }

    # Extracting and adding topics to skills, assuming 1 as a level indicator for topic presence
    for topic in source.get("topics", []):
        for key, value in topic.items():
            if value:  # Only include topics that have a '1' indicating proficiency or interest
                target["skills"][key] = {
                    "type": "knowledge",  # Assuming topics fall under a "knowledge" category
                    "level": 1  # Arbitrary level for topics, adjust as necessary
                }

    return target


def main():
    existing_devs = json.loads(open("codespread.developers.json").read())
    new = list()
    for dev in existing_devs:
        modified_dev = modify_dict(dev)
        dev_username = modified_dev.get("username")
        print(f"uploading {dev_username} to the new_mongo")
        new.append(modified_dev)
    json.dump(new, open("modified.json", "w"))


if __name__ == '__main__':
    main()
