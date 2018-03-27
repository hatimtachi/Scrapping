"""
Created by hatim tachi.
Copyright © 2018 hatim tachi. All rights reserved.

"""

import bs4
import urllib.request


class beautifulSoupSC:
    def __init__(self, url):
        self.url = url

    def readUrl(self, url):
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
            soup = bs4.BeautifulSoup(data, 'html.parser')
        return soup

