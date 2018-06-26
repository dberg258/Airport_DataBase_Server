import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('<html><body><form method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.write('<input type="button" value="New Submission" onClick="window.location.reload()">')
        airportName = airportDB3.posts.find_one({'name': self.get_body_argument("message")})
        self.write("Phone: " + airportName['phone'])


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


app = make_app()
app.listen(8888)
tornado.ioloop.IOLoop.current().start()