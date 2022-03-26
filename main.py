#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import json
import os

#Function to load into the json
def saveJson(dict):
    with open("sampleParts.json", "w") as datafile:
        json.dump(dict, datafile)

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        self.render("secIndex.html", dict=theDict)
        theName = self.get_argument('name', '')
        theEmail = self.get_argument('email', '')
        theItem = self.get_argument('item', '')
        theNotes = self.get_argument('notes', '')
        theType = self.get_argument('type', '')

        if not theType:
            theType = 'Misc'

        print(f'{theName} {theEmail} {theItem} {theNotes} {theType}')
        if (theName):
            newPart = {}
            newPart["name"] = theName
            newPart["email"] = theEmail
            newPart["item"] = theItem
            newPart["notes"] = theNotes
            newPart["type"] = theType
            theDict[newPart["item"]] = newPart
        print(theDict)
        saveJson(theDict)
#<center>
#<img src="https://www.tornadoweb.org/en/stable/_images/tornado.png">
#</center>
#''')
        #for line in theDict:
            #self.write(f'<center> {theDict[line]} </center>')
        #if "newAddition" not in theDict:
            #theDict["newAddition"] = "Testing"
            #with open("theJson.txt", "w") as dataFile:
                #json.dump(theDict, dataFile)
    def get(self):       
        self.render("secIndex.html", dict=theDict)


        
'''
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])
    '''
class make_app(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/", MainHandler),
                    ]
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":

    data = open("sampleParts.json")
    theDict = json.load(data)
    r = "hello"
    #app = make_app()
    settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
    app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/(.*)", tornado.web.StaticFileHandler,
     dict(path=settings['static_path'])),
], **settings)

    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()
