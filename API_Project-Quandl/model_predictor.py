1. Where does your application/platform sit in the flow of payments (what do you receive from an upstream system, if any)?

CPY operates as a critical middleware translation service within PNC's payment ecosystem, functioning as the primary interface between client payment data and PNC's internal payment processing systems. The system receives payment files from multiple upstream sources through various channels:

- Primary Input Channel: Secure File Gateway (SFG) serves as the main transmission mechanism for external client files, handling various protocols like SMTP and HTTPS
- Internal System Inputs: CPY also receives files from other internal PNC applications through direct mainframe connections using DDM (Direct Data Movement) processes
- Client Integration Points: The system interfaces with numerous internal PNC systems as documented in their Service Now architectural diagrams, though the specific list of interfacing applications was temporarily unavailable during the call due to system changes

CPY's positioning is specifically designed to be "client-facing," meaning it adapts to whatever format clients can provide rather than forcing clients to conform to a single standard. This flexibility makes CPY a crucial buffer between diverse client systems and PNC's standardized payment processing infrastructure. The system operates on a Cobalt DP2 mainframe platform and has been in operation for over 20 years, processing payments 24/7 without predetermined volume expectations.

2. In what format do you receive transactions/files/information?

CPY's input format flexibility is one of its key architectural features, designed to accommodate virtually any client preference through an extensive onboarding and implementation process:

- XML Files: Structured markup language files that provide hierarchical data organization
- Proprietary Formats: Custom client-specific formats developed during the implementation process
- IDOC Files: Intermediate Document format, commonly used in SAP environments
- Standard Flat Files: CPY's internal standard format that some sophisticated clients create directly
- Standard Delimited Files: CPY's standardized comma or other delimiter-separated format
- Client-Specific Delimited Files: Custom delimiter formats (comma, tab, pipe, semicolon) tailored to individual client preferences

The system philosophy is "whatever the client wants, we will do what we have to do to get that payment" processed correctly. However, this flexibility requires a formal onboarding process where the translation rules are established and tested before going live. All input formats ultimately get converted to CPY's internal "standard flat file" format before being processed into the payment table, ensuring consistency in downstream processing regardless of the original input format.

3. In what format do you send transactions/files/information?

CPY translates all processed payment data into highly specific formats required by each downstream payment channel, with each format optimized for the receiving system's requirements:

- ACH Domestic Payments: Converted to NACHA (National Automated Clearing House Association) format, which includes specific batch header information provided by ACH systems and assigned to sender IDs in client profiles
- Wire Transfers: Formatted using a proprietary "ISI backs wire" format that has been in use for years, containing an SRF (Sender Reference Field) that carries the sender ID to the staging system, which then converts it to additional information before sending to PME (Payment Management Engine)
- Canadian ACH: Special processing that involves sending data back to RTS (Real-Time Screening) for OFAC (Office of Foreign Assets Control) screening before proceeding to staging based on PNC's Canadian policy requirements
- Card Payments: Formatted according to specifications required by their card processor, using proprietary formats specific to that vendor
- Check Payments: Formatted for the print center with specific layout requirements for physical check printing, transmitted through SFG to the printing facility

Each format transformation is automated and includes the appropriate identification and routing information required by the downstream systems, ensuring proper processing and settlement.

4. Do you have any unique identifier that you add to the transactions from your system? Do you pass that to the next system in the step? Do you create a new one? If so, do you maintain an index?

CPY's identifier management system is primarily client-focused rather than transaction-tracking focused:

- Sender ID System: Every client is assigned a unique "sender ID" that serves as the primary client identifier throughout the CPY system
- Format-Specific Identifiers: Each payment channel requires different identification schemes:
  - ACH uses batch header information provided by ACH systems and embedded in client profiles
  - Wire transfers use the SRF (Sender Reference Field) containing the sender ID
  - Card processors have their own identification requirements
  - Check processing uses specific formatting for print center identification

Critical Limitation: CPY does not create or maintain universal tracking identifiers that follow transactions through the entire payment lifecycle. As stated in the transcript: "Nothing we'll be able to trace back, no. Because once it leaves us, we basically wash our hands." This represents a significant gap in end-to-end transaction traceability.

