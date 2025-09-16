1. Where does your application/platform sit in the flow of payments? (Beginning, middle, end)

ACH operates in the middle of the payment flow, functioning as a comprehensive processing and distribution hub that collects, edits, and routes payment files from multiple sources. ACH describes itself as operating "more or less as a passer" that collects files from different entities both inside and outside the bank, processes them through editing and validation procedures, then distributes them to appropriate downstream destinations.

Processing hub role involves ACH receiving payment files from various upstream sources including internal PNC systems, external clients, and clearing networks, then performing comprehensive processing including validation, formatting, editing, and routing to ensure payments reach their intended destinations through appropriate channels.

Multi-directional processing encompasses both origination and receivables workflows, with ACH handling outbound payments initiated by PNC clients as well as inbound payments received from external clearing networks that must be distributed to internal PNC systems for account crediting and processing.

Distribution responsibilities include routing processed payments to multiple downstream destinations including the Federal Reserve, clearing houses, internal core banking systems, reporting applications, and various specialized systems that require ACH transaction data for their processing workflows.

Intermediary positioning reflects ACH's role as a critical bridge between PNC's internal payment origination systems and external clearing networks, as well as between external payment sources and internal PNC processing and account management systems.

The middleware positioning enables ACH to serve as PNC's comprehensive ACH processing platform while providing standardized interfaces to diverse upstream and downstream systems across PNC's payment ecosystem.

 2. What are your downstream applications for originations?

ACH distributes origination data to an extensive array of downstream applications and systems:

Federal Reserve serves as the primary clearing network destination for ACH origination transactions that require processing through the federal ACH network for settlement with other financial institutions.

CARS (Core Account Reporting System) receives ACH transaction data for memo posting and account management functions, ensuring that originated payments are properly reflected in customer account records and available for customer service and account inquiry purposes.

Hard posting systems receive ACH transaction information for final account posting and balance updates, ensuring that originated payments are properly debited from customer accounts and reflected in official account balances.

Billing systems receive ACH origination data for fee calculation, client billing, and revenue recognition purposes related to ACH processing services provided to PNC clients.

CFE (Cash Flow Engine) receives ACH transaction information for cash flow management, liquidity planning, and treasury operations that require comprehensive visibility into ACH-related cash flows.

FinCEN reporting systems receive ACH transaction data for regulatory reporting requirements including suspicious activity monitoring, currency transaction reporting, and other anti-money laundering compliance obligations.

Client reporting systems generate various reports and statements for PNC clients who originate ACH transactions, providing transaction confirmations, processing summaries, and account activity reports.

EFG (Enterprise Fraud Gateway) receives ACH transaction data for fraud monitoring and detection activities that help identify suspicious payment patterns or potentially fraudulent ACH activity.

STX (Securities Trading Exchange) receives relevant ACH transaction information for coordination with securities trading and settlement activities.

Risk limits monitoring systems receive ACH transaction data for credit risk management, exposure monitoring, and compliance with various risk management policies and procedures.

COD (Corporate Online Data) receives comprehensive ACH transaction data for data warehousing, business intelligence, and enterprise reporting purposes.

The extensive downstream ecosystem reflects ACH's central role in PNC's payment processing operations and the broad organizational need for ACH transaction information across multiple business functions and regulatory requirements.

 3. What are your downstream applications for receivables?

ACH processes receivables through similar downstream distribution patterns with some specialized considerations for inbound payments:

Core banking systems including CARS receive inbound ACH transaction data for account crediting, customer notification, and account balance updates, ensuring that received payments are properly credited to customer accounts and reflected in account records.

Account posting systems handle the actual crediting of customer accounts with received ACH payments, updating official account balances and generating appropriate accounting entries for received funds.

Customer notification systems may receive information about inbound ACH payments to generate customer alerts, account statements, or other communication related to payments received to customer accounts.

Reporting applications receive inbound ACH transaction data for various business and operational reporting requirements including volume analysis, fee calculation, and performance monitoring related to ACH receivables processing.

Reconciliation systems receive inbound ACH data for automated reconciliation with expected payments, clearing network confirmations, and internal processing controls that ensure complete and accurate processing of all received payments.

