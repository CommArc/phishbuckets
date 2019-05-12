#
#   pbcalc.py - various functions to calculate stuff...
#

def calc_timestamp(task):
    """
        Take text output from the Linux 'atq' command and return an
        ISO (YYYY-MM-DDTHH:MM:SS.mmmmmm) value that we can sort by.
    """
    import calendar

    dd = task[3].zfill(2)
    mmm = task[2]
    tttt = task[4]
    yyyy = task[5]
    months = {v: k for k, v in enumerate(calendar.month_abbr)}
    mm = str(months[mmm]).zfill(2)
    timestamp = str(yyyy) + "-" + str(mm) + "-" + dd + " " + str(tttt)
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



