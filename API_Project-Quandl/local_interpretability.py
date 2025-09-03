Based on the bank meeting transcript, here are comprehensive and detailed answers to your 18 questions:

 1. Where does your application/platform sit in the flow of payments? (Beginning, middle, end)

The PST (Payment Services Team) application operates primarily at the beginning of the payment flow with some middle-layer functionality. The system functions as an intermediary channel that interfaces with CAP, which serves as PNC's universal API layer for all payment system interactions. 

The PST team receives payment instructions from corporate clients through multiple channels including file transmission, the Pinnacle web module for file uploads, and one-off instruction creation capabilities. Importantly, while they operate in the payment space, they do not facilitate actual money movement. Instead, they process what they specifically term "instructions" rather than payments, emphasizing the distinction between instruction processing and actual fund transfers.

Their role involves providing a white-labeled solution that makes interactions appear to come directly from their corporate clients rather than PNC. After collecting and processing payment instructions, they interface with various downstream middle-layer applications that handle the actual money movement. This positioning makes them a crucial first step in the payment lifecycle, collecting, validating, and routing instructions while maintaining the client's brand identity throughout the process.

 2. What are your downstream applications for originations?

The PST system interfaces with multiple downstream applications for different payment rails:

MLP API serves as a primary downstream system handling two distinct payment types. For direct deposit payments, MLP performs account lookups, account verification, and routing determinations including whether payments qualify for RTP (Real-Time Payments) processing. For PayPal and Venmo payments, the process involves a two-step money movement where RTP transfers funds from the client account to PNC's GL account, followed by wire transfers from the GL account to PayPal to facilitate the actual payments to end recipients.

PTD (Push to Debit) handles direct debit card payments through a specialized integration with Tempus for tokenization and PCI compliance, ultimately routing through the Visa Direct network. This system manages the secure processing of card-based payments while maintaining required security standards.

Zell processing involves a unique workflow where PST indicates to the Zell network through EWS (Early Warning Services) that funds will be available, but the actual money movement occurs through ACH processing. This creates a notification-first, settlement-later model for Zell transactions.

ACH processing handles multiple payment types by creating properly formatted files that get transmitted to Dell services for further processing and eventual settlement through the federal ACH network.

CPY application manages check payments through file creation and transmission to Dell services, which handle the check printing process and associated money movement verification.

Cybersource represents a legacy payment rail owned by Erie (another PNC entity) that only one client utilizes. This system provides direct debit card processing similar to their internal PTD capabilities but requires Erie to serve as the interface for any issues or modifications.

 3. What are your downstream applications for receivables?

This question does not apply to the PST system. The transcript clearly establishes that PST exclusively handles disbursements and outbound payments. They process instructions for paying out funds to recipients but do not handle any inbound receivables or incoming payments. Their entire business model revolves around corporate clients submitting payment instructions for distribution to their payees or beneficiaries.

 4. What are your upstream applications for originations?

PST receives payment instructions through three primary upstream channels:

CAP (Corporate API Platform) functions as PNC's universal API layer that provides secure interfaces for all payment systems across the bank. CAP handles security protocols, authentication, and initial request validation before routing payment instructions to PST. This system ensures that all API-based interactions follow consistent security and processing standards regardless of which payment application ultimately processes the instructions.

Pinnacle operates as a web-based module where corporate clients can log in to upload files containing payment instructions or create individual one-off payment instructions through a user interface. This system provides flexibility for clients who prefer web-based interaction over automated file transmission or API integration.

SFG (Sterling File Gateway) creates secure tunnels between client systems and PNC infrastructure to enable automated file transmission. This system is particularly valuable for clients with ERP systems or other automated payment processing workflows that need to transmit files on scheduled or triggered bases without manual intervention. SFG handles the secure connectivity and file transfer protocols necessary for automated B2B payment instruction transmission.

 5. What are your upstream applications for receivables?

This question is not applicable to PST operations. As established in the transcript, PST only processes outbound disbursements and originations. They do not handle any receivables or inbound payment processing functionality.

 6. Of those downstream applications, which do you receive acknowledgments or notifications from?

PST receives various forms of acknowledgment from their downstream systems:

MLP API returns a specific key-value response containing "ACTC" (Accepted) status, which indicates that MLP has successfully received the payment instruction and forwarded it to the appropriate processing system. This acknowledgment allows PST to update their internal status tracking and notify clients that their payment instruction has been accepted for processing.

PTD (Push to Debit) provides API-based responses with similar "accepted" status indicators, confirming that direct debit card payment instructions have been received and are being processed through the Tempus tokenization system and Visa Direct network.

