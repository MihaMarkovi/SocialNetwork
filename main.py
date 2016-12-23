#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo
from google.appengine.api import users


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        # naprej dobimo uporabnika
        user = users.get_current_user()
        seznam = Sporocilo.query().order(-Sporocilo.datum).fetch()
        #preverimo ce obstaja
        if user:
            logiran = True
            logout_url = users.create_logout_url("/")


            params={"logiran": logiran, "logout_url": logout_url, "user": user}

        else:
            logiran = False

            login_url = users.create_login_url("/")

            params={"login_url": login_url, "logiran": logiran}
        params["seznam"] = seznam
        return self.render_template("hello.html", params=params)

    def post(self):
        user = users.get_current_user()
        rezultat = self.request.get("vnos")
        besedilo = str(jinja2.escape(rezultat))
        objava = besedilo.replace("SmartNinja", '<img style="width:100px; height:100px" src="assets/emotes/ninja.gif">');("lolek", "bolek")
        posiljatelj = user.nickname()
        sporocilo = Sporocilo(vnos=objava, poslal=posiljatelj)
        sporocilo.put()
        return self.redirect_to("glavna_stran")



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="glavna_stran"),
], debug=True)
