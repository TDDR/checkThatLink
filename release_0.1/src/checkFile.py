#!/usr/bin/env python3

import urllib3
import codecs
import re

from src.colourText import colourText
from src.parseURL import re_weburl

class checkFile:
    def __init__(self, filetoCheck, *args):
        self.file = codecs.open(filetoCheck)
        self.style = colourText()
        self.timeout = urllib3.Timeout(connect=2.5, read=2.5,)
        self.manager = urllib3.PoolManager(timeout=self.timeout)
        self.secureCheck = args[0]
        self.jsonOut = args[1]
        self.json = []

        self.checkThatFile()


    def checkThatFile(self):
        print('Getting status of links...')
        for line in self.file:
            line = self.parseWebAddress(line)
            if(not self.jsonOut):
                self.printStatusCode(line)
                if(self.secureCheck):
                    self.secureHttpChecker(line)
            else:
                self.printStatusAsJSON(line)
                if(self.secureCheck):
                    self.secureHttpCheckerJSON(line)
        if(self.jsonOut):
            print(self.json)
                
        
    def printStatusCode(self, link):
            try:
                response = self.manager.request('HEAD', link)
                status = response.status

                if(status < 400):
                    print(f"{self.style._goodLink}[{status}] {link} {self.style._plainText}")
                elif(status > 399):
                    print(f"{self.style._badLink}[{status}] {link} {self.style._plainText}")
            except Exception as e:
                print(f"{self.style._unknownLink}[???] {link} {self.style._plainText}")


    def printStatusAsJSON(self, link):
            try:
                response = self.manager.request('HEAD', link)
                status = response.status
                self.json.append({"url": link, "status": status})

            except Exception as e:
                self.json.append({"url": link, "status": "???"})

       
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
                status = response.status

                if(status < 400):
                    print(f"{self.style._securedLink}[{status}] {link} {self.style._plainText}")
            except Exception as e:
                pass


    def secureHttpCheckerJSON(self, link):
            isHttp = re.match('(http)', link)
            
            if(isHttp):
                link = re.sub('(http)','https', link)
                try:
                    response = self.manager.request('HEAD', link)
                    status = response.status

                    if(status < 400):
                        self.json.append({"url": link, "status": status})
                except Exception as e:
                    pass
