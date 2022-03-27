#!/usr/bin/env python3
#main.py
#This program provides the ability to run the part::out web page whilst using python code for tools
#Currently, it runs on the localhost - for a demonstration of the web page this is sufficient
#2022 Hesburgh Hackathon

import tornado.ioloop
import tornado.web
import json
import os
import re


#Function to load into the json
def saveJson(dict):
    with open("sampleParts.json", "w") as datafile:
        json.dump(dict, datafile)

#Builds lists of complete and semi complete computer builds
#Each build is a monitor, desktop, keyboard, and mouse
#Broken items are not listed in builds
#Input is the overall dictionary, lists for builds, and a list for already used parts
def compBuilder(theDict, buildList, theUsed):
    theDict = sorted(theDict.items(), key=lambda y: y[1]["type"])
    theDict = dict(theDict)
    for x in range(3):
        for key in buildList[0]:
            if buildList[x][key]["item"] == ' ':
                for dkey in theDict: 
                    if theDict[dkey]["type"] == key:
                        if theDict[dkey]["broken"] == False:
                            if theDict[dkey]["item"] not in theUsed:
                                buildList[x][key] = theDict[dkey]
                                theUsed.append(theDict[dkey]["item"])
                                del theDict[dkey]
                                break 

#makes a list of broken objects
#searches through common synonyms for broken
def makeBroken(theDict):
    theRegex = re.compile(r'fix|broke|crack|repair|busted|not work|does not work|fixing')
    for key in theDict:
        if re.search(theRegex, theDict[key]["notes"].lower()):
            theDict[key]["broken"] = True;
            

#makes an output ticket
#The ticket has properties to contact the owners of the parts
def makeOutput(theDict, buildList):
    fileName = "buildTicket.txt"
    with open(fileName, 'w') as outFile:
        for x in range(3):
            if  {"item": " "} not in buildList[x].values():
                outFile.write(f'Build {x+1}:\n')
                outFile.write(f'Desktop: {buildList[x]["desktop"]["item"]} from {buildList[x]["desktop"]["name"]} at {buildList[x]["desktop"]["dorm"]} with email of {buildList[x]["desktop"]["email"]}\n')
                outFile.write(f'Mouse: {buildList[x]["mouse"]["item"]} from {buildList[x]["mouse"]["name"]} at {buildList[x]["mouse"]["dorm"]} with email of {buildList[x]["mouse"]["email"]}\n')
                outFile.write(f'Keyboard: {buildList[x]["keyboard"]["item"]} from {buildList[x]["keyboard"]["name"]} at {buildList[x]["keyboard"]["dorm"]} with email of {buildList[x]["keyboard"]["email"]}\n')
                outFile.write(f'Monitor: {buildList[x]["monitor"]["item"]} from {buildList[x]["monitor"]["name"]} at {buildList[x]["monitor"]["dorm"]} with email of {buildList[x]["monitor"]["email"]}\n\n')


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        self.render("sevIndex.html", dict=theDict, theBuilds=theBuilds, theUsed=theUsed)
        
        #Gathers user entries to put in the dictionary
        theName = self.get_argument('name', '')
        theEmail = self.get_argument('email', '')
        theItem = self.get_argument('item', '')
        theNotes = self.get_argument('notes', '')
        theType = self.get_argument('type', '').lower()
        theDorm = self.get_argument('dorm', '')

        #if the type is not entered by default it is misc
        if not theType:
            theType = 'misc'

        #puts the new entry in the dictionary
        if (theItem):
            newPart = {}
            newPart["name"] = theName
            newPart["email"] = theEmail
            newPart["item"] = theItem
            newPart["notes"] = theNotes
            newPart["type"] = theType
            newPart["dorm"] = theDorm
            newPart["broken"] = False
            theDict[newPart["item"]] = newPart

        #builds computers and saves output
        makeBroken(theDict)
        compBuilder(theDict, theBuilds, theUsed)
        saveJson(theDict)
        makeOutput(theDict, theBuilds)
        
    def get(self):       
        self.render("sevIndex.html", dict=theDict, theBuilds=theBuilds, theUsed=theUsed)

 
if __name__ == "__main__":

    #first gets the dictionary from the json
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
    makeOutput(theDict, theBuilds)

    #main web page loop
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()