CPY application sends file-level acknowledgments confirming receipt of check payment instruction files. These acknowledgments verify that the file transmission was successful and that the check printing and processing workflow has been initiated.

ACH processing through Dell services provides acknowledgments for both ACH transactions and CPY-related files. Dell confirms receipt of properly formatted files without errors, which PST treats as confirmation that the payment instructions have been successfully handed off for further processing. If Dell reports file receipt without errors, PST considers their responsibility fulfilled for that batch of transactions.

The acknowledgment system allows PST to maintain accurate status tracking and provide clients with confidence that their payment instructions have been successfully transmitted to the appropriate processing systems.

 7. Of those upstream applications, which do you receive acknowledgments or notifications from?

PST receives different types of acknowledgments from their upstream systems:

SFG (Sterling File Gateway) provides the most comprehensive acknowledgment system, sending two types of response files. The first is an immediate acknowledgment indicating whether the transmitted file was accepted or rejected based on basic validation criteria. The second is a detailed processing report that analyzes the contents of accepted files, identifying any individual payment instructions that were rejected during processing and providing specific reasons for each rejection. This allows clients to understand which payments from a large batch file need attention while allowing valid payments to proceed normally.

CAP does not provide webhook responses or automated acknowledgments back to the originating systems. This means that API-based payment submissions through CAP do not generate automated confirmations of receipt or processing status.

Pinnacle operates on a real-time, UI-based feedback model where users receive immediate notification of errors, missing required fields, or file format issues during the upload and submission process. This real-time validation helps prevent submission of incomplete or incorrectly formatted payment instructions.

 8. In what format do you receive transactions/files/data?

PST supports multiple inbound data formats to accommodate different client preferences and technical capabilities:

CSV files represent the most common format for batch payment instructions, allowing clients to submit structured data in a format that's easily generated from spreadsheets, databases, or ERP systems. This format provides flexibility for clients who need to submit large volumes of payment instructions with consistent data structures.

JSON files support more complex data structures and are particularly useful for clients with modern API-based systems that can generate structured JSON output. This format allows for nested data elements and more sophisticated instruction details.

API calls accept JSON-formatted requests through standard HTTP methods including POST for creating new payment instructions, PUT for updating existing instructions, and GET for retrieving status information. This real-time integration option supports clients who prefer immediate processing over batch file submission.

ZIP files accommodate supporting documentation requirements by allowing clients to attach PDF documents such as explanation of benefits statements, receipts, or other documentation that recipients might need to understand their payments. The ZIP files can only contain PDFs to maintain security and processing consistency.

This multi-format approach ensures that clients can integrate payment instruction submission into their existing workflows regardless of their technical infrastructure or processing preferences.

 9. In what format do you send transactions/files/data?

PST transmits data to downstream systems using formats appropriate for each target system:

API calls are used for real-time integrations with MLP, PTD, and CPY systems. These JSON-formatted API requests contain all necessary payment instruction data formatted according to each downstream system's requirements.

TXT files in Nacha format are transmitted to Dell services for ACH processing. The Nacha format represents the standard ACH file structure required by the federal ACH network, containing properly formatted payment instructions with all required fields for electronic fund transfers.

TXT files for CPY processing are also sent to Dell services but contain check payment instruction data formatted according to check processing requirements. Dell reformats this data for transmission to the CPY application for check printing and mailing.

CSV and JSON status files are sent back to clients who subscribe to automated status reporting. These files contain updates on payment processing status, including progression from pending to accepted to completed states, along with selected payment methods and any relevant error conditions.

The format selection for each downstream system reflects the technical requirements and processing capabilities of the receiving applications, ensuring compatibility and efficient processing.

 10. Do you have any unique identifier that you add to the transactions from your system?

PST generates and manages a comprehensive unique identifier system:

Trace ID generation utilizes an Oracle-based tool to automatically create unique identifiers consisting of 9-15 numeric characters for each payment instruction. This trace ID serves as the primary tracking mechanism throughout the payment lifecycle and gets passed to all downstream systems for consistent reference.

Downstream system integration adapts the trace ID for each target system's naming conventions. For PTD (Push to Debit) transactions, the trace ID becomes the "client payment ID" in their system. For Zell transactions processed through ACH, the identifier is formatted as an ACH identifier with a "PNB" prefix (representing Pittsburgh National Bank) followed by the trace ID. For RTP payments processed through PRT, the trace ID is incorporated into the "end-to-end ID" field required by real-time payment networks.

Client-provided identifiers are also accepted and stored within the PST system, but these remain internal to the e-payment ecosystem including Pinnacle UI and internal databases. Client-provided IDs do not get transmitted to downstream systems, maintaining separation between internal client reference systems and external payment network requirements.

