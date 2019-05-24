#
#   gophish.py - functions that call the 'gophish' server
#


def check_for_subgroups(base_group):
    """Check that the sub-groups have been setup on the 'gophish' server."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    full_url = URL + "/api/groups"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    groups = resp.json()
    targetgroup = []

    for sub in range(10):
        targetgroup_name = base_group + "-" + str(sub)
        targetgroup.insert(sub, targetgroup_name)
        missing = True

        for group in enumerate(groups):
            if dict(group[1])["name"] == targetgroup[sub]:
                print("[OK] Found: ", targetgroup[sub])
                missing = False

        if missing:
            print("[Error] The email group '", targetgroup[sub], "' not found")
            sys.exit("[Error] All the subgroups must be setup first\n")

    print("[OK] Subgroups have been setup on the server")


def check_group(base_group):
    """Check that the base group exists."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    full_url = URL + "/api/groups"
    print("[OK]: Talking to the API at: ", full_url)

    resp = requests.get(full_url, params=GOPHISH_KEY)

    groups = resp.json()
    found = False

    for group in groups:
        if group["name"] == base_group:
            found = True
            base_group_object = group
            print('[OK] Found base group:  "', base_group, sep='')
            return base_group_object

    if not found:
        exit_msg = "[Error] The base group: '" + base_group + "' not found."
        sys.exit(exit_msg)


def delete_group(grp_id, grp_name):
    """Delete an group, by it's id."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    headers = {'content-type': 'application/json'}
    full_url = URL + "/api/groups/" + str(grp_id)
    resp = requests.delete(full_url, params=GOPHISH_KEY, headers=headers)
    if resp.status_code == 200:
        print("Deleted group:", grp_name, "(", grp_id, ")")
    else:
        print("Houston, we have a problem....")
        print("\nText: ")
        print(resp.text)
        print("\nEncoding: ")
        print(resp.encoding)
        sys.exit()


def create_camp(n_data):
    """Create a new campaign."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    headers = {'content-type': 'application/json'}
    full_url = URL + "/api/campaigns/"
    resp = requests.post(full_url, n_data, params=GOPHISH_KEY, headers=headers)
    if resp.status_code == 201:
        print("[OK] Added, and all went fine")
    else:
        sys.exit("Bugger! campaign creation failed, code: " + str(resp.status_code))
    return resp


def delete_camp(camp_id, name):
    """Delete a campaign, by it's id."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    headers = {'content-type': 'application/json'}
    full_url = URL + "/api/campaigns/" + str(camp_id)
    resp = requests.delete(full_url, params=GOPHISH_KEY, headers=headers)
    if resp.status_code == 200:
        print("Deleted campaign:", name, "(", camp_id, ")")
    else:
        print("Houston, we have a problem....")
        print("\nText: ")
        print(resp.text)
        print("\nEncoding: ")
        print(resp.encoding)
        sys.exit()
    return


def check_templates(phishes):
    """Check that the templates exist."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    full_url = URL + "/api/templates/"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    templates = resp.json()

    for phish in phishes:
        missing = True
        for template in enumerate(templates):
            if dict(template[1])["name"] == phish[0]:
                # print("Found: ", phish[0])
                missing = False
                break
        if missing:
            print("[Error] The email template '", phish[0], "' is not there")
            sys.exit("[Error] All the email templates must be setup first\n")

    print("[OK] The email templates we need are there...")


def check_smtp_profiles(phishes):
    """Check that the smtp profiles exist."""

    from pbsettings import URL, GOPHISH_KEY
    import sys
    import requests
    full_url = URL + "/api/smtp"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    smtp_profiles = resp.json()

    for phish in phishes:
        missing = True
        for smtp in enumerate(smtp_profiles):
            if dict(smtp[1])["name"] == phish[2]:
                missing = False
        if missing:
            print("[Error] SMTP profile '", phish[2], "' is missing")
            sys.exit("[Error] All smtp profiles must be setup first\n")

    print("[OK] All smtp profiles exist...")


