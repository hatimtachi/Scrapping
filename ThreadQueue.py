"""
Created by hatim tachi.
Copyright © 2018 hatim tachi. All rights reserved.

"""
import threading
import tools


class Thread(threading.Thread):
    exitFlag = 0

    def __init__(self, threadId, q, queueLock, workQueue, unityBT):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.q = q
        self.queueLock = queueLock
        self.workQueue = workQueue
        self.unityBT = unityBT

    def run(self):
        print("Starting thread Id :" + self.threadId)
        tools.process_data(self.threadId, self.unityBT, self.q, self.queueLock, self.workQueue)
        print("Exiting thread Id :" + self.threadId)