This dual-identifier approach allows clients to maintain their own reference systems while ensuring that PST can track payments throughout the external processing workflow using standardized trace IDs.

 11. Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction?

PST maintains several reporting mechanisms with varying levels of sophistication:

Client-facing status tracking operates through the Pinnacle UI and provides real-time visibility into payment progression through various states including pending client approval, compliance review, waiting for payee action, and final completion status. This system allows clients to track their payment instructions from submission through final disposition.

Automated status files are available to clients who subscribe to daily transmission services. These files contain comprehensive details about all payment instructions that changed status during each 24-hour period, providing clients with automated updates on their payment portfolio performance.

Basic internal reporting consists of a rudimentary daily report system accessible via VPN that shows fundamental metrics including number of payments created, completed, and total dollar amounts processed. While functional, this reporting is acknowledged as basic and not comparable to modern business intelligence tools.

Monthly reporting is generated by the run-the-bank team and provides more comprehensive analysis including payment volume trends, client-specific breakdowns, and payment method selection patterns. However, these reports lack the sophistication of modern dashboard or BI reporting tools.

Reporting limitations exist because PST does not process the actual payments, meaning that detailed payment performance metrics are captured by the individual payment rails (RTP, ACH, etc.) rather than being consolidated in PST reporting. This distributed processing model creates challenges for comprehensive payment lifecycle reporting from a single source.

The reporting infrastructure is hosted within Pinnacle UI and their Oracle/MongoDB database systems, with consumption by both internal teams and external clients depending on the report type.

 12. Can a client check on the status of their payment?

PST provides multiple mechanisms for clients to monitor payment status:

Real-time Pinnacle access allows clients to log into the Pinnacle module and view current status information for all their payment instructions. When payees make payment method selections or when status changes occur in downstream systems, these updates are reflected in real-time within the Pinnacle interface.

Automated daily status files are available to clients who subscribe to this service, providing comprehensive daily reports containing all payment instructions that experienced status changes during the previous 24-hour period. These files include details about status transitions, payment method selections by recipients, and any error conditions that require client attention.

On-demand status reporting allows clients to generate quasi-status files through the Pinnacle interface, essentially providing access to the same information that would be included in subscribed daily status files but available whenever the client needs it rather than on a scheduled basis.

Status granularity includes tracking of client approval workflows, compliance review processes, payee interaction stages, and final payment completion. This comprehensive status tracking helps clients understand where their payments are in the overall process and whether any action is required on their part.

This multi-channel approach ensures that clients can access payment status information through their preferred method, whether that's real-time web access or automated file transmission for integration into their own systems.

 13. What sort of data management are you doing? What type of database do you use?

PST operates a dual-database environment reflecting both current operations and strategic modernization:

Oracle database currently serves as the primary operational database, handling the majority of current transaction processing, status tracking, and reporting functions. This represents the established infrastructure that has supported PST operations historically.

MongoDB implementation represents their strategic direction as part of the broader transition to IPF (Integrated Payment Framework) infrastructure. MongoDB's unstructured relational database capabilities provide greater flexibility for handling diverse payment instruction formats and complex data relationships that characterize modern payment processing.

Transition strategy involves gradually migrating processes and data structures from Oracle to MongoDB as IPF capabilities are developed and proven. PST represents one of the early adopters of this technology transition within PNC's payment ecosystem, making them a pilot case for the broader organizational shift toward more flexible database architectures.

Data management complexity results from maintaining operations across both database systems during the transition period, requiring data synchronization, format translation, and operational procedures that accommodate both platforms until the migration is complete.

The dual-database approach reflects the broader industry trend toward more flexible, cloud-native database solutions while maintaining operational continuity during the transition period.

 14. Is your database split between operational and reporting databases?

PST implements a time-based database separation strategy:

Production database maintains all operationally relevant data for approximately 90 days, ensuring that active payment instructions, recent status changes, and current client interactions are readily accessible for real-time processing and immediate historical reference.

Archival database stores historical data beyond the 90-day operational window to satisfy PNC's seven-year data retention requirements. This separation ensures that operational database performance is not impacted by large volumes of historical data while maintaining compliance with regulatory and internal policy requirements for data preservation.

Data lifecycle management involves automated processes that migrate data from production to archival storage based on age and operational relevance, ensuring that current operations have optimal database performance while maintaining long-term data availability for compliance, audit, and historical analysis purposes.

This separation strategy balances operational performance requirements with regulatory compliance obligations, ensuring that active payment processing is not impacted by the storage requirements for historical data retention.

 15. Is your data being streamed anywhere? For ex. a warehouse like COD?

