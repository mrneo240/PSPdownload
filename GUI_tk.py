#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
from tkinter.ttk import Progressbar
from functions import *
from GUI_main import *

class Window:
    
    search_term = None
    results = []

    def __init__(self, master):
        self.master = master
        self.search_term = tk.StringVar(self.master)

        init_program()
        self.frame = tk.Frame(self.master)
        self.frame.winfo_toplevel().title("PSPDownload")
        self.search_button = tk.Button(self.frame, text = 'Search', width = 15, command = self.search_func)
        self.search_button.pack()
        self.search_entry = tk.Entry(self.frame, width=80, textvariable=self.search_term)
        self.search_entry.pack()
        self.listbox = tk.Listbox(self.frame,width=80)
        self.listbox.pack()
        self.download_button = tk.Button(self.frame, text = 'Download as CSO(9)', width = 15, command = self.download_func)
        self.download_button.pack()

        self.frame.pack()
        self.setup_window()

    def setup_window(self):
        self.db = get_db_obj()
        self.games = get_games_obj()
        for game in games:
            self.listbox.insert(tk.END, "{}, {}, {}".format(game['Title ID'],game['Region'],game["Name"]))
            self.results.append({'title_id':game['Title ID'],'region':game['Region'],'name':game["Name"]})
    
    def search_func(self):
        self.listbox.delete(0,tk.END)
        self.results = []
        self.results = search_list(get_games_obj(),self.search_term.get().lower())
        if self.results == []:
            self.listbox.insert("No Results found")
        else:
           for game in self.results:
                self.listbox.insert(tk.END, "{}, {}, {}".format(game["Title ID"],game["Region"],game["Name"])) 

    def download_func(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = ProgressWindow(self.newWindow)

        item = self.listbox.curselection()
        clevel = 9
        tid = self.results[item[0]]["Title ID"].upper()
        filetype = 'c'
        self.app.start(clevel,tid,filetype)

class ProgressWindow:
    def __init__(self,master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.winfo_toplevel().title("Downloading")
        self.info = tk.Label(self.frame,text="0/0 MB",width=30)
        self.info.pack()
        self.progressbar = Progressbar(self.frame, orient="horizontal", length=250, mode="determinate")
        self.progressbar.pack()
        self.frame.pack()
        set_tk_window(self)

    def close_window(self):
        self.destroy()

    def start(self,clevel,tid,filetype):
        self.progressbar["value"] = 0
        self.progressbar["maximum"] = 100 

        dl = process_dl(get_games_obj(), filetype, clevel, tid, get_p2z_obj())
        if dl == None:
            tk.messagebox.showinfo("Error", "Incorrect title ID or link is not in database")
        tk.messagebox.showinfo("Success!", "Download finished")    

    def update_bar(self,downloaded, total):
        self.progressbar["value"] = downloaded/1024/1024
        self.progressbar["maximum"] = total/1024/1024
        self.info['text'] = '%d/%d MB' % (downloaded/1024/1024,total/1024/1024)  
        if downloaded == total:
            self.info['text'] = "Finished! Now Converting..."
        self.master.update_idletasks()
        self.master.update()


Window
def main(): 
    root = tk.Tk()
    app = Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()