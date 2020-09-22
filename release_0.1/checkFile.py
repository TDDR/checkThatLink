#!/usr/bin/env python3

import urllib3
import codecs
import re

from colourText import colourText

class checkFile:
    def __init__(self, filetoCheck, *args):
        self.file = filetoCheck
        self.file = codecs.open(self.file)
        self.style = colourText()
        self.manager = urllib3.PoolManager()
        self.secureCheck = args
        
        self.checkThatFile()

    def checkThatFile(self):
        print('Getting status of link...')
        for line in self.file:
            line = self.parseWebAddress(line)
            status = 0

            self.printStatusCode(line)
            
            if(self.secureCheck):
                self.secureHttpChecker(line)
    
    
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

            
    def parseWebAddress(self, anchor):
        anchor = re.sub('<a href="', '', anchor)
        anchor = re.sub('">.*$[\r\n]', '', anchor)

        return anchor
            
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
