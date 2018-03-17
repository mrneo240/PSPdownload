import dataset
from functions import *

db = dataset.connect("sqlite:///games.db")
games = db['games']

print("PSP game download client")

while True:
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
        print("Modes: s (search), d (download), h (help)")

    else:
        print("Not a valid mode! (h for help)")
