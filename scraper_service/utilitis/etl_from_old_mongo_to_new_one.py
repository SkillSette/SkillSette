import json


def modify_dev(data):
    skills = dict()
    if data.get("github_code_level"):
        skills = data["github_code_level"]
    if data.get("topics"):
        topics_dict = {topic: value for d in data["topics"] for topic, value in d.items()}
        skills.update(topics_dict)

    data["skills"] = skills

    if data.get("github_code_level"):
        del data["github_code_level"]
    if data.get("topics"):
        del data["topics"]
    return data


def main():
    existing_devs = json.loads(open("codespread.developers.json").read())
    new = list()
    for dev in existing_devs:
        modified_dev = modify_dev(dev)
        dev_id = modified_dev.get("id")
        dev_username = modified_dev.get("username")
        print(f"uploading {dev_username} to the new_mongo")
        new.append(modified_dev)
    json.dump(new, open("modified.json", "w"))


if __name__ == '__main__':
    main()
