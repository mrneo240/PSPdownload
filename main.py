import dataset, sys, os
from functions import *

db = dataset.connect("sqlite:///games.db")
games = db['games']

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
        print("Starting download (please wait)")
        for g in games:
            if g['Title ID'] == tid:
                download_game(g)
        print("download finished")
    elif mode == "h":
        print("Modes: s (search), d (download), h (help), q (quit)")

    elif mode == "q":
        sys.exit()

    else:
        print("Not a valid mode! (h for help)")
