#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import json
import os


#Function to load into the json
def saveJson(dict):
    with open("sampleParts.json", "w") as datafile:
        json.dump(dict, datafile)

def compBuilder(theDict, buildList, theUsed):
    theDict = sorted(theDict.items(), key=lambda y: y[1]["type"])
    theDict = dict(theDict)
    for x in range(3):
        for key in buildList[0]:
            if buildList[x][key]["item"] == ' ':
                for dkey in theDict: 
                    if theDict[dkey]["type"] == key:
                        if theDict[dkey]["item"] not in theUsed:
                            buildList[x][key] = theDict[dkey]
                            theUsed.append(theDict[dkey]["item"])
                            del theDict[dkey]
                            break 
    

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        self.render("fifIndex.html", dict=theDict, theBuilds=theBuilds, theUsed=theUsed)
        
        #Gathers user entries to put in the dictionary
        theName = self.get_argument('name', '')
        theEmail = self.get_argument('email', '')
        theItem = self.get_argument('item', '')
        theNotes = self.get_argument('notes', '')
        theType = self.get_argument('type', '').lower()
        theDorm = self.get_argument('dorm', '')

        if not theType:
            theType = 'misc'

        if (theItem):
            newPart = {}
            newPart["name"] = theName
            newPart["email"] = theEmail
            newPart["item"] = theItem
            newPart["notes"] = theNotes
            newPart["type"] = theType
            newPart["dorm"] = theDorm
            theDict[newPart["item"]] = newPart

        compBuilder(theDict, theBuilds, theUsed)
        saveJson(theDict)
        
        #compBuilder(theDict, theBuilds, theUsed)
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
        self.render("fifIndex.html", dict=theDict, theBuilds=theBuilds, theUsed=theUsed)


        
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

    #load settings for Tornado to import the proper css/images
    settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

    #Set up the web app
    app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/(.*)", tornado.web.StaticFileHandler,
     dict(path=settings['static_path'])),
], **settings)

    #initialize the builds as empty
    theBuilds = []
    theUsed = []
    for x in range(3):
        emptyDict = {}
        plainDict = {"item": " "}
        emptyDict["desktop"] = plainDict
        emptyDict["monitor"] = plainDict
        emptyDict["keyboard"] = plainDict
        emptyDict["mouse"] = plainDict
        theBuilds.append(emptyDict)

    #Build computers
    compBuilder(theDict, theBuilds, theUsed)

    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()