No Index Maintenance: CPY does not maintain an index of unique transaction identifiers that could be used for downstream tracking. The mainframe system has file naming limitations (255 files maximum) and relies on Generation Data Groups (GDG) for file version management, but these are not designed for transaction-level tracking.

5. Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction? If so, where is that hosted? Are there consumers for said report today?

CPY maintains comprehensive reporting capabilities through multiple systems and channels:

Primary Reporting Platform - SystemWare:
- Accessible to anyone within PNC with appropriate access credentials
- Contains detailed transaction data and processing information
- Provides operational visibility into CPY processing activities
- Used by internal teams for monitoring and troubleshooting

Client-Facing Reporting - Pinnacle Integrated Payables Module:
- Available to approximately 99% of CPY clients
- Allows clients to view their payment data in real-time
- Shows transaction status including acceptance and rejection details
- Provides self-service capability for client inquiries
- Accessible through PNC's Pinnacle platform

Automated Client Communications:
- Summary emails sent to clients detailing transmitted payments
- Acceptance/rejection status reporting
- Volume and processing confirmations

Current Report Consumers:
- CPY EC (Electronic Commerce) operations staff for client support
- Clients through Pinnacle self-service portal
- Internal PNC teams through SystemWare access
- Data warehouse consumers through COD integration

Operational Support: When clients cannot access Pinnacle or need detailed rejection information, they contact CPY's EC operations staff who can access detailed transaction data and provide specific information about processing issues or rejections.

6. Is your data being streamed anywhere? For example, a warehouse like COD.

Yes, CPY has established comprehensive data streaming to PNC's enterprise data warehouse:

COD Integration Details:
- All CPY input data is systematically sent to COD (Corporate Operations Database)
- Integration has been operational for 5-7 years through OLT (Online Transaction) processes
- Implemented by Mike Yoman (recently retired) who created comprehensive queries to extract CPY data

Data Scope:
- Complete input transaction data from all client sources
- Processing status and results information
- Rejection and exception data
- Historical data maintained according to retention policies

Custom Code Development: CPY had to write special code specifically to support the COD data extraction requirements, indicating the integration was designed to be comprehensive and systematic rather than ad hoc.

Uncertainty About Downstream Data: While all input data flows to COD, there's uncertainty about whether downstream processing results (ACH confirmations, wire handshakes, etc.) are also captured in COD, as the CPY team wasn't directly involved in that aspect of the data pipeline design.

Current Status: With Mike Yoman's retirement, there may be knowledge gaps about the specific implementation details of the COD integration, though the automated processes continue to operate.

7. What happens if a file dies at SFG?

The transcript does not provide specific details about SFG failure recovery procedures. However, several contextual points emerge:

SFG's Role in CPY Operations:
- SFG handles both inbound client file transmission and outbound file delivery to external systems
- Used for external communications while internal transfers use DDM (Direct Data Movement)
- Critical component in the payment processing chain for external client interactions

Operational Context:
- CPY operations staff use Tableau to access SFG transmission data for client inquiries
- SFG appears to have logging and tracking capabilities that operations can reference
- The system operates 24/7 with no predefined expectations for file volumes or timing

Knowledge Gap: The lack of specific SFG failure procedures in the transcript suggests this may be an area requiring further investigation with SFG specialists or operations teams who handle transmission issues.

8. What do you do if you didn't get a file or transaction that you were expecting to get on a certain day?

CPY operates under a fundamentally reactive rather than proactive monitoring model:

No Proactive Monitoring:
- CPY does not track expected file volumes or schedules
- No alerts or notifications for missing files
- No baseline expectations for daily transaction volumes
- System processes whatever arrives whenever it arrives

24/7 Operation Model:
- Files are received and processed continuously around the clock
- Volume varies unpredictably based on client business patterns
- Multiple clients sending files at different frequencies and times
- Cannot predict when or how many transactions to expect on any given day

Client Responsibility Model:
- Clients are responsible for ensuring their files are transmitted
- No service level agreements for specific file delivery timing
- CPY's role is to process what arrives, not to monitor what should arrive

Exception Scenario: The only situation that would be considered unusual would be receiving zero transactions across all clients, which would be highly abnormal given the 24/7 operational pattern and multiple client base.

Alternative Monitoring: While CPY doesn't monitor expected files, clients have access to Pinnacle and can track their own transmission status and results.

