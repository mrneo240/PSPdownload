# -*- coding: utf8 -*-

import requests, csv, sqlite3

def download_game(g):
    local_filename = g['Name'] + ".pkg"
    # NOTE the stream=True parameter
    r = requests.get(g['PKG direct link'], stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

def init_db():
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE games (\"Title ID\", \"Region\", \"Name\", \"PKG direct link\");")
    
    with open('PSP_GAMES.tsv','r') as fin:
        dr = csv.DictReader(fin, delimiter="\t")
        to_db = [(i['Title ID'], i['Region'], i['Name'],i['PKG direct link']) for i in dr]
    
    cur.executemany("INSERT INTO games (\"Title ID\", \"Region\", \"Name\", \"PKG direct link\") VALUES (?, ?, ?, ?);", to_db)
    con.commit()
    con.close()
    
    