def check_scare_page(base_group):
    """Check that a correctly-named "Scare page" for this client exists."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    full_url = URL + "/api/pages"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    pages = resp.json()
    scare_page = "Scare page - " + base_group

    missing = True
    for page in enumerate(pages):
        if dict(page[1])["name"] == scare_page:
            missing = False

    if missing:
        print("[Error] The landing page   '", scare_page, "' is missing")
        sys.exit("[Error] A 'scare' landing page must be setup\n")

    print('[OK] Found "', scare_page, '"', sep="")


def create_sub(grp_name, grp_targets):
    """Create the sub-groups on the server. """

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import json
    import sys

    o_data = {
        "name": grp_name,
        "targets": grp_targets
    }
    n_data = json.dumps(o_data)
    headers = {'content-type': 'application/json'}
    full_url = URL + "/api/groups/"
    resp = requests.post(full_url, n_data, params=GOPHISH_KEY, headers=headers)

    if resp.status_code == 201:
        print("[OK] Successfully added:", grp_name)
    else:
        print("[Error] Problem creating subgroup: ", grp_name)
        print("\nText: ")
        print(resp.text)
        print("\nEncoding: ")
        print(resp.encoding)
        sys.exit("[Error] You may need to run 'pbcleanup'\n")

    return


def select_the_group(base_group):
    """Get the list of groups."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    full_url = URL + "/api/groups"
    try:
        resp = requests.get(full_url, params=GOPHISH_KEY)
        if not (resp.status_code == 200):
            print("[Error] The API lookup of groups gave a",
            resp.status_code, "return code")
            sys.exit("[Error] Something appears to have gone wrong.\n")
    except requests.exceptions.Timeout:
        print("[Error] Connection to server timed out!")
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        print("[Error] Too many redirects")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print("[Error] Big problems... error:", e)
        sys.exit(1)

    groups = resp.json()
    found = False
    for group in groups:
        if group["name"] == base_group:
            found = True
            num_of_targets = len(group["targets"])
            print("[OK] Found base group: ", base_group, "with ",
                  num_of_targets, "members")
    if not found:
        pass
        sys.exit("[Error] Target group: '" + base_group + "' not found.\n")
    return


def local_time(ISO_datestring):
    """Converts UTC ISO datastring to local date string"""

    from datetime import datetime
    from dateutil import tz
    import dateutil.parser

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Pacific/Auckland')
    ISO_date = dateutil.parser.parse(ISO_datestring)
    nz_date = ISO_date.astimezone(to_zone)
    nz_date_str = nz_date.isoformat(sep='T')
    return  nz_date_str


def UTC_time(ISO_datestring):
    """Converts local ISO datastring to UTC date string"""

    from datetime import datetime
    from dateutil import tz
    import dateutil.parser

    from_zone = tz.gettz('Pacific/Auckland')
    to_zone = tz.gettz('UTC')
    ISO_date = dateutil.parser.parse(ISO_datestring)
    UTC_date = ISO_date.astimezone(to_zone)
    UTC_date_str = UTC_date.isoformat(sep='T')
    return UTC_date_str


