import web
from web import form
import models
from pymongo import Connection
from pymongo.objectid import ObjectId


web.config.debug = False

urls = (
    '/', 'index',
    '/add/', 'add',
    '/page/(.+)/', 'page',
    '/feed/(.+)/', 'feed',
    '/login/', 'login',
    '/logout/', 'logout',
)


app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'))
render = web.template.render('templates/', base='layout')

connection = Connection()
db = connection.fuzzr
users = db.users
actions = db.actions

def logged():
    if hasattr(session, 'loggedin') == True:
        return True
    else:
        return False

def notfound():
	return web.notfound(render.error("404 - Unable to find the requested page"))

class index:
    def GET(self):
        return render.index()


class add:
    def __init__(self):
        self.add_form = form.Form(
            form.Textbox("title"),
            form.Textbox("description"))

    def GET(self):
        
        if not logged():
            return render.error("You don't have the priviledges to add actions")

        form = self.add_form()
        return render.add(form)

    def POST(self):
        form = self.add_form()
        if not form.validates(): 
            return render.add(form)
        else:
            act = models.create_post(form.d.title, form.d.description)
            actions.insert(act)
            raise web.seeother("/add/")

class page:
    def GET(self, name):
#         if logged() == False:
#             return render.error("You are not logged in")

        user = users.find_one({"username" : name})

        if user == None:
            return render.error("Page not found")

        l = list()  # We need to give a list because mongo returns an iterator.
        
        for id in user["actions-accomplished"]:
            act = actions.find_one({"_id" : ObjectId(id)})
            if act != None:
                l.append(act)

        
        return render.page(l, name)

class feed:
    def GET(self, name):

        user = users.find_one({"username" : name})
        if user == None:
            return render.error("Page not found")

        l = list()  # We need to give a list because mongo returns an iterator.
        
        for id in user["actions-accomplished"]:
            act = actions.find_one({"_id" : ObjectId(id)})
            if act != None:
                l.append(act)
        
        feed_render = web.template.render('templates/')
        web.header('Content-Type', 'application/rss+xml')
        return feed_render.feed(l, name)
        
        
class login:

    def __init__(self):
        self.login_form = form.Form(
            form.Textbox("username"),
            form.Textbox("password"))
    
    def GET(self):
        form = self.login_form()
        return render.login(form, None)

    def POST(self):
        form = self.login_form()
        if not form.validates(): 
            return render.login(form, None)
        else:
            user = users.find_one({"username" : form.d.username})
            if user == None:
                return render.login(form, "Incorrect username or password")
            else:
                session.loggedin = True
                session.username = user["username"]

            raise web.seeother("/page/" + user["username"] + "/")

class logout:
    def GET(self):
        session.kill()
        raise web.seeother("/")

web.internalerror = web.debugerror

if __name__ == "__main__":
   app.run()

