import webapp2


class MainPage(webapp2.RequestHandler):

    def get(self):
        #echostr = self.request.get('echostr')
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("echostr")


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

# http://www.google.com:80/
