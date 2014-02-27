import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket

from tornado.ioloop import PeriodicCallback

from session import *
from loadConf import *
from login import *

confAveug = False
ficLog = Login()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        iden = self.get_argument("id","")
        mdp = self.get_argument("mdp","")

        login = Login()
        autorise = login.connexion(iden, mdp)
        #maison = httplib.HTTPConnection("192.168.16.150", 80)
        if autorise == True:
            ficLog.enregDansLog(iden,"Authorized user connection","IP TO DO")
            if confAveug == True:
                print '->Send audio alarm authorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20autorisee")'
            else:
                print '->Send visual alarm authorized user'
                print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->Authorized user access"
            self.set_secure_cookie("user", iden)
            self.redirect("/video")
        else:
            ficLog.enregDansLog(iden,"Unauthorized user connection","IP TO DO")
            if confAveug == True:
                print '->Send audio alarm unauthorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20non%20autorisee")'
            else:
                    print '->Send visual alarm unauthorized user'
                    print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->An unauthorized user try to access"
            self.write("Unauthorized user access")

class VideoHandler(BaseHandler):
    def get(self):
        if not self.current_user :
            self.redirect("/")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class UnauthorizedHandler(BaseHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        force = self.get_argument("id","")
        if force == 1 :
            self.set_secure_cookie("user", "illegalUser")
        else :
            self.redirect("/")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/video", VideoHandler),
    (r"/unauthorized", UnauthorizedHandler),
], cookie_secret="1213215656")

if __name__ == "__main__":
    hand = LoadConf()
    confAveug = hand.estAveugle()
    if confAveug == True:
        print "->Blind unhabitant system configuration"
    else :
        print "->Not blind unhabitant system configuration"

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()

