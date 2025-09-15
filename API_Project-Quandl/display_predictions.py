1. Where does your application/platform sit in the flow of payments? (Beginning, middle, end)

GPP operates at both the beginning and end of the payment flow, depending on whether the focus is on originations or receivables processing. This dual positioning reflects GPP's role as PNC's core payment processing engine that handles both outbound payment initiation and inbound payment receipt.

For origination processing, GPP sits towards the end of the payment flow. Payment instructions flow through various upstream channels including origination systems, middleware platforms like staging and dial, before reaching GPP for final processing, validation, settlement coordination, and clearing network transmission. GPP represents the final internal processing step before payments are sent to external clearing networks like the Federal Reserve, RTP networks, or correspondent banking partners.

For receivables processing, GPP sits at the beginning of PNC's internal payment flow. Incoming payments from external clearing networks, correspondent banks, and payment networks are received directly by GPP systems, which then initiate internal processing workflows including account crediting, customer notification, and downstream system updates for reporting and reconciliation purposes.

Processing complexity involves GPP serving as PNC's central payment hub that orchestrates complex payment processing workflows including account validation through MDM (Master Data Management), sanctions screening through RTS (Real-Time Sanctions), fraud detection, regulatory compliance checks, and settlement coordination with multiple clearing networks and correspondent banking relationships.

System architecture positions GPP as the authoritative payment processing platform that maintains payment transaction records, coordinates with external networks, manages settlement processes, and provides payment status information to upstream applications and client-facing systems.

The dual positioning enables GPP to serve as PNC's comprehensive payment processing platform while maintaining specialized capabilities for both outbound payment origination and inbound payment receipt processing workflows.

 2. What are your downstream applications for originations?

GPP interfaces with an extensive array of downstream applications that support comprehensive payment reporting, reconciliation, and business operations:

STX (Securities Trading Exchange) receives payment transaction data related to securities trading and settlement activities, enabling coordination between payment processing and securities operations for institutional clients and trading activities.

GL (General Ledger) receives detailed payment transaction information for financial reporting, accounting, and regulatory compliance purposes. GL integration ensures that all payment activities are properly recorded in PNC's financial systems and available for financial statement preparation and regulatory reporting.

RCF (Reconciliation and Control Framework) receives transaction data for automated reconciliation processes that ensure payment processing accuracy and identify discrepancies between internal records and external clearing network confirmations.

CFE (Cash Flow Engine) receives payment information for cash management, liquidity planning, and treasury operations. CFE integration enables comprehensive cash flow forecasting and liquidity management across PNC's payment processing activities.

FRE (Financial Reporting Engine) receives payment transaction data for regulatory reporting, management reporting, and compliance monitoring purposes. FRE supports various regulatory requirements including BSA/AML reporting, FFIEC compliance, and internal risk management reporting.

CDR (Customer Data Repository) and PDR (Payment Data Repository) receive comprehensive payment transaction information for customer relationship management, payment history tracking, and analytical purposes that support business development and customer service operations.

Receivables applications handle customer billing, account management, and collection processes that may be triggered by payment processing activities or require payment transaction information for customer account management.

ADI (Automated Data Interface) provides data feed capabilities for various internal and external systems that require payment transaction information for their specialized processing requirements.

Pinnacle receives payment status and transaction information to support client-facing reporting and account management capabilities, enabling clients to access payment history and status information through web-based interfaces.

EDI (Electronic Data Interchange) systems receive payment information for clients who require EDI-formatted transaction reporting and status updates as part of their automated account management and reconciliation processes.

The extensive downstream ecosystem reflects GPP's role as the authoritative source of payment transaction information across PNC's enterprise systems and client-facing applications.

 3. What are your downstream applications for receivables?

GPP's downstream applications for receivables processing largely overlap with origination processing, reflecting the integrated nature of payment processing operations:

CDR (Customer Data Repository) and PDR (Payment Data Repository) receive incoming payment information for customer account updates, payment history tracking, and relationship management purposes. Incoming payments must be properly attributed to customer accounts and made available for customer service and account management operations.

EDI systems receive incoming payment information for clients who require automated notification and reporting when they receive payments to their PNC accounts. These EDI feeds enable client systems to automatically update their internal records when payments are received.

