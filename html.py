# -*- coding: utf-8 -*-
"""
Created on Jun 29, 2014

@author: dukie
"""

import urllib2 as urllib2
from StringIO import StringIO
import gzip
import BeautifulSoup

defaultCoding = "utf-8"


class Taker:
    def __init__(self, url=None):
        if url:
            self.url = url
        else:
            self.url = "http://www.vkursax.ru"

    def getHTML(self, url=None):
        if url != None:
            self.url = url
            self.opener = urllib2.Request(self.url)
        self.opener.add_header("User-Agent",
                                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36")

        try:
            htmlResult = urllib2.urlopen(self.opener)
            byteText = None
            if htmlResult.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(htmlResult.read())
                f = gzip.GzipFile(fileobj=buf)
                byteText = f.read()
            else:
                byteText = htmlResult.read()
            htmlResult.close()
            soup = BeautifulSoup.BeautifulSoup(byteText)
            coding = soup.originalEncoding
            if not coding:
                coding = defaultCoding
            text = byteText.decode(coding)
            return text

        except urllib2.HTTPError as e:
            print e
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "404 not found"
            return '404'
        except urllib2.URLError:
            # TODO: need to prevent stack overflow
            print "Address temporary not available, retry"
            return self.getHTML(url)

if __name__ == '__main__':
    testTaker = Taker()
    print testTaker.getHTML('http://www.vkursax.ru/')