# -*- coding: utf-8 -*-

import pycurl, csv, sqlite3, os, shutil, glob, sys, time, re
import subprocess as sp
from GUI_main import get_tk_window

START_TIME = None

def sanitize_name(name):
	clean_name = re.sub(r'\W+', '', name)
	return clean_name
	

def download_game(g):
    local_filename = sanitize_name(g['Name']) + ".pkg"
    local_file = open(local_filename,"wb")
    c = pycurl.Curl()
    c.setopt(pycurl.URL, g['PKG direct link'])
    c.setopt(pycurl.WRITEDATA, local_file)
    c.setopt(pycurl.NOPROGRESS, 0)
    c.setopt(c.PROGRESSFUNCTION, progress)
    c.perform()
    c.close()
    return local_filename

def download_game_gui(g):
    local_filename = sanitize_name(g['Name']) + ".pkg"
    local_file = open(local_filename,"wb")
    c = pycurl.Curl()
    c.setopt(pycurl.URL, g['PKG direct link'])
    c.setopt(pycurl.WRITEDATA, local_file)
    c.setopt(pycurl.NOPROGRESS, 0)
    c.setopt(c.PROGRESSFUNCTION, progress_gui)
    c.perform()
    c.close()
    return local_filename

def init_db():
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE games (\"Title ID\", \"Region\", \"Name\", \"PKG direct link\", \"File Size\");")
    
    with open('PSP_GAMES.tsv','r', encoding="utf8") as fin:
        dr = csv.DictReader(fin, delimiter="\t")
        to_db = [(i['Title ID'], i['Region'], i['Name'],i['PKG direct link'], i['File Size']) for i in dr if i['PKG direct link'] != 'MISSING']
    
    cur.executemany("INSERT INTO games (\"Title ID\", \"Region\", \"Name\", \"PKG direct link\", \"File Size\") VALUES (?, ?, ?, ?, ?);", to_db)
    con.commit()
    con.close()

def isocso(name,compression, p2z):
    sp.run(["./" + p2z,"-x",name, "-c" + str(compression)])
    dst_file = 'ISO/{}'.format(os.path.basename(glob.glob("pspemu/ISO/*")[0]))
    if os.path.exists(dst_file):
            try:
                os.remove(dst_file)
            except EnvironmentError as exc:
                pass
    shutil.move(glob.glob("pspemu/ISO/*")[0],"ISO")
    shutil.rmtree("pspemu")
    os.remove(name)

def psxpbp(name,compression, p2z):
    sp.run(["./" + p2z,"-x",name, "-c" + str(compression)])
    #shutil.move(glob.glob("pspemu/PSP/*")[0],"PSP")
    #shutil.rmtree("pspemu")
    os.remove(name)

def search(games, term):
    results = []
    for g in games:
        if term in g['Name'].lower():
            results.append("{}, {}, {}, {}".format(g['Title ID'],g['Region'],g["Name"],g["File Size"]))
    return results

def search_list(games, term):
    results = []
    for g in games:
        if term in g['Name'].lower():
            results.append({'Title ID':g['Title ID'],'Region':g['Region'],'Name':g["Name"],'File Size':g["File Size"]})
    return results

def process_dl(games, filetype, clevel, tid, p2z):
    gn = None
    for g in games:
        if g['Title ID'] == tid:
            gn = g
    if gn is not None:
        download_game_gui(gn)
        if filetype == "pbp" or filetype == "p":
            psxpbp(sanitize_name(gn['Name']) + ".pkg",0,p2z)
        if filetype == 'i' or filetype == "iso":
            isocso(sanitize_name(gn['Name']) + ".pkg",0,p2z)
        elif filetype == 'c' or filetype == "cso":
            isocso(sanitize_name(gn['Name']) + ".pkg",clevel,p2z)
        return gn
    else:
        return None
    return gn

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

def progress_gui(download_t, download_d, upload_t, upload_d):
    if int(download_t) == 0:
        return
    global START_TIME
    if START_TIME is None:
        START_TIME = time.time()
    get_tk_window().update_bar(download_d,download_t)