GL (General Ledger) receives incoming payment information for financial reporting and accounting purposes, ensuring that all received payments are properly recorded in PNC's financial systems and available for regulatory reporting and financial statement preparation.

Reporting applications receive incoming payment data for various business and operational reporting requirements including volume tracking, fee calculation, and performance monitoring related to incoming payment processing activities.

Customer notification systems may receive information about incoming payments to generate customer alerts, statements, and other communication related to payments received to customer accounts.

Reconciliation systems receive incoming payment data for automated reconciliation with expected payments, clearing network confirmations, and internal processing controls that ensure complete and accurate processing of all incoming payments.

The downstream ecosystem for receivables processing focuses primarily on customer account management, financial reporting, and operational monitoring rather than the broader business system integration required for origination processing.

 4. What are your upstream applications for originations?

GPP receives payment origination instructions from a diverse array of upstream systems reflecting PNC's comprehensive payment origination capabilities:

CAP (Corporate API Platform) provides API-based payment origination for corporate clients who integrate payment submission into their enterprise systems. CAP handles authentication, API management, and format standardization before routing payment instructions to GPP for processing.

Pinnacle serves as PNC's primary web-based payment origination platform for clients who prefer browser-based payment submission, file upload capabilities, or manual payment entry through user-friendly interfaces.

PSI (Payment Services Interface) provides specialized payment origination capabilities for specific client segments or payment types that require customized processing workflows or integration patterns.

Direct transmission capabilities enable high-volume clients to submit payment files directly to GPP through secure file transfer protocols, supporting automated payment processing workflows for clients with sophisticated treasury management systems.

File origination systems support batch payment processing for clients who prefer to submit large volumes of payments through structured file formats rather than individual transaction submission through web interfaces or APIs.

Standing orders processing handles recurring payment instructions that have been pre-authorized by clients for regular execution on specified schedules. This includes fixed transfers, sweep arrangements, and other automated payment services that operate without individual transaction authorization.

ILV (Internal Liquidity and Velocity) provides specialized payment origination for internal PNC treasury operations and liquidity management activities.

IOB (Internal Operations Banking) serves PRT-specific payment origination requirements related to real-time payment processing and specialized internal banking operations.

MLP API (Multi-Location Processing API) enables various internal PNC systems to originate real-time payments through standardized API interfaces that support high-volume, low-latency payment processing requirements.

FPT (File Processing and Transmission) handles specialized file-based payment origination requirements for clients or internal systems that require customized file processing workflows.

Canada ACH systems provide payment origination capabilities for Canadian dollar payments processed through Canadian clearing networks, supporting PNC's cross-border payment processing capabilities.

The diverse upstream ecosystem enables GPP to serve comprehensive payment origination requirements across retail, commercial, and institutional client segments while supporting both real-time and batch processing workflows.

 5. What are your upstream applications for receivables?

GPP's upstream applications for receivables processing are identical to origination applications because the same systems that originate payments also generate reporting and inquiry requests related to incoming payments received by their accounts.

Shared upstream architecture means that applications like CAP, Pinnacle, PSI, and other origination systems also serve as sources of inquiries about incoming payments, status requests for received payments, and reporting requests related to receivables processing activities.

Integrated processing model reflects the practical reality that clients and internal systems that originate payments also need visibility into payments they receive, creating natural integration between origination and receivables processing workflows through the same upstream application interfaces.

Reporting and inquiry capabilities through upstream applications enable clients to access information about payments they have received, generate reports about incoming payment volumes and patterns, and integrate receivables information into their internal treasury and accounting systems.

Consistent interface design across origination and receivables processing reduces complexity for upstream applications and clients who need both capabilities, enabling them to access comprehensive payment processing services through familiar interfaces and integration patterns.

 6. Of those downstream applications, which do you receive acknowledgments or notifications from?

GPP operates primarily on a fire-and-forget model for most downstream integrations, with limited acknowledgment requirements from downstream applications:

No systematic acknowledgments are received from most downstream applications including STX, GL, RCF, CFE, FRE, CDR, PDR, receivables systems, ADI, or EDI systems. These applications are designed to consume payment transaction data provided by GPP without requiring acknowledgment confirmation.

