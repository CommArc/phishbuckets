# Roadmap for "phishbuckets" 

_Keep the core concept, but make it easier to use over
 time by removing the need for Linux expertise, and by
 providing a web interface_


## v0.1 (current production)
It works, but is not pretty

## v0.3 (current dev as at November 2016)
After moving all code to modules, and extensive renaming.

## v0.4

1 - Remove the use of Linux "at" - replacing with 'gophish's own scheduling.

2 - Without using operating system scheduling, 'collect results' will now need to
    be run manually.

3 - Replace the embarrassing "hack" used for spear phishing, with ????

4 - Rethink the 'schedule' idea, probably replalcing with a default of simply
    "random time", favoring 8:30, 1:15 and 4:30 (say)

5 - Removing any hard limitation to a two week run - so that we can specify
    anything from now/immediate, to today, one week, 2 or 3 etc.

6 - Mark campaigns as finished once all have 'fired' - and the collect-results 
    has been run.

7 - Make sure that any/every email alert functionality works on Windows

## v0.5 - finally a GUI!

1- Build a Flask interface, as the primary way that the system is used.


