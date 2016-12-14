#
#   pbcalc.py - various functions to calculate stuff...
#


def calc_timestamp(task):
    """
        Take text output from the Linux 'atq' command and return an
        ISO (YYYY-MM-DDTHH:MM:SS.mmmmmm) value that we can sort by.
    """

    dd = task[3].zfill(2)
    MMM = task[2]
    tttt = task[4]
    YYYY = task[5]
    months = {v: k for k, v in enumerate(calendar.month_abbr)}
    mm = str(months[MMM]).zfill(2)
    timestamp = str(YYYY) + "-" + str(mm) + "-" + dd + " " + str(tttt)
    return timestamp


def check_date(start_date):
    """Check that the date is valid."""
    import datetime
    import sys

    if start_date == 'now':
        print("[OK] Using 'now' - so cool!")
        return 'now'

    else:
        try:
            start = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        except ValueError:
            print("[Error] Date needs to be in dd/mm/YYYY format")
            sys.exit()

        if not (start.weekday() == 0):
            print("[Error] The starting date must be a Monday")
            sys.exit("[Error] Invalid starting date\n")

        print("[OK] Starting date is a Monday...")
        return start


def split_and_check(mailshot_data):
    """Split the text, returning them as a list. Fatal exit if any problems"""

    import sys
    import datetime
    from urllib.parse import urlparse

    # Check 'mailshotdata', a single string like this:
    #
    #    "28/11/2016 16:15 http://dropbox.secserv.kr/0098098.jpg"
    
    try:
        date = mailshot_data.split()[0]
        time = mailshot_data.split()[1]
        ph_url = mailshot_data.split()[2]
    except:
        print("[ERROR] 'Position' is blank or misformed")
        sys.exit()
    try:
        datetime.datetime.strptime(time, '%H:%M')
    except ValueError:
        print("[ERROR] 'Position' time value not in hh:mm format: ", time)
        sys.exit()
    try:
        datetime.datetime.strptime(date, '%d/%m/%Y')
    except ValueError:
        print("[ERROR] 'Position' date not in dd/mm/YYYY format: ", date)
        sys.exit()
    urlbits = urlparse(ph_url)
    if (urlbits.scheme != "") and (urlbits.netloc != ""):
        pass
    else:
        print("[ERROR] 'Position' URL is not valid: ", ph_url)
        sys.exit()

    print("[OK]   Mailshot data looks fine...")
    return [date, time, ph_url]
