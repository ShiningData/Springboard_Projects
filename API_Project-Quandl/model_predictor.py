PNC Mobile Banking Payment System Analysis
Question 1: Where does your application/platform sit in the flow of
payments (what do you receive from an upstream system, if any? What
do you send downstream)?
Answer:
The PNC mobile banking payment system serves as an intermediary application layer that sits
between the mobile user interface and PNC's core payment processing operations, functioning as a
critical bridge that enables customers to initiate various types of payments through their mobile
devices while leveraging backend processing capabilities.
Upstream Input Sources: The mobile banking application receives payment requests directly from
the mobile user interface (UI) when customers initiate transactions through their mobile devices.
The system processes customer-initiated transactions that include various payment types such as
ACH payments, credit card payments, wire transfers (both international and domestic), Zelle
transactions, internal transfers, and external transfers. Unlike web banking systems that may
accept bulk file uploads, the mobile platform exclusively handles individual transactions initiated
in real-time by customers through the mobile interface.
When customers use the mobile application to initiate payments, the system receives
comprehensive transaction details from the UI including selected accounts (both from and to
accounts), payment amounts, payment types, timing specifications (whether it's a future
payment or same-day payment), and customer identification information through the user
party ID. The system also receives session information that includes the customer's unique party
ID which serves as a key identifier throughout the payment processing workflow.
Payment Type Diversity: The mobile system handles a comprehensive range of payment types
that flow through the same processing architecture. These include ACH transactions (which fall
under regular external transfers), credit card payments, loan payments, wire transfers for
both international and domestic purposes, Zelle peer-to-peer payments, internal transfers
between PNC accounts, and external transfers to accounts at other financial institutions.
Downstream Processing Architecture: All payment requests received from the mobile UI are sent
downstream to PPO (Payment Processing Operations), which serves as the central payment
processing engine for mobile-initiated transactions. The mobile application does not perform
actual payment processing but rather serves as a collection and validation layer that packages
customer input and forwards it to specialized payment processing systems.
PPO Integration and Responsibilities: When the mobile system sends payment requests to PPO,
it includes all necessary transaction details in a structured format. PPO performs multiple critical
functions including payment eligibility evaluation, account verification, payment type
determination, business rule validation (such as wire limits based on customer profiles), and actual
payment execution. PPO also handles writing payment information to the DSP (Data Streaming
Platform) which serves as the central database for payment tracking and history management.
Payment Eligibility and Validation Workflow: The mobile system implements a multi-step
validation process where it first sends an evaluation call to PPO with the selected accounts to
determine eligible payment types and account combinations. PPO returns information about
which payment types are available for the selected accounts, and the mobile system presents these
options to customers. Once customers make their selections, the mobile system performs a
payment evaluation through PPO to confirm the transaction details, and only after confirmation
does it submit the actual payment through PPO.
Data Flow to DSP Database: After successful payment processing, PPO writes payment details
to the DSP database, which serves as the central repository for payment information that enables
payment history retrieval, status tracking, and customer service support. When customers access
their payment history through the mobile application, the system retrieves information from the
DSP database that has been populated by PPO's payment processing activities.
Real-Time Processing Model: Unlike batch processing systems, the mobile banking payment
architecture operates on a real-time transaction processing model where each customer
interaction triggers immediate API calls to backend processing systems. This enables immediate
validation, confirmation, and processing of payment requests without requiring customers to
wait for batch processing cycles or file transmission windows.
Question 2: In what format do you receive transactions/files/information?
Answer:
The PNC mobile banking payment system operates exclusively through real-time API-based
transaction processing rather than traditional file-based input methods, reflecting the modern
mobile banking approach where customers interact directly through application interfaces rather
than submitting structured data files.
Primary Input Format - JSON API Transactions: The mobile banking system receives all
transaction requests in JSON (JavaScript Object Notation) format through API calls initiated
from the mobile user interface. When customers use their mobile devices to initiate payments,
their input is immediately converted into structured JSON format that includes all necessary
payment parameters such as account selections, payment amounts, payment types, timing
specifications, and customer identification information.
Real-Time UI Integration: The transaction format originates from direct customer input through
the mobile application interface where customers select accounts, enter payment amounts,
choose payment dates, and specify other transaction details. This information is immediately
structured into JSON format and transmitted through secure API calls to the mobile banking
backend systems for processing validation and execution.
Absence of File-Based Processing: Unlike web banking systems that may accept bulk transaction
files or batch uploads, the mobile banking platform does not support file-based transaction
submission. Customers cannot upload spreadsheets, CSV files, or other structured data files
containing multiple transactions. The system is designed exclusively for individual transaction
initiation through the mobile interface, ensuring that each payment request is handled as a
discrete, real-time transaction.
Structured JSON Data Elements: The JSON format received by the mobile system includes
comprehensive transaction data elements necessary for payment processing. These elements
include from account identification, to account identification, payment amounts, payment
type specifications, transaction timing (same-day or future-dated payments), customer party
ID for identification, session information for security validation, and any additional
parameters required for specific payment types such as wire transfer details or international
payment specifications.
Customer Authentication and Session Data: In addition to transaction-specific information, the
mobile system receives authentication and session data that validates customer identity and
authorization to perform payment transactions. This includes user party ID information that
uniquely identifies customers and links their payment requests to their specific account
relationships and authorization profiles.
Payment Type Specific Formatting: Different payment types may require additional data
elements within the JSON structure. For example, wire transfers include specific routing
information, international payment details, and regulatory compliance data, while Zelle
transactions include recipient identification information and peer-to-peer payment
specifications. The JSON format accommodates these varying data requirements while
maintaining consistent structure across all payment types.
Business Rule Validation Input: The mobile system receives business rule parameters that
enable real-time validation of transaction requests. This includes information about customer
profile limitations, account balance verification requirements, daily or monthly payment
limits, and regulatory compliance parameters that must be validated before payment processing
can proceed.
Error Handling and Validation Response: When transaction requests are received in JSON format,
the mobile system immediately validates format compliance, data completeness, and business
rule adherence. Any formatting errors, missing data elements, or business rule violations result in
immediate error responses that are communicated back to customers through the mobile
interface, enabling real-time correction and resubmission.
Integration with Backend Processing: The JSON format received by the mobile system is
designed for seamless integration with downstream processing systems, particularly PPO, which
expects structured data in specific formats for payment evaluation, validation, and execution. The
mobile system ensures that all necessary data elements are properly formatted and included to
support comprehensive payment processing workflows.
Question 3: In what format do you send transactions/files/information?
Answer:
The PNC mobile banking system transmits all payment information and transaction requests in
JSON format through secure API communications to downstream processing systems, maintaining
consistency with modern web service standards and ensuring reliable data transmission throughout
the payment processing workflow.
Primary Output Format - JSON API Communications: All transaction requests and payment
information are sent from the mobile banking system to PPO (Payment Processing Operations)
in JSON format through structured API calls. When customers submit payment requests through
the mobile interface, the system packages all transaction details into comprehensive JSON
payloads that include account information, payment amounts, timing specifications, customer
identification, and payment type details necessary for downstream processing.
Structured API Call Architecture: The mobile system implements multiple types of API calls to
PPO depending on the stage of payment processing. Initial evaluation calls are sent in JSON
format to determine account eligibility and available payment types for customer selections.
Payment evaluation calls are transmitted in JSON format to validate specific transaction details
and confirm processing feasibility. Final payment submission calls are sent in JSON format to
execute approved transactions and initiate actual payment processing.
Comprehensive Transaction Data Transmission: The JSON format used for downstream
transmission includes all necessary data elements collected from customer input and system
validation processes. This includes from account identification, to account identification,
payment amounts, payment type specifications, transaction dates and timing, customer
party ID for identification, session information for security validation, business rule
parameters for compliance verification, and any specialized data required for specific
payment types such as wire transfers or international payments.
PPO Integration Specifications: All JSON transmissions to PPO follow standardized API contract
specifications that ensure consistent data formatting and reliable system integration. The mobile
system formats transaction data according to PPO's expected JSON schema that includes specific
field names, data types, validation requirements, and structural specifications necessary for
successful payment processing.
Payment Type Specific Formatting: Different payment types require specialized JSON
formatting to accommodate varying processing requirements. Wire transfers include additional
routing information, international payment specifications, and regulatory compliance data.
Zelle transactions include peer-to-peer payment identifiers and recipient validation
information. ACH transactions include standard banking routing and account information.
The mobile system customizes JSON payloads based on payment type while maintaining
consistent overall structure.
Real-Time Response Handling: After sending JSON-formatted payment requests to PPO, the
mobile system receives JSON-formatted responses that include processing status, confirmation
numbers, error messages, or additional validation requirements. These responses are immediately
processed by the mobile system and converted into appropriate user interface messages and
status updates for customer communication.
DSP Database Integration: When PPO successfully processes payments, it writes payment
information to the DSP (Data Streaming Platform) database using data originally transmitted
from the mobile system in JSON format. This ensures that payment history and status
information retrieved later by the mobile system maintains consistency with the original
transaction data submitted through JSON API calls.
Error Communication and Validation: When payment submissions encounter validation errors or
processing issues, error information is communicated back to the mobile system in JSON
format through PPO responses. The mobile system processes these JSON error responses and
converts them into user-friendly error messages displayed through the mobile interface, enabling
customers to understand issues and make necessary corrections.
Security and Encryption: All JSON transmissions between the mobile system and downstream
processing systems utilize secure API protocols with encryption to protect sensitive customer
financial information. The JSON format accommodates security headers, authentication tokens,
and encrypted data elements necessary for compliance with financial industry security standards.
Audit Trail and Logging: The mobile system maintains comprehensive logging of all JSON API
communications with downstream systems to support audit trail requirements, troubleshooting
activities, and regulatory compliance verification. These logs capture complete request and
response data while maintaining appropriate security controls for sensitive financial information.
Question 4: Do you have any unique identifier that you add to the
transactions from your system? Do you pass that to the next system in the
step? Do you create a new one? If so, do you maintain an index?
Answer:
The PNC mobile banking system implements a multi-layered unique identification approach
that combines customer-specific identifiers with transaction-specific identifiers to ensure
comprehensive tracking throughout the payment processing lifecycle, with different identifier types
serving different purposes in the payment workflow.
Primary Customer Identification - User Party ID: The mobile system utilizes the user party ID as
the primary customer identifier that uniquely identifies each customer within the mobile banking
system. This identifier is not created by the mobile system itself but rather represents the
customer's unique identification within PNC's broader customer management systems. The user
party ID is passed to all downstream systems including PPO to ensure that payment requests are
properly attributed to the correct customer account relationships.
Transaction Identification Through Combination Approach: Rather than creating a single
unique transaction identifier, the mobile system initially relies on a combination of multiple data
elements to uniquely identify payment requests. This combination includes user party ID, account
selections (both from and to accounts), payment amounts, payment types, and transaction
timing information. This multi-element approach ensures that each payment request can be
uniquely identified even before downstream processing systems assign formal confirmation
numbers.
Downstream Confirmation Number Generation: When payment requests are successfully
processed by PPO (Payment Processing Operations), PPO generates a unique confirmation
number that serves as the definitive transaction identifier throughout the payment lifecycle. This
confirmation number is created by PPO rather than the mobile system and represents the
authoritative unique identifier for each completed payment transaction.
Confirmation Number Management and Storage: The confirmation numbers generated by
PPO are stored in the DSP (Data Streaming Platform) database and are passed back to the
mobile system for customer communication and future reference. These confirmation numbers
serve as the primary tracking mechanism for payment status inquiries, customer service support,
and payment history retrieval. The mobile system maintains access to these confirmation
numbers through its integration with the DSP database but does not create or modify them
independently.
Duplicate Transaction Prevention: The system implements sophisticated duplicate prevention
logic that considers timing elements in addition to basic transaction parameters. Even when
customers submit payments with identical user party IDs, account selections, and payment
amounts, the system incorporates transaction timing information to ensure that each payment
receives a unique confirmation number. For example, if a customer schedules identical weekly
payments, each payment receives a distinct confirmation number based on its specific processing
date and time.
Transaction State Tracking: The mobile system can track payments throughout different
processing states using the confirmation numbers assigned by PPO. Payments in pending states
maintain the same confirmation number as they progress through processing, with status
updates reflected in the DSP database. Whether payments are pending, completed, rejected, or
canceled, they retain the same unique confirmation number for consistent tracking throughout
their lifecycle.
Database Indexing and Retrieval: The DSP database maintains comprehensive indexing of
confirmation numbers and associated transaction details to support rapid retrieval for customer
service inquiries and payment history displays. The mobile system accesses this indexed
information when customers request payment status updates or review their transaction history
through the mobile interface.
Customer Service and Support Integration: The confirmation numbers serve as critical
customer service tools that enable both customers and support representatives to quickly locate
and discuss specific payment transactions. When customers contact support with payment
inquiries, confirmation numbers provide immediate access to complete transaction details,
processing status, and any issues that may require resolution.
Cross-System Integration: The confirmation numbers generated by PPO are recognized and
utilized across multiple PNC systems beyond just the mobile banking platform. This ensures that
payment tracking and customer service capabilities remain consistent whether customers
access information through mobile banking, web banking, customer service channels, or other PNC
interfaces.
Audit Trail and Compliance: The unique identification system supports comprehensive audit
trail requirements by ensuring that every payment transaction can be definitively tracked from
initiation through completion. The combination of user party IDs and PPO-generated confirmation
numbers provides complete accountability for all payment processing activities and supports
regulatory compliance verification.
Future Reference and Historical Access: Once assigned, confirmation numbers remain
permanently associated with their respective payment transactions, enabling long-term historical
tracking and reference. Customers can retrieve payment information months or years later
using confirmation numbers, and the mobile system maintains access to this historical data through
its DSP database integration.
Question 5: Do you have any reporting that captures the activity that
takes place at your stop in the lifecycle of a transaction? If so, where is
that hosted? Are there consumers for said report today?
Answer:
The PNC mobile banking system maintains comprehensive reporting capabilities that capture
detailed transaction activity and payment status information, with multiple reporting mechanisms
serving both customer-facing and operational requirements through integrated database systems
and user interface components.
Primary Reporting System - Payment History: The mobile banking system provides detailed
payment history reporting that displays comprehensive information about all customer payment
transactions processed through the mobile platform. This payment history includes pending
payments, completed payments, canceled payments, and other transaction status categories
that enable customers to track their payment activity comprehensively. The payment history
functionality serves as the primary customer-facing reporting mechanism for transaction
monitoring and status verification.
Payment Status Categorization: The reporting system categorizes payments into distinct status
groups that provide clear visibility into transaction progression. Pending payments are displayed
separately from completed payments, with completed status encompassing various final states
including successfully processed payments, canceled transactions, and rejected payments.
Once payments reach a completed status, customers can no longer modify or interact with
them, providing clear delineation between active and finalized transactions.
DSP Database as Reporting Foundation: All payment history and transaction reporting is
supported by the DSP (Data Streaming Platform) database, which serves as the central
repository for payment information used by the mobile banking system. The DSP database is
hosted on Oracle database technology and maintains comprehensive records of all payment
transactions processed through the mobile platform. This database serves as the authoritative
source for payment status information and transaction history data.
Real-Time Reporting Updates: The reporting system provides real-time status updates through
its integration with PPO and the DSP database. When PPO initially processes payments, it writes
transaction information to the DSP database with initial status indicators. As payments progress
through processing stages, PPO updates the DSP database with current status information,
ensuring that mobile banking reporting reflects the most current payment status available.
Customer Dashboard Integration: The mobile banking system includes a comprehensive
customer dashboard that displays recent payment activity and transaction status information. This
dashboard provides customers with immediate visibility into their payment processing activity
including wire transfers, ACH transactions, and other payment types. The dashboard serves as a
centralized reporting interface that eliminates the need for customers to search through multiple
screens or sections to understand their payment activity.
Activity Tracking and Transaction Monitoring: Beyond basic payment history, the reporting
system captures comprehensive activity data about customer interactions with payment
processing features. This includes transaction initiation attempts, error encounters, successful
submissions, and status changes throughout the payment lifecycle. This activity tracking supports
both customer service needs and operational monitoring requirements.
Kafka Integration for Data Streaming: The DSP database utilizes Kafka topics for data
integration and real-time information streaming. PPO publishes payment information to Kafka
topics that are subsequently mapped to the DSP database, ensuring that reporting data is
updated in near real-time as payment processing activities occur. This Kafka-based architecture
enables efficient data movement and supports scalable reporting capabilities.
Cross-System Reporting Consistency: The mobile banking reporting system maintains
consistency with other PNC banking channels including web banking applications. The same
DSP database and underlying data structures support reporting across multiple customer access
channels, ensuring that customers see consistent payment information regardless of how they
access PNC banking services.
Customer Service Support Integration: The reporting capabilities extend beyond customerfacing interfaces to support customer service representatives and support teams who need
access to detailed payment information for inquiry resolution. The DSP database provides
comprehensive transaction details that enable customer service teams to assist customers with
payment status questions, processing issues, and transaction history inquiries.
Operational Monitoring Capabilities: While specific operational reporting metrics were not
detailed in the discussion, the comprehensive data capture in the DSP database supports
operational monitoring and performance analysis of mobile banking payment processing. This
includes the ability to track transaction volumes, processing success rates, error frequencies,
and other operational metrics necessary for system performance monitoring and improvement.
Database Management and Hosting: The Oracle-based DSP database hosting provides
enterprise-grade reliability and performance for reporting operations. The database infrastructure
supports high-volume transaction logging, rapid data retrieval for customer inquiries, and
comprehensive data retention for historical reporting and compliance requirements.
Integration with Payment Processing Workflow: The reporting system is fully integrated with
the payment processing workflow rather than operating as a separate reporting mechanism. This
integration ensures that all payment processing activities are automatically captured in
reporting data without requiring separate data entry or manual reporting processes that could
introduce errors or omissions.
Question 6: Is your data being streamed (KAFKA stream, etc) anywhere?
For example, a warehouse like COD.
Answer:
The PNC mobile banking system implements comprehensive data streaming capabilities
through Kafka-based architecture that enables real-time data movement and integration with
enterprise data platforms, representing a modern approach to payment transaction data
management and analytics support.
Kafka Topics Integration: The mobile banking system utilizes Kafka topics as a central
component of its data streaming architecture. PPO (Payment Processing Operations) publishes
payment transaction data to Kafka topics that serve as the primary mechanism for real-time data
distribution throughout PNC's technology infrastructure. This Kafka-based approach enables
immediate data availability for downstream systems and analytics platforms rather than relying
on traditional batch processing methods.
DSP Database Data Flow: The DSP (Data Streaming Platform) database receives payment
information through Kafka topics that are mapped directly to database storage structures.
When PPO processes mobile banking payment transactions, it publishes transaction details to
designated Kafka topics, and these topics are automatically processed and stored in the Oraclebased DSP database. This streaming approach ensures that payment status updates and
transaction information are available in near real-time for customer reporting and system
integration purposes.
Real-Time Data Streaming Architecture: Unlike traditional batch processing systems that update
data on scheduled intervals, the mobile banking system's Kafka-based streaming architecture
provides continuous data flow that enables immediate data availability for reporting, customer
service, and operational monitoring. This real-time streaming capability supports the mobile
banking requirement for immediate customer feedback and status updates when payment
transactions are processed.
Enterprise Data Integration: While specific details about COD (Corporate Online Data
warehouse) integration were not extensively covered in the operational discussion, the Kafka
streaming infrastructure provides the foundation for enterprise data warehouse integration. The
Kafka topics that capture mobile banking payment data can be configured for distribution to
multiple downstream systems including data warehouses, analytics platforms, and reporting
systems that require payment transaction information.
Multi-Channel Data Streaming: The DSP database and Kafka integration serves multiple PNC
banking channels beyond just mobile banking, suggesting that the data streaming architecture
supports comprehensive enterprise data requirements. This multi-channel approach ensures that
payment data from mobile banking transactions is available for cross-channel analytics,
customer service support, and enterprise reporting that spans multiple customer interaction
platforms.
Data Streaming Contacts and Expertise: The mobile banking team acknowledged that they are
not experts on the detailed technical aspects of the Kafka streaming implementation and
provided contact information for DSP specialists who can provide comprehensive technical
details about streaming architecture, data warehouse integration, and enterprise data flow
management. This suggests that sophisticated data streaming capabilities exist beyond what is
visible to application development teams.
Operational Versus Technical Architecture: The discussion revealed that while application teams
utilize Kafka streaming capabilities through their integration with PPO and DSP systems, the
detailed technical architecture and data warehouse integration are managed by specialized
data platform teams who have comprehensive expertise in enterprise data streaming and
warehouse management.
Scalable Data Architecture: The Kafka-based streaming approach provides scalable data
architecture that can accommodate high-volume transaction processing typical of mobile banking
operations. This scalability ensures that data streaming capabilities can support growing
transaction volumes and additional data integration requirements as mobile banking usage
continues to expand.
Near Real-Time Data Availability: The Kafka streaming implementation enables near real-time
data availability for customer service, operational monitoring, and analytics purposes. This
immediate data availability supports responsive customer service, real-time operational
monitoring, and current analytics reporting that provides value for both customer service and
business operations.
Enterprise Data Platform Integration: The Kafka topics and DSP database integration
represent components of a broader enterprise data platform that likely includes data warehouse
capabilities, analytics platforms, and business intelligence systems. While specific integration
details require consultation with specialized technical teams, the infrastructure foundation exists
to support comprehensive enterprise data requirements.
Future Data Streaming Capabilities: The modern Kafka-based architecture provides flexibility
for future data streaming enhancements and additional integration requirements. This
foundation enables expansion of data streaming capabilities as business requirements evolve
and additional systems require access to mobile banking payment transaction data.
Technical Expertise and Support: For detailed information about specific data warehouse
integration, COD connectivity, advanced streaming configurations, and enterprise data
platform capabilities, the mobile banking team recommended consultation with DSP technical
specialists who maintain comprehensive expertise in data streaming architecture and enterprise
data management.
Question 7: What happens if a file dies at your step in the process?
Answer:
The PNC mobile banking system handles transaction failures and processing errors through
comprehensive real-time error detection and customer communication mechanisms rather
than traditional file-based failure scenarios, since the system processes individual transactions
initiated directly by customers through the mobile interface rather than batch files.
Individual Transaction Error Handling: Since the mobile banking system processes individual
customer-initiated transactions in real-time rather than batch files, the concept of "file death" is
replaced by individual transaction failure scenarios that can occur at various stages of the
payment processing workflow. When individual transactions encounter processing issues, the
system implements immediate error detection and customer notification to enable rapid issue
resolution and transaction correction.
PPO-Level Rejection and Error Processing: The majority of transaction failures occur at the PPO
(Payment Processing Operations) level when payment requests are submitted for processing
validation and execution. PPO performs comprehensive validation including account verification,
payment limit checking, business rule compliance, and regulatory requirement verification. When
PPO rejects transactions for any reason, it immediately returns error information to the
mobile banking system in structured format that enables appropriate customer communication.
Real-Time Error Communication to Customers: When transaction failures occur, the mobile
banking system immediately communicates error information to customers through the mobile
interface without requiring customers to wait for batch processing results or separate error
notification processes. Error messages are displayed directly in the mobile application with
specific information about the nature of the failure and guidance for correcting issues that prevent
successful payment processing.
Pre-Submission Validation and Inline Error Prevention: The mobile banking system implements
comprehensive pre-submission validation that prevents many potential failures before
transactions are sent to PPO for processing. Inline error checking occurs as customers enter
payment information, including real-time validation of payment amounts against account
limits, verification of account selections, and business rule compliance checking. This proactive
validation prevents customers from submitting transactions that would inevitably fail during
downstream processing.
Service Availability Error Handling: When backend processing systems experience service
outages or availability issues, the mobile banking system immediately notifies customers with
service unavailable messages rather than allowing transactions to fail silently or remain in
uncertain status. This immediate service status communication enables customers to understand
when system issues prevent payment processing and allows them to retry transactions when
services are restored.
Duplicate Payment Detection and Prevention: The system implements sophisticated duplicate
payment detection that identifies when customers attempt to submit identical payment requests
within short timeframes. When duplicate payment scenarios are detected, the system provides
immediate error messages that prevent unintended duplicate transactions while allowing
customers to confirm intentional duplicate payments when appropriate.
Customer Retry and Correction Mechanisms: When transaction failures occur, customers have
immediate ability to retry transactions after addressing the issues that caused initial failures. The
mobile interface maintains customer input data when errors occur, enabling customers to
modify payment details and resubmit transactions without requiring complete re-entry of
payment information. This streamlined retry process minimizes customer frustration and enables
rapid transaction completion once issues are resolved.
Error Status Tracking and History: When transactions fail during processing, the failure
information is captured in the DSP database along with specific error details and timing
information. This error history enables customer service representatives to provide detailed
assistance when customers contact support about failed transactions, and it supports operational
monitoring of error patterns that may indicate systematic issues requiring attention.
Business Rule Validation Error Handling: The system provides specific error messaging for
business rule violations such as exceeding wire transfer limits, attempting payments outside
of allowed timeframes, or violating account-specific restrictions. These detailed error
messages enable customers to understand the specific nature of business rule violations and
make appropriate adjustments to ensure successful payment processing.
Technical Error Recovery and Logging: When technical errors occur during API communications
between the mobile system and PPO, the system implements comprehensive error logging and
recovery mechanisms. These technical errors are logged for operational monitoring while
appropriate user-friendly error messages are displayed to customers to explain service issues
without exposing technical system details.
Account Status Error Handling: When payment failures occur due to account status issues such
as insufficient funds, account closures, or account restrictions, the system provides specific
error messaging that enables customers to understand account-related issues that prevent
successful payment processing. This account-specific error communication enables customers to
take appropriate corrective action through account management or customer service channels.
Integration with Customer Service Support: All transaction failure information is available to
customer service representatives through the DSP database and Partner Care systems, enabling
comprehensive customer support when customers need assistance resolving payment processing
issues. Customer service representatives can access detailed error information and provide
specific guidance for resolving issues that prevent successful payment completion.
Question 8: What do you do if you didn't get a file or transaction that you
were expecting to get on a certain day?
Answer:
The PNC mobile banking system operates on a customer-initiated transaction model rather than
scheduled file delivery or expected transaction volume monitoring, which fundamentally changes
the approach to handling missing or expected transactions compared to batch processing systems.
Customer-Initiated Transaction Model: The mobile banking system does not implement
proactive monitoring for expected transactions or files because all payment processing is
triggered directly by customer interactions through the mobile interface. Unlike systems that
expect scheduled file deliveries or predetermined transaction volumes, the mobile platform
processes transactions only when customers actively initiate them through the mobile
application interface.
Absence of Negative Tracking Capabilities: The mobile banking team explicitly confirmed that
they do not perform negative tracking where the system would monitor for expected transaction
volumes from specific customers or alert when anticipated transactions fail to materialize. The
system does not maintain calendars of expected transaction patterns or implement monitoring
capabilities that would identify when regular customers fail to submit their typical payment
transactions.
No Proactive Customer Outreach: Since the mobile banking system does not track expected
transaction patterns, there are no automated processes for reaching out to customers when
they fail to submit transactions that might have been expected based on historical patterns. The
system operates purely in reactive mode where it processes transactions that customers choose
to submit rather than monitoring for transactions that customers might be expected to submit.
PPO Communication Model: The relationship between the mobile banking system and PPO
(Payment Processing Operations) follows a strict request-response model where mobile
banking always initiates communication and PPO responds to specific requests. PPO does not
send proactive notifications to the mobile banking system about missing files, expected
transactions, or processing issues unless the mobile system specifically requests information.
Customer-Driven Transaction Timing: Since customers have complete control over when they
initiate transactions through the mobile interface, the concept of "missing" transactions is largely
irrelevant to the mobile banking operational model. Customers may choose to delay payments,
cancel planned transactions, or modify payment timing based on their individual financial
management preferences, and the system accommodates this customer-controlled approach.
No Scheduled File Dependencies: Unlike some payment processing systems that depend on
scheduled file deliveries from customers or other systems, the mobile banking platform does
not rely on external file deliveries for transaction processing. All transaction data originates from
direct customer input through the mobile interface, eliminating dependencies on file delivery
schedules that could create scenarios where expected files fail to arrive.
Reactive Customer Service Model: When customers experience issues with payment processing
or have questions about transaction status, they contact customer service directly rather than
being contacted proactively by the bank when expected transactions don't occur. The customer
service model assumes that customers will reach out when they need assistance rather than
implementing proactive monitoring that might identify customers who haven't submitted expected
transactions.
Individual Transaction Focus: The mobile banking system's focus on individual transaction
processing means that each payment request is handled independently without consideration of
patterns or expectations based on previous customer behavior. This transaction-by-transaction
approach eliminates the complexity of managing expected transaction volumes while providing
maximum flexibility for customers to manage their payment timing according to their preferences.
Operational Simplicity Benefits: The absence of negative tracking and expected transaction
monitoring provides operational simplicity for the mobile banking system by eliminating the need
for complex pattern recognition, customer communication protocols, and exception handling
processes that would be required if the system attempted to monitor and respond to missing
expected transactions.
Customer Self-Service Philosophy: The mobile banking platform emphasizes customer selfservice capabilities where customers have comprehensive control over their payment processing
timing and frequency. This philosophy assumes that customers are responsible for managing
their own payment schedules and will utilize the mobile banking system according to their
individual needs rather than predetermined patterns that the bank might monitor.
System Architecture Implications: The request-response architecture between mobile banking
and PPO reflects this customer-initiated approach where all system communications are
triggered by customer actions rather than scheduled processes or expected transaction
monitoring. This architecture provides scalability and simplicity but does not accommodate
proactive monitoring of customer transaction patterns.
Future Monitoring Considerations: While the current mobile banking system does not
implement negative tracking capabilities, the comprehensive data capture in the DSP
database could potentially support future development of customer pattern analysis and
proactive customer engagement if business requirements evolve to include such capabilities.
However, implementing such features would require significant changes to the current customerinitiated transaction model.
Question 9: Can a client check on the status of their file?
Answer:
PNC mobile banking customers have comprehensive access to payment status information
through multiple integrated interfaces and real-time status tracking capabilities that provide
detailed visibility into all aspects of their payment processing activities and transaction histories.
Primary Status Access Through Mobile Dashboard: Customers can check payment status directly
through the mobile banking application dashboard that displays comprehensive information
about all their payment transactions. The dashboard provides real-time status updates for wire
transfers, ACH transactions, credit card payments, loan payments, and other payment types
processed through the mobile platform. This centralized dashboard approach enables customers
to access complete payment information through a single interface without navigating multiple
screens or applications.
Payment Status Categories and Visibility: The mobile banking system provides detailed status
categorization that enables customers to understand exactly where their payments stand in the
processing workflow. Confirmation messages are displayed immediately when payments are
successfully submitted, providing customers with confirmation numbers that serve as unique
identifiers for tracking purposes. Pending status is displayed for payments that have been
submitted but are still being processed in the background, and completed status is shown for
payments that have finished processing, whether successfully or with issues.
Real-Time Status Updates: The system provides immediate status updates as payments progress
through different processing stages. When customers submit payment requests, they receive
immediate confirmation of successful submission along with unique confirmation numbers for
future reference. As payments are processed by PPO (Payment Processing Operations) and
updated in the DSP database, status changes are reflected in real-time in the customer's mobile
banking interface.
Payment History Access: Customers have access to comprehensive payment history that shows
both current and historical transaction information. This payment history includes pending
payments that are still being processed, completed payments with final status information,
and canceled payments that were submitted but subsequently canceled before processing. The
payment history provides complete transaction details including amounts, recipients, processing
dates, and current status for all payment types.
Wire Transfer Activity Monitoring: For customers who utilize wire transfer capabilities, the
mobile banking system provides specialized wire activity dashboards that show recent wire
transfer activity with detailed status information. This includes domestic and international
wire transfers with specific status indicators that help customers understand whether transfers
have been successfully transmitted, are pending processing, or have encountered issues that
require attention.
Error and Issue Notification: When payments encounter processing issues or validation errors,
customers receive immediate notification through the mobile interface with specific error
messages that explain the nature of the problems encountered. These error messages provide
actionable information that enables customers to understand what changes are needed to ensure
successful payment processing, whether the issues relate to account limits, business rule
violations, or technical processing problems.
Confirmation Number Tracking: The unique confirmation numbers generated by PPO for each
payment transaction serve as permanent tracking identifiers that customers can use for future
reference and customer service inquiries. These confirmation numbers are displayed
immediately when payments are successfully submitted and remain permanently associated with
each transaction for long-term tracking and historical reference purposes.
Service Availability Status: When backend processing systems experience service outages or
availability issues, customers receive immediate notification through service unavailable
messages that explain when payment processing capabilities are temporarily interrupted. This
transparent service status communication enables customers to understand when system issues
may affect payment processing and plan accordingly.
Duplicate Payment Alerts: The system provides immediate alerts when duplicate payment
scenarios are detected, enabling customers to confirm intentional duplicate payments or
cancel unintended duplicate submissions. This duplicate detection and notification capability
helps customers avoid accidental duplicate payments while providing flexibility for legitimate
scenarios where duplicate payments may be intended.
Customer Service Integration: When customers need additional assistance with payment
status inquiries, they can contact PNC customer service representatives who have
comprehensive access to payment details through integrated systems. Customer service
representatives can provide detailed explanations of payment status, processing timelines, and
resolution steps for any issues that may require customer action or system intervention.
Cross-Platform Status Consistency: The payment status information displayed through mobile
banking is consistent with other PNC banking channels including web banking and customer
service systems. This consistency ensures that customers receive the same status information
regardless of how they access their account information, providing reliability and confidence in the
payment tracking capabilities.
Historical Transaction Access: Customers can access historical payment information for
extended periods, enabling them to review past payment activity, confirm completion of
previous transactions, and access confirmation numbers for payments that were processed
weeks or months earlier. This long-term access capability supports customer record-keeping and
financial management requirements.
Question 10: Do you get a notification if your downstream system doesn't
receive a file from you?
Answer:
The PNC mobile banking system operates on a strict request-response communication model
with downstream systems that fundamentally eliminates the scenario of downstream systems not
receiving expected files or transactions, since all communications are initiated by the mobile system
and require immediate responses for successful operation.
Request-Response Architecture Eliminates Missing File Scenarios: The mobile banking system
maintains a synchronous request-response communication pattern with PPO (Payment
Processing Operations) where every payment request sent to PPO requires an immediate
response before the mobile system can continue processing. This architecture means that
communication failures are immediately apparent rather than being discovered later through
missing file notifications, since transactions cannot complete without successful PPO responses.
No Proactive Notifications from PPO: PPO does not send proactive notifications to the mobile
banking system about missing files, expected transactions, or processing issues. The
communication relationship is unidirectional from mobile banking to PPO, where mobile
banking always initiates requests and PPO responds to specific requests. PPO will not send
anything to mobile banking unless the mobile system specifically requests information through
API calls.
Immediate Detection of Communication Failures: When the mobile banking system sends
payment requests to PPO, it immediately receives responses that indicate successful receipt and
processing status. If PPO fails to receive requests or cannot process them successfully, this
failure is immediately communicated back to the mobile system through error responses rather
than being discovered later through missing file monitoring or notification systems.
Real-Time Error Handling Replaces Missing File Notifications: Instead of relying on
downstream notification systems for missing files, the mobile banking architecture implements
real-time error detection and handling where communication failures, processing errors, or
system availability issues are immediately identified and communicated to customers through
the mobile interface. This real-time error handling approach provides immediate problem
identification rather than delayed notification of missing transactions.
Customer Impact Drives Issue Detection: When downstream communication or processing issues
occur, they are immediately apparent through customer impact rather than through automated
monitoring systems. If PPO cannot receive or process mobile banking requests, customers
receive immediate error messages through the mobile interface, and customer service
representatives can identify system issues through customer inquiries rather than relying on
automated notification systems.
Synchronous Processing Eliminates File Dependencies: The mobile banking system does not
rely on asynchronous file delivery or batch processing that could create scenarios where
downstream systems expect files that fail to arrive. All payment processing occurs through
synchronous API calls where successful communication and processing are confirmed
immediately during the transaction processing workflow.
Service Availability Monitoring Instead of File Monitoring: Rather than monitoring for missing
files or transactions, the mobile banking system monitors service availability and immediate
response capability from downstream systems. When PPO or other downstream systems
experience availability issues, this is immediately detected through failed API responses rather
than through missing file notifications or delayed processing detection.
Customer Service Integration for Issue Resolution: When communication or processing issues
occur between mobile banking and downstream systems, issue resolution occurs through
customer service channels rather than automated notification systems. Customer service
representatives can identify system issues through customer inquiries and coordinate with
technical teams to resolve communication problems that affect payment processing.
Error Logging for Operational Monitoring: While the mobile banking system does not receive
proactive notifications from downstream systems, it maintains comprehensive error logging of
all API communication attempts and responses. This error logging enables operational teams to
identify patterns of communication failures or processing issues that may indicate systematic
problems requiring technical attention.
DSP Database Integration for Status Tracking: The DSP (Data Streaming Platform) database
integration provides comprehensive status tracking for all payment transactions without relying
on downstream notification systems. When PPO successfully processes payments and updates
the DSP database, this information is immediately available to the mobile banking system for
customer status inquiries and operational monitoring.
Future Monitoring Capabilities: While the current mobile banking system does not implement
automated downstream notification monitoring, the comprehensive API communication
logging and DSP database integration could potentially support future development of
enhanced monitoring capabilities if business requirements evolve to include proactive detection
of systematic communication or processing issues.
Operational Simplicity Benefits: The absence of complex downstream notification systems
provides operational simplicity for the mobile banking platform by eliminating dependencies on
external monitoring systems and focusing on immediate error detection and customer
communication that enables rapid issue resolution and customer service support.
Question 11: Additional Technical Architecture and Processing Details
Answer:
The meeting transcript reveals several important technical and operational characteristics of the
PNC mobile banking payment system that provide comprehensive understanding of the platform's
architecture, integration approach, and service delivery capabilities within PNC's broader payment
processing ecosystem.
Comprehensive Payment Type Support: The mobile banking system handles a diverse range of
payment types that demonstrate its role as a universal payment platform for mobile customers.
These payment types include ACH transactions (categorized as regular external transfers),
credit card payments, loan payments, wire transfers for both international and domestic
purposes, Zelle peer-to-peer payments, internal transfers between PNC accounts, and
external transfers to accounts at other financial institutions. This comprehensive payment type
support positions the mobile platform as a complete payment solution for customer financial
management needs.
PPO as Central Processing Engine: PPO (Payment Processing Operations) serves as the
central payment processing engine for all mobile banking payment transactions, regardless of
payment type. This centralized processing approach ensures consistent business rule
application, uniform security protocols, and standardized processing workflows across all
payment types. PPO performs critical functions including account eligibility evaluation,
payment limit validation, business rule compliance checking, actual payment execution, and
database updates for payment tracking and history management.
Multi-Step Validation and Processing Workflow: The mobile banking system implements a
sophisticated multi-step processing workflow that ensures comprehensive validation before
payment execution. This workflow includes initial account eligibility evaluation through PPO API
calls, payment type determination based on account selections, business rule validation
including wire limits and customer profile restrictions, payment confirmation and final
submission, and real-time status updates throughout the processing lifecycle.
DSP Database as Enterprise Data Platform: The DSP (Data Streaming Platform) database
serves as more than just a payment repository - it functions as an enterprise data platform that
supports multiple PNC banking channels and systems. The DSP database is built on Oracle
technology and maintains comprehensive payment transaction data that supports customer
service, operational monitoring, compliance reporting, and cross-channel customer
experience consistency. This enterprise-level data platform ensures that payment information is
available across multiple customer access points and service channels.
Kafka-Based Real-Time Data Architecture: The implementation of Kafka streaming technology
demonstrates PNC's commitment to modern data architecture that supports real-time data
processing and enterprise integration. PPO publishes payment transaction data to Kafka
topics that enable immediate data distribution to multiple downstream systems including the
DSP database and potentially other enterprise systems requiring payment transaction information.
Customer Profile and Business Rule Integration: The mobile banking system integrates with
comprehensive customer profile systems that enable dynamic business rule application based
on individual customer characteristics. This includes wire transfer limits based on customer
profiles, payment type eligibility based on account relationships, and regulatory compliance
requirements that vary based on customer classification and transaction characteristics.
Cross-Channel Consistency with Web Banking: The mobile banking payment processing
architecture maintains consistency with PNC's web banking application (WBA) with the primary
difference being mobile-specific features like Zelle integration. This consistency ensures that
customers receive similar payment processing capabilities regardless of their chosen access
channel while maintaining operational efficiency through shared backend processing systems.
Real-Time Customer Communication Integration: The mobile banking system implements
sophisticated real-time customer communication that provides immediate feedback for all
customer interactions. This includes instant confirmation messages for successful payment
submissions, real-time error messaging for validation failures, immediate duplicate payment
detection and notification, and service availability status communication when system issues
occur.
Security and Compliance Architecture: While specific security details were not extensively
discussed, the mobile banking system operates within enterprise-grade security frameworks that
support financial industry compliance requirements. The API-based communication with PPO,
encrypted data transmission protocols, comprehensive audit trail maintenance, and
customer authentication integration demonstrate sophisticated security architecture appropriate
for mobile financial services.
Scalable Transaction Processing: The individual transaction processing model combined with
real-time API communications provides highly scalable transaction processing capabilities
that can accommodate high-volume mobile banking usage without the complexity of batch
processing coordination or file delivery scheduling that could create bottlenecks during peak usage
periods.
Customer Service Integration Architecture: The mobile banking system maintains
comprehensive integration with customer service systems that enables seamless customer
support when issues require human intervention. This integration includes access to complete
transaction histories, real-time payment status information, detailed error logging for
troubleshooting, and confirmation number tracking that enables efficient customer service
delivery.
Technical Expertise and Support Structure: The discussion revealed specialized technical
expertise within different areas of the payment processing ecosystem, with mobile banking
teams focused on customer interface and API integration while PPO specialists manage
payment processing logic and DSP experts handle enterprise data platform capabilities. This
specialized expertise structure enables focused technical excellence in each area while
maintaining effective system integration across the complete payment processing workflow.
Future Technology Platform Flexibility: The modern API-based architecture, Kafka streaming
integration, and enterprise database platform provide flexibility for future technology
enhancements and additional payment processing capabilities. This forward-looking
architecture enables expansion of payment types, integration with new financial services, and
enhancement of customer experience features without requiring fundamental changes to the
core processing infrastructure.
