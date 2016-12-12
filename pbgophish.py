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
    # print(type_groups)
    # print(groups)
    found = False

    for group in groups:
        # print(group)
        if group["name"] == base_group:
            found = True
            base_group_object = group
            global num_of_targets
            num_of_targets = len(group["targets"])
            print('[OK] Found base group:  "', base_group, '"', sep='')
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
    full_url = URL + "/api/groups/"+str(grp_id)
    resp = requests.delete(full_url, params=GOPHISH_KEY, headers=headers)
    if (resp.status_code == 200):
        print("Deleted group:", grp_name, "(", grp_id, ")")
    else:
        print("Houston, we have a problem....")
        print("\nText: ")
        print(resp.text)
        print("\nEncoding: ")
        print(resp.encoding)
        sys.exit()
    return


def delete_camp(id, name):
    """Delete an group, by it's id."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import sys

    headers = {'content-type': 'application/json'}
    full_url = URL + "/api/campaigns/"+str(id)
    resp = requests.delete(full_url, params=GOPHISH_KEY, headers=headers)
    if (resp.status_code == 200):
        print("Deleted campaign:", name, "(", id, ")")
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
        # print("DEBUG: Looking for ", phish[0])
        for template in enumerate(templates):
            # print("DEBUG: Looking at: ", dict(template[1])["name"])
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
    for spear in range(spears):
        missing = True
        for template in enumerate(templates):
            sp_name = base_group + "-spear-" + str(spear)
            if dict(template[1])["name"] == sp_name:
                missing = False
        if missing:
            err_msg = "[Error]: The email template '" + sp_name +\
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
            err_msg = "[Error] The SMTP profile '" + sp_name +\
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

    if (resp.status_code == 201):
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
    resp = requests.get(full_url, params=GOPHISH_KEY)
    if not (resp.status_code == 200):
        print("[Error] The API lookup of groups gave a",
              resp.status_code, "return code")
        sys.exit("[Error] Something appears to have gone wrong.\n")

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


def get_mailshot_data(spear_name):
    """Get string of data (time, date, URL) from 'Position' of first user"""

    from pbsettings import GOPHISH_KEY, URL
    import sys
    import requests

    full_url = URL + "/api/groups"
    resp = requests.get(full_url, params=GOPHISH_KEY)
    groups = resp.json()
    for group in (groups):
        if group["name"] == spear_name:
            data = group["targets"][0]["position"]
            return data

    exit_msg = "[Error]: Could not find group " + spear_name
    sys.exit(exit_msg)


def get_results():
    """Find matching campaigns, and produce two report files."""

    from pbsettings import GOPHISH_KEY, URL
    import requests
    import tempfile
    import os
    import sys
    from collections import defaultdict

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
    sp_found = False
    phishes_clicked = defaultdict(int)
    sp_phishes_clicked = defaultdict(int)
    sp_targets = []     # those who were sent a spear-phish

    td = tempfile.gettempdir()
    mail_out1 = os.path.join(td, target_group + '-raw-events.csv')
    mail_out2 = os.path.join(td, target_group + '-mail-outs.csv')
    mail_out3 = os.path.join(td, target_group + '-spear-events.csv')
    mail_out4 = os.path.join(td, target_group + '-spear-outs.csv')

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
    #
    """First we look for the main campaign data"""
    f1 = open(mail_out1, 'w')
    f2 = open(mail_out2, 'w')
    for camp in campaigns:
        if "AUTO-"+target_group in camp["name"]:
            print("[OK] Processing ", camp["name"])
            if not found:
                print("Campaign, Created_date, Created_time, Completed_date",
                      "Completed_time, From, Subject, Mail, First, Last",
                      "Status", file=f1)  # header line for f1
                print("Campaign, Date, Time, Email, Action", file=f2)
            found = True
            for event in camp["timeline"]:
                #   Note the slicing of the ISO 8601 date/time into two fields
                print(camp["name"], ", ", event["time"][0:10], ", ",
                      event["time"][11:16], ", ",  event["email"], ", ",
                      event["message"], file=f2)
                if event["message"] == "Clicked Link":
                    each_click.append(event["email"])

            for result in camp["results"]:
                #   Note the slicing of the ISO 8601 date/time into two fields
                print(camp["name"],
                      ", ", camp["created_date"][0:10],
                      ", ", camp["created_date"][11:16],
                      ", ", camp["completed_date"][0:10],
                      ", ", camp["completed_date"][11:16],
                      ", ", camp["smtp"]["from_address"],
                      ", ", camp["template"]["subject"],
                      ", ", result["email"],
                      ", ", result["first_name"],
                      ", ", result["last_name"],
                      ", ", result["status"], file=f1)
                #   and we keep a tally of the sucessful 'phises'...
                if result["status"] == "Success":
                    phishes_clicked[camp["template"]["subject"]] += 1
            camp_list.append(camp)

    f1.close()
    f2.close()
    if not found:
        sys.exit("[Error] No general campaigns matching: '" +
                 target_group + "' were found.\n")

    # Part II
    #
    """ Now we go looking for all the spear-phishing data"""

    #   First, the full details of all who will have been sent 'spears'...
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
            break   # because we've found all that matter

    #   ...and then the results
    for camp in campaigns:
        if target_group+'-spear-' in camp["name"]:
            print("[OK] Processing ", camp["name"])
            sp_num_of_staff += 1    # cos only one user per spear campaign
            if not sp_found:
                f3 = open(mail_out3, 'w')
                f4 = open(mail_out4, 'w')
                print("Campaign, Created_date, Created_time, Completed_date",
                      "Completed_time, From, Mail, Subject, First, Last",
                      "Status", file=f3)  # header line for f3
                print("Campaign, Date, Time, Email, Action", file=f4)
            sp_found = True
            for event in camp["timeline"]:
                # Note the slicing of the ISO 8601 date/time into two fields
                print(camp["name"], ", ", event["time"][0:10], ", ",
                      event["time"][11:16], ", ",  event["email"], ", ",
                      event["message"], file=f4)

                #   grab all email addresses seen, many will be dups
                # sp_targets_seen.append(event["email"])
                if event["message"] == "Clicked Link":
                    sp_each_click.append(event["email"])

            for result in camp["results"]:
                # Note the slicing of the ISO 8601 date/time into two fields
                print(camp["name"],
                      ", ", camp["created_date"][0:10],
                      ", ", camp["created_date"][11:16],
                      ", ", camp["completed_date"][0:10],
                      ", ", camp["completed_date"][11:16],
                      ", ", camp["smtp"]["from_address"],
                      ", ", camp["template"]["subject"],
                      ", ", result["email"],
                      ", ", result["first_name"],
                      ", ", result["last_name"],
                      ", ", result["status"], file=f3)
                # and we keep a tally of the sucessful 'phishes'...
                if result["status"] == "Success":
                    sp_phishes_clicked[camp["template"]["subject"]] += 1
            sp_camp_list.append(camp)

    if sp_found:
        f3.close()
        f4.close()
    else:
        # not a fatal problem, so we don't call 'os.exit' for this..
        print("[Error]: No spear-phishing campaigns matching: '" +
              target_group + "' were found.\n")

    # Part III - now total everthing up...

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

    #   Return the results in a dict...
    return {
        "num_of_staff": num_of_targets, "num_who_clicked": num_who_clicked,
        "those_who_clicked": those_who_clicked, "phish_score": phish_score,
        "sp_num_of_staff": sp_num_of_staff,
        "sp_targets": sp_targets,
        "sp_num_who_clicked": sp_num_who_clicked,
        "sp_those_who_clicked": sp_those_who_clicked,
        "sp_phish_score": sp_phish_score,
        "f1": mail_out1, "f2": mail_out2, "f3": mail_out3, "f4": mail_out4
        }