End-of-day file processing generates files that are transmitted to downstream applications, but these applications are not required to provide formal acknowledgments confirming successful receipt or processing of the transmitted files.

Staging-based confirmations represent the primary exception where GPP relies on staging systems to handle confirmation workflows back to clients and upstream applications. GPP generates payment processing results that staging systems use to create appropriate client confirmations and status updates.

Operational monitoring rather than systematic acknowledgments provides oversight of downstream integration health through run-the-bank teams who monitor for processing issues, but this occurs through operational procedures rather than automated acknowledgment systems.

Exception-based communication occurs when downstream applications experience processing issues that require GPP attention, but this represents exception handling rather than routine acknowledgment workflows.

The fire-and-forget approach reflects the high-volume, high-performance requirements of payment processing where systematic acknowledgment collection could introduce performance bottlenecks and operational complexity without providing substantial operational benefits.

 7. Of those upstream applications, which do you receive acknowledgments or notifications from?

GPP provides selective acknowledgments and reporting to upstream applications based on processing requirements and client preferences:

Staging systems receive comprehensive processing status and results from GPP that enable staging to provide appropriate confirmations and status updates to originating clients and systems. This represents the primary acknowledgment workflow for payment processing results.

Real-time processing acknowledgments are provided immediately for API-based payment submissions through CAP and other real-time interfaces, enabling upstream applications to provide immediate feedback to clients about payment submission status.

File processing confirmations are provided for batch payment submissions through Pinnacle and other file-based interfaces, confirming successful receipt, validation, and processing initiation for batch payment files.

Error notifications are provided to upstream applications when payment processing encounters validation errors, compliance issues, or other processing failures that require upstream attention or client notification.

Status reporting is available through various upstream interfaces for clients who need ongoing visibility into payment processing status and completion.

Scheduled confirmations are provided to clients who prefer batch reporting about payment processing results rather than real-time status updates, supporting various client preferences for processing confirmation delivery.

The acknowledgment model balances upstream application requirements for processing confirmation with GPP's high-performance processing requirements and operational efficiency objectives.

 8. In what format do you receive transactions/files/data?

GPP supports multiple inbound data formats to accommodate diverse upstream application requirements and client preferences:

JSON formats are received from Pinnacle for web-based payment submissions and modern API integrations that prefer structured JSON data for payment instruction transmission. JSON provides flexibility for complex payment instructions and supports dynamic field structures.

XML formats are received from staging systems that perform format conversion and standardization before transmitting payment instructions to GPP. XML formats support structured data with validation capabilities and standardized field definitions.

ISO formats are supported for payment instructions that comply with international payment messaging standards. ISO formats provide standardized field definitions and validation rules that support cross-border payments and correspondent banking relationships.

Legacy formats including various proprietary and historical data formats are supported for existing clients and internal systems that have not migrated to modern payment messaging standards.

File-based formats support batch payment processing for high-volume clients who prefer to submit structured files containing multiple payment instructions rather than individual transaction submission.

API-based formats support real-time payment processing for clients and systems that require immediate payment processing with minimal latency.

Multi-format support reflects GPP's role as PNC's comprehensive payment processing platform that must accommodate diverse client technical capabilities and preferences while providing consistent processing quality across all supported formats.

 9. In what format do you send transactions/files/data?

GPP performs format transformation and standardization for downstream transmission based on recipient requirements:

IPS (Integrated Payment Services) translation converts various inbound formats into standardized ISO formats for PME processing. This transformation ensures consistent downstream processing regardless of original submission format while supporting international payment standards.

ISO format standardization represents GPP's strategic direction for downstream integration, providing consistent message formats that support regulatory compliance, international payments, and correspondent banking relationships.

XML formats are used for downstream applications that require structured XML data for their processing workflows, including reporting systems and reconciliation applications.

Specialized formats are generated for downstream applications that require customized data layouts or field structures to support their specific processing requirements.

File generation creates structured files for downstream applications that prefer batch data transmission rather than real-time data streaming or API-based integration.