COD data warehouse receives comprehensive inbound ACH transaction information for enterprise-wide reporting, business intelligence, and analytical capabilities that support strategic decision-making and operational oversight.

Compliance monitoring systems receive inbound ACH transaction data for anti-money laundering monitoring, suspicious activity detection, and other regulatory compliance requirements related to received payments.

The receivables downstream distribution ensures that inbound ACH payments are properly processed, credited to appropriate accounts, and made available for comprehensive reporting and compliance monitoring across PNC's enterprise systems.

 4. What are your upstream applications for originations?

ACH receives origination instructions from diverse upstream sources reflecting PNC's comprehensive ACH origination capabilities:

Internal PNC systems generate ACH origination instructions for various business lines including retail banking, commercial banking, and treasury services. These internal systems submit payment files containing customer-initiated ACH transactions that require processing and transmission to clearing networks.

External client systems submit ACH origination files through various channels including secure file transfer protocols, direct connections, and web-based interfaces. These clients include corporate customers who utilize ACH services for payroll, vendor payments, and other business payment requirements.

SFG (Sterling File Gateway) provides secure file transmission capabilities for clients who submit ACH origination files through automated batch processing workflows. SFG enables high-volume clients to integrate ACH processing into their enterprise resource planning and treasury management systems.

Payment staging systems route ACH origination instructions from various internal and external sources, providing format conversion, validation, and routing services before transmitting files to ACH for processing.

Third-party processors may submit ACH files on behalf of their clients who utilize outsourced payment processing services, requiring ACH to handle files from multiple processing entities with varying format and processing requirements.

Government entities may submit ACH files for tax payments, benefits distribution, and other government-related payment activities that require specialized handling and compliance procedures.

Network sources include clearing house systems and Federal Reserve networks that may generate ACH files for return processing, correction processing, or other network-initiated activities that require ACH processing.

The diverse upstream ecosystem requires ACH to support multiple file formats, communication protocols, and processing requirements while maintaining consistent processing quality across all origination sources.

 5. What are your upstream applications for receivables?

ACH receives inbound payments from external clearing networks and processes them for distribution to internal PNC systems:

Federal Reserve ACH network provides the primary source of inbound ACH transactions from other financial institutions, government entities, and third-party processors who initiate payments to PNC customer accounts.

Clearing house networks including private ACH operators provide additional sources of inbound ACH transactions that require processing and distribution to appropriate PNC customer accounts.

Correspondent banking relationships may generate inbound ACH transactions from partner financial institutions or specialized payment processors who route transactions through PNC for final delivery to customer accounts.

Return processing networks generate inbound ACH transactions related to returned payments, corrections, and other exception processing that requires specialized handling and customer notification procedures.

Government payment systems generate inbound ACH transactions for benefits payments, tax refunds, and other government-to-citizen payments that require processing and crediting to PNC customer accounts.

Third-party payment processors may generate inbound ACH transactions on behalf of their merchant or corporate clients who are making payments to PNC customers, requiring ACH to handle payments from diverse processing sources.

The inbound payment sources require ACH to maintain compatibility with multiple clearing networks, handle various transaction types and formats, and ensure accurate routing and processing of received payments across PNC's customer base.

 6. Of those downstream applications, which do you receive acknowledgments or notifications from?

ACH receives acknowledgments from select downstream systems with varying levels of detail and automation:

EPN (Electronic Payments Network) provides automated acknowledgments for outbound file transmissions, confirming successful receipt and initial processing of ACH files transmitted to clearing networks. These acknowledgments are critical for ensuring that outbound payments have been successfully delivered to clearing networks for settlement processing.

Core banking systems and CARS provide balancing reports and confirmations that verify successful receipt and processing of ACH transaction data. These balance confirmations help ensure that all ACH transactions have been properly posted to customer accounts and are reflected accurately in PNC's core banking systems.

EFG (Enterprise Fraud Gateway) provides file receipt confirmations when they receive ACH transaction files for fraud monitoring purposes, ensuring that fraud detection systems have access to complete ACH transaction data for analysis and monitoring.

Memo posting systems provide confirmations that ACH transaction data has been successfully processed for account memo posting, ensuring that customers can see pending ACH transactions in their account information before final settlement occurs.

