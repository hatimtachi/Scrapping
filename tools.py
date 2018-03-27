"""
Created by hatim tachi.
Copyright © 2018 hatim tachi. All rights reserved.

"""
import ThreadQueue
import os
import SingleThread
import json


def process_data(threadId, unityBT, q, queueLock, workQueue):
    while not ThreadQueue.Thread.exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            link = q.get()
            startPosition = link.find("id=")
            queueLock.release()
            writeDiscussionJson("data", unityBT, link, getAllDiscussion(link, unityBT), link[startPosition:])
            file = open("./data/indexJsonFiles.txt", "a")
            file.write(link[startPosition:]+"\n")
            print(threadId, "--", link[startPosition:])
        else:
            queueLock.release()


def getAllLinksSujet(threadId, url, unityBTSC):
    listOfLinks = []
    listOfLinks.extend(unityBTSC.getAllSujet(url))
    linkNext = unityBTSC.hasNextPage(url)
    while linkNext is not None:
        if SingleThread.SingleThread.exitFlag:
            threadId.exit()
        listOfLinks.extend(unityBTSC.getAllSujet(linkNext))
        linkNext = unityBTSC.hasNextPage(linkNext)
    return listOfLinks


# create SignleThreads to get all links from url
def startCrowlingAllLinks(links, unityBT, dirName):
    threads = []
    for link in range(len(links)):
        threads.append(SingleThread.SingleThread(link, links[link], unityBT, dirName))
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()


def getQueueLinks(nameDir):
    res = []
    if os.path.exists("./" + nameDir):
        file = open("./" + nameDir + "/links.txt", "r")
        for line in file:
            res.append(line.replace("\n", ""))
    print(len(res))
    return res


def getAllDiscussion(url, unityBT):
    listDisc = []
    listDisc.extend(unityBT.getDiscussions(url))
    nextLink = unityBT.hasNextPage(url)
    while nextLink is not None:
        listDisc.extend(unityBT.getDiscussions(nextLink))
        nextLink = unityBT.hasNextPage(nextLink)
    return listDisc


def writeDiscussionJson(nameDir, unityBT, url, listDiscussion, idLink):
    if not os.path.exists('./' + nameDir):
        os.makedirs("./" + nameDir)
    file = open("./" + nameDir + "/"+idLink+".json", "w")
    title = unityBT.getTitleComments(url)
    jsonArrayTitle = []
    jsonArrayDisc = []
    for ti in title:
        jsonTitle = {'path': ti}
        jsonArrayTitle.append(jsonTitle)
    for disc in listDiscussion:
        jsonDisc = {"text": disc}
        jsonArrayDisc.append(jsonDisc)
    dic = {"title ": jsonArrayTitle, "Discussion": jsonArrayDisc}
    file.write(json.dumps(dic, ensure_ascii=False))


def startScrapingLinks(listLinks, nbThread, queueLock, workQueue, unityBT):
    threadList = [str(thread) for thread in range(nbThread)]
    ThreadQueue.Thread.exitFlag = 0
    nameList = listLinks
    threads = []
    for tId in threadList:
        thread = ThreadQueue.Thread(tId, workQueue, queueLock, workQueue, unityBT)
        thread.start()
        threads.append(thread)

    queueLock.acquire()
    for data in nameList:
        workQueue.put(data)
    queueLock.release()

    while not workQueue.empty():
        pass

    ThreadQueue.Thread.exitFlag = 1

    for t in threads:
        t.join(timeout=1)
