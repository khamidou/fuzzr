from pymongo import Connection
from pymongo.objectid import ObjectId


connection = Connection()

db = connection.fuzzr

users = db.users
actions = db.actions

def create_post(title, desc, for_musicians=0):
    return {"title": title,
            "description": desc,
            "for-musicians": for_musicians,
	}

def create_user(username, passwd, is_root, is_musician=0):
    return {"username": username,
            "password": passwd,
            "actions-accomplished": [],
            "is_root": is_root,
            "is_musician": is_musician,
            }

def user_has_done(username, action):
            user = users.find_one({"username" : username})

            if user == None:
                return

            user["actions-accomplished"].append(action["_id"])
            users.save(user, safe=True)

# Simply insert a post and a root user
def create_db(root, passwd):

    ac = create_post("Wear something green", "Today you're gonna wear something green, to celebrate your irish ancestors")
    actions.insert(ac)

    us = create_user(root, passwd, 1)
    users.insert(us)

    
