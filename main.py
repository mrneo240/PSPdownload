#!/usr/bin/python
# -*- coding: utf8 -*-

import dataset, sys, os, glob, shutil
import subprocess as sp
from functions import *

db = dataset.connect("sqlite:///games.db")
games = db['games']
p2z = glob.glob("pkg2zip*")[0]

print("PSP game download client")

while True:
    if not os.path.exists("games.db"):
        print("database doesn't exist, do you wish to initialise it?")
        yn = input()
        if yn == "y":
            init_db()
            print("Init finished")
        else:
            sys.exit()

    mode = input("Select mode (h for help):")


    if mode == "s":
        search = input("Search term:").lower()
        for g in games:
            if search in g['Name'].lower():
                print("{}, {}, {}".format(g['Title ID'],g['Region'],g["Name"]))
    elif mode == "d":
        tid = input("title ID to download: ").upper()
        iso = True if input("Convert to ISO? (y/n):") else False 
        print("Starting download (please wait)")
        gn = None
        for g in games:
            if g['Title ID'] == tid:
                gn = g
        if gn is not None:
            download_game(gn)
            if iso == True:
                print("Converting to ISO")
                sp.run(["./" + p2z,"-x",gn['Name'] + ".pkg"])
                shutil.move("pspemu/ISO", "ISO")
                shutil.rmtree("pspemu")
                os.remove(gn['Name'] + ".pkg")
            print("download finished")
        else:
            print("title key invalid or other database error")
    elif mode == "h":
        print("Modes: s (search), d (download), h (help), q (quit)")

    elif mode == "q":
        sys.exit()

    else:
        print("Not a valid mode! (h for help)")
