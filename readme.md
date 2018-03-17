## PSP Download tool

this is a tool to download PSP games. requires `requests` and `dataset` from pip.

### Setup

Get a copy of the psp games database file.

then convert to a format the program can read: (this will be automated soon):
```
sqlite3 games.db
.mode tabs
.import [PSP game file here] games
```
the program is  now ready to use.


### Usage

this program has a simple command line interface, and has in inbuilt help system. Report any issues via the github issue tracker.