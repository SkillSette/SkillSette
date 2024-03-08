import json
from datetime import datetime


def modify_dict(source):
    # Initialize the target dictionary structure
    target = {
        "_id": source.get("_id", {}),  # Keeping the _id structure as is
        "first_name": source.get("first_name", ""),
        "last_name": source.get("last_name", ""),
        "avatar": source.get("avatar", ""),
        "date_of_birth": datetime.strptime(source.get("date_of_birth", ""), "%Y-%m-%d").strftime("%d/%m/%Y") if source.get("date_of_birth") else "",
        "country": source.get("country", ""),
        "email": source.get("email", ""),
        "token": "",  # Placeholder as the example data does not include this field
        "score": {"$numberInt": str(int(source.get("github_rate", 0)))},  # Convert github_rate to int
        "github_username": "",  # Placeholder as the example data does not include a direct github_username field
        "english_level": str(source.get("english_level", "")),  # Ensure it's a string
        "verified": source.get("verified", False),
        "skills": []
    }

    # Extracting skills from github_code_level
    if source.get("github_code_level"):
        for skill in source["github_code_level"].keys():
            target["skills"].append(skill)

    # Extracting and adding topics to skills
    if source.get("topics"):
        for topic in source["topics"]:
            for skill in topic.keys():
                if skill not in target["skills"]:  # Avoid duplicating skills
                    target["skills"].append(skill)

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