Control total reconciliation occurs with various downstream systems where ACH sends transaction counts and dollar amounts that downstream systems confirm against their processing results, enabling identification of any processing discrepancies or missing transactions.

Manual monitoring processes supplement automated acknowledgments through operational procedures where ACH staff manually verify that critical files have been transmitted and received successfully, particularly for time-sensitive processing requirements.

The acknowledgment system provides multiple layers of confirmation to ensure that ACH processing results are successfully transmitted and processed by downstream systems that depend on ACH transaction data.

 7. Of those upstream applications, which do you receive acknowledgments or notifications from?

ACH provides comprehensive acknowledgments and confirmations to upstream applications based on processing results and client requirements:

Control total confirmations are provided to internal clients who submit payment files with control totals, enabling them to verify that ACH has received and processed the expected number of transactions and dollar amounts from their submitted files.

EDI (Electronic Data Interchange) systems receive control total confirmations and processing status reports that enable automated reconciliation of submitted payment files with ACH processing results.

VRU (Voice Response Unit) confirmations are provided to clients who call in to submit control totals for their payment files, providing immediate confirmation that files have been received and are processing correctly.

Automated control total files are sent to clients who prefer file-based confirmation of their payment submissions, providing detailed information about file receipt, processing status, and any identified issues.

File processing confirmations are available to clients who submit payment files and request confirmation that their files have been successfully processed, including details about accepted transactions, rejected transactions, and processing results.

Real-time processing status may be provided to certain upstream systems that require immediate feedback about payment processing status, particularly for time-sensitive payment submissions.

Exception reporting is provided to upstream systems when processing issues are identified, enabling them to take corrective action for rejected transactions or processing errors.

The acknowledgment strategy ensures that upstream applications and clients have appropriate visibility into ACH processing results while supporting their operational and reconciliation requirements.

 8. In what format do you receive transactions/files/data?

ACH supports multiple inbound data formats to accommodate diverse upstream application requirements:

NACHA format represents the standard ACH file format used for external clearing network communication and many internal PNC systems. NACHA formatting provides standardized field definitions, record structures, and validation rules that ensure consistent processing across the ACH network.

Proprietary formats are used for internal PNC applications including Core banking systems and General Ledger systems that may utilize customized data formats optimized for their specific processing requirements or legacy system constraints.

Standardized file structures accommodate various fixed-width, delimited, and other structured formats that upstream applications utilize based on their technical capabilities and integration preferences.

Electronic file transmission through secure protocols enables automated submission of ACH files from high-volume clients and internal systems that require reliable, secure file transfer capabilities.

VRU-based submissions allow clients to submit control totals and initiate file processing through voice response systems, providing an alternative submission method for clients who prefer telephone-based interaction.

Multiple format support enables ACH to serve diverse upstream applications with varying technical capabilities while maintaining consistent processing quality and ensuring that all submitted payments receive appropriate validation and processing.

The multi-format approach balances standardization requirements with practical integration needs across PNC's diverse payment processing ecosystem.

 9. In what format do you send transactions/files/data?

ACH transmits data in formats appropriate for each downstream destination:

NACHA format is used for transmissions to external clearing networks including the Federal Reserve and private clearing house operators, ensuring compliance with industry standards and clearing network requirements.

EPN format is used for Electronic Payments Network transmissions, providing specialized formatting required for EPN processing and settlement activities.

Proprietary formats are used for internal PNC systems including Core banking systems and General Ledger applications that require customized data formats optimized for their specific processing workflows and system architectures.

Standardized reporting formats are used for various downstream applications that require ACH transaction data for reporting, compliance monitoring, and business intelligence purposes.

Control file formats are used for transmissions that require specific control totals, batch headers, and trailer records that enable downstream systems to validate file completeness and processing accuracy.

Specialized formats may be used for specific downstream applications that have unique data layout requirements or processing constraints that require customized formatting approaches.

The output format strategy ensures that downstream systems receive ACH data in formats they can process effectively while maintaining data integrity and processing efficiency throughout the distribution process.

 10. Do you have any unique identifier that you add to the transactions from your system?

ACH implements a comprehensive identifier management strategy that balances standardization with internal tracking requirements:

