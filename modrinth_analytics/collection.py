import labrinth.user
import json
import os
import time


def collect(user_ids, token, db):
    if os.path.exists(db):
        with open(db, 'r') as f:
            analytics = json.loads(f.read())
    else:
        analytics = {}

    for user_id in user_ids:
        user = labrinth.user.user(user_id, token)
        if user.id not in analytics:
            analytics[user.id] = []

        projects = labrinth.user.projects(user.id, token)
        analytics[user.id].append({
            'time': int(time.time())
        })
        for project in projects:
            analytics[user.id][-1][project.id] = project.downloads

    with open(db, 'w') as f:
        f.write(json.dumps(analytics, indent=2))
