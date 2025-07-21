PNC Pinnacle Payment System Analysis
Question 1: Where does your application/platform sit in the flow of
payments (what do you receive from an upstream system, if any? What
do you send downstream)?
Answer:
Pinnacle serves as the primary front-end application layer that initiates and manages payments
within PNC's payment ecosystem. The application acts as the central entry point for two distinct
payment processing channels that handle different customer segments and payment types.
The first channel is Pinnacle Fund Transfer (PFT), which serves retail and business customers by
handling wire payments, real-time payments (RTP), ACH payments, and various other payment
types. Users interact with this system through web-based interfaces where they can manually enter
payment details, set up scheduled and recurring payments, or upload payment files using templatebased import functionality that supports multiple input formats.
The second channel is Commercial Experience (Comex), which is specifically designed for
commercial clients and manages their business payment needs through a separate but integrated
platform that processes commercial payments with different workflow requirements.
From an upstream perspective, Pinnacle does not receive transactions from other internal systems -
instead, it serves as the origination point where customers and clients initiate payment requests.
The upstream sources include direct user input through manual screen entry, scheduled and
recurring payment configurations, and file uploads through template-based import capabilities.
From a downstream perspective, all payments from both Pinnacle systems flow to the PSG
(Payment Staging Group) team, which functions as intelligent middleware in the payment
processing architecture. The PSG staging team receives all payment requests and performs critical
functions including payment type identification, format validation, and intelligent routing decisions.
Once the staging team processes and validates the payments, they route transactions to the
appropriate downstream processing systems based on payment characteristics. These downstream
systems include PME (Payment Management Engine) which processes wire payments and other
traditional payment types, PRT (Payment Real-Time) which handles real-time payments and RTP
transactions, and various ACH processing systems when payments are routed from the
commercial experience platform.
The payment flow includes comprehensive status tracking where users receive initial
acknowledgement when payments are successfully sent to staging, followed by status updates to
"confirmed" once payments are successfully processed by the downstream systems, providing endto-end visibility throughout the payment lifecycle.
Question 2: In what format do you receive transactions/files/information?
Answer:
The transaction format received by Pinnacle varies significantly depending on which system channel
is being used, with each channel designed to support different communication protocols and data
structures optimized for their respective user bases.
Pinnacle Fund Transfer receives all payment transactions in XML format that strictly follows the
Pain.001 ISO standard, which is an internationally recognized format for credit transfer requests.
The specific implementation uses a mutually agreed version of the Pain.001 standard that has been
customized to meet PNC's specific requirements while maintaining ISO compliance. This system
utilizes SOAP (Simple Object Access Protocol) web services for all communication, which is a
traditional but robust web service protocol that ensures reliable message transmission. All data
transmission occurs through Message Queues (MQ) infrastructure, which exclusively supports XML
format messaging and provides guaranteed message delivery with built-in error handling and retry
mechanisms.
When customers use the import functionality within Pinnacle Fund Transfer, the system accepts
various input formats through template-based uploads, but the platform automatically converts
everything to the native XML format at the point of upload. This conversion process eliminates the
need for multiple reformatting steps during transmission and ensures consistency throughout the
payment processing pipeline.
Commercial Experience (Comex) operates using a more modern approach by receiving payment
transactions in JSON (JavaScript Object Notation) format with standardized schema structures
that follow JSON technology standards. This system uses REST (Representational State Transfer)
web services for communication, which is a more contemporary web service architecture that
provides flexibility and easier integration capabilities compared to traditional SOAP services. The
JSON message format includes all required formatting structures and business rule validations
necessary for commercial payment processing.
Both systems maintain their respective format standards throughout the internal processing
workflow, ensuring that data integrity is preserved and that downstream systems receive
consistently formatted information regardless of the origination channel used by the customer.
Question 3: In what format do you send transactions/files/information?
Answer:
Pinnacle maintains strict format consistency when transmitting transactions to downstream
systems, ensuring that the format received is preserved through to the staging team without
unnecessary conversions or reformatting that could introduce errors or processing delays.
Pinnacle Fund Transfer sends all transactions to the PSG staging system in XML format using
SOAP web service calls transmitted through the Message Queue infrastructure. When users
place payment requests through the interface, the system's programming logic makes web service
calls that translate the user input into the standardized XML format and places these formatted
messages into the messaging queue system. The messaging queue then handles the reliable
transmission of these requests to the staging team with built-in delivery confirmation and error
handling capabilities.
Commercial Experience (Comex) transmits transactions to the staging system in JSON format
using REST web service calls. The system maintains the JSON structure throughout the
transmission process, preserving the original data format and schema that was used for the initial
transaction input.
The critical aspect of Pinnacle's transmission approach is that both applications maintain complete
format consistency from receipt to transmission. There are no intermediate format conversions or
transformations that occur between receiving customer input and sending data to the staging
team. This approach eliminates potential formatting errors and reduces processing complexity
while ensuring that the staging team receives data in predictable, standardized formats.
The PSG staging system serves as the format normalization point in the architecture. When
staging receives transactions in either XML or JSON format, it performs backend normalization
processes that convert both formats into the appropriate format required by the specific
downstream payment engine that will handle each transaction. This centralized normalization
approach allows Pinnacle to maintain its format consistency while enabling the staging team to
optimize data formats for each downstream processing system's requirements.
Question 4: Do you have any unique identifier that you add to the
transactions from your system? Do you pass that to the next system in the
step? Do you create a new one? If so, do you maintain an index?
Answer:
Pinnacle implements a comprehensive unique identifier system that ensures complete transaction
traceability throughout the payment processing lifecycle, with different identifier types used
depending on the originating system and specific tracking requirements for various downstream
processes.
Pinnacle Fund Transfer creates a Wire ID for every single transaction that enters the system,
regardless of whether the transaction is actually a wire transfer or another payment type such as
RTP or ACH. This Wire ID serves as the primary unique identifier and is also referred to as the
"Pinnacle ID" in various downstream systems, including PME and PRT databases where it appears
in transaction records for cross-system tracking purposes. The Wire ID designation is maintained
consistently even when transactions are routed to non-wire processing systems - for example, realtime payments that are routed to PRT still carry and use the Wire ID terminology for tracking
purposes.
The system also manages End-to-End ID functionality, which provides flexibility for customersupplied identifiers. Clients have the option of supplying their own End-to-End ID when initiating
transactions, and if they choose not to provide one or leave this field empty, the system
automatically uses the Wire ID (Pinnacle ID) as the End-to-End ID. This automatic substitution
occurs because the End-to-End ID becomes mandatory at some point in the downstream
processing workflow, so the system ensures this requirement is always met by using an existing
reliable identifier when customer-supplied IDs are not available.
When transactions are sent to the staging team, Pinnacle receives a Transaction ID as part of the
acknowledgment response from PSG. This Transaction ID serves as the staging system's unique
identifier for the payment and enables cross-system tracking capabilities. When payment status
inquiries or troubleshooting is needed, teams can provide either the Wire ID or the Transaction ID
to PSG for comprehensive payment tracking and status information retrieval.
Commercial Experience (Comex) uses a different identifier structure with Trace ID as the primary
unique identifier for all commercial payment transactions. The Trace ID is stored in the database
and serves as the main reference point for tracking commercial payment transactions throughout
their lifecycle. Similar to the Fund Transfer system, Comex also receives an acknowledgment ID from
the staging system that enables end-to-end tracking and status verification.
System Identification and Uniqueness: The systems use distinct Sender IDs to ensure proper
identification and routing. Pinnacle Fund Transfer uses sender ID "PINFT" while Commercial
Experience uses sender ID "PPS" (with exact naming to be confirmed from database records). These
sender IDs enable PSG to identify the originating application and apply appropriate routing logic
for each transaction type.
An important architectural principle is that transactions cannot have both a Wire ID and a Trace ID
simultaneously - the identifier type is guaranteed to be one or the other based on the originating
system. The sender ID field definitively determines which identifier type will be present for any
given transaction, ensuring clear identification throughout the processing chain.
Index Maintenance: Both systems maintain comprehensive indexes of their respective identifiers in
Oracle databases, enabling rapid transaction lookup, status tracking, and historical reporting
throughout the payment lifecycle. These indexes support both operational transaction processing
and comprehensive audit trail requirements for regulatory compliance and customer service
purposes.
Question 5: Do you have any reporting that captures the activity that
takes place at your stop in the lifecycle of a transaction? If so, where is
that hosted? Are there consumers for said report today?
Answer:
Pinnacle maintains extensive reporting capabilities that comprehensively capture all transaction
activity occurring at their stage in the payment lifecycle, with both current operational systems and
ongoing modernization efforts to enhance reporting functionality and accessibility.
Current Reporting Infrastructure: The system operates two distinct reporting platforms that serve
different phases of the technology modernization timeline. Actuate serves as the legacy reporting
system that currently hosts a significant portion of existing reports, but this platform is undergoing
planned decommissioning with complete retirement scheduled for the end of the current year.
Magellan represents the new reporting platform where all reports are actively being migrated, and
this system will serve as the primary reporting infrastructure once the transition is complete.
Both reporting systems provide comprehensive capabilities for customers to track payment activity,
transaction status, historical processing data, and detailed audit trails for all transactions processed
through either Pinnacle Fund Transfer or Commercial Experience platforms. The reporting systems
maintain detailed records of all activity that occurs at Pinnacle's stage in the transaction lifecycle,
including transaction initiation, status changes, processing confirmations, and any exception
handling that occurs.
Automated Reporting Systems: Pinnacle has implemented several automated reporting
mechanisms that provide regular updates to various stakeholders. Daily Consolidated Reports are
automatically generated and distributed to business teams after 6:45 PM each day, providing
comprehensive status information including the total number of wire transfers processed, detailed
payment status summaries categorized by processing stage, and overall processing metrics that
help teams understand daily transaction volumes and processing efficiency.
The system also generates Daily Manual Reconciliation Reports that facilitate reconciliation
processes between PSG systems and Pinnacle databases. These reports ensure status alignment
across systems and enable operations teams to take necessary corrective actions when
discrepancies are identified between system records.
Alert and Exception Reporting: Pinnacle maintains an automated alert system that generates
notifications when payments remain stuck in particular statuses for extended time periods. These
alerts trigger investigations and provide early warning of processing issues that require manual
intervention or system troubleshooting.
OFAC Status Reports are automatically generated for payments requiring OFAC (Office of Foreign
Assets Control) confirmation. These specialized reports track payments that may show as "received
only" status while awaiting OFAC clearance, ensuring compliance monitoring and appropriate status
communication.
Out-of-Sync Notification Reports are automatically generated and distributed via email when
status discrepancies are detected between Pinnacle and downstream systems, enabling rapid
identification and resolution of data consistency issues.
Report Access and Consumers: Access to both reporting systems requires proper entitlement
submission processes that ensure appropriate security and access controls. Reports are available for
both Pinnacle Fund Transfer and Commercial Experience users, with permissions managed based on
business roles and operational requirements.
Current consumers of these reports include business operations teams who use daily consolidated
reports for operational oversight, reconciliation teams who rely on daily reconciliation reports for
system alignment verification, customer service teams who access transaction-specific reports for
client inquiries, and compliance teams who utilize specialized reports for regulatory monitoring and
audit trail requirements.
The reporting systems capture comprehensive activity occurring specifically at Pinnacle's stage in
the transaction lifecycle, providing complete visibility into transaction initiation, processing status,
exception handling, and final disposition for all payments processed through the platform.
Question 6: Is your data being streamed (KAFKA stream, etc) anywhere?
For example, a warehouse like COD.
Answer:
Pinnacle's current data architecture does not implement modern streaming technologies,
representing a significant architectural characteristic that impacts real-time data processing and
analytics capabilities across the payment processing platform.
Current Streaming Status: The system definitively does not implement Kafka streaming in either
Pinnacle Fund Transfer or Commercial Experience systems. This was explicitly confirmed during the
technical discussion, with the team stating that "Kafka definitely is not in picture" for either of the
two payment processing systems. The absence of Kafka or other modern streaming platforms
means that real-time data streaming, event-driven processing, and modern analytics capabilities are
not currently available through streaming architecture.
COD (Corporate Online Data warehouse) Integration: The status of data streaming to the COD
warehouse system remains unclear and requires additional investigation. The technical team
acknowledged that they need to verify with the mainframe team whether data is being streamed to
COD warehouse systems through other mechanisms or batch processes. This represents a gap in
current system knowledge that needs to be addressed through coordination with mainframe
operations teams who would have definitive information about data warehouse integration
patterns.
Current Technical Architecture: All current data flow operates primarily through traditional
Message Queue architecture rather than modern streaming technologies. The payment
processing workflow relies on established MQ (Message Queue) systems for reliable data
transmission, which provides transactional integrity and guaranteed message delivery but lacks the
real-time streaming capabilities that modern analytics and monitoring systems typically require.
The Message Queue approach ensures reliable transactional processing with built-in error handling,
retry mechanisms, and delivery confirmation, but it operates on a request-response model rather
than continuous data streaming. This architecture is well-suited for transactional payment
processing but may limit opportunities for real-time analytics, continuous monitoring, and eventdriven processing capabilities that streaming architectures typically enable.
Implications for Data Architecture: The absence of streaming technologies means that data
integration with analytics platforms, real-time monitoring systems, and business intelligence tools
likely relies on batch processing or traditional database integration methods rather than continuous
data streams. This architectural characteristic should be considered when planning future system
enhancements, analytics implementations, or real-time monitoring capabilities that might benefit
from streaming data architecture.
The technical team's need to verify COD integration status suggests that there may be existing data
movement processes that occur outside of the primary payment processing workflow, potentially
through batch jobs or other integration mechanisms that operate independently of the core
transaction processing systems.
Question 7: What happens if a file dies at your step in the process?
Answer:
Pinnacle has implemented a comprehensive approach to handling transaction failures and
processing errors, with multiple layers of validation, error handling, and recovery mechanisms
designed to ensure reliable payment processing and appropriate customer communication when
issues occur.
Validation and Rejection Process: The transaction validation process occurs at multiple levels to
ensure comprehensive error detection and appropriate handling. Application-level validation is
performed at the Pinnacle level before any transmission to downstream systems, ensuring that
basic mandatory field checks are completed and required data elements are present and properly
formatted before transactions are sent to the staging team.
PSG Staging Validation provides the primary comprehensive validation layer where detailed
format verification occurs. The staging team performs extensive validation including special
character checking to identify potentially problematic characters that could interfere with
downstream processing, acceptable format verification to ensure messages conform to required
standards, and comprehensive business rule validation to verify that transaction data meets all
processing requirements.
When the staging team identifies validation failures or processing errors, they send detailed
rejection status responses back to Pinnacle that include specific reject reasons providing
transparency about why transactions cannot be processed. These detailed rejection explanations
enable both operations teams and customers to understand the specific issues that need to be
addressed for successful transaction processing.
User Notification and Status Management: When transactions are rejected or fail validation, the
rejection status is immediately reflected in user interfaces and comprehensive reporting systems
with detailed explanations of the specific issues encountered. Pinnacle maintains all transaction
status information in its Oracle database, ensuring that whatever status is acknowledged by PSG is
accurately displayed to users through both online interfaces and reporting systems.
Communication and Issue Resolution Channels: Pinnacle maintains 24/7 Teams Chat as the
primary support channel for real-time payment tracking and issue resolution. This enables
immediate communication between operations teams and the staging team when transaction
problems require investigation or manual intervention.
Email communication is utilized for more complex issues, particularly bulk payment inquiries that
require detailed documentation. In these cases, operations teams share comprehensive payment
details through Excel attachments that provide staging teams with all necessary information for
thorough investigation and resolution.
Alert-Driven Investigation Process: When automated alerts are triggered for stuck payments,
Pinnacle teams follow a systematic investigation process. They first verify that no issues exist on the
Pinnacle side by thoroughly checking logs and database records to confirm that payments were
successfully prepared and transmitted. Only after confirming that payments were successfully
handed over to staging do they escalate issues to PSG for downstream investigation.
Manual Intervention Scenarios: Several scenarios require manual intervention to ensure customer
service and data accuracy. When PSG systems experience downtime and cannot send automated
acknowledgments, Pinnacle operations teams perform manual status updates to ensure users
continue to see accurate, current information rather than outdated or incorrect status displays.
For transactions that PSG determines cannot be processed due to technical issues, staging may
request Pinnacle to reject the payment and coordinate with the PMCC resolution team to handle
customer communication and facilitate resubmission of corrected transactions.
Resubmission and Recovery Process: Pinnacle maintains the capability to change payment status
to "resend" for scenarios where reprocessing is appropriate and feasible. The automated Scoop
Job that runs every 10 minutes from 1:00 AM to 6:45 PM processes up to 250 payments per batch
cycle and can handle both scheduled payments and resubmission of previously failed transactions.
For more complex cases requiring direct customer interaction, payments are manually cancelled or
rejected with appropriate status updates, while the PMCC resolution team handles customer
communication to facilitate proper resubmission with corrected information or formatting.
Question 8: What do you do if you didn't get a file or transaction that you
were expecting to get on a certain day?
Answer:
Pinnacle currently operates with a reactive monitoring approach rather than proactive negative
tracking capabilities, representing a significant gap in comprehensive payment monitoring that
could impact early detection of missing or delayed transactions.
Current Monitoring Approach: The system does not implement proactive negative tracking,
which means it does not monitor expected versus received transaction volumes or track when
anticipated payments fail to arrive as scheduled. Unlike systems that maintain calendars of expected
transaction patterns or monitor for anticipated file deliveries, Pinnacle focuses exclusively on
processing transactions that are actually received rather than tracking transactions that should have
been received but are missing.
The current approach is reactive monitoring only, where operations teams monitor for stuck
payments through automated alert systems rather than proactively identifying missing transactions
or unexpected gaps in transaction volume. This means that detection of missing transactions
typically occurs only when customers contact support to inquire about payments they expected to
process, rather than through systematic monitoring that could identify issues before customer
impact occurs.
Absence of Client-Specific Volume Tracking: The system does not maintain tracking capabilities
for client-specific patterns such as "Client X always sends 10,000 transactions on Tuesday" to detect
anomalies when expected volumes don't materialize. This represents a missed opportunity for
proactive customer service and early detection of processing issues that could affect client
operations.
Holiday Processing Procedures: While the system doesn't track missing regular transactions, it
does maintain restricted holiday procedures for special circumstances. These procedures address
holidays other than major closures like January 1st and December 25th, focusing on situations
where international payments may need processing even when domestic operations are limited.
The automated Scoop Job that normally runs every 10 minutes from 1:00 AM to 6:45 PM is not
scheduled to run on major US holidays. However, for restricted holidays where business operations
continue and international payments require processing, the job can be manually triggered to
ensure that time-sensitive international payments are not delayed due to holiday scheduling.
Communication Channels for Missing Transaction Issues: When missing transaction issues do
arise, they are typically handled through 24/7 Teams Chat which serves as the primary support
channel for payment tracking inquiries and immediate issue resolution. Email communication is
used for more complex situations involving multiple missing transactions, where operations teams
may need to provide detailed documentation through Excel attachments to facilitate
comprehensive investigation.
The current alert-driven process generates automated notifications for stuck payments that are
actively in the system, but it does not generate alerts for payments or transaction volumes that are
expected but have not been received. This means that missing transaction detection relies heavily
on customer reporting rather than proactive system monitoring.
Impact Assessment and Business Implications: The absence of negative tracking capabilities
means that clients may need to proactively contact support when expected payments don't arrive,
rather than receiving proactive notifications about missing transactions from PNC. This places the
burden of detection on customers and potentially creates delays in identifying and resolving issues
that could affect time-sensitive payment processing.
This represents a significant gap in comprehensive payment monitoring capabilities, particularly for
clients with predictable transaction patterns or critical payment timing requirements. The lack of
negative tracking could result in delayed identification of upstream issues, customer service
challenges, and missed opportunities for proactive issue resolution that could prevent customer
impact.
Potential for Enhancement: While the current system lacks comprehensive negative tracking, the
technical infrastructure exists to implement such capabilities through the existing alert system
architecture and database monitoring tools, suggesting that this gap could be addressed through
system enhancements if business requirements support the investment in proactive monitoring
capabilities.
Question 9: Can a client check on the status of their file?
Answer:
Clients have comprehensive capabilities to check payment status through multiple channels and
interfaces, with real-time status updates and detailed historical information available through both
online systems and extensive reporting platforms.
Primary Status Visibility Through User Interface: Clients can check detailed payment status
information through the Pinnacle user interface which provides real-time updates and
comprehensive transaction information. The interface displays current status for all transactions and
provides detailed information about transaction progress through various processing stages, from
initial submission through final confirmation or resolution of any issues that may arise.
Database Integration and Real-Time Updates: All status updates received from PSG staging and
downstream processing systems are immediately reflected in Pinnacle's Oracle database and
automatically displayed to users through the web interface. This integration ensures that clients
always see the most current and accurate status information available, with automatic updates
occurring as acknowledgments and status changes are received from downstream processing
systems throughout the payment lifecycle.
When payments progress through various stages - from initial submission to staging
acknowledgment to final processing confirmation - these status changes are automatically reflected
in the client interface without requiring manual refresh or system updates. This provides clients with
continuous visibility into their payment processing progress.
Comprehensive Reporting Access: Clients can access extensive status information and detailed
transaction history through both Actuate and Magellan reporting systems. These reporting
platforms provide comprehensive capabilities for tracking payment activity, transaction status
history, detailed audit trails, and advanced filtering and search capabilities that enable clients to
analyze their payment processing patterns and history.
The reporting systems maintain detailed records of all processing activity, status changes, exception
handling, and final transaction disposition, providing clients with complete visibility into their
payment processing history for operational planning, reconciliation, and audit purposes.
Historical Status Tracking: The system maintains comprehensive status history throughout the
complete payment lifecycle, enabling clients to track their payments from initial initiation through
all intermediate processing stages to final processing confirmation. This historical tracking capability
supports client reconciliation processes, audit requirements, and operational analysis of payment
processing patterns and timing.
Manual Status Management for Accuracy: To ensure consistent client service and data accuracy,
Pinnacle operations teams perform manual status updates when automated acknowledgment
systems experience failures or delays. When automated systems cannot send timely
acknowledgments due to technical issues, operations teams manually update transaction status to
ensure clients continue to see accurate, current information rather than stale or incorrect status
displays.
This manual oversight capability ensures that client status visibility is maintained even during
system technical difficulties, preventing client confusion or incorrect assumptions about payment
processing progress.
Integration with Customer Support: When clients have questions about complex payment
processing issues or need assistance with transaction status interpretation, the PMCC resolution
team handles customer communications and provides detailed explanations of transaction status
and any actions required for successful processing completion.
This support integration ensures that clients not only have access to status information but also
have expert assistance available when they need help interpreting status information or resolving
processing issues that may require customer action.
Accessibility and User Experience: The status checking capabilities are designed to be accessible
through the same interfaces that clients use for payment initiation, providing a consistent user
experience where clients can both submit payments and track their progress through a unified
platform. This integration eliminates the need for clients to use separate systems or contact support
for routine status inquiries, improving operational efficiency for both clients and PNC operations
teams.
Question 10: Do you get a notification if your downstream system doesn't
receive a file from you?
Answer:
Pinnacle currently lacks automated notification capabilities from downstream systems, representing
a significant architectural gap in the end-to-end payment monitoring system that could impact
early detection and resolution of processing issues throughout the payment ecosystem.
Absence of Automated Downstream Notifications: The system does not receive automated
notifications from downstream processing systems such as PME (Payment Management Engine) or
PRT (Payment Real-Time) when they fail to receive expected files or transactions from Pinnacle
through the PSG staging system. This means that if downstream systems experience technical
difficulties, processing interruptions, or fail to receive transmitted files, Pinnacle operations teams
are not automatically alerted to these issues through system-generated notifications.
No Negative Acknowledgment System: There is no negative acknowledgment system
implemented across the complete payment processing chain that would automatically notify
upstream systems when expected transmissions are not received by downstream components.
Unlike positive acknowledgments that confirm successful receipt and processing, there are no
automated negative acknowledgments that would alert Pinnacle when downstream systems detect
missing files, processing failures, or other issues that prevent normal transaction processing.
Manual Communication Dependency: Information about missing files, processing failures, or
downstream system issues typically flows through manual communication channels including
Teams chat conversations and email correspondence rather than automated system notifications.
This manual approach means that detection and communication of downstream issues depends on
human intervention rather than automated monitoring systems that could provide immediate
notification of processing problems.
The reliance on manual communication creates potential delays in issue identification and
resolution, as problems must be discovered by downstream system operators and then manually
communicated back through the support chain rather than being automatically detected and
reported through system monitoring capabilities.
Systemic Architectural Gap: This represents a significant architectural gap in the end-to-end
payment monitoring system where downstream system failures, missing transmissions, processing
interruptions, or technical issues may not be immediately apparent to upstream systems like
Pinnacle. Without automated feedback loops, issues that prevent successful transaction processing
may only surface through manual investigation triggered by customer inquiries or periodic
reconciliation processes rather than through proactive system monitoring.
Current Issue Resolution Process: When downstream processing issues do occur, resolution relies
on manual escalation through established support channels rather than automated system
notifications that could enable immediate response. Operations teams typically become aware of
downstream issues through one of several manual methods: direct communication from
downstream system operators through Teams chat, email notifications from technical teams
managing downstream systems, or customer inquiries about transactions that have not processed
as expected.
Impact on Operations and Customer Service: The absence of automated downstream
notifications means that processing issues may not be detected until they have already impacted
customer transactions or until periodic reconciliation processes identify discrepancies between
expected and actual processing results. This reactive approach could result in extended resolution
times and potential customer service challenges when processing issues affect multiple transactions
before being identified and addressed.
Potential for Improvement: While automated downstream notification capabilities do not
currently exist, the technical infrastructure including established communication protocols,
database systems, and alert mechanisms could potentially support the implementation of
automated notification systems if business requirements justify the investment in enhanced
monitoring capabilities.
The existing manual communication channels demonstrate that information flow between systems
is possible, suggesting that automated notification systems could be developed using similar
communication pathways enhanced with system-generated monitoring and alerting capabilities.
Question 11: Additional Technical Architecture and Processing Details
Answer:
Beyond the specific operational questions addressed above, the meeting revealed several
important technical architecture details and processing characteristics that provide comprehensive
understanding of Pinnacle's payment processing infrastructure and capabilities.
Database Architecture and Technology Stack: Pinnacle implements a hybrid database
architecture that optimizes different database technologies for specific functional requirements.
Pinnacle Fund Transfer uses Oracle database exclusively for both transactional payment data
storage and reporting functions, providing a unified platform that supports both operational
processing and analytical reporting requirements through a single database technology.
Commercial Experience (Comex) implements a more complex hybrid architecture that leverages
MongoDB for reporting and analytics management while utilizing Oracle database for
payment transaction details and core processing data. This approach optimizes MongoDB's
document-oriented capabilities for flexible reporting and analytics while maintaining Oracle's
robust transactional processing capabilities for critical payment data that requires ACID compliance
and strong consistency guarantees.
Daily Reconciliation Processes: Both systems maintain comprehensive daily manual
reconciliation processes between Pinnacle systems and PSG staging systems to ensure data
consistency and status alignment across the payment processing ecosystem. These reconciliation
processes identify discrepancies between system records and enable operations teams to take
necessary corrective actions to maintain data integrity throughout the payment processing
workflow.
Batch Processing vs Individual Transaction Handling: An important architectural characteristic is
that both Pinnacle Fund Transfer and Comex send only individual payment items to
downstream systems, even when clients use bulk upload or batch submission functionality. When
clients submit multiple payments through upload capabilities, each payment is treated as an
individual item from the time it's uploaded forward, eliminating true batch processing in favor
of individual transaction handling.
This approach means that there is no concept of true batching for Pinnacle-initiated wires or
RTPs. Even when multiple payments are processed together, they are handled as individual items
within a pseudo-batch wrapper construct rather than true batch processing where multiple
transactions would be processed as a single unit.
Unique Transaction Identification: Each payment maintains individual tracking and
identification regardless of the submission method used by the client, whether it's single payment
entry through the user interface or bulk upload through template-based file submission. This
ensures consistent tracking capabilities and status management across all transaction submission
methods.
Processing Schedules and Operational Timing: The automated Scoop Job represents a critical
component of the processing architecture, running every 10 minutes from 1:00 AM to 6:45 PM
daily with a processing limit of 250 payments per batch cycle. This job handles both scheduled
payments and resubmission of previously failed transactions, providing consistent processing
cadence throughout normal business hours.
Holiday handling procedures are implemented with job suspension on major US holidays while
maintaining manual processing capability for restricted holidays when international payments
require processing despite domestic holiday limitations. This flexibility ensures that time-sensitive
international transactions can be processed even during domestic holiday periods when normal
automated processing is suspended.
Daily reporting automation is integrated into the processing schedule with automated
consolidation reports generated after 6:45 PM daily, providing comprehensive daily processing
summaries and status reports to business operations teams.
Web Service Communication Architecture: The systems implement established web service
communication protocols with SOAP services for Pinnacle Fund Transfer providing traditional,
robust messaging capabilities with built-in error handling and delivery confirmation, while REST
services for Commercial Experience offer modern, flexible integration capabilities that support
contemporary web service standards.
Message Queue Infrastructure: The Message Queue architecture ensures reliable transmission
and processing through proven messaging infrastructure that provides guaranteed message
delivery, built-in retry mechanisms, and comprehensive error handling capabilities. This
infrastructure supports the transactional integrity requirements necessary for financial payment
processing while maintaining high availability and reliability standards.
Sender ID-Based Routing Intelligence: The implementation of distinct Sender IDs enables
proper system identification and intelligent routing throughout the payment processing
ecosystem. PSG staging systems use these Sender IDs to identify originating applications and apply
appropriate routing logic, business rules, and processing procedures for each transaction type and
source system.
Existing Specialized Monitoring Capabilities: While the system generally lacks comprehensive
negative tracking, the meeting revealed that PNC already implements limited negative tracking
for specific high-value partnerships. For example, the system monitors inbound wires from
Team Force and Stripe on an hourly basis due to the high-volume nature of these partnerships
and the operational requirement to proactively manage these critical payment flows.
This specialized monitoring demonstrates that the technical capability for negative tracking exists
within the current architecture, but it has not been generalized across the broader payment
platform. This represents an opportunity for expanding successful monitoring approaches to other
client relationships and payment patterns where proactive monitoring would provide operational
value.
System Integration and Interoperability: The overall architecture demonstrates strong system
integration capabilities through standardized communication protocols, consistent database
management approaches, and established operational procedures that support reliable payment
processing across multiple system components and downstream processing engines.
