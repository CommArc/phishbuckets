#
#   pbos.py - functions calling the Linux OS, and utilities
#


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
        filename = mail_out1
        attachment = open(mail_out1, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % os.path.basename(filename))
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
                        "attachment; filename= %s" % os.path.basename(filename))
        msg.attach(part)
    except FileNotFoundError:
        print("file is missing")

    # There is no longer a third and fourth file (these were for the
    # 'spear-phishing' features that no longer exist).

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

    try:
        os.remove(mail_out1)
    except FileNotFoundError:
        pass
    try:
        os.remove(mail_out2)
    except FileNotFoundError:
        pass
    try:
        os.remove(mail_out3)
    except FileNotFoundError:
        pass
    try:
        os.remove(mail_out4)
    except FileNotFoundError:
        pass


def check_date(start_date):
    """Check that the date is valid."""
    import datetime
    import sys

    if start_date == 'now':
        print("[OK] Using 'now' - so mailouts will start very soon!")
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