End-of-day processing generates comprehensive files containing transaction summaries, status reports, and reconciliation data for downstream applications that operate on batch processing schedules.

IPF (Integrated Payment Framework) preparation involves format transformation to support migration toward PNC's next-generation payment processing infrastructure, ensuring compatibility with future platform capabilities.

The output format strategy supports both current operational requirements and strategic platform evolution while maintaining compatibility with diverse downstream application technical capabilities.

 10. Do you have any unique identifier that you add to the transactions from your system?

GPP utilizes MID (Message Identifier) as the primary unique identifier for payment transaction tracking and management:

MID implementation provides consistent transaction identification throughout the payment processing lifecycle, enabling correlation between upstream submission, internal processing, downstream integration, and external clearing network transmission.

Dial integration involves coordination with dial systems for additional identifier management and correlation capabilities that support complex payment processing workflows requiring multiple system integration.

Processing-specific identifiers may be generated for specialized processing requirements or integration scenarios that require additional tracking capabilities beyond standard MID implementation.

Cross-system correlation enables MID-based tracking across upstream applications, GPP processing, downstream applications, and external network integration, providing comprehensive payment lifecycle visibility.

Transaction reference consistency ensures that payment tracking remains consistent across all system interfaces and processing stages, supporting effective operational monitoring, client inquiry handling, and regulatory compliance requirements.

Identifier preservation maintains original client-provided identifiers where appropriate while ensuring that internal processing identifiers support comprehensive operational and audit requirements.

The identifier strategy balances client requirements for transaction tracking with internal operational needs and regulatory compliance requirements across GPP's comprehensive payment processing ecosystem.

 11. Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction?

GPP maintains comprehensive reporting capabilities through multiple platforms and interfaces:

OBI (Oracle Business Intelligence) serves as GPP's primary reporting platform, providing dashboard capabilities and specialized reports for various stakeholders including operational teams, client relationship managers, and regulatory compliance teams.

Customer-specific reporting includes specialized drawdown reports and other customized reporting capabilities for clients who require detailed payment processing information tailored to their specific business requirements and reporting preferences.

Operational dashboards provide real-time visibility into payment processing volumes, error rates, processing performance, and system health metrics that support day-to-day operational management and performance monitoring.

Regulatory reporting capabilities support various compliance requirements including BSA/AML reporting, regulatory examination support, and internal audit requirements that require detailed payment processing information.

Client-facing reporting through Pinnacle and other interfaces enables clients to access payment history, processing status, and transaction details through self-service reporting capabilities.

API-based reporting through CAP enables clients who prefer programmatic access to payment processing information for integration into their internal reporting and reconciliation systems.

Batch reporting through various file-based interfaces provides comprehensive payment processing summaries for clients who prefer scheduled reporting rather than real-time access to payment information.

Legacy system integration maintains OBI reporting capabilities despite ongoing efforts to modernize reporting infrastructure, ensuring continuity of critical reporting functions while platform evolution continues.

The comprehensive reporting approach ensures that payment processing information remains accessible to diverse stakeholders through appropriate interfaces while supporting both operational management and client service requirements.

 12. Can a client check on the status of their payment?

GPP provides multiple mechanisms for clients to access payment status information based on their integration preferences and technical capabilities:

Pinnacle web interface enables clients to log in and access real-time payment status information, transaction history, and processing details through user-friendly web interfaces that support both individual transaction lookup and comprehensive payment portfolio management.

CAP API integration provides programmatic access to payment status information for clients who prefer to integrate payment status checking into their internal systems and automated workflows.

File-based status reporting generates regular status files for clients who prefer batch reporting rather than real-time status checking. These files can be customized to client-specific schedules and content requirements.

Real-time acknowledgment files are available for clients who utilize file-based payment submission and prefer immediate confirmation of submission receipt and initial processing status.

Scheduled status reporting provides regular updates about payment processing status for clients like Stripe who receive status files every 15 minutes, enabling near real-time visibility without requiring API integration.

Customer service integration enables PNC client service representatives to access comprehensive payment status information to support client inquiries and issue resolution through internal systems and processes.

Multi-channel access ensures that clients can access payment status information through their preferred method whether that involves web interfaces, API integration, file-based reporting, or traditional customer service channels.

