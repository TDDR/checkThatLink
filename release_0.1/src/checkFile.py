#!/usr/bin/env python3

import urllib3
import codecs
import re
import sys

from src.colourText import colourText
from src.parseURL import re_weburl

class checkFile:
    def __init__(self, args):
        self.file = codecs.open(args.file)
        self.style = colourText()
        self.timeout = urllib3.Timeout(connect=2.5, read=2.5,)
        self.manager = urllib3.PoolManager(timeout=self.timeout)
        self.secureCheck = args.secureHttp
        self.jsonOut = args.json
        self.json = []
        self.all = args.all
        self.good = args.good
        self.bad = args.bad
        self.ignoreList = self.getIgnoreList(args.ignoreFile)
        self.allLinks = []

        self.checkThatFile()

        if(self.good):
            if(self.jsonOut):
                self.printGoodResultsJSON()
            else:
                self.printGoodResults()
        elif(self.bad):
            if(self.jsonOut):
                self.printBadResultsJSON()
            else:
                self.printBadResults()
        else:
            if(self.jsonOut):
                self.printAllJSON()
            else:
                self.printAll()


    def checkThatFile(self):
        print('Getting status of links...')
        for line in self.file:
            line = self.parseWebAddress(line)
            if self.doNotIgnore(line):
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
    

    def printAllJSON(self):
        stripped = []

        for l in self.allLinks:
            stripped.append({"url":l["url"], "status": l["status"]})
      
        print(f'{stripped}')

    def printGoodResults(self):
        for l in self.allLinks:
            if(l["status"] == "???"):
                pass
            elif(l["status"] < 400 and l["secured"]):
                print(f'{self.style._securedLink}[{l["status"]}] {l["url"]}{self.style._plainText}')
            elif(l["status"] < 400 and not l["secured"]):
                print(f'{self.style._goodLink}[{l["status"]}] {l["url"]}{self.style._plainText}')


    def printGoodResultsJSON(self):
        goodLinks = []

        for l in self.allLinks:
            if(l["status"] == "???"):
                pass
            elif(l["status"] < 400):
                goodLinks.append({"url":l["url"], "status": l["status"]})
        
        print(f'{goodLinks}')

    def printBadResults(self):
        for l in self.allLinks:
            if(l["status"] == "???"):
                    print(f'{self.style._unknownLink}[{l["status"]}] {l["url"]}{self.style._plainText}')
            elif(l["status"] > 399):
                print(f'{self.style._badLink}[{l["status"]}] {l["url"]}{self.style._plainText}')


    def printBadResultsJSON(self):
        badLinks = []

        for l in self.allLinks:
            if(l["status"] == "???"):
                badLinks.append({"url":l["url"], "status": l["status"]})
            elif(l["status"] > 399):
                badLinks.append({"url":l["url"], "status": l["status"]})
       
        print(f'{badLinks}')
    

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
          
    # returns false if url's domain is in ignoreList
    def doNotIgnore(self, url):   
      if url is not None:
        domain = re.split('(?<!/|:)/', url)[0]
        if domain in self.ignoreList:
          return False
      return True

    # returns a list of all regex matches inside ignoreFile
    def getIgnoreList(self, ignoreFile):    
        found = []
        try: 
            if ignoreFile:
                with open(ignoreFile) as src:
                    text = src.read() 
                    found = re.findall('^https?://.*[^\s/]', text, flags=re.MULTILINE)
                    comment = re.search('^#.*', text, flags=re.MULTILINE)
                    return found if comment or found else sys.exit(1)
            return found
        except:
            print(f'Error with {ignoreFile}')
            sys.exit(1)