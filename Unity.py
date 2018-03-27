"""
Created by hatim tachi.
Copyright © 2018 hatim tachi. All rights reserved.

"""
import beautifulSoupSC


class Unity(beautifulSoupSC.beautifulSoupSC):
    def __init__(self, url):
        beautifulSoupSC.beautifulSoupSC.__init__(self, url)
        self.url = url

    def getAllForums(self, url):

        soup = self.readUrl(url)
        res = []
        for d in soup.find_all('div', class_='tclcon'):
            for link in d.find_all('a', href=True):
                href = link.attrs['href']
                if href[0:2] != "./":
                    if href[0:7] != "http://":
                        res.append(self.changeLigneToLink(href))
        return res

    def getAllSujet(self, url):
        soup = self.readUrl(url)
        res = []
        for d in soup.find_all('div', class_='tclcon'):
            for link in d.find_all('a', href=True):
                try:
                    int(link.text)
                except ValueError:
                    href = link.attrs['href']
                    res.append(self.changeLigneToLink(href))
        return res

    def hasNextPage(self, url):
        soup = self.readUrl(url)
        res = None
        for d in soup.find_all('p', class_='pagelink conl'):
            for ligne in d.find_all('a', rel='next', href=True):
                href = ligne['href']
                if href != res:
                    res = self.changeLigneToLink(href)
        return res

    def getTitleComments(self, url):
        soup = self.readUrl(url)
        res = []
        for ti in soup.find_all('ul', class_='crumbs'):
            for title in ti.find_all('a'):
                if title.text not in res:
                    res.append(title.text)
        return res

    def getDiscussions(self, url):
        soup = self.readUrl(url)
        res = []
        for d in soup.find_all('div', class_='postmsg'):
            if len(d['class']) == 1:
                res.append(d.text)
        return res

    def changeLigneToLink(self, ligne):
        return self.url + "/" + ligne
