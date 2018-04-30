## PSP Download tool

this is a tool to download PSP games as ISOs.

NOTICE: When upgrading from older versions to a newer commit, you may need to recreate the database file.  Simply deleting `games.db` will work.

### Setup

* Install [Python 3](https://python.org/downloads)
* In a terminal/powershell run `pip install -r requirements.txt`
* download the required files (specified below)
* You can now start the program with `pspdownload2.py`

### Required Files
To run this program you need a copy of the following files in the same folder as the program:

* PSP_GAMES.tsv (find it online)
* pkg2zip/pkg2zip.exe ([Available here, check "releases" for a zip](https://github.com/mmozeiko/pkg2zip))

### Usage

This program has two interfaces.

* `main.py` is a simple interactive command line interface, and has an inbuilt help system. This is the original interface.
* `pspdownload2.py` is a tkinter-based GUI. It's not quite Complete yet, but worth using if you like to have a graphical interface.

### Scripting
This program can be used entirely from the command line, and in scripts. Command line argument format is this:
```
./main.py titleID filetype [compression level]
```

### Screenshots

![Screenshot 1](https://luke.feen.us/bpd8f4.png)
![Screenshot 2](https://luke.feen.us/fgnqcf.png)