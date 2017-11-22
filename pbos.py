#
#   pbos.py - functions calling the Linux OS, and utilities
#


def get_at_tasks():
    """Show the queued tasks."""
    import subprocess

    #   Calls standard 'atq'
    bash = "atq"
    atlist = subprocess.check_output([bash], shell=True)
    #   Comes back as bytes, hence the decode bit...
    alljobs = atlist.decode("utf-8")
    jobslist = alljobs.split("\n")
    del jobslist[-1]  # delete the blank one at the end

    at_tasks = []
    job_num = 0
    for job in jobslist:
        job_num += 1
        job_bits = job.split()

        #   Remove the last two fields
        del job_bits[-1]
        del job_bits[-1]

        #   Append into the new list
        at_tasks.append(job_bits)
    return at_tasks


# noinspection PyBroadException
def get_details(tasknum):
    """ Get the details for an 'at' task, based on its #."""

    import subprocess
    import csv

    bash = "at -c " + tasknum + "| tail -2 |head -1"
    atdet = (subprocess.check_output([bash], shell=True)).decode("utf-8")
    atdet_list = [atdet]
    read_items = csv.reader(atdet_list, delimiter=' ',
                            quotechar="'", skipinitialspace=True)
    key_items = list(read_items)
    try:
        the_two = [key_items[0][1], key_items[0][2]]
        return the_two
    except:
        return


def schedule_mailshots(base_group, start_date, phish_set, sched_name):
    """Schedule the 20 phishing mailshot tasks as 'at' jobs"""

    import os
    import time
    import datetime
    from pbconfig import get_mailshot_time, get_phishes

    mailshot_time = get_mailshot_time(sched_name)
    phishes = get_phishes(phish_set)

    for shot in range(0, 20):
        """
        strptime == "parse (convert) string to datetime object."
        strftime == "create formatted string for given datetime object
                     according to specified format."

        """
        if start_date == 'now':
            # Delay for a minute then send email out one per minute...
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
            shot_time = mailshot_time[shot][1]

        # Backslashes so that the "at" command line is properly quoted,
        # The 'shot % 10' is because phishes.json includes named 'sets' of
        # ten defined 'phishes'. If just five are required for a particular
        # engagement, then they can be doubled up to make a set of 10.
        script_path = os.path.abspath(os.path.dirname(__file__))
        cmd = 'echo ' + script_path + '/pbcreatecampaign  ' + \
              '"\'AUTO-' + base_group + '-' + str(shot) + '\'" "\'' + \
              phishes[shot % 10][0] + '\'" ' + \
              '"\'Scare page - ' + base_group + '\'" "\'' + \
              phishes[shot % 10][1] + '\'" "\'' + \
              phishes[shot % 10][2] + '\'" "\'' + \
              base_group + '-' + str(mailshot_time[shot][2]) + '\'" ' + \
              '|at   -v  ' + \
              shot_time + ' ' + mailshot_date.strftime('%m/%d/%Y')

        # create the job...
        retvalue = os.system(cmd)

        if retvalue != 0:
            print("[Error] Creating the 'at' task gave: " + str(retvalue))

    time.sleep(2)
    print("[OK] All mailshot jobs are scheduled")


def schedule_spear_mailshots(base_group, spear_names, mailshot_data_items):
    """Schedule a series of  spear-phishing mailshots as 'at' jobs"""

    import datetime
    import os

    for spear, spear_name in enumerate(spear_names):
        # 'spear' is the index
        date = mailshot_data_items[spear][0]
        time = mailshot_data_items[spear][1]
        # noinspection PyPep8Naming
        URL = mailshot_data_items[spear][2]

        # Assume 'date' is in dd/mm/yyyy format, and move to ISO format...
        dt_date = datetime.datetime.strptime(date, "%d/%m/%Y")
        # noinspection PyPep8Naming
        ISO_date = datetime.datetime.strftime(dt_date, "%Y-%m-%d")

        # Tricky backslashing needed for the "at" command line to work
        script_path = os.path.abspath(os.path.dirname(__file__))
        cmd = 'echo ' + script_path + '/pbcreatecampaign  ' + \
              '"\'' + \
              spear_name + '\'" "\'' + \
              spear_name + '\'" ' + \
              '"\'Scare page - ' + base_group + '\'" "\'' + \
              URL + '\'" "\'' + \
              spear_name + '\'" "\'' + \
              spear_name + '\'" ' + \
              '|at   -v  ' + \
              time + ' ' + ISO_date

        # create the job...
        retvalue = os.system(cmd)

        if retvalue != 0:
            print("[Error] Creating the 'at' task gave: " + str(retvalue))


# noinspection PyBroadException
def show_schedule(base_group):
    """Show the queued tasks, using our 'pbatq' script"""

    import subprocess
    import os
    # Assume that "pbatq" is in the same directory as this current process
    cmd_path = os.path.dirname(os.path.realpath(__file__))
    print("\nHere is the list of 'at' tasks created:\n")
    bash = cmd_path + "/pbatq | grep " + base_group
    try:
        atlist = subprocess.check_output([bash], shell=True)
    except:
        pass  # no need to panic, always gets 'calledProcessError'

    # comes back as bytes, hence the decode bit...
    print(atlist.decode("utf-8"))
    print(("You can manipulate the 'at' queue as follows: "
           "\n 'pbatq' \t\t - list queued tasks"
           "\n 'at -c #' \t\t - details of one"
           "\n 'pbkill <base group>' \t - kill all tasks for a base group\n"
           ))