def get_results():
    """Find matching campaigns, and produce two report files."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import tempfile
    import os
    import sys
    import ast      # abstract syntact trees
    import re       # regexes
    from collections import defaultdict
    from datetime import datetime
    from dateutil import tz
    import dateutil.parser

    target_group = sys.argv[1]

    full_url = URL + "/api/campaigns"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    campaigns = resp.json()

    #   Variables with 'sp_' are related to the spear-phishes,
    #   while the others are for the general AUTO- campaigns...
    camp_list = []
    sp_camp_list = []
    each_click = []
    sp_each_click = []
    sp_num_of_staff = 0
    found = False
    phishes_clicked = defaultdict(int)
    sp_phishes_clicked = defaultdict(int)
    sp_targets = []  # those who were sent a spear-phish

    td = tempfile.gettempdir()
    mail_out1 = os.path.join(td, target_group + '-results-summary.csv')
    mail_out2 = os.path.join(td, target_group + '-full-timeline.csv')
    mail_out3 = os.path.join(td, target_group + '-spear-results-summary.csv')
    mail_out4 = os.path.join(td, target_group + '-spear-full-timeline.csv')

    # PART 0
    #
    """Get the total number of staff (targets) in the base group"""
    full_url = URL + "/api/groups"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    groups = resp.json()
    for group in groups:
        if group["name"] == target_group:
            found = True
            num_of_targets = len(group["targets"])

    # PART I
    """Open the output files, and write headers to them..."""

    f1 = open(mail_out1, 'w')
    print('Campaign, CreatedDate, CreatedTime, CompletedDate,',
            'CompletedTime, From, Subject, Mail, First, Last,',
            'Status, IP, Latitude, Longitude',
            file=f1)

    f2 = open(mail_out2, 'w')
    print('Campaign, Date, Time, Email, Action, IP, User Agent',
            file=f2)

    # define the format of the automated campaigns
    pattern = re.compile("AUTO-"+ target_group + "-" + "([0-9])")

    for camp in campaigns:
        # if "AUTO-" + target_group in camp["name"]:
        if pattern.match(camp["name"]):
            print("[OK] Processing ", camp["name"])
            for event in camp["timeline"]:
                #
                #  'events' are structured like this: 
                #
                #   "time": atimedate, 
                #   "message": "Clicked", 
                #   "email"; "abc@exaple.com",
                #   "details: {
                #       "payload": {
                #           "rid": ["afe4343..5sff"],
                #       "browser": {
                #               "address": "202.202.202.222",
                #               "user-agent": "Mozilla ....Mac OS X...Safari/602.3.12"
                #
                # ...but note that "details" can be a blank string...
                #
                #   timedate from the API is in UTC, which we'll convert
                #   to our local zone...

                details = event["details"]
                if not details == '':
                        details = ast.literal_eval(str(details))
                        datetime = local_time(event["time"])
                        print( camp["name"] +
                              ', ' + datetime[0:10] +
                              ', ' +  datetime[11:16] +
                              ', ' + event["email"] +
                              ' , ' + event["message"] +
                              ' , ' + details["browser"]["address"] +
                              ', ' +  details["browser"]["user-agent"].replace(',', '.') ,
                        file=f2)
                else:
                    datetime = local_time(event["time"])
                    print( camp["name"] +
                          ', ' + datetime[0:10] +
                          ', ' + datetime[11:16] +
                          ', ' + event["email"] +
                          ', ' + event["message"]+
                          ', ,  ',
                        file=f2)

                if event["message"] == "Clicked Link":
                    each_click.append(event["email"])

            for result in camp["results"]:
		# 
		# format of the results...
		#	"results": [ 
		#	{
		#	"id": "4408fd5bc60901c35e7352f0205282d26b27a9fc80bdd6ee4db4a6f87c1954bb",
		#	"email": "bjenius@morningcatch.ph",
		#	"first_name": "Boyd",
		#	"last_name": "Jenius",
		#	"position": "",
		#	"status": "Success",
		#	"ip": "x.x.x.x",
		#	"latitude": 0,
		#	"longitude": 0
		#	}
		#	]
                #   Note the slicing of the ISO 8601 date/time into two fields
                #        and the use of '+'. Also, only quoting the subject line
                #        because it sometimes has commas in it.

                print( camp["name"] +
                      ', ' + local_time(camp["created_date"])[0:10] +
                      ', ' + local_time(camp["created_date"])[11:16] +
                      ', ' + local_time(camp["completed_date"])[0:10] +
                      ', ' +  local_time(camp["completed_date"])[11:16] +
                      ', ' + camp["smtp"]["from_address"] +
                      ', ' + '"' + camp["template"]["subject"] + '"' + 
                      ', ' + result["email"] +
                      ', ' + result["first_name"] +
                      ', ' + result["last_name"] +
                      ', ' + result["status"] +
                      ', ' + result["ip"] +
                      ', ' + str(result["latitude"]) +
                      ', ' + str(result["longitude"]) ,
                      file=f1)

                #   and we keep a tally of the sucessful 'phishes'...
                if result["status"] == "Clicked Link":
                    phishes_clicked[camp["template"]["subject"]] += 1
                camp_list.append(camp)

    f1.close()
    f2.close()

    #   Convert files from CSV to nice XLSX format
    outdir = "/tmp"
    excelout_timeline(f2, outdir)
    excelout_summary(f1, outdir)


    if not found:
        sys.exit("[Error] No general campaigns matching: '" +
                 target_group + "' were found.\n")

    # Part II
    #
    """ We *used* to go looking for all the spear-phishing data"""
    # print("[OK]: We don't use spear-phishing anymore.")


    # Part III - now total everthing up...

    #   Using 'set' removes duplicates
    those_who_clicked = set(each_click)
    num_who_clicked = len(those_who_clicked)

    #   Tally up the scores of which 'phishes' were more successfull...
    phish_score = ""
    for k, v in phishes_clicked.items():
        phish_score += "\t" + str(k) + " - " + str(v) + "\n"

    # Return the results in a dict...
    #
    # Note that there's some trickiness below to get 
    # the XLSX versions; the orginal looked like:
    # 
    #    "f1": mail_out1,
    #    "f2": mail_out2,
    #    "f3": mail_out3,
    #    "f4": mail_out4
    r = {
        "num_of_staff": num_of_targets, "num_who_clicked": num_who_clicked,
        "those_who_clicked": those_who_clicked, "phish_score": phish_score,
        "sp_num_of_staff": 0,
        "sp_targets": sp_targets,
        "sp_num_who_clicked": 0,
        "sp_those_who_clicked": 0,
        "sp_phish_score": 0,
        "f1": outdir + '/' + os.path.basename(mail_out1) + '.xlsx',
        "f2": outdir + '/' + os.path.basename(mail_out2) + '.xlsx',
        "f3": outdir + '/' + os.path.basename(mail_out3) + '.xlsx',
        "f4": outdir + '/' + os.path.basename(mail_out4) + '.xlsx',
    }

    return r


def excelout_summary( csv_file, outdir):
    """
    Produce a nicely readable XLSX from the CSV of a summary

    """
    import os
    import pandas as pd
    import xlsxwriter
    csv_file = csv_file.name

    with open(csv_file, 'r') as c:
        df = pd.read_csv(c, quotechar='"', skipinitialspace=True)

    #   Write to .XLSX
    basename=os.path.basename(csv_file)
    writer = pd.ExcelWriter(outdir + '/' + basename + '.xlsx',
                            engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Sheet1', index=False)  # send df to writer
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    #   Define some formatting
    clicked = workbook.add_format({'bold': True, 'bg_color': 'orange' })
    opened = workbook.add_format({'bold': True, 'bg_color': 'yellow'})
    created = workbook.add_format({'bold': True})
    wide = workbook.add_format({'valign': 'Top', 'text_wrap': True})
    superwide = workbook.add_format({'valign': 'Top', 'text_wrap': True})
    centered = workbook.add_format({'align': 'center'})
    title = workbook.add_format({'bold': True, 'color': 'white', 'bg_color': 'gray'})
    left = workbook.add_format({'align': 'left'})

    #   Set the row height to double the default
    worksheet.set_default_row(30)

    #   We can then pass these formats as an optional third parameter to the 
    #   worksheet.write() method, or optional fourth param to set_column:
    worksheet.set_column(0, 0, 24, centered)
    worksheet.set_column(1, 1, 13, centered)
    worksheet.set_column(2, 2, 11, centered)
    worksheet.set_column(3, 3, 30, centered )
    worksheet.set_column(4, 4, 14, centered)
    worksheet.set_column(5, 5, 24, wide)
    worksheet.set_column(6, 6, 40, wide)
    worksheet.set_column(7, 7, 30, left)
    worksheet.set_column(8, 8, 12, left)
    worksheet.set_column(9, 9, 12, left)
    worksheet.set_column(10, 10, 14, centered)
    worksheet.set_column(11, 11, 15, centered)
    worksheet.set_column(12, 12, 12, wide)
    worksheet.set_column(13, 13, 12, wide)
    # Conditional formatting is nice...
    worksheet.conditional_format('K1:K9999', {'type':     'text',
                                            'criteria': 'containing',
                                            'value':    'OS X',
                                            'format':   clicked})

    worksheet.conditional_format('K1:K9999', {'type':     'text',
                                            'criteria': 'containing',
                                            'value':    'Email Opened',
                                            'format':   opened})

    worksheet.conditional_format('K1:K9999', {'type':     'text',
                                            'criteria': 'containing',
                                            'value':    'Clicked Link',
                                            'format':   clicked})

    worksheet.conditional_format('K2:K9999', {'type':     'text',
                                            'criteria': 'containing',
                                            'value':  'Campaign Created',
                                            'format':   created})
    writer.save()
    writer.close()
    return


def excelout_timeline( csv_file, outdir):
    """
    Produce a nicely readable XLSX from the CSV of a timeline

    """
    import os
    import pandas as pd
    import xlsxwriter
    csv_file = csv_file.name

    with open(csv_file, 'r') as c:
        df = pd.read_csv(c, quotechar="'", skipinitialspace=True)

    #   Write to .XLSX
    basename=os.path.basename(csv_file)
    writer = pd.ExcelWriter(outdir + '/' + basename + '.xlsx',
                            engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Sheet1', index=False)  # send df to writer
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    #   Define some formatting
    clicked = workbook.add_format({'bold': True, 'bg_color': 'orange' })
    opened = workbook.add_format({'bold': True, 'bg_color': 'yellow'})
    created = workbook.add_format({'bold': True})
    wide = workbook.add_format({'valign': 'Top', 'text_wrap': True})
    superwide = workbook.add_format({'valign': 'Top', 'text_wrap': True})
    centered = workbook.add_format({'align': 'center'})
    title = workbook.add_format({'bold': True, 'color': 'white', 'bg_color': 'gray'})

    #   Set the row height to double the default
    worksheet.set_default_row(30)

    #   We can then pass these formats as an optional third parameter to the 
    #   worksheet.write() method, or optional fourth param to set_column:
    worksheet.set_column(0, 0, 32, centered)
    worksheet.set_column(1, 1, 16, centered)
    worksheet.set_column(2, 2, 8, centered)
    worksheet.set_column(3, 3, 48, centered )
    worksheet.set_column(4, 4, 20, centered)
    worksheet.set_column(5, 5, 20, wide)
    worksheet.set_column(6, 6, 60, wide)

    # Conditional formatting is nice...
    worksheet.conditional_format('E2:G9999', {'type':     'text',
                                            'criteria': 'containing',
                                            'value':    'OS X',
                                            'format':   clicked})

    worksheet.conditional_format('E2:G9999', {'type':     'text',
                                            'criteria': 'containing',
                                            'value':    'Email Opened',
                                            'format':   opened})

    worksheet.conditional_format('E2:G9999', {'type':     'text',
                                            'criteria': 'containing',
                                            'value':    'Clicked Link',
                                            'format':   clicked})

    worksheet.conditional_format('E2:G9999', {'type':     'text',
                                            'criteria': 'containing',
                                            'value':  'Campaign Created',
                                            'format':   created})
    writer.save()
    writer.close()
    return


def mailshots(base_group, start_date, phish_set, sched_name):
    """
    Schedule the 20 phishing mailshot tasks, via the 'gophish' API

    """

    import os
    import time
    import datetime
    import pytz
    import json
    from pbconfig import get_mailshot_time, get_phishes
    from pbgophish import create_camp

    mailshot_time = get_mailshot_time(sched_name)
    phishes = get_phishes(phish_set)

    for shot in range(0, 20):
        if start_date == 'now':
            delay = shot + 1
            mailshot_date = datetime.datetime.now()
            shot_td = mailshot_date + datetime.timedelta(minutes=delay)
            shot_time = shot_td.strftime('%H') + ":" + shot_td.strftime('%M')

        else:
            try:
                mailshot_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
                mailshot_date += datetime.timedelta(days=mailshot_time[shot][0] - 1)
            except ValueError:
                print("[Error] Date is not in dd/mm/YYYY format")
            #    
            shot_time = mailshot_time[shot][1]

        # Now create the campaign via the API, with scheduling controlled by
        # the 'launch_date" attribute...

        # Making sure we handle time correctly...
        UTC_offset = pytz.timezone('Pacific/Auckland').localize(mailshot_date).strftime('%z')
        nz_launch_date = mailshot_date.strftime('%Y-%m-%d') + 'T' + shot_time + UTC_offset
        UTC_launch_date = UTC_time(nz_launch_date)

        o_data = {"name": 'AUTO-' + base_group + '-' + str(shot),
              "template": {"name": phishes[shot % 10][0]},
              "page": {"name": 'Scare page - ' + base_group},
              "url": phishes[shot % 10][1],
              "smtp": {"name": phishes[shot % 10][2]},
              "launch_date": UTC_launch_date,
              "send_by_date":"0001-01-01T00:00:00Z",
              "groups": [{"name": base_group + '-' + str(mailshot_time[shot][2])}]
              }
        n_data = json.dumps(o_data)

        #   Now create the new campaign
        resp = create_camp(n_data)
        time.sleep(2)

    print("[OK] All mailshot jobs are scheduled")


