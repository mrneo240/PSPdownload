## PSP Download tool

this is a tool to download PSP games as ISOs. requires `pycurl` and `dataset` from pip.

### Setup

### Required Files
To run this program you need a copy of the following files in the same folder as the program:

* PSP_GAMES.tsv (find it online)
* pkg2zip/pkg2zip.exe ([Available here, check "releases" for a zip](https://github.com/mmozeiko/pkg2zip))

### Usage

this program has a simple interactive command line interface, and has an inbuilt help system. Report any issues via the github issue tracker.

### Scripting
This program can be used entirely from the command line, and in scripts. Command line argument format is this:
```
./main.py titleID filetype [compression level]
```