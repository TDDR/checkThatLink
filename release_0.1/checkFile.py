#!/usr/bin/env python3

import urllib.request
import urllib.error
import codecs
import re

from colourText import colourText

class checkFile:
    def __init__(self, filetoCheck):
        self.file = filetoCheck
        self.file = codecs.open(self.file)
        style = colourText()
        
        for line in self.file:
            line = self.parseWebAddress(line)
            try:
                with urllib.request.urlopen(line) as response:
                    status = response.getcode()
                    if(status < 300):
                        print(f"{style._goodLink}{line}{style._plainText}")
                    elif(status == 400 or status == 404):
                        print(f"{style._badLink}{line} **{status}** {style._plainText}")
                    else:
                        print(f"{style._unknownLink}{line} **{status}** {style._plainText}")
            except urllib.error.URLError as e:
                print(e.reason)
            
    def parseWebAddress(self, anchor):
        anchor = re.sub('<a href="', '', anchor)
        anchor = re.sub('">.*$', '', anchor)
        anchor = re.sub('(/feed)', '', anchor)

        return anchor
            
    def secureHttpChecker(self):
        print("checking for secured links")