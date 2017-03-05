# Phishbuckets

_Forcc use with 'gophish' from Jordan Wright_

(Note: This is a work in progress - and 'gophish' itself is only v0.2.0)

These scripts are based on a series of assumptions which are true for our own
work. If these don't match the way you do your phishing, then these scripts 
may not be for you...

1 - The core concept is that of a named "base group" of staff to be tested.
    Generally either all staff at a client, or one department of a business.
    Probably should be no more than about 500 staff, but there is no problem
    having phishing campaigns going for multiple "base groups" at one time.

2 - Rather than send a base group all the same 'phish', and all at once - the 
    scripts instead send different 'phishes', spread over two weeks, with each 
    staff member getting at least 2 of the 10 different 'phishes'.

3 - There will be 'sets' of 10 phishes, so that we can send a new "base group" 
    of users the same set as was sent to other users (which can allow useful 
    comparisons), or the one "base group" different sets in the future - if for 
    example, regular 'fire drill' testing is done.

4 - The schedules of when 'phishes' are sent out are also able to be selected. 
    One named schedule might be "NormalFortnight" where phishes are sent out 
    evenly over a two week period, another might be "BigBang", where 50% of 
    phishes are sent on the first day - then a trickle over the rest of a week.

5 - Although the 'gophish' server is doing the bulk of the work, apart from 
    initial loading of the users, setting up of templates etc. there is no 
    need to login to its interface. As 'phishes' are sent out a 'phish master'
    email address is advised - and some time after the last phish of a schedule,
    the full results are also emailed to that address.
    
6 - A Linux server should be used to run these scripts, because: (a) they 
    rely on the Linux 'at' command, and (b) a laptop or workstation is probably
    not suitable unless it's "always on" as the 'at' jobs are queued up there.
    
7 - The 'gophish' server however, could be running on a Windows or OSX machine.

8 - Despite the above, most development and testing has been done with one Linux
    server that runs both 'gophish' and these scripts, so not everthing may go
    according to plan in other environments. Any problems, raise a bug issue.

At the time this work was begun, 'gophish' had no ability to schedule campaigns.
Now that it does, it makes sense to transition these scripts to use that feature
but that will take some extra work...

## Installation

* Place scripts on the path, and set executable with 'chmod +x'
* Good locations would be _/usr/bin/local_ or _~/bin_

## Configuration

* The scripts expect configuration files in _~/.phishbuckets_ - as follows:
*  - _config_ - Main configuration options
*  - _mailshot_time.json_ - Sets of one of more mailshot times
*  - _phishes.json_ - Sets of 'phishes', email templates, URLs and senders

An example of _config_ is:

    [Global]
    GOPHISH_SERVER_URL="http://phish.example.com:3333"
    GOPHISH_KEY="12345ce123238a79d303146d283f0601a3818f1fd12345e0252bd08069a5c3cd"

    # where various informational emails will be sent:
    PHISH_MASTER="phishy@example.com"

    # ...and who they'll appear to be from:
    FROM="phishserver@phish.example.com"

The format of _phishes.json_ and _mailshot_time.json_ is documented in _pbconfig.py_
with examples.

## Required setup in 'gophish'

These automation scripts only make sense if you've already configured gophish
and can sucessfully "manually" send off campaigns, and collect results. At that
point:
* Setup ten email templates, sending smtp profiles and decided upon the URLs you
will use
* Document these ten phishes in your _phishes.json_ file
* Decide on a schedule, and document in _mailshot_time.json_ 
* Add your server URL, API key and your 'phishmaster' email to the _config_ file
At this point you should be able to test the system by typing something like:

    pbcreateplan MYGROUP 15/5/2017 first first

The script is pretty good at giving useful feedback on what is wrong.

## Cleanup

The key point of the 'phishbuckets' system is to take a large group of users, and
make 20 campaigns to target them. Once finished it's helpful to be able to clean up
the gophish "Dashboard" view by deleting all these campaigns - and the ten
"sub-groups" of users. The script _pbcleanup_ allows this.

## Spear-phishing

The _pbcreate_spear_ script is included; but should probably be avoided as it uses
a rather hackery approach.

