Based on the transcript, here's the categorization and details for the CPY (payment translation service) system:

## 1. Application/Platform Position in Payment Flow

What CPY receives (upstream):
- Files from clients in various formats through multiple channels:
  - SFG (Secure File Gateway)
  - Various other internal PNC systems (referenced in architectural diagram)
  - XML, proprietary formats, IDOC, standard flat files, delimited files, client-specific delimited files
- Input formats are flexible - "whatever file a client sends to us"
- All inputs are internal to PNC (no direct external client connections)

What CPY sends (downstream):
- ACH format files to ACH processing systems
- Wire format files (ISI backs wire format) to staging/PSG systems  
- Card format files to card processors
- Check files to print centers
- Everything gets converted to a "standard flat file" format internally first

## 2. Transaction/File Formats Received

Input Formats Supported:
- XML
- Proprietary formats
- IDOC
- Standard flat file
- Standard delimited file
- Client-specific delimited files
- Mixed payment type files (can contain ACH, wire, RTP, etc. in single file)

Process:
- All automated translation (no manual intervention)
- Onboarding/implementation process required for new clients
- Edit validation occurs before processing
- Converts everything to internal "standard flat file" format first

## 3. Unique Identifiers

Current Identifiers:
- Sender ID: Client identifier used by CPY
- Batch Headers: For ACH (provided by ACH system, assigned to sender ID)
- SRF Field: For wires (contains sender ID information)
- Each payment method has its own identification requirements

Traceability Limitations:
- No unique CPY-generated tracking ID that follows transactions downstream
- "Once it leaves us, we basically wash our hands"
- Cannot trace back to CPY once transactions leave the system
- Different downstream systems use their own identification schemes

## 4. Reporting and Activity Capture

Current Reporting:
- COD (Corporate Operations Database): Primary repository for CPY transaction data
  - All input data sent to COD
  - Established for 5-7 years
  - Michael Yoeman (recently retired) built queries to extract CPY data
  - Uncertain about downstream data capture in COD

- SystemWare: Transaction data reporting system
  - Accessible to anyone in PNC with proper access
  - Contains transaction-level data

- Pinnacle Integrated Payables Module: 
  - Client-facing portal
  - 99% of clients have access
  - Shows transaction status, rejections, summaries

Acknowledgment/Confirmation:
- ACH: No confirmations for domestic ACH; some confirmations for Canadian ACH
- Wire: Handshake confirmation from staging
- Card: Confirmation file from card processor
- Check: Confirmation file from print center

## 5. File Processing and Rejection Handling

Rejection Types:
- Transaction-level rejection (default): Rejects individual bad transactions, processes good ones
- Complete file rejection: Rejects entire file if any transaction fails
- Client chooses rejection type during setup

Notification Process:
- Email summaries sent to clients showing accepted/rejected transactions
- Clients can check status via Pinnacle portal
- Operations staff available for questions

## 6. Volume and Scheduling

Transaction Volume:
- Files received 24/7
- No volume expectations or monitoring
- Multiple daily extract jobs:
  - ACH: 7 times per day
  - Wire: Multiple times per day
  - Various scheduled extracts

Data Retention:
- Payment table data kept for 730 days (2 years)
- Limited to 255 mainframe files at any time

## Other Details

Technical Architecture:
- Platform: Cobalt DP2 on mainframe
- File Transfer: 
  - External: SFG for client communications
  - Internal: DDM (connector app) for internal PNC system transfers
- File Naming: Mainframe naming convention (e.g., CPY.PCPP.XXX.GDGXXXX)
  - PA = Payables and Payments
  - GDG = Generation Data Group (versioned files)
  - File names change when transferred to server environments

Integration Points:
- Multiple input systems (detailed in architectural diagram to be shared)
- SFG for external file transmission
- ACH processing systems
- Wire processing (staging/PSG)
- Card processors
- Check print centers
- COD for reporting/monitoring

Monitoring Gaps:
- No proactive volume monitoring
- No alerts for missing expected files
- No end-to-end transaction tracking capability
- Limited visibility into downstream processing status
