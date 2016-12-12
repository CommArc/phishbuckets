# Running a Phishing Campaign with "phishbuckets"

## OVERVIEW
This process details how to perform a targeted phishing campaign for a client or
department. The aim is both to measure how cautious staff are, and to raise 
their awareness of what phishing attacks can look like.

The process currently contains two types of attack:
* General hoax emails, targeting most staff members with 1-2 generic types of 
messages each
* Some “spear phishing”, targeting senior staff with custom social media 
invites, etc, and a CFO (Chief Financial Officer) or similar with a “CEO fraud” 
style email, asking them to transfer funds.

## CLIENT DISCUSSION
It is important that we are have clear communication with the client. Approval 
needs to be appropriate and properly documented (i.e. confirmed in writing by an
email).
Use text such as this in an initial contact email:

> `<Contact Name>`, 
>
> You’ve recently approved us running a “phishing awareness campaign” for your 
> business or department.
>
> Before we start, we need to confirm some details:
>
> *	Your preferred start date. Our process runs for two weeks, starting on a Monday
> *	The “pool” of staff from which we can pick targets for “spear-phishing”
> *	Confirm that we have the correct two names in the following sentence:
>
> “This test was run by Acme Consulting Ltd on behalf of `<Their Company>`.  
> It was done at the request of `<Contact Name>`, and with the approval of 
> `<Senior Contact>`.  
> If you have any concerns about this, then please contact them to discuss.” 
>  
> (This will be part of the webpage shown to any staff who click on links in the
> emails)
> 
> Also, could you please confirm that you have read and understood the following:
> 
> Although nothing we are doing is dangerous to your staff or business – an 
> approved “phishing campaign” like this does have the potential to be upsetting
> to staff. 
> 
> In particular, if you have chosen not to announce the campaign to staff 
> beforehand, there is an element of deception in the process as well as the 
> actual emails. Regardless of the fact that this is exactly what the “bad guys"
> are trying all the time, 
> when you ask us to target your own staff we need to ensure that it is approved
> at an appropriate level.  
> 
> Our procedures require that we have the prior approval of two members of the 
> management or board/partnership – and that their names will appear on the 
> “scare screen” that we show to any staff who click on links in these emails. 
> 
> Please bear in mind that we will be targeting all staff, and that the custom 
> “spear phishing” emails will specifically target senior staff.
> 
> And of course, please feel free to contact me to discuss further if any of 
> this is unclear.

The response to this should give us all the information that we need to begin.

## COLLECTING THE TARGET LIST
We need a list of email address in CSV format. 
For very small sites, or ones that don’t have a Domain Controller, you will need
to create the file manually, but the script below is handy for larger AD sites. 
It should only collect active users with mailboxes and that aren’t called Admin 
(or Administrator), Test, or Training. 

###PowerShell Script
Connect to a Domain Controller, either by RDP or remotely via a Remote 
PowerShell session
> Get-ADUser -Filter {(mail -ne "null") -and (Enabled -eq "true") -and (Name -notlike "admin") 
> -and (Surname -notlike "admin") -and (GivenName -notlike "admin") -and (Name -notlike "test") 
> -and (Name -notlike "training")} -Properties Surname,GivenName,mail | Select-Object 
> GivenName,Surname,mail | Export-CSV C:\phishlist.csv -NoTypeInformation 

(If this fails, it may be because you need to run `Import-Module ActiveDirectory` 
first)

Save the results in a convenient place, and:

1. Edit so that the first line has headers exactly like:
 "First Name", "Last Name", "Email"
2. Check for, and delete, any Admin, Test, Training or TempUser type “users”. 

It is also strongly advised to send this list through to the IT contact and ask 
if is correct – and if there are additional accounts that should be included or 
excluded (including service accounts, departed staff that haven’t been removed, 
etc.).

## SETTING UP AN AUTOMATED PHISHING CAMPAIGN
###Base Name
Decide on a Base Name for the campaign. This will be used to title the campaign,
and also to create the Scare Page. The name should have no spaces, and use 
dashes as a delimiter to avoid problems with the scripted elements of the 
process. If our client is Acme Cartoon Violence Inc. and the campaign is being 
run in August of 2016 – we might name it: ACME-AUG16

###Connecting to the gophish Web Interface
* Access the gophish interface, e.g:  http://gophish.example.net:3333/login

###Create an Email Group
* Click on the Users & Groups option in the menu on the left
* Click on New Group
* Set the name to `<BASE-NAME>` (e.g. “ACME-AUG16”)
* If you have a userlist in CSV format, click on Bulk Import Users and browse to the location of your bulk list. Otherwise, manually enter the required information
* Click on Save Changes to complete the process

Scroll through and check that all the names look OK, that it doesn’t include 
contractors, special users like “Webinar” or that names haven’t be mangled 
in some way. 

The import process is a very picky; the .CSV file needs the correct
column names, including capitalisation and the right sort of quote characters
– and then it should go fine. Opening in Excel to check the format may help.

###Create a “Scare Page”
* Click on the Landing Pages option in the menu on the left
* Copy an existing page, such as “Scare page - NEW TEMPLATE”, by clicking on the
“copy” button to the right hand side
* Change the name to “Scare page - `<BASE-NAME>`” (e.g. “Scare page - ACME-AUG16”),
and note that capitalisation and spaces etc. need to be consistent.
* Edit the content of the scare page for the client. You can do this in HTML or
WYSIWYG (click on the Source button to change view). Update the following 
details:

* Client Name
* IT Contact 
* Internal Approver