Individual ID field preservation ensures that the standard ACH Individual ID field remains unchanged throughout processing, maintaining consistency with clearing network requirements and enabling end-to-end transaction tracking across the ACH ecosystem.

PAR number assignment involves ACH generating a unique reference number for every transaction processed through their system. The PAR (Pep Plus Assigned Reference) number provides internal tracking capability and supports operational monitoring and customer service requirements.

PAR number structure includes century digits, year digits, three-character Julian date, two zero-filled buffer positions for internal use, and a seven-character unique assigned number, creating a comprehensive identifier that supports both chronological organization and unique transaction identification.

Clearing network formatting involves modifying the PAR number for external transmission by removing internal formatting elements (century, year, Julian date) and replacing them with PNC's ABA routing number in the trace field, ensuring compliance with clearing network requirements while maintaining internal tracking capability.

Core system integration ensures that PAR numbers are transmitted to Core banking and other internal systems for comprehensive transaction tracking and customer service support, though the Individual ID field may not be included in all internal system transmissions.

Network compliance balances internal tracking requirements with clearing network standards, ensuring that external transmissions comply with ACH network requirements while maintaining internal operational capabilities.

The identifier strategy provides comprehensive transaction tracking throughout ACH processing while ensuring compliance with both internal operational requirements and external clearing network standards.

 11. Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction?

ACH maintains limited internal reporting capabilities while contributing to enterprise-wide payment lifecycle tracking through data streaming:

Transaction lifecycle limitations prevent ACH from providing comprehensive transaction lifecycle reporting because they don't stream the detailed tracking data required to monitor transaction progression from point A to point B within their processing workflows.

Processing transaction streaming occurs when ACH streams information about successfully processed transactions to COD, providing visibility into completed ACH processing activities for enterprise-wide reporting and analytics purposes.

Volume reporting capabilities are maintained through COD data feeds that support analysis of ACH processing volumes, trends, and operational performance metrics.

Returns monitoring utilizes COD feeds to track and report on ACH return transactions, enabling analysis of return patterns, return reasons, and originator performance related to ACH processing quality.

External reporting coordination involves collaboration with Brian Thompson's strategy and risk team who utilize ACH data for comprehensive reporting and oversight activities, though specific reporting platform details are managed by external teams.

Processing status visibility is limited to high-level processing completion rather than detailed transaction lifecycle tracking, reflecting ACH's focus on efficient processing rather than comprehensive status monitoring throughout individual transaction workflows.

Enterprise integration through COD streaming enables ACH processing data to contribute to broader payment lifecycle reporting initiatives even though ACH doesn't maintain comprehensive internal transaction tracking capabilities.

The reporting approach focuses on supporting enterprise-wide payment analytics and operational oversight while acknowledging limitations in detailed transaction lifecycle visibility within ACH processing workflows.

 12. Can a client check on the status of their payment?

ACH operates as a fire-and-forget system with limited client status checking capabilities:

VRU confirmation system provides clients with confirmation numbers when they call in to submit control totals for their payment files. The confirmation number (based on stone ID and control totals) enables clients to verify that their file has been received and is processing, but does not provide detailed transaction-level status information.

File processing confirmations are available as an opt-in service for clients who request confirmation that their submitted files have been successfully processed by ACH, providing basic processing completion status without detailed transaction tracking.

Successful transaction reporting is available as an opt-in service where clients can receive reports containing all transactions that were successfully processed by ACH from their submitted files, enabling them to identify which payments were completed successfully.

Limited status granularity means that most clients operate on a fire-and-forget basis where they submit payment files and assume successful processing unless they are notified of issues, rather than having access to detailed transaction status tracking.

Batch-oriented processing reflects ACH's operational model where status information is provided at the file or batch level rather than individual transaction level, consistent with traditional ACH processing approaches focused on efficiency over detailed tracking.

Opt-in service model requires clients to specifically request status reporting services rather than providing automatic status visibility, reflecting the operational efficiency focus of ACH processing workflows.

The status checking approach balances operational efficiency requirements with client needs for processing confirmation while maintaining the high-volume, low-cost processing model that characterizes ACH operations.

 13. What sort of data management are you doing? What type of database do you use?

