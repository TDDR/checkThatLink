#!/usr/bin/env python3

import argparse
from src.checkFile import checkFile

if __name__ =="__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        'file',
        help="file that contains links to check"
    )
    argParser.add_argument(
        '-v','--version',
        action='version',
        version='%(prog)s 0.1'
    )
    argParser.add_argument(
        '-s', '--secureHttp', 
        dest='secureHttp',
        action='store_true',
        help="flag to check if https works on http links",
        required=False
    )
    argParser.add_argument(
        '-j', '--json',
        dest='json', 
        action='store_true',
        help="display output as JSON",
        required=False
    )

    args = argParser.parse_args()
    fileToCheck = args.file
    secureCheck = args.secureHttp if args.secureHttp else None
    json = args.json if args.json else None 
    
    if not args:
        checkFile(fileToCheck)
    else:
        checkFile(fileToCheck, secureCheck, json)