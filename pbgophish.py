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
    resp = requests.get(full_url, params=GOPHISH_KEY)
    groups = resp.json()
    found = False

    for group in groups:
        if group["name"] == base_group:
            found = True
            base_group_object = group
            print('[OK] Found base group:  "', base_group, '"', sep='')
            return base_group_object

    if not found:
        exit_msg = "[Error] The base group: '" + base_group + "' not found."
        sys.exit(exit_msg)


def get_at_jobs():
    """Gets a list of the queued up 'at' jobs, by number."""

    import subprocess

    cmd = "atq | cut -f1 "
    output = subprocess.check_output(cmd, shell=True)
    #   Comes back as bytes, hence the decode bit...
    alljobs = output.decode("utf-8")
    list_of_at_jobs = alljobs.split("\n")
    del list_of_at_jobs[-1]
    return list_of_at_jobs


def group_name(job):
    import subprocess
    cmd = 'at -c ' + job + ' | tail -2| head -1| cut -f 2 -d" "'
    base_name = str(subprocess.check_output(cmd, shell=True))
    return base_name


def kill_job(job):
    import subprocess
    cmd = 'atrm ' + job
    subprocess.check_output(cmd, shell=True)
    return


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
        sys.exit("Bugger! campaign creation failed")
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

def dump_camp(name):
    """Dump a campaign, by its name."""
    #TODO fix this up so it does something useful...
    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys
    headers = {'content-type': 'application/json'}
    full_url = URL + "/api/campaigns"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    campaigns = resp.json()

    dumped = 0
    for camp in campaigns:
        print(type(name), type(camp["name"]))
        if name == camp["name"]:
            print(camp["name"], camp["launch_date"])
            dumped += 1
    if dumped > 0:
        print("[OK] Dumped ", dumped, " campaigns")
    else:
        print("[Error] No campaigns found to dump")
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


def check_spear_templates(base_group, spears):
    """Check that the spear-phishing templates exist."""

    import sys
    import requests
    from pbsettings import GOPHISH_KEY, URL

    full_url = URL + "/api/templates"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    templates = resp.json()
    sp_name = ""
    for spear in range(spears):
        missing = True
        for template in enumerate(templates):
            sp_name = base_group + "-spear-" + str(spear)
            if dict(template[1])["name"] == sp_name:
                missing = False
        if missing:
            err_msg = "[Error]: The email template '" + sp_name + \
                      "' does not exist on the server"
            print(err_msg)
            sys.exit("{Error] All the email templates must be setup first\n")

    print("[OK] Found all required templates")


def get_num_spear_groups(base_group):
    """Counts the number of 'spears': BASE-spear-1, BASE-spear-2 etc."""

    from pbsettings import GOPHISH_KEY, URL
    import requests

    full_url = URL + "/api/groups"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    groups = resp.json()

    num_of_spears = 0
    for spear in range(10):
        missing = True
        sp_name = base_group + "-spear-" + str(spear)
        for group in groups:
            if group["name"] == sp_name:
                num_of_spears += 1
                print('[OK] Found "', sp_name, '"', sep='')
                missing = False
                break

        if missing:
            break

    print("[OK] Found ", num_of_spears, " spear groups")
    return num_of_spears


