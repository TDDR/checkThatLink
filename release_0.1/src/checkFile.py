#!/usr/bin/env python3

import urllib3
import codecs
import re

from src.colourText import colourText
from src.parseURL import re_weburl

class checkFile:
    def __init__(self, args):
        self.file = codecs.open(args.file)
        self.style = colourText()
        self.timeout = urllib3.Timeout(connect=2.5, read=2.5,)
        self.manager = urllib3.PoolManager(timeout=self.timeout)
        self.secureCheck = args.secureHttp
        self.all = args.all
        self.good = args.good
        self.bad = args.bad
        self.allLinks = []
        
        self.checkThatFile()

        if(self.good):
            self.printGoodResults()
        elif(self.bad):
            self.printBadResults()
        else:
            self.printAll()


    def checkThatFile(self):
        print('Getting status of links...')
        for line in self.file:
            line = self.parseWebAddress(line)
            self.headRequest(line)
            
            if(self.secureCheck):
                self.secureHttpChecker(line)
            

    def printAll(self):    
        for l in self.allLinks:
            if(l["status"] == "???"):
                print(f'{self.style._unknownLink}[{l["status"]}] {l["url"]}{self.style._plainText}')
            elif(l["status"] < 400 and l["secured"]):
                print(f'{self.style._securedLink}[{l["status"]}] {l["url"]}{self.style._plainText}')
            elif(l["status"] < 400 and not l["secured"]):
                print(f'{self.style._goodLink}[{l["status"]}] {l["url"]}{self.style._plainText}')
            else:
                print(f'{self.style._badLink}[{l["status"]}] {l["url"]}{self.style._plainText}')

    def printGoodResults(self):
        for l in self.allLinks:
            if(l["status"] == "???"):
                pass
            elif(l["status"] < 400 and l["secured"]):
                print(f'{self.style._securedLink}[{l["status"]}] {l["url"]}{self.style._plainText}')
            elif(l["status"] < 400 and not l["secured"]):
                print(f'{self.style._goodLink}[{l["status"]}] {l["url"]}{self.style._plainText}')


    def printBadResults(self):
        for l in self.allLinks:
            if(l["status"] == "???"):
                    print(f'{self.style._unknownLink}[{l["status"]}] {l["url"]}{self.style._plainText}')
            elif(l["status"] > 399):
                print(f'{self.style._badLink}[{l["status"]}] {l["url"]}{self.style._plainText}')
    

    def headRequest(self, link):
            try:
                response = self.manager.request('HEAD', link)
                self.allLinks.append({"url":link, "status": response.status, "secured": False})
            except Exception as e:
                    self.allLinks.append({"url":link, "status": "???", "secured": False})

            
    def parseWebAddress(self,line):
        line = re.sub('<a href="', '', line)
        line = re.sub('">.*$[\r\n]', '', line)         
        url = re_weburl.search(line)

        if(url):
            url = url.group(0)     

        return url

            
    def secureHttpChecker(self, link):
        isHttp = re.match('(http)', link)
        
        if(isHttp):
            link = re.sub('(http)','https', link)
            try:
                response = self.manager.request('HEAD', link)
                self.allLinks.append({"url":link, "status": response.status, "secured": True})
            except Exception as e:
                pass