ACH operates a multi-platform database architecture with specialized functions for each database environment:

DB2 database platform serves as the primary database technology across all ACH processing platforms, providing robust transaction processing capabilities required for high-volume ACH processing and maintaining the data persistence required for payment instruction tracking.

Three logical platforms each maintain their own separate DB2 database instances, with information stored on one database not accessible to the others, creating isolated processing environments that support different aspects of ACH operations or client segments.

Platform-specific data isolation means that transaction information processed on one platform is not shared with other platforms, requiring careful routing and processing management to ensure that transactions are processed on appropriate platforms for their requirements.

COD streaming integration occurs from processed files once ACH processing is complete, with transaction data flowing to Corporate Online Data warehouse systems for enterprise-wide reporting and analytics capabilities.

Processing-focused design emphasizes operational transaction processing over comprehensive data warehousing, with primary database functions supporting real-time ACH processing workflows rather than complex analytical or reporting queries.

ASIS integration involves a proprietary pre-processing system that also utilizes DB2 database technology for file ingestion, quality checking, and routing preparation before transactions are processed through the main ACH processing platforms.

The multi-platform approach enables ACH to optimize processing for different client segments or transaction types while maintaining consistent database technology and operational procedures across all processing environments.

 14. Is your database split between operational and reporting databases?

ACH maintains specialized database separation based on processing functions rather than traditional operational versus reporting divisions:

Three separate databases support different logical processing platforms, each optimized for specific ACH processing requirements or client segments rather than being divided between operational and reporting functions.

Processing-only databases are used exclusively for operational transaction processing and data warehousing, focusing on supporting real-time ACH processing workflows rather than comprehensive reporting capabilities.

COD-only database serves exclusively reporting purposes, receiving processed transaction data from ACH systems but not participating in operational processing activities.

Functional specialization means that each database platform serves specific processing requirements without duplication of data or functionality across platforms, creating clear separation of responsibilities and processing workflows.

No shared data architecture prevents information sharing between the operational processing databases, requiring careful transaction routing and platform selection to ensure appropriate processing for each transaction type.

External reporting dependency through COD integration eliminates the need for comprehensive internal reporting databases since enterprise-wide reporting and analytics are handled by specialized external systems.

The database architecture reflects ACH's focus on processing efficiency and platform optimization while ensuring that comprehensive reporting capabilities are available through appropriate enterprise data management systems.

 15. Is your data being streamed anywhere? For ex. a warehouse like COD?

ACH actively streams processed transaction data to COD as part of PNC's enterprise data management strategy:

Post-processing streaming occurs after ACH completes file processing, with comprehensive transaction information flowing to Corporate Online Data warehouse systems for enterprise-wide analytics and reporting capabilities.

Processed data focus means that ACH streams information about completed transactions rather than in-process data, ensuring that COD receives accurate, finalized transaction information for reporting and analytics purposes.

ASIS streaming considerations involve the pre-processing system that currently does not stream data to COD, though this capability is being considered for implementation to provide more comprehensive transaction lifecycle visibility.

Enterprise integration enables ACH transaction data to be combined with information from other payment processing systems within COD, supporting comprehensive payment analytics and cross-system reporting capabilities.

Reporting enablement through COD streaming provides the foundation for enterprise-wide payment reporting, business intelligence, and regulatory compliance monitoring that utilizes ACH processing data alongside information from other payment processing systems.

Lifecycle tracking potential could be enhanced through ASIS streaming implementation, which would provide visibility into pre-processing activities and enable more comprehensive transaction lifecycle monitoring across ACH processing workflows.

The streaming strategy balances operational processing efficiency with enterprise data management requirements while positioning ACH as a key contributor to PNC's comprehensive payment processing analytics and reporting capabilities.

 16. Is it possible for there to be a failure at your stage in the payments flow? If so, what happens if there is one?

ACH faces multiple types of failures with comprehensive recovery procedures tailored to different failure scenarios:

Pep Plus system failures represent the most significant failure type since Pep Plus serves as the core database engine behind all ACH processing. When Pep Plus fails, comprehensive system recovery procedures must be executed before the full impact of the failure can be assessed or resolved.

