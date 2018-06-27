from pymongo import MongoClient
import tornado.ioloop
import tornado.web


client = MongoClient()
db = client.Airports
posts = db.posts


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('<html><body background= "file:///Users/Daniel/Downloads/airport-runway-wallpaper-2.jpg"'
                   'style="height: 100% background-position: '
                   'center; background-repeat: no-repeat; background-size: '
                   'cover"> <form method="POST" style="text-align: center; '
                   'padding-top: 22%">Insert Airport Name:<br><br><input type="text" name="message" '
                   'style="background: transparent;"><br><input type="submit" '
                   'value="Submit" style="background: transparent;"></form></body></html>')

    def post(self):
        airportName = posts.find_one({'name': self.get_body_argument("message")})
        self.write('<div align="center" style="padding-top: 22%"><textarea rows="4" cols="30" style="background: '
                   'transparent;">Airport: ' + airportName['name'] + '\nLocation: '+airportName['location']+'\nPhone:'
                   + airportName['phone'] + '</textarea><br><input type="button" value="New Submission" '
                   'style="background: transparent;" onClick="window.location.reload()"></div>')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


app = make_app()
app.listen(8888)
tornado.ioloop.IOLoop.current().start()