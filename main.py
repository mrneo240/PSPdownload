#!/usr/bin/python
# -*- coding: utf-8 -*-

import dataset, sys, os, glob, shutil
from functions import *
#import uidefs

db = dataset.connect("sqlite:///games.db")
games = db['games']
p2z = "pkg2zip.exe" if os.name == 'nt' else "pkg2zip"

print("PSP game download client")

if len(sys.argv) >= 2:
    clevel = 0
    if sys.argv[2] == "cso":
        clevel = sys.argv[3]
    process_dl(games, sys.argv[2], clevel, sys.argv[1], p2z)
    sys.exit()
        
while True:
    if not os.path.exists("games.db"):
        print("database doesn't exist, do you wish to initialise it?")
        yn = input()
        if yn == "y":
            init_db()
            print("Init finished")
        else:
            sys.exit()
    if not os.path.exists("ISO"):
        os.mkdir("ISO")

    mode = input("Select mode (h for help):")


    if mode == "s":
        results = search(games,input("Search term:").lower())
        if results == []:
            print("No Results found")
        else:
            for result in results:
                print(result)
    elif mode == "d":
        clevel = 0
        tid = input("Title ID to download:").upper()
        filetype = input("Output file type ([i]so, [c]so, [p]kg):").lower()
        if filetype == 'c':
            clevel = input("CSO compression level (1-9):")
        print("Starting download (please wait)")
        dl = process_dl(games, filetype, clevel, tid, p2z)
        if dl == None:
            print("Incorrect title ID or link is not in database")
        print("download finished")
        
    elif mode == "h":
        print("Interactive Modes: [s]earch, [d]ownload), [h]elp, [q]uit)")
        print("The program can also be scripted. Command line options should use the format \"./main.py titleID filetype [compressionLevel]\"" )
        print("Compression level is ONLY if type is cso.")

    elif mode == "q":
        sys.exit()

    else:
        print("Not a valid mode! (h for help)")
