#!/usr/bin/env python3

import argparse
from checkFile import checkFile

def main(file, *args):    
    fileChecker = checkFile(file)
    if(args):
        fileChecker.secureHttpChecker()

if __name__ =="__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        'file',
        help="file that contains links to check"
    )
    argParser.add_argument(
        '-s', 
        dest='secureHttp',
        action='store_true',
        help="Flag to check if https works on http links",
        required=False
    )
    args = argParser.parse_args()
    fileToCheck, secureCheck = args.file, args.secureHttp 
    
    if not secureCheck:
        main(fileToCheck)
    else:
        main(fileToCheck, secureCheck)