Platform-level failures can occur on any of the three logical processing platforms, requiring platform-specific recovery procedures that may involve database restoration, transaction reprocessing, and processing workflow resumption.

File processing failures may occur during various stages of file ingestion, validation, editing, or distribution, requiring identification of the failure point and appropriate recovery procedures based on the processing stage affected.

Network transmission failures can prevent successful delivery of files to downstream systems or clearing networks, requiring retransmission procedures and coordination with downstream applications to ensure processing completion.

ASIS pre-processing failures can prevent files from being properly prepared for main system processing, requiring specialized recovery procedures for the pre-processing system and potential manual intervention to ensure file processing continuation.

Recovery assessment procedures involve data teams utilizing COD information or direct file analysis to determine which transactions or processing workflows were impacted by system failures, enabling targeted recovery efforts.

Manual intervention capabilities support recovery scenarios that cannot be resolved through automated procedures, including transaction reprocessing, file reconstruction, and coordination with downstream systems to ensure complete processing recovery.

Impact analysis procedures utilize multiple data sources including COD streams and processing logs to assess the scope of failure impact and develop appropriate recovery strategies for affected transactions and processing workflows.

The comprehensive failure management approach ensures that ACH processing can recover effectively from various types of system, network, and processing failures while maintaining data integrity and processing completeness.

 17. Do you do any negative tracking or volume tracking to account for expected transactions on a certain day?

ACH implements selective volume monitoring with both automated and manual components:

Monthly volume reviews provide regular analysis of ACH processing volumes and patterns, enabling identification of significant volume changes or unusual processing patterns that may require investigation or operational adjustment.

Must-have file tracking includes manual monitoring for critical files that ACH must receive from clearing networks including the Federal Reserve and clearing houses. This manual tracking ensures that all required files are received and processed successfully.

Control total reconciliation enables identification of missing files from clients who submit control totals along with their payment files. When control totals are received without corresponding payment files, ACH can proactively contact clients to resolve the discrepancy.

Volume variability challenges make comprehensive negative tracking difficult because ACH volumes fluctuate significantly based on day of week, day of month, seasonal patterns, and various external factors that affect client payment behavior.

Client-specific limitations exist for clients who do not submit control totals, where ACH cannot identify missing files unless clients contact them directly about processing issues.

Desired monitoring enhancements include implementing comprehensive monitoring similar to other PNC systems where alerts are generated when expected files are not received, though this capability is not currently implemented across ACH processing.

Network file monitoring ensures that all required files from clearing networks are received and processed successfully, preventing processing gaps that could affect customer accounts or regulatory compliance.

The monitoring approach balances practical operational constraints with risk management requirements while identifying opportunities for enhanced monitoring capabilities that could improve operational oversight and client service.

 18. Do you get any notifications from downstream systems if they don't receive a file or transaction from you?

ACH receives limited notifications from downstream systems regarding missing files or transactions:

Core system alerting exists where Core banking systems will generate alerts if they do not receive expected ACH files, though this monitoring may be managed by IT teams rather than business operations teams.

File-level monitoring rather than transaction-level monitoring represents the scope of most missing file detection, where downstream systems monitor for expected file delivery rather than tracking individual transaction completion.

APN monitoring includes ACH actively monitoring their own file transmissions to ensure successful delivery to critical downstream systems, representing proactive monitoring rather than reactive notification from downstream systems.

Limited transaction-level visibility means that missing file notifications typically occur at the file or batch level rather than identifying missing individual transactions within successfully transmitted files.

Manual coordination procedures supplement automated notifications when downstream applications identify potential missing file or transaction issues, requiring operational coordination between ACH teams and downstream system operators.

Critical file focus concentrates monitoring efforts on must-have files and processing workflows where missing transmissions could have significant operational or regulatory impact rather than implementing comprehensive monitoring across all downstream integrations.

Operational escalation occurs when downstream systems identify missing files or processing discrepancies, but this typically involves manual coordination rather than automated notification systems specifically designed to detect missing ACH transmissions.

The notification approach reflects the distributed nature of ACH processing where comprehensive missing file detection requires coordination across multiple systems and operational teams rather than relying solely on automated notification mechanisms.