PST does not stream data to COD or similar data warehouse environments:

COD exclusion results from data classification requirements that COD infrastructure could not accommodate. The sensitive nature of payment instruction data and associated security requirements created incompatibility with COD's data handling capabilities.

Alternative data sharing occurs through status file transmission to other applications such as healthcare systems, but this represents structured file transfer rather than continuous data streaming. These transmissions maintain data security and compliance requirements while providing necessary information to dependent systems.

Data warehouse strategy differs from other PNC applications that may use COD as their archival and analytical data repository. PST's data sensitivity and security requirements necessitate different approaches to long-term data storage and analysis.

The absence of data warehouse streaming reflects the specialized security and compliance requirements associated with payment processing data, requiring more controlled and secure data sharing mechanisms.

 16. Is it possible for there to be a failure at your stage in the payments flow? If so, what happens if there is one?

PST has implemented comprehensive failure detection and response mechanisms:

Automated alerting system monitors all payment statuses using timer-based controls with Service Level Agreements typically set at one-hour intervals. Any payment instruction that remains in a non-permanent status (excluding final states, pending compliance review, or awaiting client action) beyond the SLA threshold triggers automated incident creation.

Status monitoring scope includes temporary workflow statuses such as "pending RTS response" or "waiting for downstream system confirmation" that should transition quickly under normal circumstances. Extended delays in these statuses indicate potential interface problems, system outages, or data processing errors.

Incident routing directs automated alerts to the dedicated run-the-bank team responsible for PST operations. This team investigates whether issues stem from data quality problems, interface connectivity issues, downstream system outages, or temporary system disruptions that may resolve automatically.

Visibility limitations exist for failures that occur after PST successfully hands off payment instructions to downstream systems. For example, if MLP accepts a payment instruction but subsequent processing fails in PRT (real-time payment processing), PST would not be aware of the failure since their interface responsibility ended with successful MLP acceptance.

Recovery procedures depend on the failure type, ranging from data correction and resubmission for data quality issues to coordination with downstream system operators for interface or connectivity problems. The run-the-bank team has established procedures for triaging different failure types and escalating issues that require cross-system coordination.

This failure management system ensures that payment processing disruptions are quickly identified and addressed while acknowledging the distributed nature of payment processing that limits visibility into downstream system performance.

 17. Do you do any negative tracking or volume tracking to account for expected transactions on a certain day?

PST does not implement negative or volume tracking systems:

Client autonomy represents the primary reason for avoiding volume tracking, as corporate clients have complete discretion over when and how frequently they submit payment instructions. Some clients operate on weekly payment cycles, others monthly, and some submit payments irregularly based on their business needs.

Variable payment patterns make it impossible to establish reliable baseline expectations for daily transaction volumes. Client payment behavior depends on their business cycles, cash flow management practices, and operational procedures that are outside PST's control or visibility.

Recipient dependency adds another layer of variability since payment completion depends on recipient actions. Even when clients submit payment instructions, if recipients do not make payment method selections or take required actions, no downstream transactions may occur on any given day.

Business model alignment with client-driven timing means that zero-transaction days are normal and expected rather than indicators of system problems. PST's role is to process instructions when clients submit them rather than to expect or monitor for specific transaction volumes.

This approach reflects the service-oriented nature of PST's business model, where transaction volume is determined entirely by client needs rather than system-driven expectations or requirements.

 18. Do you get any notifications from downstream systems if they don't receive a file or transaction from you?

PST does not receive direct notifications for missing files or transactions:

Absence of direct alerts means that downstream systems do not specifically notify PST when expected files or transactions are not received. This reflects the event-driven nature of payment processing where systems respond to received instructions rather than expecting specific volumes or timing.

Out-of-sync incident detection can occur indirectly when related systems identify balance or reconciliation discrepancies. For example, if PST has Zell payments in pending status but fails to send corresponding ACH files for money movement, the ACH processing group might detect out-of-balance conditions and open incidents to investigate the discrepancy.

Indirect failure detection relies on downstream systems' own monitoring and reconciliation processes to identify when expected payment flows are incomplete or inconsistent. These systems may generate alerts about their own operational issues that indirectly reveal problems with PST's file transmission or processing.

Manual coordination may be required when downstream system operators detect problems that could be related to missing PST transmissions. However, this coordination occurs through incident management processes rather than automated alerting systems specifically designed to detect missing files.

This limitation reflects the distributed nature of payment processing where each system monitors its own operations rather than implementing comprehensive cross-system transaction flow monitoring. The absence of missing file alerts means that some failure conditions might only be detected through downstream system reconciliation processes or manual investigation of processing discrepancies.
