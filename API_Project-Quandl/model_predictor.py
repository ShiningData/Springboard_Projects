
 Project Overview
 • The team is working to track the life cycle of payments from start to finish as they enter 
and leave the bank.
 • The goal is to map and document the entire flow of payments through PNC's ecosystem, 
including multiple apps, layers, and different frameworks.
 • The project aims to understand the scope of what's happening in the payments 
ecosystem through the lens of applications and layers.
 • The project was initiated due to multiple issues occurring in different layers over the last 
few months.
 SFG's Role and Limitations
 • SFG routes data between external partners (customers) and internal PNC applications.
 • SFG does not have insight into the data within the files and cannot identify payment files 
without specific file names.
 • Kristen: "To me, they're all just files. So I'm never going to be able to tell you how many 
payments files we route unless you give me file names."
 • SFG can provide context diagrams and other documentation to help understand its role 
in the ecosystem.
 SFG Context and File Routing
 • Files from external partners come through external firewalls, an F5, a secure proxy layer, 
and internal PNC firewalls before being routed to internal applications.
 • Files are not routed through SFG if they are being sent between two PNC applications.
 • SFG handles file routing for approximately 6,000 external partners to around 250 internal 
applications.
 These notes were taken with Minutes AI (https://myminutes.ai)
External Partners and Third-Party Providers
 • The 6,000 external partners include more than just payments customers.
 • Some partners send files multiple times a day, while others send files less frequently.
 • Some entities send files on behalf of multiple companies as third-party providers.
 Tableau Report
 • The speaker can send a link to the Tableau report or download it and send it in Excel 
format.
 • The report shows the last seven days of all traffic.
 • The report shows:
 • External company (e.g., Apria Health)
 • Producer (entity creating the file, e.g., Apria)
 • Consumer (e.g., HCA, PNC HCA application)
 • File name (e.g., PMT1)
 • The file can be sorted by application to see which apps are relevant.
 SFG File Handling
 • SFG does not parse, open, or inspect the data within the files. "We don't want to know 
what's in your data. We're safer not knowing what's in the file."
 • Files land on an encrypted NAS briefly and are then automatically routed.
 • External partners and internal applications have credentials built into PNC's corporate 
LDAP.
 • SFG uses a combination of partner credentials, file name, and route setup to route files.
 • If an external partner sends an unexpected file name, it will not be routed and will "die on 
SFG."
 File Routing and Error Handling
 These notes were taken with Minutes AI (https://myminutes.ai)
• If a file fails to route, it creates an automated event in PNC's Big Panda monitoring 
application.
 • The 24x7 level one support team monitors these events and works to resolve the issue, 
potentially reaching out to the external partner or relevant internal teams.
 • Routing rules are codified in SFG, based on a combination of partner credentials, file 
name, and the pre-defined route.
 Monitoring Expectations
 • PNC does not implement extensive negative monitoring or alerting at the SFG level due 
to the high volume of files and the variability in file sending patterns. "It's very challenging 
for us to figure out what that should look like."
 • Individual applications are responsible for knowing what files they expect and when.
 • SFG processes 50,000 to 60,000 files daily, making comprehensive negative monitoring 
impractical.
 Data Availability and Limitations
 • PNC has a lot of data available, but it's hard to distinguish payments data from other 
types of data.
 • They can provide data on the average number of files traversing and their size on any 
given day or hour.
 • They may not be able to provide specific information about PSG.
 Access to Data and Reporting
 • The speaker will send the spreadsheet that monitors inbound files and how they are 
routed.
 • Access to the Tableau dashboard will also be granted, but an entitlement request is 
required.
 • The Tableau dashboard refreshes when opened, showing the most recent data.
 Historical Data and File Monitoring
 These notes were taken with Minutes AI (https://myminutes.ai)
• The speaker's report covers the last 7 days, with a similar report available for the last 31 
days.
 • They don't retain data for longer periods due to the large volume of files processed.
 • SFG routes files to PSG without sending a notification beforehand and does not expect 
or receive a response from PSG.
 File Transfer Process and Potential Issues
 • SFG uses Connect Direct to transfer files internally.
 • Once the Connect Direct process from SFG to PSG is successful, SFG's involvement 
ends.
 • The speaker is unaware of instances where files sent by SFG to PSG get stuck.
 File Transfer Issues and Notifications
 • If the PSG subdirectory fills up and can't accept the entire file, SFG won't necessarily 
know because from their perspective, the file left the application.
 • SFG would know if they couldn't even log into PSG due to application unavailability and 
would create an event, prompting them to contact PSG.
 • If SFG can hit PSG and initiate the file transfer, their job is considered done, and they 
won't be aware if PSG can't accept or process the file.
 • SFG doesn't analyze file formats or contents.
 Data Storage and Archiving
 • SFG doesn't store the actual payload file from Kyriba, as they are not a data store.
 • They do keep information on when things happen, such as when the file arrived, when it 
left, and where it went.
 • They don't keep tons of historical data and don't archive to COD or similar systems.
 • The data is stored in Oracle databases.
 Tableau Dashboard and Data Retention
 These notes were taken with Minutes AI (https://myminutes.ai)
• The Tableau dashboard displays the most recent seven days of data, but there's also a 
31-day view, though it's slow to load due to the large amount of file transfer data.
 • The exact duration of event storage in the databases is unknown.
 • Data granularity is limited due to database size constraints, with regular logging focusing 
on errors and issues, while more data can be gathered for troubleshooting.
 Database Information and File Names
 • The team is willing to share database and table schemas, including file names and 
timestamps of events.
 • The Tableau reports pull data from the SFG application database, the SFG workflow 
database, and the ICC database.
 • The SFG workflow database is an operational database, and data is not offloaded to a 
data warehouse.
 • Producer and consumer file names can sometimes differ, with SFG renaming files before 
sending them to PSG based on configurations.
 Data Extraction and Storage
 • The data displayed on the Tableau report is stored in a database.
 • The data is extracted directly from the databases using a live query, which joins and 
presents the data.
 File Handling and Events
 • When a file comes in, it is written to navs.
 • The actual file from Kyriba does not go to a database; only the events surrounding the 
file are stored in the database.
 • These events are written directly to the database.
 PSG and Log Files
 • PSG does not search the speaker's log files.
 These notes were taken with Minutes AI (https://myminutes.ai)
• PSG would not have direct access to the databases to look for data.
 Wrap-up
 • The speaker will send the diagram, the downloaded report, a link to the Tableau site, and 
the entitlement needed.
 These notes were taken with Minutes AI (https://myminutes.ai)
