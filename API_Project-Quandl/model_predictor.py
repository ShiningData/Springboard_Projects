Summary:
CPY Service Overview
Core Function: Translation service converting client payment data into correct formats for ACH, card, check, wire payments
Technology Stack: Uses Cobalt DP2 on mainframe for all processing
Service Duration: Stephen has 20 years experience with CPY
Client Flexibility: Accepts multiple input formats (XML, proprietary, IDOC, standard flat file, delimited files)
Standard Processing: Converts all inputs to standard flat file format before entering payment table
Automation Level: Fully automated with no human intervention in translation process
Input Channels and Data Sources
Primary Channel: SFG (Secure File Gateway) for external client file transmission
Internal Sources: Multiple internal PNC applications (diagram referenced but not fully visible)
File Format Variety: XML, proprietary formats, IDOC, standard flat files, client-specific delimited files
Client Onboarding: Implementation/onboarding process required before clients can submit files
24/7 Processing: Continuous file reception and processing capability
Client Identification and Processing
Sender ID: Each client assigned unique sender ID as primary identifier
Payment Method Specific IDs: Different identification requirements for ACH, wire, card, check processors
No Universal Tracking ID: CPY doesn't attach system-specific unique identifiers for downstream tracing
File Rejection Options: Clients can choose transaction-level rejection or complete file rejection
Transaction rejection: Failed transactions rejected, valid ones processed
Complete file rejection: One failed transaction rejects entire file
Output Formats and Downstream Systems
ACH: NACHA format to domestic ACH processing
Wire: ISI backs wire format (proprietary) to staging system
Card: Special format to card processor
Check: Specific format to print center via SFG
Canadian ACH: Separate process through Royal Bank of Canada with RTS OFAC screening
Acknowledgment and Confirmation Systems
Wire: Handshake confirmation from staging
Card: Confirmation file from card processor
Check: Handshake confirmation from print center
ACH Domestic: No confirmation from FedACH
ACH Canadian: Confirmation from staging for Canadian policy compliance
Data Retention and Reporting
Payment Table: 730 days (2 years) data retention
Mainframe Files: Limited to 255 files due to mainframe constraints
COD Integration: All CPY input data sent to COD (Central Operations Database)
Michael Yoman (recently retired) created comprehensive query system
Special code written for COD data gathering
SystemWare: Primary reporting system accessible to all PNC users
Client Access: 99% of clients have Pinnacle access with Integrated Payables module for transaction status
File Naming and Tracking
Mainframe Naming Convention: Complex structure (e.g., CPY.PCPP.CPYPC207.GDG)
CPY.PCPP: High-level qualifier
CPYPC207: Specific job identifier
GDG: Generation Data Group file type
PA: Payables and Payments identifier
Version Control: Sequential numbering system (001, 002, etc.) up to 255 versions
Server Translation: Mainframe file names converted to server format when transmitted via SFG
Internal vs External Communication
Internal Systems: Use Connect:Direct (DDM) for file movement between mainframe and staging
External Clients: All communication through SFG
No Direct External Access: All external interactions routed through SFG transmission layer
Operational Monitoring
Volume Expectations: No specific volume monitoring or alerts
24/7 Operations: Continuous processing with no downtime expectations
Extract Jobs: Scheduled runs (ACH: 7 times daily, wire: multiple times)
Client Notifications: Email summaries sent for file processing results
Exception Handling: EC operations staff handle client inquiries about rejections
Architecture Integration Points
Upstream: SFG and multiple internal PNC applications
Downstream: ACH platforms, wire staging, card processors, check print centers
Monitoring: COD for comprehensive data capture and reporting
Client Interface: Pinnacle system for client self-service transaction monitoring
Action Items:
Review architectural diagram and interface documentation to be sent by team
Examine COD data structure and Michael Yoman's query system for CPY data extraction
Map complete data flow from SFG through CPY to downstream payment systems
Investigate SystemWare reporting capabilities for CPY transaction monitoring
Document file naming conventions and version control for mainframe-to-server translations
Analyze acknowledgment/confirmation patterns across different payment types
Identify gaps in downstream system feedback loops for payment tracking
Explore Pinnacle Integrated Payables module for client-side transaction visibility
Schedule follow-up session after documentation review to clarify remaining questions
Connect with COD team to understand comprehensive payment flow data capture
Investigate Connect:Direct (DDM) internal file movement processes
Map client rejection notification workflows and storage mechanisms
                                           
