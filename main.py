"""
Created by hatim tachi.
Copyright © 2018 hatim tachi. All rights reserved.

"""
import Unity
import tools
import os
import threading
import queue
import SingleThread
import convertJsonToXml


def main(url, numbreOfThreads):
    unityBT = Unity.Unity(url)
    links = unityBT.getAllForums(url)
    linksDirName = "links"
    dataDirName = "data"
    print("1 - getAllLinks")
    if not os.path.exists("./" + linksDirName):
        tools.startCrowlingAllLinks(links, unityBT, dirName)
    print("2 - getAllComments")
    if not os.path.exists("./" + dataDirName):
        os.makedirs("./" + dataDirName)
    listLinks = tools.getQueueLinks(linksDirName)
    queueLock = threading.Lock()
    workQueue = queue.Queue(len(listLinks))
    tools.startScrapingLinks(listLinks, numbreOfThreads, queueLock, workQueue, unityBT)
    print("Exiting Main Thread")


def convertJsonToXml(dirNameXml="xmlData"):
    if not os.path.exists("./" + dirNameXml):
        os.makedirs("./" + dirNameXml)
    file = open("./data/indexJsonFiles.txt", "r")
    for f in file:
        f = f.replace("\n", "")
        convertJsonToXml.convertJsonToXml("./data/" + f + ".json", "./" + dirNameXml + "/" + f + ".xml")


if __name__ == '__main__':
    main(url='http://forum.ubuntu-fr.org', numbreOfThreads=50)