The diverse status access options accommodate varying client technical capabilities and preferences while ensuring that comprehensive payment status information remains readily available through appropriate channels.

 13. What sort of data management are you doing? What type of database do you use?

GPP's data management strategy centers on COD (Corporate Online Data) integration with supporting database infrastructure:

COD integration serves as the primary data repository for comprehensive payment transaction information, providing centralized storage that supports reporting, analytics, compliance monitoring, and regulatory examination requirements across PNC's payment processing ecosystem.

Enterprise data architecture positions COD as the authoritative source for payment processing data that enables cross-system reporting, regulatory compliance, and business intelligence capabilities while supporting GPP's operational processing requirements.

Operational database systems support real-time payment processing requirements including transaction validation, status tracking, and processing workflow management, though specific database platforms may vary based on technical architecture decisions and performance requirements.

Data lifecycle management involves coordination between operational processing databases and COD repositories to ensure that payment processing data remains available for immediate operational requirements while supporting long-term reporting and compliance needs.

Integration architecture enables seamless data flow between GPP processing systems and enterprise data repositories while maintaining operational performance and data consistency across complex payment processing workflows.

Performance optimization balances real-time processing requirements with comprehensive data capture and reporting needs, ensuring that data management strategies support both operational excellence and regulatory compliance requirements.

The data management approach reflects GPP's critical role in PNC's payment processing ecosystem while supporting comprehensive data availability for enterprise-wide reporting and compliance requirements.

 14. Is your database split between operational and reporting databases?

The transcript does not provide specific details about GPP's database architecture separation, but the COD integration model suggests a hybrid approach:

COD serving reporting functions indicates that comprehensive reporting and analytics requirements are handled through enterprise data warehouse capabilities rather than dedicated reporting databases within GPP infrastructure.

Operational processing focus suggests that GPP's internal database systems are optimized for real-time payment processing, transaction validation, and workflow management rather than supporting complex reporting and analytical queries.

Enterprise data architecture leverages COD's specialized capabilities for reporting, compliance monitoring, and business intelligence while enabling GPP to focus on operational processing excellence without the performance impact of supporting complex reporting queries.

Data flow integration between operational processing and enterprise reporting systems provides the benefits of database separation while maintaining data consistency and comprehensive reporting capabilities across PNC's payment ecosystem.

The architecture appears to provide functional separation between operational and reporting requirements through integration with specialized enterprise data systems rather than maintaining separate database instances within GPP infrastructure.

 15. Is your data being streamed anywhere? For ex. a warehouse like COD?

GPP actively streams data to COD as part of PNC's comprehensive enterprise data management strategy:

COD integration involves continuous data streaming that captures payment processing activities, status changes, and transaction details throughout the payment lifecycle. This streaming approach ensures that enterprise reporting and analytics systems have access to current payment processing information.

Real-time data availability through COD streaming enables enterprise-wide reporting, compliance monitoring, and business intelligence capabilities that support decision-making and regulatory requirements across PNC's payment processing operations.

Comprehensive data capture includes transaction details, processing status changes, error conditions, and operational metrics that provide complete visibility into payment processing activities for enterprise stakeholders.

Enterprise analytics support through COD enables cross-system analysis, trend identification, and performance monitoring that support strategic decision-making and operational optimization across PNC's payment processing ecosystem.

Regulatory compliance support through comprehensive data streaming ensures that all payment processing activities are captured and available for regulatory examination, audit requirements, and compliance monitoring activities.

Business intelligence integration enables COD data to support various enterprise reporting and analytics platforms that serve different stakeholder requirements across PNC's organization.

The data streaming strategy positions GPP as a key contributor to PNC's enterprise data ecosystem while enabling specialized enterprise systems to provide comprehensive reporting and analytics capabilities.

 16. Is it possible for there to be a failure at your stage in the payments flow? If so, what happens if there is one?

GPP encounters multiple types of failures with comprehensive handling procedures for each scenario:

Interface failures occur when GPP cannot successfully communicate with supporting systems like MDM (Master Data Management) for address information, account lookup systems, or RTS (Real-Time Sanctions) screening systems. These failures require different handling approaches based on the criticality of the failed interface and the type of payment being processed.