9. Can a client check on the status of their file?

Clients have multiple comprehensive options for checking file status:

Primary Self-Service Option - Pinnacle Integrated Payables Module:
- Available to approximately 99% of CPY clients
- Real-time access to payment data and transaction status
- Detailed rejection information and reasons
- Processing confirmation and acceptance status
- Historical transaction data access

Automated Communications:
- Summary emails automatically sent to clients
- Details include volume processed, acceptance rates, rejection counts
- Specific information about which transactions were accepted or rejected
- Provides proactive status information without requiring client inquiry

Assisted Support - EC Operations Staff:
- Available for clients who cannot access Pinnacle
- Detailed transaction-level support for complex inquiries
- Can provide specific rejection codes and resolution guidance
- Handles approximately 1% of clients who lack Pinnacle access

Status Information Available:
- File receipt confirmation
- Transaction-level processing results
- Rejection details with specific error codes
- Volume confirmations and summaries
- Historical processing data

Response Timing: Status information is available immediately after processing, allowing clients to quickly identify and resolve any issues with their payment files.

10. Do you get a notification if your downstream system doesn't receive a file from you?

CPY receives limited and inconsistent acknowledgments from downstream systems, with significant gaps in delivery confirmation:

ACH Processing Acknowledgments:
- Domestic ACH: No acknowledgment or confirmation received from the processing system
- Canadian ACH: More complex process involving OFAC screening through RTS with some feedback received
- ACH Staging: Some handshake confirmations for Canadian processing based on PNC policy

Wire Transfer Confirmations:
- Staging System: Receives handshake completion confirmation
- Limited Information: Confirmation only indicates successful handshake, not complete processing
- Downstream Processing: No visibility into what happens after staging receives the file

Card Processing Acknowledgments:
- Card Processor: Receives confirmation file indicating handshake completion
- Basic Confirmation: Limited to transmission acknowledgment rather than processing confirmation

Check Processing Confirmations:
- Print Center: Receives confirmation that handshake has been completed
- Physical Processing: No confirmation about actual check printing or mailing

Significant Limitations:
- No systematic notification system for delivery failures
- Confirmations are limited to initial handshake or receipt acknowledgment
- No end-to-end processing confirmation
- No alerts if expected downstream acknowledgments are not received
- Manual investigation required if processing issues are suspected

Operational Impact: The lack of comprehensive downstream notifications means that issues in the payment processing chain may not be immediately apparent to CPY operations, potentially delaying issue identification and resolution.

11. Others

Several additional critical operational and technical details emerged from the discussion:

Transaction Rejection Management:
- Client Policy Options: Clients can choose between complete file rejection (one bad transaction rejects entire file) or individual transaction rejection (only bad transactions are rejected)
- Data Validation: All data is edited and validated before being placed in the payment table
- Rejection Reporting: Detailed rejection information provided through Pinnacle and email notifications

Data Retention and File Management:
- Payment Table Retention: Transaction data maintained for 730 days (two years) before automatic purging
- Mainframe File Limitations: System can only maintain 255 file versions using GDG (Generation Data Groups)
- File Naming Convention: Complex mainframe naming structure (e.g., CPY.PCPY.PA.CPYPC207.GDG) where components indicate high-level qualifiers, application areas, and specific job functions

Technical Architecture Details:
- Mainframe Platform: Operates on Cobalt DP2 mainframe system
- Internal Communications: Uses DDM (Direct Data Movement) for internal PNC system communications
- External Communications: Uses SFG for all external client and vendor communications
- Processing Philosophy: "House analogy" - SFG is the front door for external access, internal movement uses different mechanisms

File Naming and Tracking:
- Mainframe to Server Translation: File names change when transferred from mainframe to server environments through SFG
- Version Management: GDG system creates sequential numbering (001, 002, etc.) up to 255 versions
- Limited Traceability: File name correlation between systems exists but requires understanding of both mainframe and server naming conventions

Operational Support Structure:
- 24/7 Processing: Continuous operation with varying extraction job schedules (ACH runs seven times daily, wire runs multiple times)
- Multiple Client Support: Extensive client base with varying file formats and processing requirements
- Flexible Implementation: Each client onboarding involves custom translation rule development and testing
