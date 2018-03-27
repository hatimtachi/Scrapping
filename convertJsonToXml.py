"""
Created by hatim tachi.
Copyright © 2018 hatim tachi. All rights reserved.

"""
import json
import xml.etree.ElementTree as ET


def convertJsonToXml(jsonFile, xmlFileOutput):
    positionText = 0
    isQuestion = True
    data = json.load(open(jsonFile))
    string = ""
    response = ""
    question = ""
    for description in data:
        for element in data[description]:

            for text in element:

                index = element[text].find("Dernière modification")
                if index != -1:
                    string = element[text]
                    string = string[:index]
                else:
                    string = element[text]

            if (positionText == 2 or positionText == 3) and isQuestion:
                question += " " + string
            elif positionText == 0 and not isQuestion:
                question += " " + string

            elif not isQuestion:
                response += " " + string

            positionText += 1
        string = ""
        positionText = 0
        isQuestion = False

    createXmlFile(question, response, xmlFileOutput)


def createXmlFile(question, response, fileName):
    root = ET.Element("Data")

    ET.SubElement(root, "Question").text = question
    ET.SubElement(root, "Response").text = response

    tree = ET.ElementTree(root)
    tree.write(fileName)
