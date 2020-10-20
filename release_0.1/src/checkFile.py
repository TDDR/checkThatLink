#!/usr/bin/env python3

import urllib3
import codecs
import re
import sys

from src.colourText import colourText
from src.parseURL import re_weburl

class checkFile:
    def __init__(self, args):
        self.fileToCheck = codecs.open(args.file)
        self.secureCheck = args.secureHttp
        self.jsonOut = args.json
        self.all = args.all
        self.good = args.good
        self.bad = args.bad
        self.ignoreFile = args.ignoreFile
       
        self.style = colourText()
        self.timeout = urllib3.Timeout(connect=2.5, read=2.5,)
        self.manager = urllib3.PoolManager(timeout=self.timeout)
       
        self.allLinks = []
        self.jsonLinks = []
        self.ignoreList = []

        try:
            if self.ignoreFile:
                self.getIgnoreList(self.ignoreFile)
            
            self.checkThatFile()
        except Exception as e:
            print(f'\n{e}')

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

    #Main function that performs a head request on every line
    #of the file
    def checkThatFile(self):
        print('Getting status of links...')
        for line in self.fileToCheck:
            line = self.parseWebAddress(line)
            if self.doNotIgnore(line):
              self.headRequest(line)
              if(self.secureCheck):
                  self.secureHttpChecker(line)

    #Parse the web address from the given line of a file
    def parseWebAddress(self,line):
        line = re.sub('<a href="', '', line)
        line = re.sub('">.*$[\r\n]', '', line)         
        url = re_weburl.search(line)

        if(url):
            url = url.group(0)     

        return url

    #Gets the status of a URL response
    def headRequest(self, link):
            try:
                response = self.manager.request('HEAD', link)
                self.allLinks.append({"url":link, "status": response.status, "secured": False})
            except Exception as e:
                    self.allLinks.append({"url":link, "status": "???", "secured": False})

    #Checks to see if a 'http' link will work with 'https'
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
      for domain in self.ignoreList:
            if re.match(f'{domain}', url):
                return False
      return True

    # returns a list of all regex matches inside ignoreFile
    def getIgnoreList(self, ignoreFile):    
        try: 
            if ignoreFile:
                with open(ignoreFile) as src:
                    self.ignoreList = re.findall(r'^http[s]?://.*[^\s/]', src.read(), re.MULTILINE)
                    src.seek(0)
                    for line in src:
                        if re.match('#', line) or re.match('\n', line):
                            pass
                        elif re.match(r'^http[s]?://', line):
                            pass
                        else:
                            raise ValueError('\nInvalid file format for --ignore. Lines must start with "#", "http://", or "https://" only.')
        except FileNotFoundError as e:             
            raise
            

    def printAll(self):    
        for line in self.allLinks:
            if(line["status"] == "???"):
                print(f'{self.style._unknownLink}[{line["status"]}] {line["url"]}{self.style._plainText}')
            elif(line["status"] < 400 and line["secured"]):
                print(f'{self.style._securedLink}[{line["status"]}] {line["url"]}{self.style._plainText}')
            elif(line["status"] < 400 and not line["secured"]):
                print(f'{self.style._goodLink}[{line["status"]}] {line["url"]}{self.style._plainText}')
            else:
                print(f'{self.style._badLink}[{line["status"]}] {line["url"]}{self.style._plainText}')
    

    def printAllJSON(self):
        for line in self.allLinks:
            self.jsonLinks.append({"url":line["url"], "status": line["status"]})
      
        print(f'{self.jsonLinks}')

    def printGoodResults(self):
        for line in self.allLinks:
            if(line["status"] == "???"):
                pass
            elif(line["status"] < 400 and line["secured"]):
                print(f'{self.style._securedLink}[{line["status"]}] {line["url"]}{self.style._plainText}')
            elif(line["status"] < 400 and not line["secured"]):
                print(f'{self.style._goodLink}[{line["status"]}] {line["url"]}{self.style._plainText}')


    def printGoodResultsJSON(self):
        for line in self.allLinks:
            if(line["status"] == "???"):
                pass
            elif(line["status"] < 400):
                self.jsonLinks.append({"url":line["url"], "status": line["status"]})
        
        print(f'{self.jsonLinks}')

    def printBadResults(self):
        for line in self.allLinks:
            if(line["status"] == "???"):
                    print(f'{self.style._unknownLink}[{line["status"]}] {line["url"]}{self.style._plainText}')
            elif(line["status"] > 399):
                print(f'{self.style._badLink}[{line["status"]}] {line["url"]}{self.style._plainText}')


    def printBadResultsJSON(self):
        for line in self.allLinks:
            if(line["status"] == "???"):
                self.jsonLinks.append({"url":line["url"], "status": line["status"]})
            elif(line["status"] > 399):
                self.jsonLinks.append({"url":line["url"], "status": line["status"]})

        print(f'{self.jsonLinks}')