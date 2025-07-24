PNC Legacy Online Banking System (WBB) Analysis
Question 1: Where does your application/platform sit in the flow of
payments (what do you receive from an upstream system, if any? What
do you send downstream)?
Answer:
The PNC legacy online banking system (WBB - Web Banking Business) serves as a customer-facing
transaction initiation platform that sits at the front end of PNC's payment processing ecosystem,
functioning primarily as a transaction collection and routing system that does not receive payments
from upstream systems but rather originates payment requests from customer interactions and
routes them to appropriate downstream processing systems.
Absence of Upstream Payment Sources: The WBB system does not receive any payment
transactions from upstream systems. Unlike middleware or processing systems that might
receive payments from other internal systems or external sources, WBB operates exclusively as a
customer origination point where all payment requests begin with direct customer input through
the online banking interface. The system serves as the initial entry point for customer-initiated
payment transactions rather than processing payments that originate from other systems.
Multiple Downstream Processing Channels: The WBB system routes payment transactions to
different downstream systems depending on the payment type and processing requirements.
This multi-channel approach ensures that various payment types are handled by specialized
processing systems optimized for their specific requirements and operational characteristics.
Internal Transfer Processing: For internal transfers between PNC accounts, WBB sends
payment requests to the Transfer Warehouse (TWH) system. This routing enables customers to
move funds between their own PNC accounts or transfer funds to other PNC customers' accounts
through a specialized internal transfer processing engine that handles account-to-account
movements within PNC's banking infrastructure.
External Transfer Processing: For external transfers to accounts at other financial institutions,
WBB routes transactions through CashEdge, which serves as the external transfer processing
platform. This routing enables customers to send funds to accounts at other banks and financial
institutions through CashEdge's network and processing capabilities that connect PNC to external
financial institutions.
Bill Pay Processing Through Fiserv: Bill pay transactions are handled entirely by Fiserv with
WBB serving as the customer interface layer. The system utilizes Fiserv's APIs and hosted pages
directly, meaning that bill pay functionality is controlled entirely on Fiserv's end while WBB
provides the customer access point and integration framework. This approach ensures that
customers can access comprehensive bill pay capabilities while leveraging Fiserv's specialized bill
pay processing expertise.
Limited PPO Integration: While some payment types do flow through PPO (Payment
Processing Operations), these are primarily handled by the lending team and represent
specialized payment scenarios rather than the standard WBB payment processing workflow. The
PPO integration appears to be limited to specific lending-related payment types that require
specialized processing capabilities beyond the standard online banking payment offerings.
Legacy System Positioning: As a legacy system, WBB represents PNC's established online
banking platform that continues to serve customers while WBA (Web Banking Application)
represents the modernized online banking system. Both systems provide online banking
capabilities, but WBA has more comprehensive PPO integration while WBB maintains its
established routing patterns to Transfer Warehouse, CashEdge, and Fiserv for different payment
types.
API-Based Downstream Communication: All downstream communication from WBB occurs
through API-based integrations that enable real-time communication and immediate response
processing. This API approach ensures that payment requests are transmitted immediately to
downstream processing systems and that response information is available immediately for
customer communication and status updates.
Customer-Centric Processing Model: The WBB system operates on a customer-centric
processing model where all payment activity originates from customer interactions through the
online banking interface. This model positions WBB as the primary customer touchpoint for
payment initiation while relying on specialized downstream systems to handle the technical aspects
of payment processing and execution.
Question 2: In what format do you receive transactions/files/information?
Answer:
The PNC legacy online banking system (WBB) operates exclusively through customer-initiated
form-based input rather than receiving structured transaction files or data feeds from external
sources, reflecting its role as a customer-facing transaction origination platform rather than a
system that processes incoming transaction data from other systems.
Form-Based Customer Input Only: The WBB system receives transaction information
exclusively through web-based forms that customers complete when initiating payments
through the online banking interface. Customers enter payment details directly into form fields
including recipient information, payment amounts, account selections, and timing specifications,
and this form-based input represents the only method for transaction data entry into the WBB
system.
Absence of File Upload Capabilities: Unlike some banking systems that support bulk transaction
processing through file uploads, the WBB system does not provide any file upload
functionality for customers. There is no capability for customers to upload CSV files, Excel
spreadsheets, or other structured data files containing multiple transactions for batch
processing. The system is designed exclusively for individual transaction entry through the web
interface forms.
Real-Time Individual Transaction Processing: Each payment transaction is entered and
processed individually through the form-based interface, ensuring that all transaction data
originates from direct customer input rather than from structured data files or automated system
feeds. This individual transaction approach provides immediate validation and processing of each
payment request as customers complete the form submission process.
Customer Account and Profile Integration: While the system does not receive transaction files, it
integrates with customer account and profile information that enables form pre-population
and validation. The system accesses customer ALK (Account Lookup Key) information, which
typically corresponds to the customer's Social Security Number or alternate identification key, to
validate customer identity and account relationships when processing form-based payment
requests.
No Batch Processing Capabilities: The absence of file-based input means that WBB does not
support traditional batch processing where multiple transactions would be submitted
simultaneously through structured data files. Each transaction must be individually initiated and
processed through the customer interface, which provides immediate feedback but requires
separate form completion for each payment request.
Multiple Payee Capability Within Forms: While the system does not accept transaction files, it
does provide enhanced form functionality that enables customers to enter payments to
multiple payees within a single session. Customers can access summary pages that display
multiple payees and enter payment amounts for each individual payee, then submit all
payments simultaneously to Fiserv for bill pay processing. This represents the closest
approximation to batch processing available within the form-based input model.
Recurring Payment Configuration: The form-based input system supports recurring payment
setup where customers can configure payments to occur automatically on specified schedules
(weekly, monthly, or other intervals). While these recurring payments are initially configured
through form input, once established, they process automatically without requiring repeated
customer form completion for each occurrence.
Customer Identification and Authentication Input: In addition to transaction-specific
information, the system receives customer authentication and identification data through the
login process and session management. This includes customer ALK information and related
profile data that enables the system to validate customer identity and account access rights
before allowing payment transaction processing.
Integration with Customer Account Data: While transaction details come exclusively from form
input, the system integrates with existing customer account information to validate account
selections, verify available balances, and confirm account relationships that support the
payment processing workflow. This integration ensures that form-based input is validated
against current account status and customer profile information.
Real-Time Validation of Form Input: The form-based input undergoes immediate validation
as customers complete transaction details, ensuring that invalid or incorrect information is
identified immediately rather than being discovered later during downstream processing. This
real-time validation approach prevents customers from submitting invalid payment requests
and enables immediate correction of input errors.
Question 3: In what format do you send transactions/files/information?
Answer:
The PNC legacy online banking system (WBB) transmits all payment information and transaction
requests through API-based communications that utilize different protocols and systems
depending on the payment type and destination processing system, ensuring reliable and
immediate data transmission throughout the payment processing workflow.
Primary API-Based Communication: Most transaction transmissions occur through API calls
that provide real-time communication between WBB and downstream processing systems. This API
approach ensures that payment requests are transmitted immediately when customers submit
transactions through the online banking interface, enabling immediate response and
confirmation for customer communication and status updates.
Transfer Warehouse Integration: For internal transfer transactions, WBB sends payment
information to the Transfer Warehouse (TWH) system using MQ (Message Queue) services.
While this MQ communication is still fundamentally API-based, it utilizes message queuing
protocols that ensure reliable message delivery and processing confirmation for internal accountto-account transfers within PNC's infrastructure.
CashEdge API Integration: External transfer transactions are transmitted to CashEdge through
API calls that include all necessary information for processing transfers to accounts at other
financial institutions. These API communications contain customer identification, recipient
account details, transfer amounts, and processing timing information required for external
transfer execution and confirmation.
Fiserv API and Hosted Page Integration: Bill pay transactions utilize a dual approach for
communication with Fiserv systems. WBB sends payment information through Fiserv APIs that
include payment details, customer identification, and payee information. Additionally, the system
integrates with Fiserv hosted pages that are displayed within the WBB interface, enabling
customers to interact directly with Fiserv functionality while maintaining seamless integration with
the WBB customer experience.
Customer ALK-Based Identification: All API communications include customer ALK (Account
Lookup Key) information that serves as the primary customer identifier for downstream
processing systems. For most customers, the ALK corresponds to their Social Security Number,
but the system accommodates alternate keys for customers without SSNs or customers who
maintain multiple ALKs for different account relationships or profile configurations.
Subscriber ID Integration with Fiserv: When communicating with Fiserv for bill pay
processing, WBB includes subscriber ID information that corresponds to the customer's ALK,
ensuring that Fiserv can properly identify and process payment requests within their bill pay
system. This subscriber ID serves as the cross-system identifier that enables consistent customer
identification between WBB and Fiserv processing systems.
Payee-Specific Information: For bill pay transactions, the system transmits payee-specific
identification information that enables Fiserv to properly route payments to the correct
recipients. While these payee IDs are interconnected with the customer ALK, they provide
unique identification for each payment recipient that customers have established within their
bill pay profile.
Real-Time Transaction Data: All API communications include comprehensive transaction
details such as payment amounts, account selections (both source and destination), payment
timing specifications (immediate or future-dated), and any special processing instructions
required for successful payment execution. This comprehensive data transmission ensures that
downstream systems receive all information necessary for complete payment processing.
Multiple Payee Processing: When customers initiate payments to multiple payees through the
enhanced form functionality, WBB transmits all payment details simultaneously to Fiserv
through API calls that include complete payment information for each individual payee. This
batch-style API communication enables efficient processing of multi-payee payments while
maintaining the real-time communication model.
Error Handling and Response Processing: The API-based communication model enables
immediate error detection and response processing where downstream systems can return
error information immediately if payment requests cannot be processed successfully. WBB
processes these API responses and communicates appropriate error messages to customers
through the online banking interface.
Recurring Payment Configuration Data: For recurring payment setups, WBB transmits
recurring payment configuration information through APIs that include scheduling details,
payment amounts, payee information, and duration specifications. This configuration data
enables downstream systems to establish automatic recurring payment processing without
requiring repeated API calls for each recurring payment occurrence.
Session and Authentication Data: All API communications include appropriate session and
authentication information that validates the customer's identity and authorization to initiate
payment transactions. This security data ensures that downstream systems can verify that
payment requests originate from properly authenticated customers with appropriate account
access rights.
Question 4: Do you have any unique identifier that you add to the
transactions from your system? Do you pass that to the next system in the
step? Do you create a new one? If so, do you maintain an index?
Answer:
The PNC legacy online banking system (WBB) does not create unique transaction identifiers but
instead relies on customer-based identification systems and transaction context information
to track and manage payment processing, utilizing the customer ALK (Account Lookup Key) as
the primary identification mechanism for all payment-related activities.
Primary Customer Identification - ALK System: The ALK (Account Lookup Key) serves as the
fundamental customer identifier that WBB uses for all transaction processing and downstream
communication. For most customers, the ALK corresponds to their Social Security Number,
providing a consistent and reliable customer identification method that enables transaction
tracking and account relationship management throughout the payment processing workflow.
ALK Variations and Multiple Key Support: The system accommodates customers who do not
have Social Security Numbers by providing alternate key assignments that serve the same
identification function as SSNs while maintaining unique customer identification. Additionally, the
system supports scenarios where individual customers may hold multiple ALKs, enabling
customers to maintain separate profiles or account relationships that require distinct
identification for different banking purposes or account structures.
Absence of Transaction-Specific Unique Identifiers: WBB does not generate unique identifiers
for individual payment transactions that would be passed to downstream processing systems.
Instead, the system relies on the combination of customer ALK and transaction context (such
as amounts, accounts, and timing) to provide sufficient identification for payment tracking and
processing coordination with downstream systems.
Payee-Specific Identification Integration: For bill pay transactions, the system maintains payeespecific identification information that enables unique identification of payment recipients within
each customer's bill pay profile. However, these payee IDs are interconnected with the customer
ALK rather than representing independent transaction identifiers, ensuring that payee identification
remains linked to the customer's overall identification structure.
Subscriber ID for Fiserv Integration: When communicating with Fiserv for bill pay processing,
WBB utilizes subscriber ID information that corresponds directly to the customer's ALK. This
subscriber ID enables Fiserv to maintain consistent customer identification across the
integrated bill pay processing workflow while ensuring that WBB and Fiserv systems can
coordinate customer-specific payment processing activities.
Transaction Context as Identification: Rather than creating unique transaction identifiers, WBB
relies on transaction context information including customer ALK, payment amounts, account
selections, payee information, and processing timing to provide sufficient identification for
payment tracking and coordination. This context-based identification approach enables
downstream systems to properly associate payment requests with customer accounts and
processing requirements.
No Transaction Database or Indexing: The system does not maintain a comprehensive
transaction database or indexing system for payment tracking on the WBB side. Instead, payment
tracking and status management are handled by downstream processing systems that
maintain their own transaction identification and tracking mechanisms once payment requests are
transmitted from WBB.
Real-Time Processing Model Impact: The real-time API-based processing model reduces the
need for complex transaction identification systems within WBB because payment requests are
immediately transmitted to downstream systems and responses are received immediately. This
immediate processing approach eliminates the need for long-term transaction tracking within
the WBB system itself.
Limited Transaction History Storage: While WBB does not create unique transaction
identifiers, the system does maintain limited transaction history information primarily for
Virtual Wallet functionality where check processing information is stored in the WBB database.
This represents the primary exception to the general pattern of not maintaining transactionspecific data within the WBB system.
Downstream System Responsibility: The responsibility for unique transaction identification
lies with downstream processing systems such as Transfer Warehouse, CashEdge, and Fiserv,
which generate their own unique identifiers and maintain comprehensive transaction tracking
capabilities. WBB provides sufficient customer and transaction context to enable these
downstream systems to create and maintain appropriate unique identification structures.
Customer Service and Dispute Support: For customer service and dispute resolution
purposes, the system does maintain confirmation numbers for certain transaction types,
particularly dispute-related transactions. However, these confirmation numbers are generated
for specific dispute processes rather than representing comprehensive unique identification for all
payment transactions processed through WBB.
Cross-System Coordination: The ALK-based identification system enables effective
coordination between WBB and downstream systems by providing consistent customer
identification that downstream systems can utilize for their own transaction tracking and
processing purposes. This approach ensures that customer identity remains consistent
throughout the payment processing workflow while allowing specialized systems to implement
their own unique identification and tracking mechanisms.
Question 5: Do you have any reporting that captures the activity that
takes place at your stop in the lifecycle of a transaction? If so, where is
that hosted? Are there consumers for said report today?
Answer:
The PNC legacy online banking system (WBB) maintains comprehensive activity logging
capabilities that capture detailed information about all customer interactions and transaction
activities, with a systematic reporting process that involves multiple systems and stakeholders for
data collection, processing, and analysis.
Comprehensive Activity Logging System: The WBB system logs all customer activities that
occur within the online banking platform, including login activities, account inquiries, payment
transactions, and all other customer interactions with the banking interface. This logging
approach ensures that complete customer activity information is captured for operational
monitoring, security analysis, and business intelligence purposes.
Transaction-Specific Activity Capture: When customers initiate payment transactions, the
system generates detailed log entries that include transaction details, customer identification,
timing information, and processing status. These transaction logs capture the complete
payment initiation process from customer input through downstream system communication,
providing comprehensive visibility into payment processing activities at the WBB level.
Multi-Level Logging Architecture: The logging system operates through multiple processing
levels that ensure comprehensive data capture and reliable data transmission. Individual log
entries are created for each customer activity and stored locally on WBB servers before being
transmitted through batch processing to centralized data management systems for further
processing and analysis.
Mainframe Data Transmission: All logged activity information is transmitted to mainframe
systems on a regular schedule through automated batch processing jobs. These batch jobs run
every three to four hours on each server, collecting all accumulated log statements and
transmitting them to mainframe storage for centralized data management and processing
coordination.
ADAPT Team Processing and Analysis: The ADAPT team receives logged activity data from the
mainframe systems and processes this information for reporting and analysis purposes. The
ADAPT team transforms raw log data into structured reporting formats and creates analytical
dashboards and reports using tools such as Tableau that enable stakeholders to understand
customer activity patterns and operational performance metrics.
Tableau Dashboard Implementation: The processed activity data is presented through Tableau
dashboards that provide visual analytics and reporting capabilities for business stakeholders
who need to monitor customer activity, transaction volumes, and operational performance.
These dashboards enable comprehensive analysis of online banking activity including payment
processing patterns and customer behavior trends.
Non-Payment-Specific Logging: The logging system captures all online banking activities
rather than focusing exclusively on payments, meaning that login activities, account inquiries,
profile management, and other customer interactions are included in the same logging and
reporting infrastructure. This comprehensive approach provides complete customer activity
visibility but requires filtering and analysis to isolate payment-specific information.
Standardized Log Format Requirements: All logged information follows standardized format
requirements that ensure consistent data structure for downstream processing and analysis.
While there may be slight variations in log formats for different activity types, the system
maintains overall format consistency that enables reliable automated processing by the ADAPT
team and other data consumers.
Stakeholder Report Access: The processed reporting information is available to business
stakeholders who require visibility into online banking activity and performance metrics.
These stakeholders can access Tableau dashboards and other reporting tools to analyze
customer activity patterns, monitor transaction volumes, and evaluate operational
performance across the online banking platform.
Data Retention and Historical Analysis: The logging and reporting system maintains historical
activity data that enables trend analysis and long-term performance monitoring. This historical
data capability supports business planning, operational optimization, and regulatory
compliance requirements that depend on comprehensive activity tracking and reporting.
Operational Monitoring Support: The activity logging and reporting infrastructure supports
operational monitoring requirements by providing real-time and historical visibility into
system performance, customer activity levels, and transaction processing volumes. This monitoring
capability enables proactive identification of operational issues and performance optimization
opportunities.
Limited Payment-Specific Differentiation: While the logging system captures comprehensive
activity information, it does not specifically differentiate payment activities from other types
of customer interactions within the log files themselves. Payment-specific analysis and reporting
require downstream processing and filtering by the ADAPT team or other data consumers who
can identify and analyze payment-related log entries.
Integration with Enterprise Data Management: The logging and reporting system integrates
with PNC's broader enterprise data management infrastructure through the mainframe
transmission and ADAPT team processing. This integration ensures that WBB activity data
contributes to enterprise-wide business intelligence and operational monitoring capabilities.
Contact and Support Structure: For detailed information about specific reporting capabilities
and data access, stakeholders can contact the ADAPT team rather than mainframe personnel, as
the ADAPT team manages the data processing and reporting functions while mainframe
systems provide data storage and transmission infrastructure rather than user-accessible
reporting capabilities.
Question 6: Is your data being streamed (KAFKA stream, etc) anywhere?
For example, a warehouse like COD.
Answer:
The PNC legacy online banking system (WBB) does not implement modern data streaming
technologies such as Kafka streams or real-time data streaming to data warehouses, instead
relying on traditional batch processing methods for data movement and integration with
enterprise data management systems.
Absence of Streaming Technology: The WBB system does not utilize Kafka streaming, realtime data feeds, or other modern streaming technologies for data transmission to data
warehouses or analytics platforms. The system's data architecture reflects its legacy status and
relies on established batch processing approaches that were implemented before streaming
technologies became prevalent in enterprise data management.
Traditional Batch Processing Model: Instead of streaming data, the WBB system utilizes
traditional batch processing jobs that run every three to four hours on each server to collect
accumulated log statements and activity data. This batch processing approach consolidates
multiple customer activities into scheduled data transmission cycles rather than providing realtime data streaming capabilities.
Mainframe-Based Data Architecture: The primary data movement occurs through mainframe
systems that receive batched activity logs from WBB servers on regular intervals. This
mainframe-based architecture represents a traditional enterprise data management approach
that predates modern streaming technologies and focuses on reliable bulk data transmission
rather than real-time streaming capabilities.
Transfer Warehouse Integration: The only data streaming-related technology mentioned in the
discussion is the Transfer Warehouse (TWH) system, which appears to serve internal transfer
processing functions rather than representing a comprehensive data streaming or warehousing
solution. The Transfer Warehouse appears to be focused on transaction processing rather than
data analytics or business intelligence functions.
ADAPT Team Data Processing: The data flow from WBB ultimately reaches the ADAPT team
through the mainframe systems, where data is processed for reporting and analytics purposes.
However, this data movement follows traditional extract, transform, and load (ETL) patterns
rather than modern streaming architectures that would provide real-time data availability for
analytics and reporting.
Limited Data Warehouse Integration: The discussion did not reveal comprehensive integration
with modern data warehouses such as COD (Corporate Online Data warehouse) or other
enterprise data warehousing solutions. The primary data destination appears to be the ADAPT
team's reporting systems rather than comprehensive enterprise data warehouses that would
support advanced analytics and business intelligence.
Legacy System Limitations: As a legacy online banking system, WBB's data architecture
reflects older technology approaches that prioritize reliable transaction processing and basic
reporting rather than advanced data streaming and real-time analytics capabilities. This legacy
architecture may limit integration opportunities with modern data streaming and warehousing
technologies.
Operational Focus Over Analytics: The WBB data management approach appears to prioritize
operational monitoring and basic reporting rather than advanced analytics and business
intelligence that would benefit from streaming data architectures. The batch processing model
supports operational needs but may not provide the real-time data availability required for
advanced analytics and business intelligence applications.
Potential Integration Opportunities: While WBB does not currently implement streaming
technologies, the systematic activity logging and data collection provides a foundation that
could potentially support future integration with streaming technologies and modern data
warehousing solutions if business requirements and technology modernization efforts support such
enhancements.
Enterprise Data Strategy Considerations: The absence of streaming technology in WBB may
reflect broader enterprise data strategy decisions where newer systems like WBA (Web
Banking Application) may implement more modern data streaming and warehousing integration
while legacy systems like WBB continue to utilize established batch processing approaches for
operational stability and cost management.
Need for Technical Clarification: To obtain comprehensive information about enterprise data
streaming and warehousing integration, including potential COD integration or other
streaming technologies, consultation with enterprise data architecture teams or the ADAPT
team would be necessary, as operational WBB teams focus on application functionality rather
than enterprise data management architecture.
Future Modernization Potential: While current WBB architecture does not include streaming
capabilities, the comprehensive activity logging and structured data collection could
potentially support future modernization efforts that might implement streaming technologies or
enhanced data warehouse integration as part of broader technology modernization initiatives.
Question 7: What happens if a file dies at your step in the process?
Answer:
The PNC legacy online banking system (WBB) does not experience traditional "file death"
scenarios because it operates through real-time API-based processing and form-based
customer input rather than batch file processing, with immediate error detection and customer
notification replacing the concept of failed file processing that might occur in batch processing
systems.
Real-Time API Processing Eliminates File Death: Since WBB processes all transactions through
immediate API calls to downstream systems, there are no files that can "die" during
processing. Each customer transaction is processed individually and immediately through API
communications, meaning that processing failures are detected instantly rather than being
discovered later through failed batch file processing.
Immediate Error Detection and Response: When customers submit incorrect transaction
information through the online banking forms, errors are detected immediately and displayed
instantly on the customer's screen. This real-time validation approach means that customers
cannot successfully submit invalid payment requests that would later fail during processing,
eliminating the delayed error discovery that characterizes file-based processing systems.
Customer Interface Error Handling: If customers attempt to submit payments with invalid
information, they receive immediate error messages through the online banking interface that
prevent the transaction from being submitted to downstream processing systems. Customers
can see error notifications immediately and make corrections on the same screen without
needing to wait for batch processing results or error notifications from downstream systems.
API Communication Failure Management: In the rare cases where API communications with
downstream systems fail, the failure is detected immediately during the transaction submission
process. Customers receive immediate notification that their transaction could not be processed,
and they can attempt to resubmit the transaction immediately rather than waiting for delayed
error notification or file reprocessing procedures.
No Batch File Dependencies: Since WBB does not rely on batch file processing, there are no
file transmission schedules, file format requirements, or file processing dependencies that
could create scenarios where files fail to process successfully. All transaction processing occurs
through real-time API communications that provide immediate confirmation or error
notification for each individual transaction.
Instantaneous Customer Feedback: The real-time processing model ensures that customers
receive immediate feedback about the success or failure of their transaction submissions.
Successful transactions receive immediate confirmation, while failed transactions generate
immediate error messages that enable customers to understand and correct issues without
delay.
Validation Before Submission: The WBB interface includes comprehensive validation that
occurs before transactions are submitted to downstream processing systems. This presubmission validation identifies common errors such as insufficient information, invalid
account selections, or format problems and prevents customers from submitting transactions
that would inevitably fail during downstream processing.
Service Availability Error Handling: When downstream processing systems experience
availability issues, customers receive immediate notification that services are unavailable
rather than having transactions fail during processing. This transparent service status
communication enables customers to understand when system issues prevent transaction
processing and retry transactions when services are restored.
No Resubmission Requirements: Since transaction errors are identified immediately,
customers do not need to resubmit failed transactions through separate processes. Instead,
customers can correct errors immediately on the same interface screen and resubmit corrected
transactions instantly without navigating through complex error resolution or resubmission
procedures.
Downstream System Error Communication: When downstream systems encounter processing
issues, error information is communicated immediately back to WBB through API responses,
which WBB immediately displays to customers through appropriate error messages. This realtime error communication eliminates delays between error occurrence and customer notification
that might occur in file-based processing systems.
Risk Team Monitoring for Unusual Activity: While not directly related to file processing errors,
the system does implement risk team monitoring that can identify unusual transaction patterns
and proactively contact customers when suspicious activity is detected. This monitoring capability
represents proactive error prevention rather than reactive error handling after processing failures.
Customer Self-Service Error Resolution: The immediate error detection and correction
capabilities enable customers to resolve transaction issues independently through the online
banking interface without requiring customer service intervention or manual error resolution
processes that might be necessary in systems where file processing failures require administrative
intervention.
System Reliability Through Real-Time Processing: The real-time processing approach provides
higher system reliability and customer satisfaction compared to batch file processing by
eliminating the delays and uncertainties associated with batch processing cycles and providing
immediate confirmation of transaction success or failure that enables customers to manage
their payment processing with confidence.
Question 8: What do you do if you didn't get a file or transaction that you
were expecting to get on a certain day?
Answer:
The PNC legacy online banking system (WBB) does not implement negative tracking or
monitoring for expected transactions because it operates on a customer-initiated transaction
model where all payment processing originates from direct customer input rather than scheduled
file deliveries or predetermined transaction volumes that would require proactive monitoring.
Customer-Initiated Transaction Model: The WBB system operates exclusively on customerinitiated transactions where all payment processing begins with customer input through the
online banking interface. Since customers have complete control over when they initiate
transactions, the concept of "expected" transactions that should arrive on specific days is not
applicable to the WBB operational model.
Absence of Negative Tracking Capabilities: The WBB team explicitly confirmed that they do
not perform negative tracking where the system would monitor for expected transaction
volumes from specific customers or alert when anticipated transactions fail to materialize. The
system does not maintain calendars of expected transaction patterns or implement monitoring
capabilities that would identify when regular customers fail to submit their typical payment
transactions.
No Scheduled Transaction Dependencies: Unlike systems that might depend on scheduled file
deliveries or predetermined transaction volumes, WBB does not rely on external transaction
sources that could create scenarios where expected transactions fail to arrive as scheduled. All
transaction data originates from direct customer interaction with the online banking interface,
eliminating dependencies on external transaction delivery schedules.
Real-Time Processing Eliminates Missing Transaction Scenarios: The real-time API processing
model means that WBB only processes transactions when customers actively initiate them,
and downstream systems only receive transactions when WBB transmits them immediately.
This real-time processing approach eliminates scenarios where downstream systems would be
expecting transactions that fail to arrive, since transaction transmission occurs immediately when
customers submit payment requests.
Customer-Controlled Transaction Timing: Customers have complete autonomy over when
they choose to initiate transactions through the WBB interface. Customers may delay payments,
modify payment schedules, or skip planned transactions based on their individual financial
management preferences, and the system accommodates this customer-controlled approach
without requiring proactive monitoring or customer contact about missing transactions.
Risk Team Monitoring for Unusual Patterns: While WBB does not implement comprehensive
negative tracking, there is some level of risk monitoring that can identify unusual transaction
patterns for security and fraud prevention purposes. Risk team personnel may contact
customers when unusual transaction activity is detected, but this represents security
monitoring rather than missing transaction tracking.
Example of Risk Team Intervention: The discussion included a personal example where risk
team personnel contacted an employee after detecting unusual transaction patterns involving
transfers between personal accounts and subsequent movement to other destinations. This
demonstrates that some level of pattern monitoring exists but focuses on identifying
potentially fraudulent activity rather than tracking missing expected transactions.
No Proactive Customer Outreach for Missing Transactions: The WBB system does not
implement proactive customer outreach when customers fail to submit transactions that might
have been expected based on historical patterns. Customer service interactions occur reactively
when customers contact support with questions or issues rather than proactively when the bank
identifies missing expected transactions.
Downstream System Communication Model: The relationship between WBB and downstream
systems follows a strict request-response model where WBB initiates all communication and
downstream systems respond to specific requests. Downstream systems do not send
proactive notifications to WBB about missing transactions or expected processing volumes,
eliminating the need for WBB to respond to missing transaction alerts from downstream systems.
Operational Simplicity Benefits: The absence of negative tracking and expected transaction
monitoring provides operational simplicity for the WBB system by eliminating the need for
complex pattern recognition, customer communication protocols, and exception handling
processes that would be required if the system attempted to monitor and respond to missing
expected transactions.
Customer Responsibility for Transaction Management: The WBB operational philosophy
assumes that customers are responsible for managing their own payment schedules and will
utilize the online banking system according to their individual needs rather than predetermined
patterns that the bank might monitor. This customer self-service approach provides flexibility
while reducing operational complexity.
Future Monitoring Considerations: While current WBB operations do not include negative
tracking, the comprehensive activity logging system could potentially support future
development of customer pattern analysis if business requirements evolve to include such
capabilities. However, implementing such features would require significant changes to the current
customer-initiated transaction model.
Question 9: Can a client check on the status of their file?
Answer:
PNC legacy online banking system (WBB) customers can check the status of their payment
transactions directly through the online banking interface, with real-time status visibility that
provides immediate information about transaction processing progress and completion status for
all payment types processed through the system.
Real-Time Status Visibility Through Online Interface: Customers can access comprehensive
payment status information directly through their online banking dashboard and transaction
screens. The WBB interface displays current status information for all transactions that
customers have initiated, providing immediate visibility into transaction progress without
requiring customers to contact customer service or wait for separate status notifications.
Transaction Status Categories: The system provides detailed status categorization that enables
customers to understand exactly where their payments stand in the processing workflow. Pending
status is displayed for transactions that have been submitted but are still being processed by
downstream systems. Completed status is shown for transactions that have finished processing
successfully, regardless of the payment type or downstream processing system involved.
Multi-Payment Type Status Support: Status checking capabilities are available for all
payment types processed through WBB, including internal transfers processed through
Transfer Warehouse, external transfers handled by CashEdge, and bill pay transactions
processed by Fiserv. This comprehensive status coverage ensures that customers can track all
their payment activities through a unified interface regardless of the underlying processing
system.
Immediate Status Updates: The real-time API processing model enables immediate status
updates as transactions progress through different processing stages. When customers submit
payment requests, they can see status changes reflected immediately in their online banking
interface as downstream systems process and complete transactions.
Absence of Confirmation Numbers: The WBB system does not typically provide confirmation
numbers for standard payment transactions that customers can use for reference or tracking
purposes. While confirmation numbers are generated for dispute-related transactions, the
standard payment processing workflow relies on status information displayed through the
interface rather than providing unique tracking numbers for each transaction.
Bill Pay Status Integration: For bill pay transactions processed through Fiserv, customers can
view status information directly within the WBB interface even though the actual processing
occurs on Fiserv systems. This integrated status display ensures that customers do not need to
access separate Fiserv interfaces to understand the processing status of their bill pay transactions.
Internal Transfer Status Tracking: Internal transfers processed through Transfer Warehouse
provide status visibility within the WBB interface that enables customers to confirm when
funds have been successfully transferred between their accounts or to other PNC customers'
accounts. This status information helps customers manage their account balances and
transaction timing.
External Transfer Status Coordination: External transfers processed through CashEdge include
status information that is communicated back to WBB and displayed in customer interfaces.
This enables customers to track the progress of transfers to external financial institutions and
understand when transfers have been completed successfully.
Error and Issue Status Communication: When transactions encounter processing issues or
validation errors, customers can see error status information directly through their online
banking interface. This immediate error visibility enables customers to understand what issues
prevent successful processing and take appropriate corrective action when necessary.
Historical Transaction Status Access: Customers can access historical status information for
transactions they have completed in the past, enabling them to review previous payment
activities and confirm completion of earlier transactions. This historical access supports
customer record-keeping and financial management requirements.
Customer Service Integration for Complex Status Inquiries: While basic status information is
available through the online interface, customers can contact customer service
representatives for detailed status inquiries or complex transaction issues that require
additional investigation or explanation beyond what is displayed in the standard interface.
Virtual Wallet Enhanced Status Information: For Virtual Wallet customers, the system provides
enhanced status tracking capabilities particularly for check processing activities where detailed
processing information is maintained in WBB databases. This represents one of the few areas
where WBB maintains comprehensive transaction processing details rather than relying solely
on downstream system status information.
No Separate Status Tracking Systems: Customers do not need to access separate status
tracking systems or portals to monitor their payment processing activities. All status
information is integrated within the standard WBB online banking interface, providing
centralized access to transaction status across all payment types and processing systems.
Limited Unique Identification for Status Tracking: While customers can view transaction status
information, the absence of comprehensive confirmation numbers means that customers
cannot always provide unique identifiers when contacting customer service about specific
transactions. Status inquiries may require customers to provide transaction details such as
amounts, dates, and payee information rather than unique tracking numbers.
Question 10: Do you get a notification if your downstream system doesn't
receive a file from you?
Answer:
The PNC legacy online banking system (WBB) does not receive notifications from downstream
systems about missing files or transactions because the system operates through a real-time
API communication model that eliminates the possibility of downstream systems not receiving
expected files, since all communications occur through immediate request-response cycles rather
than scheduled file deliveries.
Real-Time API Communication Eliminates Missing File Scenarios: Since WBB utilizes real-time
API communications with all downstream processing systems including Transfer Warehouse,
CashEdge, and Fiserv, there are no scheduled file deliveries that could fail to arrive at
downstream systems. Every transaction is transmitted immediately when customers submit
payment requests, and downstream systems receive transactions immediately through API calls
rather than waiting for batch file deliveries.
Immediate Response Model: The API-based communication architecture requires immediate
responses from downstream systems for every transaction request sent by WBB. This
synchronous communication model means that communication failures are detected instantly
during the transaction submission process rather than being discovered later through missing file
notifications or batch processing failure alerts.
No File-Based Processing Dependencies: WBB does not rely on file-based processing that
could create scenarios where downstream systems expect files that fail to arrive. All transaction
processing occurs through individual API calls that are initiated by customer input and
completed through immediate downstream system responses. This eliminates the concept of
missing files that downstream systems might not receive.
Customer-Initiated Processing Model: Since all WBB transaction processing is initiated by
customer input, downstream systems only receive transactions when customers actively
submit them through the online banking interface. Downstream systems do not maintain
schedules of expected transactions from WBB that could create scenarios where missing
transactions would require notification back to WBB.
Immediate Error Detection Through API Responses: When downstream processing systems
encounter issues that prevent successful transaction processing, error information is
communicated immediately back to WBB through API response mechanisms. WBB receives
error responses immediately and displays appropriate error messages to customers without
waiting for separate notification systems or batch processing error reports.
Service Availability Immediate Notification: If downstream systems experience service
availability issues, WBB detects these issues immediately through failed API responses when
attempting to process customer transactions. Customers receive immediate notification that
services are unavailable rather than having transactions fail silently or requiring separate notification
systems to alert WBB about downstream system issues.
Transfer Warehouse Communication: For internal transfers processed through Transfer
Warehouse, the MQ (Message Queue) service communication provides immediate
confirmation of message delivery and processing. Transfer Warehouse receives transaction
requests immediately when WBB transmits them, eliminating scenarios where Transfer Warehouse
might not receive expected transaction files from WBB.
CashEdge API Integration: External transfers to CashEdge occur through immediate API
communications that require immediate responses from CashEdge systems. CashEdge receives
transaction requests immediately when customers submit external transfer requests, and any
communication failures are detected instantly during the transaction submission process.
Fiserv Real-Time Integration: Bill pay transactions processed through Fiserv utilize immediate
API calls and hosted page integration that ensures Fiserv receives transaction information
immediately when customers submit bill pay requests. Fiserv does not wait for scheduled file
deliveries from WBB that could create missing file scenarios requiring notification back to WBB.
Operational Simplicity Through Real-Time Processing: The real-time API processing model
provides operational simplicity by eliminating the need for complex file monitoring, missing
file notification systems, and batch processing error handling that would be necessary if WBB
relied on scheduled file deliveries to downstream systems.
Customer Service Integration for Communication Issues: When communication issues
between WBB and downstream systems do occur, they are typically identified through
customer inquiries rather than through automated notification systems. Customer service
representatives can investigate communication issues when customers report transaction
processing problems, providing human oversight of system integration issues.
Risk Team Monitoring for Pattern Issues: While WBB does not receive automated
notifications about missing files, the risk team monitoring capabilities can identify unusual
patterns that might indicate systematic communication issues with downstream systems. However,
this monitoring focuses on security and fraud prevention rather than missing file notification
from downstream systems.
Legacy System Architecture Implications: As a legacy system, WBB's communication
architecture reflects established integration patterns that prioritize reliable real-time
processing over complex batch processing and notification systems that might be found in more
modern enterprise architectures. This legacy approach provides operational stability while
eliminating the complexity of missing file notification systems.
Future Integration Considerations: While current WBB architecture does not include
downstream notification systems, the real-time API communication model provides a
foundation that could potentially support enhanced monitoring and notification capabilities if
future business requirements or system modernization efforts require such enhancements.
Question 11: Additional Technical Architecture and Processing Details
Answer:
The meeting transcript reveals several important technical and operational characteristics of the
PNC legacy online banking system (WBB) that provide comprehensive understanding of its role
within PNC's broader payment processing ecosystem and its relationship to modernization efforts
within the bank's technology infrastructure.
Legacy System Positioning and Modernization Context: WBB represents PNC's established
legacy online banking system that continues to serve customers while WBA (Web Banking
Application) represents the modernized online banking platform. Both systems provide online
banking capabilities, but WBA has more comprehensive integration with modern processing
systems like PPO while WBB maintains its established routing patterns to Transfer Warehouse,
CashEdge, and Fiserv for different payment types. This dual system architecture reflects PNC's
gradual modernization approach where legacy systems continue to operate while new systems
are developed and deployed.
Customer ALK-Based Identity Management: The ALK (Account Lookup Key) system serves as
the fundamental customer identification mechanism throughout WBB processing. For most
customers, ALK corresponds to Social Security Numbers, but the system accommodates
alternate keys for customers without SSNs and supports multiple ALKs for individual
customers who may maintain separate profiles or complex account relationships. This flexible
identification system enables consistent customer identification across different payment
processing workflows while accommodating diverse customer identification requirements.
Multi-Channel Payment Processing Architecture: WBB implements a sophisticated routing
architecture that directs different payment types to specialized processing systems based on
transaction characteristics and processing requirements. Internal transfers route to Transfer
Warehouse for PNC-to-PNC account movements, external transfers route to CashEdge for
inter-bank transfers, and bill pay transactions route to Fiserv for comprehensive bill payment
processing. This specialized routing approach ensures that each payment type receives
optimal processing through systems designed for specific payment processing requirements.
Real-Time API Integration Across Multiple Systems: The comprehensive API-based
communication model enables real-time integration with multiple downstream processing
systems simultaneously. Transfer Warehouse integration utilizes MQ services for reliable
message delivery, CashEdge integration provides immediate external transfer processing, and
Fiserv integration combines API calls with hosted page functionality for comprehensive bill pay
capabilities. This multi-system API architecture demonstrates sophisticated integration
capabilities despite the legacy system designation.
Comprehensive Activity Logging and Enterprise Data Integration: The systematic activity
logging system captures all customer interactions and transaction activities rather than
focusing exclusively on payment processing. Log entries are generated for login activities,
account inquiries, payment transactions, and all other customer interactions, providing
comprehensive customer behavior data for business intelligence and operational monitoring.
The multi-stage data processing workflow involving server-level log collection, mainframe
data transmission, and ADAPT team analysis demonstrates enterprise-level data management
integration.
Customer-Centric Processing Philosophy: The WBB operational model prioritizes customer
control and self-service capabilities where customers have complete autonomy over
transaction timing and payment management. The absence of negative tracking or proactive
transaction monitoring reflects a customer responsibility approach where customers manage
their own payment schedules without bank intervention or monitoring. This philosophy provides
operational simplicity while maximizing customer flexibility in payment timing and transaction
management.
Form-Based Transaction Processing with Enhanced Capabilities: While WBB exclusively
utilizes form-based customer input rather than file upload capabilities, the system provides
enhanced form functionality that enables multi-payee bill pay processing and recurring
payment configuration. Customers can enter payments to multiple payees within single
sessions and establish recurring payment schedules that process automatically without repeated
form completion. This enhanced form processing provides near-batch processing capabilities
while maintaining the individual transaction processing model.
Risk Management and Security Monitoring Integration: The system includes integrated risk
management capabilities that monitor customer transaction patterns for security and fraud
prevention purposes. Risk team personnel can identify unusual transaction patterns and
proactively contact customers when suspicious activity is detected. This proactive security
monitoring demonstrates sophisticated risk management integration that operates alongside
standard payment processing workflows.
Virtual Wallet Specialized Processing: Virtual Wallet functionality represents a specialized
processing area where WBB maintains enhanced transaction tracking capabilities particularly
for check processing activities. This represents one of the few areas where WBB maintains
comprehensive transaction processing details in local databases rather than relying solely on
downstream system processing and status information.
Cross-System Customer Service Integration: The customer service support model enables
integration between WBB customer interfaces and specialized support teams for complex
transaction issues. Customer service representatives can access transaction details and
coordinate with risk teams, downstream processing systems, and other support resources to
resolve customer inquiries and processing issues that require human intervention.
Operational Monitoring and Performance Management: The comprehensive activity logging
and reporting infrastructure supports operational monitoring and performance management
requirements through detailed customer activity tracking, transaction volume analysis, and
system performance monitoring. The ADAPT team processing and Tableau dashboard
implementation provides visual analytics and reporting capabilities that enable proactive
operational management and performance optimization.
Technology Architecture Flexibility: Despite its legacy system classification, WBB demonstrates
significant technology architecture flexibility through its multi-system API integration,
comprehensive logging capabilities, and customer service coordination. This flexibility
suggests that legacy systems can continue to provide value within modernized technology
ecosystems while new systems are developed and deployed for enhanced capabilities and
modern functionality.