def check_spear_smtp_profiles(base_group, spears):
    """Check that the profiles exist."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    full_url = URL + "/api/smtp"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    profiles = resp.json()

    for spear in range(spears):
        missing = True
        for profile in enumerate(profiles):
            sp_name = base_group + "-spear-" + str(spear)
            if dict(profile[1])["name"] == sp_name:
                missing = False
        if missing:
            err_msg = "[Error] The SMTP profile '" + sp_name + \
                      "' does not exist on the server"
            print(err_msg)
            sys.exit("[Error] All the SMTP sending profiles must be setup\n")

    print("[OK] Found all required SMTP sending profiles")


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

    # noinspection PyShadowingNames,PyShadowingNames


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

    # noinspection PyShadowingNames


def get_mailshot_data(spear_name):
    """Get string of data (time, date, URL) from 'Position' of first user"""

    from pbsettings import GOPHISH_KEY, URL
    import sys
    import requests

    full_url = URL + "/api/groups"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    groups = resp.json()
    for group in groups:
        if group["name"] == spear_name:
            data = group["targets"][0]["position"]
            return data

    exit_msg = "[Error]: Could not find group " + spear_name
    sys.exit(exit_msg)

    # noinspection PyShadowingNames



def local_time(ISO_datestring):
    """Converts ISO datastring to local date string"""

    from datetime import datetime
    from dateutil import tz
    import dateutil.parser

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Pacific/Auckland')
    ISO_date = dateutil.parser.parse(ISO_datestring)
    return str(ISO_date.astimezone(to_zone))


def write_results_csv(camp, phishes_clicked, filename, camp_list):
    with open(filename, 'w') as filehandle:
        print("DEBUG: Just opened ", filename)
        print('Campaign, CreatedDate, CreatedTime, CompletedDate,',
                'CompletedTime, From, Subject, Mail, First, Last,',
                'Status, IP, Latitude, Longitude',
                file=filehandle)

        for result in camp["results"]:
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
                 file=filehandle)

            #   and we keep a tally of the sucessful 'phishes'...
            if result["status"] == "Clicked Link":
                phishes_clicked[camp["template"]["subject"]] += 1
                camp_list.append(camp)
    filehandle.close()


def write_timeline_csv(camp, each_click, filename):
    import ast
    with open(filename, 'w') as filehandle:
        print("DEBUG: Just opened ", filename)
        print('Campaign, Date, Time, Email, Action, IP, User Agent',
                file=filehandle)

        for event in camp["timeline"]:
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
                    file=filehandle)
            else:
                datetime = local_time(event["time"])
                print( camp["name"] +
                    ', ' + datetime[0:10] +
                    ', ' + datetime[11:16] +
                    ', ' + event["email"] +
                    ', ' + event["message"]+
                    ', ,  ',
                    file=filehandle)

            if event["message"] == "Clicked Link":
                each_click.append(event["email"])
    filehandle.close()


def get_results():
    """Find matching campaigns, and produce two report files."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import tempfile
    import os
    import sys
    import ast      # abstract syntact trees
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
    each_click = []    # list of those_who_clicked
    phishes_clicked = defaultdict(int)    # phish subjects clicked
    found = False
    sp_num_of_staff = 0
    sp_camp_list = []
    sp_targets = []    # those sent a spear-phish
    sp_each_click = [] # list of those_who_clicked (spears)
    sp_phishes_clicked = defaultdict(int) # phish subjects clicked (spears)

    td = tempfile.gettempdir()
    mail_out1 = os.path.join(td, target_group + '-results-summary.csv')
    mail_out2 = os.path.join(td, target_group + '-full-timeline.csv')
    mail_out3 = os.path.join(td, target_group + '-spear-results-summary.csv')
    mail_out4 = os.path.join(td, target_group + '-spear-full-timeline.csv')

    # -- Main base group --

    #   ...first getting the total number of staff (targets) in the base group

    full_url = URL + "/api/groups"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    groups = resp.json()
    for group in groups:
        if group["name"] == target_group:
            found = True
            num_of_targets = len(group["targets"])

    #   ...then pulling the "results" and full "timeline"

    for camp in campaigns:
        if "AUTO-" + target_group in camp["name"]:
            print("[OK] Processing ", camp["name"])

            for result in camp["results"]:
                write_results_csv(camp, phishes_clicked, mail_out1, camp_list)

            for event in camp["timeline"]:
                write_timeline_csv(camp, each_click, mail_out2)

    #   ...and finally converting to XLSX format
    outdir = "/tmp"
    excelout_summary(mail_out1, outdir)
    excelout_timeline(mail_out2, outdir)


    if not found:
        sys.exit("[Error] No general campaigns matching: '" +
                 target_group + "' were found.\n")

    # -- Now the "spears" --

    #   ...first, the full details of all sent 'spears'...
    full_url = URL + "/api/groups"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    groups = resp.json()
    for num in range(10):
        sp_found = False
        for group in groups:
            if (target_group + '-spear-' + str(num)) in group["name"]:
                sp_targets.append(group["targets"][0])  # should only be one
                sp_found = True
        if not sp_found:
            break  # because we've found all that matter

    #   ...then pulling the "results" and full "timeline"

    for num in range(10):
        for camp in campaigns:
            if target_group + '-spear-' + str(num) in camp["name"]:
                print("[OK] Processing ", camp["name"])
                sp_num_of_staff += 1  # cos only one user per spear campaign
                sp_camp_list.append(camp)

                for result in camp["results"]:
                    write_results_csv(camp, phishes_clicked, mail_out3, camp_list)
                    #   and we keep a tally of the sucessful 'phishes'...
                    if result["status"] == "Clicked Link":
                        sp_phishes_clicked[camp["template"]["subject"]] += 1

                for event in camp["timeline"]:
                    write_timeline_csv(camp, each_click, mail_out4)

        #   ...and finally converting to XLSX format
        outdir = "/tmp"
        excelout_summary(mail_out3, outdir)
        excelout_timeline(mail_out4, outdir)

    if not found:
        sys.exit("[Error] No spear campaigns for: '" +
            target_group + "' were found.\n")


    # Part III - now total everything up...

    #   Using 'set' removes duplicates
    those_who_clicked = set(each_click)
    num_who_clicked = len(those_who_clicked)
    sp_those_who_clicked = set(sp_each_click)
    sp_num_who_clicked = len(sp_those_who_clicked)

    #   Tally up the scores of which 'phishes' were more successfull...
    phish_score = ""
    for k, v in phishes_clicked.items():
        phish_score += "\t" + str(k) + " - " + str(v) + "\n"
    sp_phish_score = ""
    for k, v in sp_phishes_clicked.items():
        sp_phish_score += "\t" + str(k) + " - " + str(v) + "\n"

    # Return the results in a dict...
    r = {
        "num_of_staff": num_of_targets, "num_who_clicked": num_who_clicked,
        "those_who_clicked": those_who_clicked, "phish_score": phish_score,
        "sp_num_of_staff": sp_num_of_staff,
        "sp_targets": sp_targets,
        "sp_num_who_clicked": sp_num_who_clicked,
        "sp_those_who_clicked": sp_those_who_clicked,
        "sp_phish_score": sp_phish_score,
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
    # csv_file = csv_file.name

    with open(csv_file, 'r') as c:
        df = pd.read_csv(c, quotechar='"', skipinitialspace=True)
    #        , header=0, skip_blank_lines=True,
    #                skipinitialspace=True, encoding='latin-1')

    #   Sort
    # df = df.sort_values(by=['Date', 'Time'])

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

    # csv_file = csv_file.name
    print(csv_file, type(csv_file))
    with open(csv_file, 'r') as c:
        df = pd.read_csv(c, quotechar="'", skipinitialspace=True)
    #        , header=0, skip_blank_lines=True,
    #                skipinitialspace=True, encoding='latin-1')

    #   Sort
    # df = df.sort_values(by=['Date', 'Time'])

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
    # worksheet.set_column(7, 7, 80, superwide)  # set column width
    # worksheet.set_column(8, 8, 80, superwide)  # set column width

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

