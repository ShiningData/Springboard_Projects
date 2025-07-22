PNC Bill Pay System Analysis
Question 1: Where does your application/platform sit in the flow of
payments (what do you receive from an upstream system, if any? What
do you send downstream)?
Answer:
The PNC bill pay system operates as an intermediary platform that sits between PNC's online
banking customers and Fiserv's payment processing infrastructure, serving as a critical bridge that
enables customers to make payments to merchants through a seamless integrated experience.
From an upstream perspective, the system receives payment requests directly from PNC
subscribers through the online banking interface. When customers access bill pay functionality,
they link over from PNC's main online banking system to the bill pay interface, which triggers
authentication calls to Fiserv to verify user access and determine whether the customer is
classified as a business or consumer user. The system does not receive traditional file-based inputs
from upstream systems, but rather processes real-time API-based payment requests initiated by
customers through the web interface.
The application interface displays comprehensive payment management capabilities including
upcoming invoices, electronic bills (e-bills), pending payments, recurring payment schedules, and
other payment-related information. All of this customer-specific data is maintained through
continuous API communications between PNC and Fiserv systems, with detailed logs of all
payment activities stored locally to populate customer screens when they access the payment
interface.
From a downstream perspective, the system sends payment instructions and processes transactions
through Fiserv as the primary payment processor. Once customers schedule payments or initiate
real-time payments through API calls, the system determines the appropriate payment method and
routes transactions accordingly. Payments can be processed through multiple channels including
ACH electronic payments, electronic check payments, draft check payments, or virtual card
payments (the latter being a new pilot program).
The payment flow architecture follows a structured sequence where PNC subscribers interact
exclusively with PNC's online banking system, which then sends API requests on behalf of
subscribers to Fiserv. Fiserv independently manages all merchant communications and payment
settlements. The flow maintains clear boundaries: subscriber to PNC, PNC to Fiserv, and Fiserv to
merchant, ensuring that direct subscriber-to-Fiserv or subscriber-to-merchant interactions do not
occur.
The system also manages comprehensive payment lifecycle tracking to ensure electronic fund
transfers are completed successfully. This includes receiving trace numbers for all transactions and
maintaining detailed transaction records in the Partner Care system, which provides both PNC
customer service representatives and Fiserv support teams with access to payment details for
customer assistance and issue resolution.
An important operational characteristic is that the system implements different payment models
depending on configuration. The current risk model approach pays merchants first and then
collects funds from subscriber accounts, ensuring merchants receive payments on time without
delays caused by fund verification or collection timing. The system is transitioning toward a realtime good funds model through Check Free Next, which will verify and collect subscriber funds
before sending payments to merchants, eliminating collection risks and providing improved
payment certainty for all parties.
Question 2: In what format do you receive transactions/files/information?
Answer:
The PNC bill pay system primarily operates through real-time API transactions rather than
traditional file-based processing, reflecting the modern digital banking approach where customers
interact directly through web interfaces rather than submitting batch files for processing.
Primary Input Method - API Transactions: The predominant format for receiving transaction
requests is through direct API calls initiated when customers use the PNC online banking interface
to access bill pay functionality. When customers navigate to the bill pay section, the system receives
their requests in real-time API format that includes payment details such as amounts, payment
dates, merchant information, and specific timing requirements for payment delivery.
These API transactions are processed immediately as customers interact with the system, enabling
real-time validation of payment requests including merchant verification, payment date feasibility
checks, and payment method determination (electronic versus draft check processing). The API
format allows the system to provide immediate feedback to customers about payment scheduling
feasibility and automatically adjust payment processing timelines based on payment method
requirements.
Optional File-Based Processing: While API transactions represent the primary input method, the
system does support optional SIS (Subscriber Information System) batch file processing for
certain client configurations. Some customers can set up payments through batch files that are
delivered in the evening, but actual payment processing does not occur until these file deliveries
are received and validated. This batch processing capability represents an alternative setup option
that accommodates different customer operational preferences, though it is not the standard
processing method.
File Delivery Protocols: When file-based processing is utilized, the system employs custom
encrypted file transfer protocols for secure delivery of payment instructions. These files are
transmitted through encrypted file interfaces that establish direct system-to-system dialogue
rather than using portal-based file retrieval methods. The file transfer system uses specific IP
addresses for secure communication and maintains detailed delivery confirmation tracking.
System Integration Formats: The bill pay system receives various types of information through
different format channels depending on the specific function being performed. Electronic bill data
is received directly from merchants in electronic format and loaded into the banking system,
enabling customers to view and pay bills directly through the interface. Authentication and
verification data is exchanged with Fiserv through API calls to confirm customer access rights and
account status.
Customer Input Validation: When customers provide payment instructions through the online
interface, the system receives this information in structured API format that includes all necessary
payment parameters. The system immediately validates this input by sending verification calls to
Fiserv to confirm merchant electronic payment capability, determine appropriate payment
timing requirements, and establish whether payments will be processed electronically or require
draft check generation.
The format structure ensures that all customer payment requests include essential elements such as
payment amounts, merchant identification, requested payment dates, and customer account
information necessary for successful payment processing and fund collection from subscriber
accounts.
Question 3: In what format do you send transactions/files/information?
Answer:
The PNC bill pay system transmits information through multiple formats and channels depending
on the destination system and the type of data being communicated, with different approaches for
operational reporting, payment processing, and system integration communications.
Operational Reporting Files to PNC: The system generates and transmits several structured data
files to PNC on regular schedules to maintain operational oversight and customer service
capabilities. The subscriber activity file is transmitted monthly and contains comprehensive
information about all activities that subscribers perform within the bill pay system, including
payment setups, modifications, cancellations, and account management activities.
The payment history file is sent weekly (Monday through Friday) and contains detailed
information about all payment-related activities, transactions, and status changes. This file provides
PNC with comprehensive visibility into payment processing activities for customer service support,
operational monitoring, and audit trail maintenance.
Specialized File Formats: For specific integration requirements, the system generates CAF
(Customer Account File) or TDF (Transaction Data File) formats that are transmitted daily
Tuesday through Friday. These files serve particular integration needs and maintain specific data
structures required by downstream PNC systems for operational processing and customer account
management.
API Communications with Fiserv: Payment processing communications with Fiserv occur through
structured API calls that contain all necessary payment instruction data including customer
identification, merchant details, payment amounts, processing dates, and payment method
specifications. These API communications enable real-time payment processing coordination and
immediate response confirmation for payment scheduling and execution.
Response and Confirmation Files: The system maintains response files that document all API
calls and responses exchanged between systems, ensuring complete audit trails and enabling
verification that all systems remain synchronized across the payment processing workflow. These
response files confirm successful communication delivery and provide troubleshooting data when
system integration issues occur.
Payment Processing Instructions: When payments are ready for execution, the system sends
payment processing instructions to Fiserv containing all details necessary for merchant payment
delivery. For electronic payments, these instructions include ACH routing information, merchant
electronic payment identifiers, and precise payment amounts and timing requirements.
For draft check payments, the system sends detailed payment information to Fiserv's payment
processing center, which then generates physical checks, places them in envelopes, and manages
postal delivery to merchants. These instructions include complete merchant mailing addresses,
payment amounts, customer account information for fund collection, and specific timing
requirements to ensure delivery before payment due dates.
Collection and Settlement Communications: The system sends fund collection instructions to
facilitate debiting subscriber accounts after merchant payments are completed. Under the current
risk model, these communications occur after merchant payments are made to ensure timely
payment delivery while managing collection timing separately from payment processing.
Customer Service Integration: All payment activity data is formatted and transmitted to the
Partner Care system that PNC customer service representatives and Fiserv support teams access
for customer assistance. This system receives comprehensive payment details in structured formats
that enable rapid customer inquiry resolution and payment status verification.
Secure Transmission Protocols: All file and data transmissions utilize encrypted communication
protocols with specific IP address authentication and secure file transfer mechanisms that ensure
data security and transmission reliability throughout all system integrations and external
communications.
Question 4: Do you have any unique identifier that you add to the
transactions from your system? Do you pass that to the next system in the
step? Do you create a new one? If so, do you maintain an index?
Answer:
The PNC bill pay system implements comprehensive transaction identification and tracking
mechanisms that enable complete payment lifecycle monitoring and cross-system coordination,
though the specific technical details of unique identifier structures were not extensively detailed in
the operational discussion.
Payment Lifecycle Tracking: The system maintains detailed tracking of payment lifecycles to
ensure that electronic fund transfers are completed successfully from initiation through final
settlement. This tracking capability suggests the presence of unique transaction identifiers that
enable monitoring of payment status changes and processing milestones throughout the entire
payment workflow.
Trace Number Management: When payments are processed, the system receives trace numbers
that provide unique identification for each transaction. These trace numbers enable tracking and
verification of payment delivery and facilitate communication with Fiserv regarding specific
payment status inquiries or issue resolution. The trace numbers appear to be generated by
downstream processing systems rather than being created by the bill pay system itself.
Cross-System Integration Identifiers: All payment information and transaction details are
maintained in the Partner Care system, which provides access to both PNC customer service
representatives and Fiserv support teams. This system architecture requires consistent unique
identification mechanisms that enable rapid transaction lookup and customer inquiry resolution
across multiple support platforms.
API Transaction Identification: Since the system operates primarily through API call
communications with Fiserv, each API transaction likely includes unique identifiers that enable
request and response correlation, ensuring that payment instructions and confirmation responses
can be properly matched and tracked throughout the processing workflow.
Payment Method Specific Tracking: The system processes payments through multiple channels
including ACH, electronic check, draft check, and virtual card payments, each of which likely
requires specific identification structures appropriate to the payment method. Different payment
types may utilize different identifier formats or additional tracking elements based on processing
requirements and industry standards.
Collections Process Identification: When payments cannot be collected from subscriber accounts
due to account closures, fraud holds, or other invalid account statuses, the system places
accounts in collection status and maintains tracking of outstanding payment amounts. This
collections management requires unique identification of both the original payment transaction
and the subsequent collection activity.
Response File Documentation: The system maintains response files that document all API calls
and responses between systems, indicating that each communication exchange includes
identification elements that enable verification of successful message delivery and system
synchronization. These response files suggest comprehensive identifier management for audit trail
and troubleshooting purposes.
Customer Service Integration: The availability of complete payment details in the Partner Care
system for customer service purposes indicates that robust unique identification systems enable
rapid access to specific transaction information when customers contact support with payment
inquiries or issues requiring investigation.
System Migration Considerations: With the ongoing transition from the current risk model to the
Check Free Next real-time good funds model, the system likely maintains identifier structures
that support both current operations and migration to new processing capabilities, ensuring
continuity of tracking and customer service capabilities throughout the system modernization
process.
While the operational discussion did not provide extensive technical details about specific unique
identifier formats, naming conventions, or database indexing structures, the comprehensive
payment tracking capabilities and cross-system integration requirements clearly indicate
sophisticated unique identification management that enables reliable payment processing and
customer service support throughout the bill pay ecosystem.
Question 5: Do you have any reporting that captures the activity that
takes place at your stop in the lifecycle of a transaction? If so, where is
that hosted? Are there consumers for said report today?
Answer:
The PNC bill pay system maintains extensive reporting capabilities that comprehensively capture all
transaction activity and customer interactions occurring within the bill pay platform, with multiple
reporting systems serving different operational and customer service requirements.
Partner Care System: The primary reporting and customer service platform is the Partner Care
system, which houses comprehensive information about all payment activities and customer
interactions. This system provides detailed access to PNC customer service representatives and
Fiserv customer service representatives, enabling both organizations to assist customers with
payment inquiries, troubleshooting, and issue resolution. The Partner Care system maintains
complete visibility into customer payment profiles, transaction histories, and account status
information necessary for effective customer support operations.
Subscriber Activity File Reporting: The system generates monthly subscriber activity files that
capture comprehensive information about all activities that customers perform within the bill pay
system. These reports document payment setups, payment modifications, payment cancellations,
recurring payment configurations, account management activities, and all other customer
interactions with the bill pay platform. This monthly reporting provides PNC with detailed
operational oversight and enables analysis of customer usage patterns and system utilization
trends.
Payment History File Reporting: Weekly payment history files are generated Monday through
Friday that contain detailed information about all payment-related transactions and activities. These
reports provide comprehensive documentation of payment processing activities, status changes,
successful completions, and any issues or exceptions that occur during payment processing. The
payment history reporting enables operational monitoring, audit trail maintenance, and detailed
analysis of payment processing performance and reliability.
Daily Operational Files: The system produces daily CAF (Customer Account File) or TDF
(Transaction Data File) reports that are transmitted Tuesday through Friday. These specialized
reports serve specific operational integration needs and provide structured data about customer
account activities and transaction processing that support downstream PNC systems and
operational processes.
Response File Documentation: The system maintains comprehensive response files that
document all API calls and responses exchanged between the bill pay system and Fiserv processing
systems. These response files provide detailed audit trails of all system communications, enable
verification that systems remain properly synchronized, and support troubleshooting activities when
system integration issues occur. These files capture the complete dialogue between systems and
ensure accountability for all transaction processing communications.
Collections Activity Reporting: When accounts are placed in collection status due to inability to
collect funds from subscriber accounts, the system maintains detailed reporting about collection
activities, outstanding amounts, and resolution status. This collections reporting enables
management of accounts that cannot complete the payment collection process and tracks
resolution of outstanding payment obligations.
Electronic Bill Integration Reporting: The system captures comprehensive information about
electronic bill delivery and processing, including bills received from merchants, bills presented to
customers, and customer payment responses to electronic bill presentations. This reporting
provides visibility into the complete electronic bill presentment and payment cycle.
Customer Service Access and Usage: Both PNC customer service representatives and Fiserv
support teams actively use these reporting systems to provide customer assistance. When
customers contact support with payment inquiries, representatives can access comprehensive
payment details, transaction histories, and account status information through the Partner Care
system. This enables rapid issue resolution and detailed explanation of payment processing status
to customers.
System Performance and Operational Monitoring: The various reporting systems provide
operations teams with detailed visibility into system performance, transaction processing
volumes, success rates, and exception handling activities. This operational reporting enables
proactive system management and rapid identification of processing issues that may require
attention or system adjustments.
Report Hosting and Accessibility: The reporting systems are hosted within the Fiserv
infrastructure as part of the bill pay service platform, with appropriate access provided to PNC
personnel who require visibility into customer activities and payment processing for operational
and customer service purposes. The hosting arrangement ensures that reporting capabilities are
maintained and updated as part of the overall bill pay service delivery.
Regulatory and Compliance Reporting: The comprehensive transaction documentation and
reporting capabilities support regulatory compliance and audit requirements by maintaining
detailed records of all customer activities, payment processing, and system interactions throughout
the payment lifecycle.
Question 6: Is your data being streamed (KAFKA stream, etc) anywhere?
For example, a warehouse like COD.
Answer:
The meeting transcript does not contain any specific information about data streaming
technologies such as Kafka streams or data warehouse integration such as COD (Corporate Online
Data warehouse). The discussion focused primarily on the operational aspects of the bill pay
system, payment processing workflows, and file-based reporting mechanisms rather than modern
streaming data architectures.
Current Data Architecture Characteristics: Based on the information provided, the bill pay system
appears to operate through traditional API-based communications and scheduled file transfers
rather than real-time streaming technologies. The system generates weekly payment history files,
monthly subscriber activity files, and daily specialized reports that follow batch processing
patterns typical of traditional data integration approaches rather than continuous streaming
models.
File-Based Data Movement: The system implements structured file delivery schedules for
operational reporting, with payment history files transmitted weekly Monday through Friday,
subscriber activity files sent monthly, and specialized CAF/TDF files delivered daily Tuesday through
Friday. This scheduled file-based approach suggests that data movement follows traditional batch
processing patterns rather than real-time streaming architectures.
API Communication Model: The primary system interactions occur through API calls between
PNC online banking, the bill pay system, and Fiserv processing systems. These API
communications appear to follow request-response patterns for payment processing and customer
authentication rather than continuous data streaming for analytics or data warehouse population.
Response File Documentation: The system maintains response files that document API calls
and responses between systems, indicating a transaction-based communication model that
focuses on payment processing completion and system synchronization verification rather than
continuous data streaming for analytical purposes.
Integration with Partner Care System: The comprehensive customer service integration through
the Partner Care system suggests that operational data is maintained within the bill pay service
platform rather than being streamed to external data warehouses or analytics platforms for
additional processing.
Need for Technical Clarification: The operational nature of the discussion means that technical
architecture details about data streaming, warehouse integration, or modern analytics
infrastructure were not covered in the meeting. To obtain definitive information about streaming
technologies, data warehouse integration, or COD connectivity, additional consultation with
application development teams or technical architecture specialists would be necessary.
Potential for Modern Data Architecture: While the current discussion suggests traditional filebased and API-based data movement, the ongoing migration to Check Free Next and
modernization of payment processing capabilities may include implementation of streaming
technologies or enhanced data integration capabilities that were not detailed in the operational
overview provided.
Recommendation for Follow-Up: Given the importance of understanding data streaming and
warehouse integration capabilities for comprehensive system analysis, follow-up discussions with
technical teams would be valuable to obtain specific information about Kafka implementation,
COD integration, real-time data streaming capabilities, or other modern data architecture
components that may be part of the bill pay system infrastructure.
Question 7: What happens if a file dies at your step in the process?
Answer:
The PNC bill pay system implements comprehensive error handling and recovery mechanisms that
address various types of processing failures, with different approaches depending on the payment
method and the specific point of failure in the payment lifecycle.
Payment Collection Failures: The most significant failure scenario occurs when the system cannot
collect funds from subscriber accounts after merchant payments have already been made under
the current risk model approach. When subscriber accounts are closed, frozen for fraud, or have
other invalid statuses, the system cannot complete the fund collection process, which triggers
automatic placement of accounts into collection status.
This collections process is managed entirely within Fiserv's internal collection system and is not
reported externally to credit agencies or other financial reporting systems. The collection status
prevents customers from using bill pay services through PNC until outstanding payment amounts
are resolved. Fiserv maintains dedicated collection representatives and systems to contact
customers and facilitate settlement of outstanding payment obligations.
Cross-Institution Collection Enforcement: When customers attempt to access bill pay services
through any other financial institution while having unresolved collection amounts with Fiserv,
the system will automatically block access across all participating institutions. This comprehensive
blocking mechanism ensures that collection issues are resolved before customers can resume bill
pay services regardless of which bank they attempt to use for access.
Account Reactivation Process: Once customers contact Fiserv collections and settle outstanding
payment amounts, their bill pay profile is immediately reactivated and they regain full access to
bill pay services through PNC. If customers never resolve the outstanding amounts, they remain
permanently blocked from bill pay services through PNC and other participating financial
institutions.
Draft Check Payment Failure Handling: For draft check payments, failure scenarios are
managed differently because funds are withdrawn directly from subscriber accounts rather than
following the pay-first-collect-later model used for electronic payments. When draft check
payments fail due to insufficient funds or account issues, customers experience immediate
account debiting consequences without the intermediary collection process, since there is no risk
exposure for Fiserv in the draft check payment model.
Electronic Payment Processing Failures: When API calls or electronic payment processing
encounters technical failures, the system maintains comprehensive response file documentation
that tracks all communication exchanges between systems. This documentation enables rapid
identification of communication failures and supports troubleshooting activities to resolve
processing interruptions.
Customer Service Integration for Failure Resolution: When payments fail or encounter
processing issues, customers can contact PNC customer service representatives who have access
to comprehensive payment details through the Partner Care system. Customer service
representatives can contact Fiserv partner assist lines to collaborate on issue resolution, but
Fiserv representatives cannot work directly with customers independently - all customer-facing
interactions must be coordinated through PNC customer service.
Multi-Tier Support Structure: The system implements multiple tiers of customer support for
failure resolution. Tier two support (PNC's operational model) handles all customer-facing
interactions, while tier one and tier 1.5 support (phone and email direct customer interaction) are
not active for PNC customers. This ensures that failure resolution maintains proper channel
management while providing comprehensive support capabilities.
Automated System Communications: When processing failures occur, the system continues to
provide automated confirmation messages to customers, such as enrollment confirmations or
payment processing notifications, but does not engage in direct customer service communications
from Fiserv representatives unless customers are working through collections processes for
unresolved payment obligations.
Migration to Good Funds Model Benefits: The planned transition to Check Free Next real-time
good funds model will significantly reduce failure scenarios by verifying and collecting funds
before sending payments to merchants. This approach eliminates collection risks and provides
greater payment certainty by ensuring funds are available before payment processing begins,
reducing the complexity of failure handling and recovery processes.
Stop Payment Considerations: Customers must understand the implications of stop payment
requests on different payment types. For electronic payments processed under the risk model, stop
payments trigger collection status because merchants have already been paid. For draft check
payments, stop payments can be processed normally since funds come directly from customer
accounts without intermediate risk exposure.
Question 8: What do you do if you didn't get a file or transaction that you
were expecting to get on a certain day?
Answer:
The meeting transcript does not provide specific information about proactive monitoring or
negative tracking capabilities for expected files or transactions that fail to arrive as scheduled. The
discussion focused primarily on payment processing workflows and customer-initiated transaction
handling rather than systematic monitoring of expected transaction volumes or file deliveries.
File Delivery Dependencies: The system does implement file delivery requirements for certain
processing scenarios, particularly for customers who utilize SIS batch file processing as an
optional setup. In these cases, the system does not process any payments until file deliveries are
received in the evening, indicating that there are dependencies on expected file arrivals for certain
customer configurations.
Optional File Processing Model: Since SIS batch file processing represents an optional setup
rather than the standard processing method, the system appears to accommodate multiple
processing approaches for different customer needs. When customers are configured for filebased processing, the system presumably has mechanisms to handle scenarios where expected files
do not arrive as scheduled, though specific procedures were not detailed in the discussion.
Lack of Comprehensive Volume Monitoring: Unlike systems that maintain detailed calendars of
expected transaction volumes or implement sophisticated negative tracking capabilities, the bill pay
system discussion suggests a primarily reactive approach to processing issues. The system
appears to focus on processing transactions that are actually received rather than proactively
monitoring for transactions or files that should have been received but are missing.
Customer Service Response Model: When processing issues occur, the Partner Care system
provides customer service representatives with access to comprehensive payment details and
transaction histories. This suggests that missing transaction detection may rely primarily on
customer inquiries rather than proactive system monitoring that would identify missing files or
transactions before customers become aware of issues.
Multi-Configuration Complexity: With the acknowledgment that "if we have a thousand
different clients, we'll probably have about six different setups," the system accommodates
significant variation in customer processing requirements. This complexity suggests that expected
transaction patterns may vary significantly between customers, making systematic negative
tracking challenging without detailed customer-specific configuration management.
Technical Team Oversight Requirements: The discussion emphasized that detailed technical
aspects of file processing, system interfaces, and specific setup configurations require consultation
with application development teams for comprehensive understanding. This suggests that
missing file monitoring procedures, if they exist, would be managed at the technical system level
rather than the operational oversight level.
API-Based Transaction Model: Since the primary transaction processing method utilizes real-time
API calls rather than scheduled file deliveries, the concept of "missing transactions" may be less
applicable to the standard customer experience. Customers initiate payments through the online
interface on demand rather than following predictable batch submission schedules that could be
monitored for missing activity.
Response File Synchronization: The system maintains response files that verify API calls and
responses between systems to ensure proper synchronization. This capability suggests that the
system can identify communication failures or incomplete transaction exchanges, though this
appears to focus on technical communication verification rather than business-level transaction
volume monitoring.
Collections Process Monitoring: The system does implement comprehensive monitoring of
collection activities when payments cannot be completed due to account issues or fund collection
failures. This suggests that the system has capabilities to track expected activities and outcomes,
though this monitoring appears to focus on exception handling rather than routine transaction
volume verification.
Need for Technical Specification: To obtain detailed information about missing file handling
procedures, expected transaction monitoring, or negative tracking capabilities, additional
consultation with technical teams would be necessary. The operational overview provided indicates
that such capabilities, if they exist, would be managed through technical system configurations
rather than operational oversight processes.
Future System Capabilities: The planned migration to Check Free Next may include enhanced
monitoring and tracking capabilities that address missing transaction scenarios, though specific
details about these capabilities were not discussed in the operational overview.
Question 9: Can a client check on the status of their file?
Answer:
Customers have comprehensive visibility into their payment status and transaction activities
through multiple access channels and integrated customer service systems that provide real-time
information and detailed transaction histories.
Primary Customer Interface Access: Customers can check payment status directly through the
PNC online banking interface when they access the bill pay functionality. The system displays
comprehensive payment information including upcoming invoices, electronic bills (e-bills),
pending payments, and recurring payment schedules all within the bill pay profile that
customers see when they log into the system.
Real-Time Payment Status Visibility: When customers access the bill pay interface, they can view
detailed status information for all their payment activities, including payments that have been
scheduled, payments that are currently being processed, and payments that have been completed
successfully. The system provides real-time updates about payment progress and delivery
confirmation when merchants receive payments.
Payment Tracking and Confirmation: The system maintains comprehensive tracking of
payment lifecycles and provides customers with trace numbers and delivery confirmation when
electronic fund transfers are completed successfully. Customers can see confirmation that
"payments were successfully delivered to merchants" through the online interface, providing
assurance that their payment obligations have been fulfilled.
Electronic Bill Integration: For customers who utilize electronic bill presentment services, the
system provides integrated visibility into both bill receipt and payment status. Customers can view
electronic bills that have been received from merchants, track payments made in response to those
bills, and see complete payment histories for all their electronic bill relationships.
Customer Service Support Access: When customers need assistance with payment status
inquiries or have questions about transaction details, they can contact PNC customer service
representatives who have comprehensive access to payment information through the Partner
Care system. Customer service representatives can view detailed payment histories, transaction
status, and account information necessary to provide complete assistance with customer inquiries.
Multi-Tier Customer Service Integration: The system implements tier two customer service
support through PNC, meaning that all customer-facing interactions are handled by PNC
representatives rather than direct communication with Fiserv. When complex issues require
additional technical assistance, PNC customer service representatives can contact Fiserv
partner assist lines to collaborate on issue resolution while maintaining proper channel
management for customer communications.
Collections Status Transparency: When accounts are placed in collection status due to payment
collection issues, customers receive clear notification of their account status and the steps required
to resolve outstanding payment obligations. The Fiserv collection system provides dedicated
representatives who can work with customers to settle outstanding amounts and reactivate their
bill pay access.
Payment Method Specific Status Information: The system provides different types of status
information depending on payment method. For electronic payments, customers can see
immediate processing confirmation and merchant delivery verification. For draft check payments,
customers can track payment processing through check generation, mailing, and delivery phases to
ensure payments reach merchants before due dates.
Automatic Communication Systems: While customers cannot receive direct email
communications from Fiserv representatives for routine inquiries, they do receive automated
system notifications such as enrollment confirmations and payment processing confirmations that
provide status updates without requiring customer service intervention.
Stop Payment Visibility: Customers can see the status of stop payment requests and
understand the implications for different payment types. The system clearly indicates when stop
payments on electronic payments may result in collection status, helping customers make informed
decisions about payment modifications.
Recurring Payment Management: For customers who utilize recurring payment setups, the
system provides comprehensive visibility into recurring payment schedules, upcoming payment
dates, and the ability to modify or cancel recurring arrangements as needed. This recurring
payment transparency helps customers manage their ongoing payment obligations effectively.
Issue Resolution Tracking: When customers contact support for payment issues or transaction
problems, the Partner Care system enables customer service representatives to provide detailed
explanations of payment status, processing timelines, and any actions required for successful
payment completion. This comprehensive customer service access ensures that customers receive
complete information about their payment activities and can resolve issues efficiently.
Question 10: Do you get a notification if your downstream system doesn't
receive a file from you?
Answer:
The meeting transcript does not provide specific information about automated notification systems
that would alert the bill pay system when downstream systems fail to receive expected files or
communications. The discussion focused primarily on payment processing workflows and customer
service procedures rather than technical monitoring of downstream system communication failures.
Response File Documentation: The system maintains comprehensive response files that
document all API calls and responses exchanged between systems, which suggests some level of
communication verification capability. These response files are designed to verify that systems
remain synchronized and provide troubleshooting support when system integration issues occur,
indicating that there may be mechanisms to detect communication failures.
Downstream Communication Architecture: The payment processing workflow follows a clear
structure where API calls are sent to Fiserv for payment processing, merchant verification, and
transaction completion. The system appears to track successful payment delivery and maintains
trace numbers for all transactions, suggesting that successful downstream communications are
monitored and confirmed.
Customer Service Integration for Issue Detection: When downstream communication issues
occur, they are likely identified through customer service channels rather than automated system
notifications. The Partner Care system provides comprehensive access to payment details for both
PNC customer service representatives and Fiserv support teams, enabling collaborative
troubleshooting when downstream processing issues affect customer transactions.
Manual Issue Resolution Process: The discussion indicates that when problems arise with
payment processing or downstream system communications, resolution typically involves manual
coordination between PNC customer service and Fiserv partner assist lines. This suggests that
downstream communication failures may be detected through customer inquiries or routine
system monitoring rather than automatic notification systems.
API Communication Verification: Since the system operates primarily through API-based
communications with Fiserv, each API transaction likely includes confirmation responses that
verify successful receipt and processing of payment instructions. The maintenance of response files
documenting API calls and responses suggests that failed communications can be identified
through analysis of communication logs and response verification.
Collections Process Exception Handling: When payments cannot be collected from subscriber
accounts due to account issues, the system automatically places accounts in collection status
and manages exception handling through established procedures. This automatic exception
detection suggests that the system has mechanisms to identify when expected downstream
processes (fund collection) do not complete successfully.
Technical Team Oversight Requirements: The discussion emphasized that detailed technical
aspects of system communications and integration monitoring require consultation with
application development teams for comprehensive understanding. This suggests that automated
notification systems for downstream communication failures, if they exist, would be managed at the
technical system level rather than operational oversight.
System Synchronization Monitoring: The response file documentation system that tracks all
API communications appears designed to ensure that systems remain properly synchronized
throughout the payment processing workflow. This synchronization monitoring may include
capabilities to detect when downstream systems do not respond appropriately to communication
attempts.
Customer Impact Detection: Rather than proactive downstream monitoring, the system appears
to rely on customer impact detection where downstream communication failures become
apparent when customers contact support about payment issues or when routine payment
processing does not complete as expected.
Integration with Multiple Payment Methods: The system processes payments through multiple
downstream channels including ACH, electronic check, draft check, and virtual card
processing, each of which may have different communication verification and failure detection
requirements. The complexity of managing multiple downstream processing paths suggests that
comprehensive notification systems would be necessary to effectively monitor all potential
communication failure points.
Need for Technical Specification: To obtain specific information about automated downstream
notification systems, communication failure detection, or system monitoring capabilities,
additional consultation with technical teams and application developers would be necessary. The
operational overview indicates that such technical monitoring capabilities, if they exist, operate at
system levels not covered in the operational discussion.
Potential Migration Benefits: The ongoing transition to Check Free Next may include enhanced
downstream monitoring and notification capabilities, though specific technical improvements in
communication monitoring were not detailed in the operational overview provided.
Question 11: Additional Technical Architecture and Processing Details
Answer:
The meeting transcript reveals several important technical and operational characteristics of the
PNC bill pay system that provide insight into the platform's architecture, business model transitions,
and service delivery approach.
Risk Model vs. Good Funds Model Architecture: The system currently operates under a risk
model approach where Fiserv pays merchants first and then collects funds from subscriber
accounts afterward. This approach ensures that merchants receive payments on time without
delays caused by fund verification or collection timing complications, but creates potential
collection risks when subscriber accounts cannot be debited successfully.
The system is transitioning to a real-time good funds model through Check Free Next that will
verify and collect subscriber funds before sending payments to merchants. This new model
eliminates collection risks by ensuring funds are confirmed and collected before payment
processing begins, providing greater payment certainty for all parties and removing the need for
complex collections processes.
Multiple Payment Processing Channels: The system supports diverse payment methods
including ACH electronic payments, electronic check payments, draft check payments, and
virtual card payments (the latter being a new pilot program). Each payment method requires
different processing timelines and customer notification requirements, with draft checks requiring
at least five days advance notice to ensure adequate postal delivery time before payment due
dates.
Authentication and User Classification System: The system implements comprehensive user
authentication through API calls to Fiserv that verify customer access rights and determine
business or consumer classification. This classification affects available features and processing
procedures, with different requirements for business and consumer users throughout the payment
processing workflow.
Electronic Bill Presentment Integration: The system provides comprehensive electronic bill
integration where electronic bills are received directly from merchants and loaded into the
banking system. Customers can view these electronic bills through the online interface and make
payments directly, creating a seamless bill presentment and payment experience that eliminates the
need for separate bill management processes.
Customer Service Tier Structure: The system implements a specific tier two customer service
model where PNC handles all customer-facing interactions while Fiserv provides backend
support through partner assist lines when needed. Tier one and tier 1.5 support (direct phone
and email customer interaction) are not active for PNC customers, ensuring that customer service
maintains proper channel management and relationship boundaries.
Collections Management System: The Fiserv collections system operates independently from
external credit reporting and maintains internal collection status management for accounts that
cannot complete payment collection processes. This internal collections approach provides
dedicated collection representatives and systems for issue resolution while maintaining
customer privacy and avoiding external credit impact for payment processing issues.
Cross-Institution Access Control: The system implements comprehensive access blocking
across all participating financial institutions when customers have unresolved collection
amounts with Fiserv. This cross-institution blocking ensures that collection issues must be resolved
before customers can access bill pay services through any participating bank, providing strong
incentive for issue resolution.
File Processing Flexibility: The system accommodates multiple customer configuration
approaches with acknowledgment that "if we have a thousand different clients, we'll probably
have about six different setups." This flexibility includes optional SIS batch file processing for
customers who prefer file-based payment submission rather than real-time API transactions.
Secure Communication Infrastructure: File deliveries utilize custom encrypted file transfer
protocols with specific IP address authentication and direct system-to-system communication
rather than portal-based file access. This security approach ensures comprehensive data
protection for all file-based communications and maintains high security standards for customer
payment information.
Payment Timing and Validation Logic: The system implements sophisticated payment timing
validation that considers payment method requirements, merchant electronic payment
capabilities, postal delivery timing for draft checks, and holiday/weekend complications. This
validation logic ensures that payments are scheduled appropriately to meet due date requirements
regardless of payment method or external timing factors.
Real-Time Payment Processing Capabilities: The transition to Check Free Next includes realtime payment processing through the Now gateway (the same gateway used by EWS - Early
Warning Services), enabling immediate fund verification, collection, and merchant payment
delivery. This real-time capability provides significant advantages over current processing
approaches and aligns with modern payment system expectations.
Stop Payment Complexity Management: The system addresses complex stop payment
scenarios where customer actions have different implications depending on payment method.
Electronic payment stop requests trigger collection status because merchants have already
been paid, while draft check stop payments can be processed normally since funds come
directly from customer accounts without risk exposure.
System Migration and Modernization: The ongoing transition from current systems to Check
Free Next represents significant platform modernization that will eliminate collection risks,
provide real-time payment processing, and offer competitive advantages against merchantdirect payment incentives. This migration demonstrates commitment to modern payment
processing capabilities while maintaining comprehensive customer service and operational
oversight.
Partner Care System Integration: The comprehensive Partner Care system provides integrated
access for both PNC and Fiserv customer service teams with complete visibility into customer
payment activities, transaction histories, and account status information. This integration enables
collaborative customer service delivery while maintaining proper channel management and
relationship boundaries throughout the support process.
