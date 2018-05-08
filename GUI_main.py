import dataset, os, errno, sys
import functions

db = None# = dataset.connect("sqlite:///games.db")
games = None# = db['games']
p2z = "pkg2zip.exe" if os.name == 'nt' else "pkg2zip"
cur_window = None

def get_games_obj():
    global games
    return games

def get_db_obj():
    global db
    return db

def get_p2z_obj():
    return p2z

def init_program():
    print("INIT_PROGRAM")
    tsv_name = 'PSP_GAMES.tsv'
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            tsv_name = sys.argv[1]
	
    if not os.path.exists(os.path.splitext(tsv_name)[0]+'.db'):
        functions.init_db_ex(tsv_name)
    try:
        os.makedirs("./ISO")
        os.makedirs("./PSP")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
	
    global db
    global games
    db = dataset.connect("sqlite:///"+os.path.splitext(tsv_name)[0]+'.db')
    games = db['games']
	
            
def set_tk_window(obj):
    global cur_window
    cur_window = obj

def get_tk_window():
    global cur_window
    return cur_window