# noinspection PyBroadException,PyBroadException
def sort_and_print(tasklist):
    try:
        tasks = sorted(tasklist, key=lambda item: item[8])
    except:
        print("Skipped...")
        return
    for task in tasks:
        try:
            print(
                task[0], ":",
                task[3],
                task[2], " @",
                task[4][0:5], " ",
                task[6], " ",
                task[7]
            )
        except:
            print("Skipped: ", task[0])
    return


def check_recip_addresses(recips):
    """Check that recipient address(es) are valid."""

    import sys
    import re
    for recip in recips:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", recip):
            print("[Error] Sorry, but parameter ", recip,
                  " doesn't look like a valid email address")
            sys.exit()
        else:
            print("[OK] Looks like a valid email address: ", recip)
    return


# noinspection PyBroadException
def send_the_report(r, base_group, recips):
    """  Create and send the report, with details as email CSV attachments. """

    import smtplib
    import os
    from email import encoders
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase

    #   unpack the values from the dict...
    num_of_staff = r["num_of_staff"]
    num_who_clicked = r["num_who_clicked"]
    those_who_clicked = r["those_who_clicked"]
    phish_score = r["phish_score"]
    sp_num_of_staff = r["sp_num_of_staff"]
    sp_targets = r["sp_targets"]
    sp_num_who_clicked = r["sp_num_who_clicked"]
    sp_those_who_clicked = r["sp_those_who_clicked"]
    sp_phish_score = r["sp_phish_score"]
    mail_out1 = r["f1"]
    mail_out2 = r["f2"]
    mail_out3 = r["f3"]
    mail_out4 = r["f4"]

    msg = MIMEMultipart()
    fromaddr = "phishserver@example.com"
    msg['From'] = "phishserver@example.com"

    #   Leaving "To:" blank simplifies things if we have multiple recipients
    msg['To'] = ""
    msg['Subject'] = ("Results from: " + base_group +
                      " phishing awareness campaign")

    body = "Main results: "
    body += "\n\nThere were "
    body += str(num_of_staff)
    body += " staff tested; with "
    body += str(round(num_who_clicked * 100 / num_of_staff, 2))
    body += "% clicking at least one web link - "
    num_who_didnt = num_of_staff - num_who_clicked
    body += "but " + str(round(num_who_didnt * 100 / num_of_staff, 2))
    body += "% were more cautious, and didn't click the links."
    body += "\nThe email addresses of the "
    body += str(num_who_clicked)
    body += " staff members who clicked:\n\n"
    for email in those_who_clicked:
        body += "\t" + str(email) + "\n"

    body += "\n\nThese are the subject lines that worked (and #):\n\n"
    body += phish_score
    body += "\n"
    body += "Spear phishing: "
    body += "\n\nThese staff were targeted:\n\n"

    for target in sp_targets:
        body += "\t" + target["first_name"] + " " + target["last_name"]
        body += " (" + target["email"] + ")\n"

    body += "\nSo far, "
    body += str(sp_num_of_staff) + " of these"
    body += " have actually been sent 'spear-phishing' emails - and of these, "

    if sp_num_of_staff > 0:  # if for some reason no spear phishes were done
        body += str(round(sp_num_who_clicked * 100 / sp_num_of_staff, 2))
    else:
        body += "zero "

    body += "% clicked at least one email link.\n"
    body += "The email addresses of the "
    body += str(sp_num_who_clicked)
    body += " staff members who clicked:\n\n"

    for email in sp_those_who_clicked:
        body += "\t" + email + "\n"

    body += "\nThese are the subject lines of the spear items clicked:\n\n"
    body += sp_phish_score

    body += "\nRaw technical detail of when emails were sent and clicked are "
    body += "in the attached XLSX files."
    body += "\nNB: The 'User Agent' column will highlight any instance of Apple"
    body += " Mac or iPhone - these *may* be 'false positives', so check"
    body += " with the users concerned, and if they insist that they did"
    body += " not click the link - then exclude them from the tally."

    #   Attach the body...
    msg.attach(MIMEText(body, 'plain'))

    #   The first file...
    try:
        filename = mail_out1  # "/tmp/ACME..." will become "tmpACME..."
        attachment = open(mail_out1, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)
    except FileNotFoundError:
        print("file is missing")

    # The second file...
    try:
        filename = mail_out2
        attachment = open(mail_out2, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)
    except FileNotFoundError:
        print("file is missing")

    # The third file...
    try:
        filename = mail_out3
        attachment = open(mail_out3, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)
    except FileNotFoundError:
        print("file is missing")

    # The fourth file...
    try:
        filename = mail_out4
        attachment = open(mail_out4, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)
    except FileNotFoundError:
        print("file is missing")

    # And now send the complete thing off!
    text = msg.as_string()
    for recip in recips:
        print("Sending to:", recip)
        try:
            server = smtplib.SMTP('localhost')
            server.sendmail(fromaddr, recip, text)
            print("[OK] Email sent out")
            server.quit()
        except:
            print("[ERROR] Email sending failed")

    # Remove the files now that we've sent them, and don't
    #   crash out if one is missing for some reason - e.g. if
    #   there were no spear phishes done, so no corresponding file.


    #DEBUG  *Actually*, for now let's don't delete the files, handy to have a
    # copy for debugging locally on the dev machine
    pass 
    #  This should skip all the logic below for now


    # try:
    #    os.remove(mail_out1)
    # except FileNotFoundError:
    #    pass
    # try:
    #    os.remove(mail_out2)
    # except FileNotFoundError:
    #    pass
    # try:
    #    os.remove(mail_out3)
    # except FileNotFoundError:
    #    pass
    # try:
    #    os.remove(mail_out4)
    # except FileNotFoundError:
    #    pass
