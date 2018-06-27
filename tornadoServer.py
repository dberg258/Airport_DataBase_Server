from pymongo import MongoClient
import tornado.ioloop
import tornado.web
import time


client = MongoClient()
db = client.Airports
posts = db.posts


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('mainPage.html')

    def post(self):

        try:
            airportName = posts.find_one({'name': self.get_body_argument("message")})
            self.write('<div align="center" style="padding-top: 22%"><textarea rows="4"'
                       ' cols="30" style="background:transparent;">Airport: ' + airportName['name']
                       + '\nLocation: '+airportName['location']+'\nPhone:' + airportName['phone']
                       + '</textarea><br><input type="button" value="New Submission" '
                         'style="background: transparent;" onClick="window.location.reload()"></div>')
        except:
            self.write('Not A Valid Airport!')
            self.render('mainPage.html')




def make_app():
    return tornado.web.Application([(r"/", MainHandler)])


app = make_app()
app.listen(8888)
tornado.ioloop.IOLoop.current().start()