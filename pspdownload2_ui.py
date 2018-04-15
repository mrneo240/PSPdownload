""" pspdownload2_ui.py --

UI generated by GUI Builder Build 146 on 2018-03-19 21:37:39 from:
    F:/VITA/PSPdownload/pspdownload2.ui
THIS IS AN AUTOGENERATED FILE AND SHOULD NOT BE EDITED.
The associated callback file should be modified instead.
"""

import tkinter
import os # needed for relative image paths
from functions import *
from GUI_main import *

# Using new-style classes: create empty base class object
# for compatibility with older python interps
#if sys.version_info < (2, 2):
#    class object:
#        pass

class Pspdownload2(object):
    _images = [] # Holds image refs to prevent GC
    results = []

    def __init__(self, root):
        self.root = root
        self.compressionVar = tkinter.IntVar(root)
        self.entryVar = tkinter.StringVar(root)

        # Create a tkinter variable
        self.formatVar = tkinter.StringVar(root)

        # Dictionary with options
        choices = {'ISO','PKG'}
        self.formatVar.set('ISO') # set the default option

        # Widget Initialization
        self._entry_1 = tkinter.Entry(root,
            textvariable = self.entryVar,
            width = 0,
        )
        self.search_btn = tkinter.Button(root,
            text = "Search",
            width = 10,
        )
        self._listbox_1 = tkinter.Listbox(root,
            width = 80
        )
        self.download_btn = tkinter.Button(root,
            text = "Download",
            width = 10,
        )
        self._scale_2 = tkinter.Scale(root,
            orient = "horizontal",
            state = "disabled",
            to = 9,
            variable = self.compressionVar,
        )

        self._ComboBox_1 = tkinter.OptionMenu(root,
            self.formatVar, 
            *choices,
            command=self._ComboBox_1_command
        )
        self._label_1 = tkinter.Label(root,
            anchor = "w",
            justify = "left",
            text = "Format",
        )
        self._label_2 = tkinter.Label(root,
            text = "Compression",
        )
        self._scrollbar_2 = tkinter.Scrollbar(root,
        )
        self.menu = tkinter.Menu(root,
        )
        
        self.scrollbar = tkinter.Scrollbar(root, orient="vertical")
        

        # widget commands
        self.search_btn.configure(
            command = self.search_btn_command
        )
        self.download_btn.configure(
            command = self.download_btn_command
        )
        self._scale_2.configure(
            command = self._scale_2_command
        )
        self._listbox_1.configure(
            yscrollcommand=self._scrollbar_2.set
        )
        self._scrollbar_2.configure(
            command = self._listbox_1.yview
        )
        self.menuitem1 = tkinter.Menu(self.menu,
            tearoff = 0,
        )
        self.menu.add_cascade(
            label = "File",
            menu = self.menuitem1,
        )
        self.menuitem1.add_command(
            accelerator = "Q",
            label = "Quit",
            command=root.quit
        )


        # Geometry Management
        self._entry_1.grid(
            in_    = root,
            column = 1,
            row    = 1,
            columnspan = 3,
            padx = 4,
            pady = 4,
            rowspan = 1,
            sticky = "ew"
        )
        self.search_btn.grid(
            in_    = root,
            column = 4,
            row    = 1,
            columnspan = 2,
            padx = 4,
            pady = 4,
            rowspan = 1,
            sticky = ""
        )
        self._listbox_1.grid(
            in_    = root,
            column = 1,
            row    = 2,
            columnspan = 4,
            padx = 4,
            pady = 4,
            rowspan = 1,
            sticky = "news"
        )
        self.download_btn.grid(
            in_    = root,
            column = 4,
            row    = 3,
            columnspan = 2,
            padx = 4,
            pady = 4,
            rowspan = 2,
            sticky = ""
        )
        self._scale_2.grid(
            in_    = root,
            column = 2,
            row    = 4,
            columnspan = 1,
            rowspan = 1,
            sticky = "ew"
        )
        
        self._ComboBox_1.grid(
            in_    = root,
            column = 1,
            row    = 4,
            columnspan = 1,
            rowspan = 1,
            sticky = ""
        )
        self._label_1.grid(
            in_    = root,
            column = 1,
            row    = 3,
            columnspan = 1,
            rowspan = 1,
            sticky = ""
        )
        self._label_2.grid(
            in_    = root,
            column = 2,
            row    = 3,
            columnspan = 1,
            rowspan = 1,
            sticky = ""
        )
        self._scrollbar_2.grid(
            in_    = root,
            column = 5,
            row    = 2,
            columnspan = 1,
            rowspan = 1,
            sticky = "nsw"
        )

        # Resize Behavior
        root.grid_rowconfigure(1, weight = 0, minsize = 36, pad = 0)
        root.grid_rowconfigure(2, weight = 1, minsize = 260, pad = 0)
        root.grid_rowconfigure(3, weight = 0, minsize = 21, pad = 0)
        root.grid_rowconfigure(4, weight = 0, minsize = 53, pad = 0)
        root.grid_columnconfigure(1, weight = 0, minsize = 162, pad = 0)
        root.grid_columnconfigure(2, weight = 1, minsize = 177, pad = 0)
        root.grid_columnconfigure(3, weight = 0, minsize = 44, pad = 0)
        root.grid_columnconfigure(4, weight = 0, minsize = 86, pad = 0)
        root.grid_columnconfigure(5, weight = 0, minsize = 56, pad = 0)
        root.configure(menu = self.menu)

        self.db = get_db_obj()
        self.games = get_games_obj()
        for game in games:
            self._listbox_1.insert(tkinter.END, "{}, {}, {}".format(game['Title ID'],game['Region'],game["Name"]))
            self.results.append({'Title ID':game['Title ID'],'Region':game['Region'],'Name':game["Name"]})