Then click on Save Page to create the Scare Page. Unless authorise , 
leave the main text exactly as per standard. The end result should look 
something like the example below: 


## Perform a Mail Delivery Test
* Check the client site for a test email account that we can access
* Create a new email group and set the name to `<BASE-NAME>`-TEST (e.g. “ACME-AUG16-TEST”)
* Add the test email account as the only user
* Copy the Scare Page and name it “Scare Page - `<BASE-NAME>`-TEST “

Using the "pbcreateplan" script, setup a test batch to check mailflow, as follows:

* pbcreateplan `<BASE-NAME>-TEST now`
* The “now” option will send 20 phishing emails out - one message a minute
* Log in to the test email account, ensure that emails are arriving
* Test that clicking any links in them will lead to the correct “scare page”
?

##Create a Campaign Schedule
Assuming the test went OK, the next step is to create the main schedule:

* Using the pbcreateplan command to setup a schedule. The command is formatted as follows:
* pbcreateplan `<BASE-NAME> <dd/mm/yyyy>`  
(e.g. pbcreateplan ACME-AUG16 15/08/2016)
* The script will check for the existence of
* An Email Group with the name matching `<BASE-NAME>`
* A Scare Page with the name “`Scare page - <BASE-NAME>`”
* That the date format is correct
* That the date given is a Monday
* If these conditions are met, 20 scheduled “at” jobs will be created to send the emails.
* The sending dates and times, and the phishing emails, are all hard-coded in the pbcreateplan script
* The script will output the tasks that have been scheduled. It will appear as follows:
 
If creation process hangs, or doesn’t seem to complete, exit with ctrl-c and try
re-running it. If it’s already created some items and you get errors like…
    [Error]: Problem creating subgroup…“Group name already in use"… Failure: - perhaps it already exists? 

…then you can reset by running:
       `pbcleanup <BASE-NAME>`
and then try again.

You can perform the following commands to administer the job queue:

* atq		Standard Linux way to view the queue of ’at’  jobs
* pbatq	Our version, more useful for our phishing jobs
* at –c #		Check the details of a specific job
* atrm #		Remove an individual job, if there is a reason for doing so

So, to view what the next ten jobs are:
 
For more output simply:
> pbatq | head -20

i.e. show the first 20 lines of output.
To see just one client’s jobs, use ‘grep’ to filter:
> pbatq \ grep "ACME-AUG16" 

## REPORTING
Once the two-week period has finished the detailed results will be sent to abc, 
who will forward them on. It’s also possible to get the stats at any point by running:
> `pbcollectresults <BASE-NAME> email@somewhere.co.kr`

## APPENDIX: SPEAR PHISHING (TARGETED ATTACKS)
(For now, these will all be done by abc)
These will always require more effort, but there is usually a maximum of five of done per campaign. The aim 
is to give the targeted staff an appreciation of how:
       (a) Information publicly available on the internet can be used maliciously
       (b) Attackers can fake email addresses 
       (c) Emails can be very credible-looking
We use only public information (i.e. not use any information that we already know personally or that we 
know through Acme’s professional relationships). So we research the target with: 
-	Google
-	Their company’s “About Us” page, company blogs and newsletters
-	Newspaper articles
-	LinkedIn, info on interests, business associations past employment
-	Companies Office, esp what companies they’re directors of shareholder of. 
From this research, work out how to do one of these sorts of emails:
-	LinkedIn invite from someone that they probably are not connected to, but might wish to be
-	An email from a credible contact person, with a tempting link
-	Faked “support@” from an association they belong to, asking them to check their account
-	For CFO-type positions, use a faked email from the CEO, requesting urgent payment of $5,280.00, and with 
a link to “full payment details” 
-	Typically, we’ll stick to very plain email to avoid the need to fake logos. The link may need a custom DNS 
entry to be added (e.g. ALPMA-techteam.secserv.kr). These are the ones we already have:
 
and…
 
###Setup and run of spear-phishes
This is now fully automated, using a set of rigid naming standards
You will need to create a create a SENDING PROFILE, EMAIL TEMPLAT and GROUP for each spear phish 
target user – all named ACME-spear-0, ACME-spear-1 etc. and populate these with the ‘phish’ details.
Yu will then run the “pbcreatespear” scripts, which checks that all is correct and then schedules the phishes 
(Note, you should have been given a “pool” of staff that are legitimate targets, and a number of staff to be 
targeted – typically 3 or 5. Use your own judgement as to who specifically attack – it’s fine to select based 
on who you found more info on – e.g. those with big online presences).
Research, and come up with a credible plan, then make a small spreadsheet to keep all 
the info at hand:
*	Create a SENDING PROFILE for the each email - name: ACME-AUG16-spear-1, from: "Angus 
Naughton" a.naughton@gmall.co, host: 37.139.15.76:25 
(domain name should be one without an SPF record; and 37.139.15.76:25 is the we ‘bounce’ email 
off) 
*	Create an EMAIL TEMPLATE for the email itself by copying an existing spear one, and calling ACME-
AUG16-spear-1 then edit the text to match your requirements.
*	Lastly, create a GROUP for each spear target, entering their name and email as usual, but putting 
the Date, Time and URL for the attack in the Position field in the format: 
        29/9/2016 5:50 http://dropbox.secserv.kr/Scan-9087987.PDF
*	When all are prepared, run pbcreatespear `<BASE-NAME>` to schedule the creation of the actual 
campaigns. Be aware that this checks everything before it does any scheduling, so you may need a 
couple of attempts to “get it right”.

