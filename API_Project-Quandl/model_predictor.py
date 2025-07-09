Based on the transcript provided, I'll answer each question from the image using the detailed information shared during the EDI meeting:

1. Where does your application/platform sit in the flow of payments (what do you receive from an upstream system, if any)?

EDI sits in the middle of the payment flow, not at the front as initially suggested. For origination, EDI receives client files from:
- SFG (primary input channel) - EDI gets client files from SFG, but does NOT get PMT files (those only go to CPI)
- Internal applications - Some files can come via mainframe transmission to EDI, not everything goes through SFG
- VAN (Value Added Network) - EDI pulls in files from VAN, which can contain multiple customers in one file, each with different 820 documents from different clients

For receivables, EDI receives files from:
- Lockbox and ARS 
- Wire data for remittance processing
- ACH (described as "our huge one")
- Real-time payments (RTP)
- Merchant services for card transactions
- CAA (Customer Account Analysis) - monthly process, internal data
- Wire remittance reporting from the Dell (but no client files from Dell)

2. In what format do receive transactions/files/information?

EDI receives files in multiple formats:
- EDI format files: ARP files, A28s and A21s, positive pay files
- NACHA format from ACH
- Flat file proprietary format for wire and RTP
- CAA flat file format
- ANSI X12 standard format - This is the standard that EDI follows, with different segments for different purposes (e.g., 820 files have segments identifying ACH transactions with dollar amounts and invoice details)

The transcript clarifies that flat files are "proprietary non-standard files" with structures like "H for header, D for detail, T for trailer" that are worked out between EDI and the sending system.

3. In what format do send transactions/files/information?

EDI sends out files in multiple formats:
- Multiple EDI formats: A20s, A23s (lockbox format), A22 (for CAA)
- ANSI X12 standard EDI documents like 820s, 823s
- Formatted files sorted by payment type to downstream systems: ACH, Wire, Hard Check, and ARP
- Files to various destinations:
  - Pinnacle
  - Lockbox (ACH and wire data, plus RTP)
  - SFT (for client delivery)
  - VAN for dispersing to different customers
  - High Radius (also a VAN)
  - Direct transmission to clients
  - CPI for check processing

4. Do you have any unique identifier that you add to the transactions from your system? Do you pass that to the next system in the step? Do you create a new one? If so, do you maintain an index?

EDI does NOT add unique identifiers to transactions. The transcript reveals:
- No EDI-specific identifiers are added to files
- Channel-based identification: Downstream systems know files came from EDI because of the channel/source, not because of any identifier in the file
- No preserved file IDs between systems - when tracing issues, they use "dollar amount, DDA, and date" to trace transactions
- File-level information only is passed to COD (not transaction-level detail)
- Traceability requires digging: For origination, high-value transactions in GPP can trace back to staging as EDI partner setup, then back to EDI input file receipt, but this requires manual correlation work

5. Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction? If so, where is that hosted? Are there consumers for said report today?

EDI has limited reporting:
- LOT (Life of Transaction): EDI sends all incoming file names to LOT
- Acknowledgement process: EDI has acknowledgement processes for PSG (not all payment types)
- Alert system: When files from PSG aren't acknowledged back, it generates alerts
- Commitment monitoring: This is a tool that generates Service Now tickets when expected client files aren't received or are late
- Error reporting: When customer files have rejections, error reports are created
- No Tableau reports: The EDI team confirmed they don't have any Tableau reports or similar monitoring dashboards

The reporting appears to be primarily operational/alerting focused rather than comprehensive transaction lifecycle reporting.

6. Is your data being streamed anywhere? For example, a warehouse like COD.

Yes, EDI data goes to COD, but it's batch processing, not streaming:
- File names only are sent to COD - no transaction-level detail
- File-level information includes file name and "generation of the data set" 
- Multiple generations per day: EDI produces 5 files a day with different generations (numbered 1, 2, 3, 4, 5)
- Customer with high volume: One customer sends 300 files a day, each getting a generational number
- No detailed content: COD receives strictly file names with no details about what's in the files, total amounts, or transaction counts
- SFG also streams to COD with file names

7. What happens if a file dies at SFG?

The transcript doesn't specifically address what happens if a file dies at SFG. However, it does cover what happens when EDI receives problematic files:
- Operations contact customer: When EDI tries to process a file and it generates an error, operations contacts the client
- Customer notification: They inform the customer about the issue and request correction and resend
- Flexible rejection levels: Based on customer preference established at implementation:
  - Can reject entire file if any transaction is bad
  - Can reject single bad transaction and process the other good ones
- Commitment monitoring: Would likely generate alerts if expected files from SFG don't arrive

8. What do you do if you didn't get a file or transaction that you were expecting to get on a certain day?

EDI has commitment monitoring in place:
- Automated monitoring: Most inbound client files are under commitment monitoring
- Service Now tickets: System generates alerts/tickets when expected files are late or missing
- Operations team: Manually monitors consistent clients and reaches out when files are missing
- Client-driven process: Since origination is "performed at the customer's will," not all clients are monitored
- Selective monitoring: Only consistent, regular clients are actively monitored for missing files
- Manual checklist: Some monitoring is still manual, particularly for error checking when customer files have rejections

9. Can a client check on the status of their file?

Limited client self-service:
- Acknowledgements only: Clients can check status through acknowledgements, but only if they signed up for this service
- Three types of acknowledgements:
  1. "Hey, we got your file"
  2. "Hey, we got your file and it processed successfully"  
  3. "Hey, all the way to the Fed, we got the Fed reference number"
- Optional service: Not all clients opt for acknowledgements (some don't want to pay for transmission)
- No email or fax: EDI doesn't offer email or fax acknowledgements
- FMG transmission: Acknowledgements go out via FMG transmission
- Recommended but not required: EDI strongly recommends acknowledgements but clients can opt out

10. Do you get a notification if your downstream system doesn't receive a file from you?

Very limited downstream notifications:
- PSG acknowledgements only: EDI only gets acknowledgements from PSG, and only for certain payment types
- No other downstream acknowledgements: No other downstream systems provide acknowledgements to EDI
- One-way communication: EDI sends acknowledgements to originating clients but doesn't receive confirmations from most downstream systems
- No lockbox confirmations: For example, EDI doesn't get acknowledgements from lockbox saying "hey, we got your file"
- Alert-based detection: EDI gets alerted when they have issues processing, but this seems to be internal error detection rather than downstream confirmation

11. Others

Additional relevant information from the transcript:

File Structure and Batching:
- Complex file structure: One input file can contain multiple customers/clients, each becoming separate batches
- Payment type sorting: EDI sorts by payment type (ACH, wire, card, check, ARP) and sends grouped files
- Batch preservation: Files maintain client segregation through batch structure even when combined

Client Acknowledgement Preferences:
- Cost consideration: Some clients opt out of acknowledgements due to transmission costs
- Most clients want acknowledgements: "Nine times out of 10, they want an acknowledgement"

Volume and Scale:
- High-volume clients: One customer sends 300 files per day
- Multiple daily generations: EDI processes 5 file generations per day

Integration Points:
- No Pinnacle files: EDI doesn't accept Pinnacle files (that's CPI only)
- Check processing handoff: EDI can accept check payments but must pass them to CPI for actual check printing vendor interaction
- Generic processing: Some processes bypass the connection warehouse and go through "generic process" for direct file translation

This detailed breakdown shows EDI serves as a critical middleware component that receives, transforms, and routes payment data while maintaining limited tracking and reporting capabilities focused primarily on operational monitoring rather than comprehensive transaction lifecycle management.
