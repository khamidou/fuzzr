#!/usr/bin/env python
#
# This small script adds daily actions for every user.
# It is run by cron

from pymongo import Connection
from pymongo.objectid import ObjectId
import random
import models

connection = Connection()
db = connection.fuzzr
random.seed(None)

users = db.users
actions = db.actions

def get_random_action():
    a = actions.find()
    r = True
    for i in range(random.randint(0, actions.count())):
    	r = a.next()

    return r
        
for user in users.find():
    act = get_random_action()
    while (act["_id"] in user["actions-accomplished"]) == True:
        act = get_random_action()

    models.user_has_done(user["username"], act)
        
