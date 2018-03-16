import jinja2
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb


def guestbook_key(guestbook_name='default_guestbook'):
    return ndb.Key('Guestbook', guestbook_name)

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Greeting(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        greetings_query = Greeting.query(ancestor=guestbook_key()).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            nickname = user.nickname()
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            nickname = 'Gast'

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(greetings=greetings,
                                                url=url,
                                                url_linktext=url_linktext,
                                                nickname=nickname))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        greeting = Greeting(parent=guestbook_key())

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)
