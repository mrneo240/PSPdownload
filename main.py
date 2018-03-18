#!/usr/bin/python
# -*- coding: utf-8 -*-

import dataset, sys, os, glob, shutil
import subprocess as sp
from functions import *

db = dataset.connect("sqlite:///games.db")
games = db['games']
p2z = "pkg2zip.exe" if os.name == 'nt' else "pkg2zip"

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
        tid = input("Title ID to download:").upper()
        filetype = input("Output file type ([i]so, [c]so, [p]kg):").lower()
        if filetype == 'c':
            clevel = input("CSO compression level (1-9):")
        print("Starting download (please wait)")
        gn = None
        for g in games:
            if g['Title ID'] == tid:
                gn = g
        if gn is not None:
            download_game(gn)
            if filetype == 'i':
                isocso(gn['Name'] + ".pkg",0,p2z)
            elif filetype == 'c':
                isocso(gn['Name'] + ".pkg",clevel,p2z)
            print("download finished")
        else:
            print("title key invalid or other database error")
    elif mode == "h":
        print("Modes: s (search), d (download), h (help), q (quit)")

    elif mode == "q":
        sys.exit()

    else:
        print("Not a valid mode! (h for help)")
