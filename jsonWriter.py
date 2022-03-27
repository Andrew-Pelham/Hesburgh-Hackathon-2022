#!/usr/bin/env python3

import json

theDict = {}

thePart = {}
thePart["name"] = "Ted Example"
thePart["item"] = "AOC Monitor"
thePart["email"] = "tedE@gmail.com"
thePart["dorm"] = "Stanford"
thePart["notes"] = "Light cracking"
thePart["type"] = "monitor"
thePart["broken"] = True


thePart2 = {}
thePart2["name"] = "Joseph Rodman"
thePart2["item"] = "Gaming Keyboard"
thePart2["email"] = "jrman@yahoo.com"
thePart2["dorm"] = "Keenan"
thePart2["notes"] = "NIB"
thePart2["type"] = "keyboard"
thePart2["broken"] = False

theDict[thePart["item"]] = thePart
theDict[thePart2["item"]] = thePart2
with open("sampleParts.json", "w") as outfile:
    json.dump(theDict, outfile)
