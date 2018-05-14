#
#   pbconfig - functions for reading configuration settings.
#


def get_mailshot_time(msset):
    """Supply the schedule for the mailshot 'campaigns'.

    Twenty times to do a mailshot 'campaign', and which groups get them...

    TODO:
      -  moving config to YAML (easier to read/write, allows comments) - DONE
      -  if no YAML, autoconvert the existing JSON

    """

    import json
    import yaml
    import sys
    from pbsettings import config_dir
    # full_path = config_dir + 'mailshot_time.json'
    full_path = config_dir + 'mailshot_time.yaml'


    try:
        with open(full_path) as data_file:
            mailshot_times = yaml.load(data_file)
            if msset not in mailshot_times:
                exit_msg = "[Error] No set: '" + msset + "' found in mailshot_time.json"
                sys.exit(exit_msg)

    except IOError:
        print("[OK] No 'mailshot_time' found, so creating a sample: ", full_path)
        """
        Format: day, hour:minute, group - e.g.: 1, "16:00", 9
        (where day=1 is the starting date of the campaign, and
        typically we don't send anything over the weekend)

        Note that this is in YAML, so  we can manually add comments, but these
        won't be read or written by the 'yaml' module

        """
        sample_mailshot_times = {
            "FIRST":
                [
                    [1, "9:00", 0],
                    [1, "10:00", 1],
                    [2, "11:59", 2],
                    [2, "15:00", 3],
                    [3, "9:00", 4],
                    [3, "16:30", 5],
                    [4, "11:00", 6],
                    [4, "14:00", 7],
                    [5, "09:00", 8],
                    [5, "10:00", 0],
                    [8, "11:55", 1],
                    [8, "15:00", 2],
                    [9, "9:00", 6],
                    [9, "16:30", 8],
                    [10, "11:00", 0],
                    [10, "14:00", 9],
                    [11, "08:30", 7],
                    [11, "10:00", 5],
                    [12, "8:30", 3],
                    [12, "10:30", 0]
                ],
            "SECOND":
                [
                    [1, "5:00", 0],
                    [1, "10:00", 1],
                    [2, "11:59", 2],
                    [2, "15:00", 3],
                    [3, "9:00", 4],
                    [3, "16:30", 5],
                    [4, "11:00", 6],
                    [4, "14:00", 7],
                    [5, "5:00", 8],
                    [5, "10:00", 0],
                    [8, "11:55", 1],
                    [8, "15:00", 2],
                    [9, "9:00", 6],
                    [9, "16:30", 8],
                    [10, "11:00", 0],
                    [10, "14:00", 9],
                    [11, "5:00", 7],
                    [11, "10:00", 5],
                    [12, "8:30", 3],
                    [12, "10:30", 0]
                ]
        }

        with open(full_path, 'w') as outfile:
            yaml.dump(sample_mailshot_times, outfile, default_flow_style=False, allow_unicode=True)
            # json.dump(sample_mailshot_times, outfile, sort_keys=True,
            #              indent=4, ensure_ascii=False)

        # Now open the file we just wrote...
        with open(full_path) as data_file:
            # mailshot_times = json.load(data_file)
            mailshot_times = yaml.load(data_file)
            
            #DEBUG
            #
            print(mailshot_times)

            if msset not in mailshot_times:
                exit_msg = "[Error] No set: '" + msset + "' found in mailshot_time.json"
                sys.exit(exit_msg)
            
    return mailshot_times[msset]


def get_phishes(phset):
    """
    Pull in all the sets of twenty phishes that we have, then return
    the one requested - or a listing of them all. If no dataset of
    phishes exists, create a sample, explaining the format.


    The format of these is:
        email_template, URL, sending_profile

    Note: templates can't include either single or double quotes in names.

    """
    import json
    import yaml
    import sys
    from pbsettings import config_dir

    full_path = config_dir + 'phishes.yaml'

    try:
        with open(config_dir + 'phishes.yaml') as data_file:
            phishes = yaml.load(data_file)
            if phset not in phishes:
                exit_msg = "[Error] No set: '" + phset + "' found in phishes.yaml"
                sys.exit(exit_msg)

    except IOError:
        print("[OK] No 'phishes' found, so creating a sample: ", full_path)
        sample_phishes = {
            "FIRST": [
                ["Wish you were here?", "gallery.yourpix.tld/664540330544", "Girl-1"],
                ["CNZ - Your account activity...", "bank.tld/secure", "Online security"],
                ["LOL - pretty funny!", "partysnaps.yourpix.tld/becks", "Girl-2"],
                ["So sad to see this...", "secserv.tld/news78757485", "Boy-2"],
                ["LinkedIn - Jill Meadows", "linkedin.sev.tld/login.html", "Woman-1"],
                ["Thought you might enjoy...", "snaps.pix.tld/jack", "Boy-1"],
                ["Airflight deal", "secserv.tld/FLIGHTS.html", "Girl-3"],
                ["Facebook comment", "facebook.secserv.tld/login.html", "Facebook"],
                ["Tax return delays", "secserv.tld/revenue.gov.tld/delay", "Taxman"],
                ["Your offer..", "ebuy.secsv.tld/a4c1kk", "Ebuyer"],
            ],
            "SECOND": [
                ["222h you were here?", "gallery.yourpix.tld/664540330544", "Girl-1"],
                ["You222r account activity...", "bank.tld/secure", "Online security"],
                ["LOL22 - pretty funny!", "part22aps.yourpix.tld/becks", "Girl-2"],
                ["So sad to see this...", "secserv.tld/news78757485", "Boy-2"],
                ["Linked22Jill Meadows", "link22edin.sev.tld/login.html", "Woman-1"],
                ["Thoug22ht you might enjoy...", "snaps.pix.tld/jack", "Boy-1"],
                ["Airf22light deal", "secserv.tld/FLIGHTS.html", "Girl-3"],
                ["Fac22ebook comment", "facebook.secserv.tld/login.html", "Facebook"],
                ["Ta22x return delays", "secserv.tld/revenue.gov.tld/delay", "Taxman"],
                ["Yo22ur offer..", "ebuy.secsv.tld/a4c1kk", "Ebuyer"],
            ]
        }

        with open(config_dir + 'phishes.yaml', 'w') as outfile:
            yaml.dump(sample_phishes, outfile, default_flow_style=False, allow_unicode= True)

        # Now open this file we just wrote...
        with open(config_dir + 'phishes.yaml') as data_file:
            phishes = yaml.load(data_file)
            print(phishes)
            if phset not in phishes:
                exit_msg = "[Error] No set: '" + phset + "' found in phishes.yaml"
                sys.exit(exit_msg)

    return phishes[phset]
