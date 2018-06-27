from pymongo import MongoClient
import tornado.ioloop
import tornado.web


client = MongoClient()
db = client.Airports
posts = db.posts


def spellCheck(inputted):
    airportNames = []
    for post in posts.find():
        airportNames.append(post['name'])

    recommendations = set()

    for word in airportNames:
        letterCount = 0
        for letter in word:
            if inputted.__contains__(letter):
                letterCount += 1

        if letterCount / len(word) >= .65:
            recommendations.add(word)

    return recommendations


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

            spellCheckRecs = spellCheck(self.get_body_argument("message"))
            self.write('Not A Valid Airport</br></br>')
            self.write("Did you mean:</br></br>")
            for word in spellCheckRecs:
                self.write(word+"<br>")
            self.render('mainPage.html')


def make_app():
    return tornado.web.Application([(r"/", MainHandler)])


app = make_app()
app.listen(8888)
tornado.ioloop.IOLoop.current().start()