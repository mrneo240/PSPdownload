import dataset, os, errno

db = dataset.connect("sqlite:///games.db")
games = db['games']
p2z = "pkg2zip.exe" if os.name == 'nt' else "pkg2zip"
cur_window = None

def get_games_obj():
    return games

def get_db_obj():
    return db

def get_p2z_obj():
    return p2z

def init_program():
    #also add stuff for the db here
    try:
        os.makedirs("./ISO")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
def set_tk_window(obj):
    global cur_window
    cur_window = obj

def get_tk_window():
    global cur_window
    return cur_window