Account lookup failures prevent GPP from validating recipient account information, which may result in payment rejection, manual review queues, or alternative processing workflows depending on payment type and risk tolerance.

Sanctions screening failures create compliance risks that typically result in payment holds or rejections until manual review can be completed by compliance specialists.

Processing workflow failures can occur at various stages of payment processing and may result in automatic retry logic, manual intervention queues, or payment cancellation depending on the specific failure type and processing stage.

Manual intervention procedures are available for complex failures that cannot be resolved through automated recovery mechanisms. Operational teams including run-the-bank specialists handle these manual interventions with established procedures for different failure types.

Automated cancellation occurs for certain failure types where automated retry is not appropriate or where continued processing would create unacceptable risk conditions.

NSF (Non-Sufficient Funds) handling for insufficient balance conditions includes specialized workflows that may involve payment rejection, retry scheduling, or customer notification depending on payment type and client relationships.

Error escalation procedures ensure that failures requiring specialized expertise are routed to appropriate teams including compliance specialists, technical support teams, or client relationship managers based on the nature of the failure and required resolution approach.

Run-the-bank coordination provides centralized management of failure resolution procedures and maintains comprehensive documentation of failure types, resolution approaches, and operational procedures that support consistent failure handling across GPP's payment processing operations.

The comprehensive failure management approach ensures that payment processing disruptions are handled appropriately while maintaining operational efficiency and regulatory compliance across diverse failure scenarios.

 17. Do you do any negative tracking or volume tracking to account for expected transactions on a certain day?

GPP implements selective volume monitoring focused on specific clients and operational risk management:

Client-specific monitoring exists for certain customers who represent significant volume or operational importance to PNC's payment processing operations. These monitoring activities help ensure that unusual volume patterns are identified and investigated appropriately.

Operational team oversight by run-the-bank specialists provides manual monitoring and analysis of payment processing volumes, particularly for clients or processing patterns that require special attention due to risk management or operational requirements.

Manual monitoring approach rather than comprehensive automated systems handles most volume tracking activities, with operational teams providing analysis and investigation of unusual volume patterns when they occur.

Risk-based focus concentrates monitoring efforts on clients or processing scenarios where volume variations could indicate operational issues, compliance concerns, or client relationship problems that require proactive management attention.

Exception-based investigation occurs when operational teams identify volume patterns that appear unusual or inconsistent with expected client activity, triggering investigation and potential client outreach to ensure processing accuracy.

Limited automation means that comprehensive negative tracking is not implemented as a standard automated procedure across all clients and processing scenarios, but manual oversight provides appropriate monitoring for critical situations.

The selective monitoring approach balances operational oversight requirements with practical resource constraints while ensuring that critical volume variations receive appropriate attention and investigation.

 18. Do you get any notifications from downstream systems if they don't receive a file or transaction from you?

GPP receives limited direct notifications from downstream systems regarding missing files or transactions:

Run-the-bank coordination serves as the primary mechanism for handling missing file or transaction issues, with downstream system operational teams contacting GPP's run-the-bank specialists when they identify missing expected data or files.

Operational escalation occurs when downstream systems identify discrepancies or missing information, but this typically involves manual coordination between operational teams rather than automated notification systems.

Individual issue resolution may involve direct contact between GPP specialists and downstream system operators when specific missing file or transaction issues are identified, but this represents exception handling rather than systematic notification procedures.

Manual coordination procedures handle most missing file or transaction issues through established operational procedures that involve coordination between GPP operational teams and downstream system specialists.

Limited automated notification means that comprehensive missing file detection is not implemented across all downstream systems, requiring operational teams to maintain awareness of processing patterns and potential issues through multiple monitoring approaches.

Exception-based communication occurs when operational teams identify potential missing file or transaction issues, triggering investigation and coordination between GPP and downstream system teams to resolve discrepancies.

The notification approach reflects the practical challenges of implementing comprehensive automated missing file detection across diverse downstream systems with varying technical capabilities and monitoring systems, requiring operational coordination to ensure complete payment processing workflow integrity.
