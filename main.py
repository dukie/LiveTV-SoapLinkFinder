# -*- coding: utf-8 -*-
"""
Created on Jun 29, 2014

@author: dukie
"""

import sys
from html import Taker
import BeautifulSoup
import re

#RegExps
expr = re.compile(u'a href=\"http:\/\/livetv.sx\/eventinfo\/(?P<linkPart>[0-9_a-z]+?)\/"', re.I)
soupExpr = re.compile('sop:\/\/', re.I)
numberExpr = re.compile('(?P<lastPageNumber>[0-9]+)', re.I)


searchTemplate = "https://www.google.ru/search?newwindow=1&q=inurl:eventinfo+site:livetv.sx+{0}"

bcTemplate = 'http://livetv.sx/eventinfo/{0}/'


def printLinksList(linksList):
    if linksList:
        for link in linksList:
            print link


def getSoupLinks(soup):
    links = soup.findAll(text=soupExpr)
    return links

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please specify teams. example: Бразилия Германия"
        exit(1)
    searchString = "+".join(sys.argv[1:])
    print searchTemplate.format(searchString)

    taker = Taker()
    searchContent = taker.getHTML(searchTemplate.format(searchString))
    searchResult = expr.search(searchContent)

    if not searchResult:
        print "Game hasn't been found. Please try another query"
        exit(1)
    print "Game was found"
    linkPart = searchResult.group('linkPart')
    print linkPart

    gameBaseUrl = bcTemplate.format(linkPart)
    bcContent = taker.getHTML(gameBaseUrl)
    soup = BeautifulSoup.BeautifulSoup(bcContent)
    gameTitle = soup.find('td', {'bgcolor': "#f0f0f0"}).find('td',{'class':'small'}).text
    print gameTitle
    numberTag = soup.find('a', {'class': 'pages1','href':re.compile('\/eventinfo\/')}).text
    curPageNum = 0
    if numberTag:
        match = numberExpr.search(numberTag)
        if match:
            curPageNum = int(match.group('lastPageNumber'))
            print "Numbers of comment pages: {0}".format(curPageNum)
        else:
            print "Comments link doesn't contain numbers"
            exit(1)
    else:
        print "No page comments section"
        exit(1)
    printLinksList(getSoupLinks(soup))

    gameBaseUrlTemplate = gameBaseUrl + '{0}/'
    while curPageNum > 0:
        print "Current Page: {0}".format(curPageNum)
        bcContent = taker.getHTML(gameBaseUrlTemplate.format(curPageNum))
        soup = BeautifulSoup.BeautifulSoup(bcContent)
        printLinksList(getSoupLinks(soup))
        curPageNum -= 1
    print "Done"