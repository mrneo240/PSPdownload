# -*- coding: utf-8 -*-

import pycurl, csv, sqlite3, os, shutil, glob
import subprocess as sp

def download_game(g):
    local_filename = g['Name'] + ".pkg"
    local_file = open(local_filename,"wb")
    if g['PKG direct link'] != "MISSING":
        c = pycurl.Curl()
        c.setopt(pycurl.URL, g['PKG direct link'])
        c.setopt(pycurl.WRITEDATA, local_file)
        c.setopt(pycurl.NOPROGRESS, 0)
        c.perform()
        c.close()
    else:
        print("There is no link associated with this game.")
    return local_filename

def init_db():
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE games (\"Title ID\", \"Region\", \"Name\", \"PKG direct link\");")
    
    with open('PSP_GAMES.tsv','r', encoding="utf8") as fin:
        dr = csv.DictReader(fin, delimiter="\t")
        to_db = [(i['Title ID'], i['Region'], i['Name'],i['PKG direct link']) for i in dr]
    
    cur.executemany("INSERT INTO games (\"Title ID\", \"Region\", \"Name\", \"PKG direct link\") VALUES (?, ?, ?, ?);", to_db)
    con.commit()
    con.close()

def isocso(name,compression, p2z):
    sp.run(["./" + p2z,"-x",name, "-c" + str(compression)])
    shutil.move(glob.glob("pspemu/ISO/*")[0],"ISO")
    shutil.rmtree("pspemu")
    os.remove(name)

def search(games, term):
    for g in games:
        if term in g['Name'].lower():
            print("{}, {}, {}".format(g['Title ID'],g['Region'],g["Name"]))

def process_dl(games, filetype, clevel, tid, p2z):
    gn = None
    for g in games:
        if g['Title ID'] == tid:
            gn = g
    if gn is not None:
        download_game(gn)
        if filetype == 'i' or filetype == "iso":
            isocso(gn['Name'] + ".pkg",0,p2z)
        elif filetype == 'c' or filetype == "cso":
            isocso(gn['Name'] + ".pkg",clevel,p2z)
    else:
        print("title key invalid or other database error")
