# -*- coding: utf-8 -*-

import pycurl, csv, sqlite3, os, shutil, glob, sys, time
import subprocess as sp

START_TIME = None

def download_game(g):
    local_filename = g['Name'] + ".pkg"
    local_file = open(local_filename,"wb")
    if g['PKG direct link'] != "MISSING":
        c = pycurl.Curl()
        c.setopt(pycurl.URL, g['PKG direct link'])
        c.setopt(pycurl.WRITEDATA, local_file)
        c.setopt(pycurl.NOPROGRESS, 0)
        c.setopt(c.PROGRESSFUNCTION, progress)
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
    results = []
    for g in games:
        if term in g['Name'].lower():
            results.append("{}, {}, {}".format(g['Title ID'],g['Region'],g["Name"]))
    return results

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
        return gn
    else:
        return None

# Print Download progress as bar
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def progress(download_t, download_d, upload_t, upload_d):
    if int(download_t) == 0:
        return
    global START_TIME
    if START_TIME is None:
        START_TIME = time.time()
    print_progress(download_d,download_t,'%d/%d MB' % (download_d/1024/1024,download_t/1024/1024),'',1,40)
