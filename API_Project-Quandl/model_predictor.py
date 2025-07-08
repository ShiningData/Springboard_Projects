Based on the transcript, here are the detailed answers to each question:

## 1. Where does your application/platform sit in the flow of payments?

CPY Position: CPY is a translation service that sits between client data inputs and payment processing systems. As Stephen explained: "CPY is a translation service. We translate client data into the correct formats for payments like ACH, card, check, or wire."

Upstream Sources:
- Multiple internal PNC systems (shown in architectural diagram)
- SFG (Secure File Gateway) - one of several input channels
- Various interfacing applications documented in ServiceNow
- Note: All inputs are internal to PNC - "This is all internal" - no direct external client connections

Downstream Recipients:
- ACH processing systems
- Wire processing (staging/PSG systems)
- Card processors  
- Check print centers
- COD (Corporate Operations Database)

## 2. In what format do you receive transactions/files/information?

Multiple Input Formats Supported:
- XML
- Proprietary formats
- IDOC
- Standard flat file
- Standard delimited file
- Client-specific delimited files

Flexibility: "Whatever they have, we translate... whatever file a client sends to us... whatever the client wants, we will do what we have to do to get that payment into ACH wire, card, or check."

Mixed Files: CPY can receive files containing multiple payment types (ACH, wire, RTP, etc.) in a single file.

## 3. In what format do you send transactions/files/information?

Output Formats by Payment Type:
- ACH: "notch format" for domestic ACH
- Wire: "ISI backs wire format" (proprietary format used for years)
- Card: "special format from our card processor"  
- Check: "check file down to our print center in a specific format for them to print checks"

Internal Standard: Everything is first converted to CPY's "standard flat file" format before being translated to the appropriate output format.

## 4. Do you have any unique identifier that you add to the transactions?

Current Identifiers:
- Sender ID: "Every client from a CPY perspective, every client we have a what we call a sender ID. That's a client identifier."
- Batch Headers: For ACH - "ACH gives us to put into the profile to assign to a sender ID"
- SRF Field: For wires - "there's a thing, a form, a field called SRF, which basically is just a sender ID"

Critical Limitation: No unique CPY tracking identifier that follows transactions downstream:
"Nothing, yeah, we don't, nothing we'll be able to trace back, no. Because once it leaves us, we basically wash our hands."

No Index Maintained: CPY does not maintain an index for tracking transactions once they leave the system.

## 5. Do you have any reporting that captures activity?

Primary Reporting Systems:

a) SystemWare:
- "We have reports that a system where... it's accessible to anybody in PNC... it's transaction data"
- Contains transaction-level data
- Accessible with proper PNC credentials

b) COD (Corporate Operations Database):
- "All the input does get sent to COD"
- Michael Yoeman (recently retired) built comprehensive queries
- "We actually had to write special code just for him to gather that information"
- Consumer: SRC (referenced as having documentation and working toward similar monitoring goals)

c) Pinnacle Integrated Payables Module:
- Client-facing reporting
- "99% of our clients have access to Pinnacle"
- Shows transaction status, rejections, summaries

## 6. Is your data being streamed anywhere?

Yes - COD (Corporate Operations Database):
- "All all the input does get sent to COD"
- Established relationship for "at least five, maybe six or seven years"
- Input data: Confirmed to go to COD
- Downstream data: "I'm not sure how he handled the downstream stuff"

Data sent to COD includes:
- All client input data
- Transaction processing results
- Rejection information

## 7. What happens if a file dies at SFG?

Not directly addressed in the transcript. The team discussed SFG as a transmission mechanism but didn't cover failure scenarios. This would require follow-up with the SFG team that was mentioned as already interviewed.

## 8. What do you do if you didn't get a file or transaction that you were expecting?

No Proactive Monitoring:
"No, we don't... this is up to the client. If they want to send... we get files up 24/7... we really don't know the volume, you know, per day. We don't expect anything."

No Volume Expectations:
"One day we, you know, we really don't know the volume... Otherwise, we get transactions 24/7."

No Missing File Alerts: CPY does not monitor for expected files or send alerts for missing transmissions.

## 9. Can a client check on the status of their file?

Yes - Multiple Methods:

a) Pinnacle Portal:
"99% of our clients have access to Pinnacle, and there's a module out there called Integrated Payables module to where they can go out there and look at their data to see what's going on."

b) Email Notifications:
"We do send an email back to the client... they'll get a summary of what they sent us. And if it's accepted or rejected."

c) Operations Support:
"Otherwise, they will have to call our EC operation staff to find out what the reject is."

## 10. Do you get a notification if your downstream system doesn't receive a file from you?

Limited Confirmations:

Confirmations Received:
- Wire: "We do get something back from wire from staging, but it's basically saying a handshake has been completed"
- Card: "We get a confirmation file back saying us a handshake is completed"  
- Check: "We get a file back saying, uh, the handshake has been completed"

No Confirmations:
- Domestic ACH: "We do not get nothing back from Pep and ACH"

No Failure Notifications: The transcript doesn't indicate that CPY receives notifications about downstream processing failures or missing file alerts from downstream systems.

## 11. Others (Mentioned in the meeting)

a) File Rejection Handling:
- Two rejection modes: Complete file rejection vs. transaction-level rejection
- "We have in our profile we have a thing called either to a complete file rejection or a transaction rejection only"
- Client chooses the rejection method during setup

b) Data Retention:
- "We keep data in our payment table for two years or 730 days"
- Limited to 255 mainframe files at any time

c) Technical Architecture:
- Platform: "Cobalt DP2 on mainframe"
- Internal transfers: DDM (connector app) - no SFG involvement
- External transfers: SFG for client communications

d) File Naming Convention:
- Mainframe naming: "CPY.PCPP.XXX.GDGXXXX"
- PA = Payables and Payments
- File names change when transferred to server environments

e) Processing Schedule:
- ACH: "runs like seven times a day"
- Wire: Multiple daily runs
- 24/7 Operations: Files received continuously

f) Onboarding Process:
- "There's an onboarding or implementation process first. So it's just not, they just don't come and throw anything and we, and we put that together"

g) Validation Process:
- "Our process will edit the data and we will reject payments based on uh uh edits. But we make sure we edit all the data first before we put it into our payment table"
