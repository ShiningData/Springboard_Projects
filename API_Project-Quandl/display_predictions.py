 1. Where does your application/platform sit in the flow of payments? (Beginning, middle, end)

PMT operates as a middleware integration platform positioned firmly in the middle of the payment flow within the CNIB (Corporate and Institutional Banking) space. The system is explicitly defined as middleware and serves as the central integration hub that connects various upstream payment engines with downstream applications and services.

PMT's positioning as middleware means it receives payment instructions and data from upstream payment engines like GPP (Global Payment Platform) or other payment systems, then orchestrates the complex web of downstream integrations required to execute, monitor, and report on payment transactions. The system does not initiate payments nor serve as the final destination, but rather acts as the critical integration layer that enables communication between payment engines and the numerous supporting systems required for complete payment processing.

Their middleware role involves handling four distinct types of services: real-time integration services that support payment execution, intraday notification services for applications that need immediate payment status updates, end-of-day batch services for mainframe applications that cannot process real-time data, and payment support services that provide essential data feeds and configuration updates to payment engines.

 2. What are your downstream applications for originations?

PMT interfaces with an extensive array of downstream applications that support payment origination processing:

Real-time and Near Real-time Integration Services include multiple critical systems. CARS (Core Account Reporting System) handles memo posting for immediate account updates. CIF (Customer Information File), which is being replaced by MDM (Master Data Management), provides customer lookup capabilities. MCA (Money Center Account) supports account verification and status checking. RTS (Real-Time Sanctions) performs sanctions screening for compliance. ACBS (Account Control and Billing System) manages daylight overdraft calculations and credit decisions. PRS (Payment Routing Services) determines optimal routing paths for payments. EFG (Enterprise Fraud Gateway) provides fraud detection and prevention services. IVR (Interactive Voice Response) systems support customer service interactions.

Intraday Services encompass applications that require immediate notification when payments are executed or when specific payment events occur. These systems need real-time awareness of payment status changes to update their own processing workflows and customer-facing systems.

End-of-Day Batch Services include mainframe applications that cannot process real-time data streams. STX (Securities Trading Exchange), CFE (Cash Flow Engine), Core banking systems, GL (General Ledger), and reconciliation applications all receive batch files containing payment transaction summaries and status updates at the end of each business day.

Payment Support Services provide essential infrastructure support including OIM (Oracle Identity Management) extracts that are fed to GPP for access control updates, and various data files downloaded from external sources such as lists of banks supporting real-time payments that are provided to PRS for routing decisions.

The system supports all major payment types including wire transfers, real-time payments, and Canadian ACH, with the notable exception of domestic ACH which remains self-contained on mainframe systems and does not require PMT integration services.

 3. What are your downstream applications for receivables?

PMT does not make a distinction between originations and receivables in their processing model. The transcript indicates that payment instructions come directly to payment engines like GPP first, and PMT does not typically receive outbound payments directly. The only potential exception mentioned is Swift payments, which may originate from SA (Securities Administration) and flow through PMT to payment engines, but this represents a specialized case rather than standard receivables processing.

The middleware architecture means that both inbound and outbound payments are initiated first by the payment engine, with PMT providing supporting integration services regardless of payment direction. The downstream applications and services remain consistent whether supporting origination or receivables processing, as PMT's role focuses on integration orchestration rather than payment direction classification.

 4. What are your upstream applications for originations?

PMT's upstream architecture centers primarily around GPP (Global Payment Platform) and other payment engines that serve as the primary sources of payment instructions and transaction data. The payment engines receive payment instructions through various channels including staging systems, PSG (Payment Services Gateway), or directly from clearing networks, then engage PMT for the necessary downstream integrations.

Swift payments represent a notable exception to the standard upstream flow, as they may originate from SA (Securities Administration) systems and flow through PMT to payment engines before proceeding to downstream processing. This creates a more complex upstream relationship where PMT serves as both a middleware integration platform and a component in the payment instruction routing path.

The upstream relationship with payment engines involves PMT receiving requests for various services including real-time account lookups, sanctions screening, fraud detection, routing decisions, and numerous other supporting functions required for payment execution. PMT does not impose format requirements on upstream systems, instead adapting to whatever communication protocols and data formats the payment engines utilize.

Communication protocols with upstream systems vary based on technical capabilities, including CICS for mainframe interactions, MQ (Message Queue) for systems supporting message-based communication, APIs for modern applications like RTS, and RPC (Remote Procedure Call) for specialized applications like ACBS.

 5. What are your upstream applications for receivables?

As with downstream applications, PMT does not distinguish between originations and receivables in their upstream architecture. The same payment engines and upstream systems provide both types of payment instructions, with PMT providing consistent integration services regardless of payment direction.

The upstream application set remains consistent whether supporting receivables or originations, reflecting PMT's role as middleware that responds to service requests from payment engines rather than managing payment-specific workflows based on transaction direction.

 6. Of those downstream applications, which do you receive acknowledgments or notifications from?

PMT's acknowledgment model varies significantly based on the type of service and downstream application capabilities:

Real-time Integration Services like RTS (Real-Time Sanctions) and EMG have strictly choreographed request-response mechanisms with detailed status tracking and acknowledgment protocols. These systems require immediate responses because GPP needs to make routing and execution decisions based on their feedback, creating a tightly coupled integration model with comprehensive acknowledgment handling.

Intraday Services operate primarily on a fire-and-forget model where PMT sends notifications to downstream applications but does not require acknowledgments. This design decision prevents imposing additional workload on receiving applications that were not originally designed to provide acknowledgment capabilities. The fire-and-forget approach reflects the notification-oriented nature of these services where PMT's responsibility ends with successful transmission.

End-of-Day Batch Services similarly operate without acknowledgment requirements, though applications may generate their own monitoring and alerting if expected files are not received within established timeframes.

Infrastructure-level acknowledgments may exist at the communication protocol level (such as MQ message delivery confirmation or CICS transaction completion), but business-level acknowledgments indicating successful processing are generally not implemented across the downstream application portfolio.

The acknowledgment strategy reflects the practical challenges of implementing comprehensive acknowledgment handling across diverse downstream applications with varying technical capabilities and processing models.

 7. Of those upstream applications, which do you receive acknowledgments or notifications from?

PMT's upstream acknowledgment handling differs significantly from downstream patterns:

GPP (Global Payment Platform) historically did not provide comprehensive request-response models, which created operational challenges for PMT. This led to the development of compensating mechanisms including alert systems, timeout controls, and pending queue monitoring. PMT implemented various workarounds such as generating alerts when requests sent to PMT remain unacknowledged for extended periods (typically five minutes or more).

Pending queue management became necessary to track requests that have been sent to PMT but have not received responses, enabling operational teams to identify potential processing delays or system issues.

Alert and control systems monitor for situations where PMT sends information to downstream systems but does not receive expected responses within defined timeframes, triggering operational investigation and potential remediation activities.

The limitations in upstream acknowledgment handling reflect the challenges of working with vendor-provided payment engines that may have architectural gaps in their acknowledgment and status reporting capabilities. PMT had to develop extensive compensating controls to provide the operational visibility and reliability required for production payment processing.

Enhanced monitoring includes various operational controls and dashboard capabilities that PMT operations teams use to track the health and performance of upstream integrations, even in the absence of comprehensive built-in acknowledgment mechanisms.

 8. In what format do you receive transactions/files/data?

PMT operates with a format-agnostic approach that represents one of its key value propositions as middleware. Rather than imposing specific format requirements on interfacing applications, PMT adapts to whatever formats upstream systems utilize, providing flexibility and reducing integration complexity for payment engines and other upstream applications.

Communication protocols vary based on downstream application capabilities and requirements. CICS (Customer Information Control System) is used for mainframe applications like CARS that only understand CICS transactions. MQ (Message Queue) supports applications capable of message-based communication including MCA and various notification services. APIs serve modern applications like RTS that support RESTful web service interactions. RPC (Remote Procedure Call) accommodates specialized applications like ACBS that require direct procedure invocations.

Data format flexibility extends beyond communication protocols to include various data structures, field layouts, and content organizations that reflect the diverse technical architectures across PNC's payment ecosystem. PMT maintains translation and transformation capabilities to bridge format differences between upstream and downstream systems.

Protocol customization means that PMT develops specific interface implementations tailored to each downstream application's technical capabilities and preferences, ensuring optimal integration performance while minimizing the burden on interfacing applications to adapt their existing formats or protocols.

This format flexibility represents a core architectural principle that enables PMT to serve as effective middleware across PNC's diverse application landscape without forcing standardization that would require extensive modifications to existing systems.

 9. In what format do you send transactions/files/data?

PMT maintains the same format-agnostic approach for outbound data transmission, adapting to the specific technical requirements and capabilities of each downstream application:

Real-time integrations use protocols appropriate for each target system. CICS transactions for mainframe applications that require structured transaction processing. MQ messages for applications supporting asynchronous message processing. API calls for modern web service-based applications. RPC calls for systems requiring direct procedure invocation.

Batch file formats for end-of-day processing vary based on mainframe application requirements, with PMT generating files in formats that downstream applications can process without modification or additional transformation steps.

Intraday notification formats are customized for each receiving application's data structure requirements and processing capabilities, ensuring that notification content is immediately usable without requiring format conversion by the receiving system.

COD (Corporate Online Data) integration occurs through MQ (Message Queue) transmission, where PMT sends data over MQ protocols that COD consumes and inserts into their database systems for data warehousing and analytical purposes.

The outbound format strategy mirrors the inbound approach, emphasizing PMT's role as a format translation and protocol adaptation layer that enables seamless integration across PNC's diverse technical ecosystem without imposing standardization requirements on existing applications.

 10. Do you have any unique identifier that you add to the transactions from your system?

PMT utilizes the MID (Message Identifier) system that originates from upstream payment engines rather than generating their own unique identifiers. The MID serves as the primary transaction tracking mechanism throughout the entire payment lifecycle, providing consistent reference capability across all systems involved in payment processing.

MID lifecycle management involves PMT receiving the Message Identifier from upstream systems (primarily GPP) and ensuring that this identifier is consistently passed to all downstream applications that require transaction tracking capabilities. This creates a unified tracking mechanism that enables end-to-end payment monitoring and troubleshooting across the entire payment processing ecosystem.

Identifier consistency across downstream systems means that applications receiving notifications or data from PMT can correlate information with upstream payment engines and other downstream systems using the same MID reference, facilitating comprehensive payment lifecycle tracking and operational monitoring.

No additional identifier generation by PMT reflects their middleware positioning where they serve as a conduit for existing identifiers rather than creating additional tracking mechanisms that could complicate system integration or create identifier conflicts across the payment processing chain.

The MID-based approach ensures that transaction tracking remains consistent and unified across all payment processing systems while avoiding the complexity and potential conflicts that could arise from multiple identifier systems operating within the same payment processing workflow.

 11. Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction?

PMT does not provide direct reporting capabilities for operations teams or business users. Instead, PMT serves as a data provider for downstream reporting systems that create operational dashboards, business intelligence reports, and analytical tools used by various PNC teams.

Data provision model means that PMT focuses on ensuring accurate and timely data transmission to systems like COD (Corporate Online Data) and other data warehousing platforms that specialize in reporting and analytics. PMT's role involves ensuring data quality, completeness, and timeliness rather than creating user-facing reports or dashboards.

COD integration represents the primary mechanism for making PMT transaction data available for reporting purposes. Data flows from PMT to COD through MQ (Message Queue) transmission, where COD systems consume the data and integrate it with information from other payment processing systems to create comprehensive payment lifecycle reporting.

Operational monitoring exists within PMT for system health and performance tracking, but this focuses on technical metrics like transaction volumes, processing times, error rates, and system availability rather than business-oriented reporting that would be consumed by payment operations teams or business stakeholders.

Downstream reporting responsibility reflects PMT's architectural role as middleware where specialized reporting and analytics systems handle the complex requirements for operational dashboards, trend analysis, compliance reporting, and business intelligence rather than building these capabilities into the integration platform itself.

The separation between data provision and reporting creation allows PMT to focus on integration excellence while enabling specialized reporting platforms to deliver sophisticated analytical capabilities tailored to specific business and operational requirements.

 12. Can a client check on the status of their payment?

PMT does not provide direct client-facing payment status capabilities due to their middleware positioning in the payment processing architecture. Client status inquiries would be directed to payment engines like GPP, which may then request supporting information from PMT if needed for status determination.

Indirect status support occurs when payment engines require additional information to respond to client status inquiries. In these scenarios, PMT can provide real-time lookups from various downstream systems including account status information, sanctions screening results, routing information, or other supporting data that enables payment engines to provide comprehensive status responses to clients.

Status information aggregation represents PMT's potential contribution to client status inquiries through their ability to query multiple downstream systems and provide consolidated information back to payment engines. However, PMT would not be aware of the original purpose of these requests or have direct interaction with clients seeking payment status information.

Payment engine responsibility for client interaction means that systems like GPP handle all direct client communication regarding payment status, with PMT serving as a supporting integration layer that enables payment engines to access necessary information from across PNC's payment ecosystem.

The architecture ensures that client interactions remain consistent and are handled by systems specifically designed for client relationship management, while PMT focuses on providing the comprehensive integration capabilities that enable payment engines to deliver accurate and timely status information.

 13. What sort of data management are you doing? What type of database do you use?

PMT operates a multi-database environment that reflects both their internal operational needs and their integration responsibilities across PNC's payment ecosystem:

Internal Oracle database serves PMT's application requirements including logging, application parameters, configuration management, and transient data storage. This database handles PMT-specific operational data rather than serving as a comprehensive payment transaction repository.

Direct database access to other applications' databases represents a key architectural capability that Enterprise Architecture has specifically authorized for PMT as an integration platform. This includes direct access to PRT (Payment Routing Table) databases and PME (Payment Management Engine) databases, both of which utilize Oracle database technology on Linux platforms.

Integration database strategy allows PMT to query downstream application databases directly rather than requiring all data access to occur through application APIs or file transfers. This direct access capability enables more efficient real-time integration services and reduces the complexity of data retrieval for supporting payment processing operations.

Transient data management involves using PMT's internal database for temporary storage during complex processing workflows, particularly for end-of-day batch processes where data may be accumulated throughout the day before being formatted and transmitted to downstream applications at scheduled intervals.

Database diversity across the payment ecosystem means that PMT must support integration with various database technologies used by different applications, though Oracle remains the predominant database platform across most payment processing systems.

The multi-database approach enables PMT to provide comprehensive integration services while maintaining separation between internal operational data and the external systems they integrate with.

 14. Is your database split between operational and reporting databases?

PMT operates with a single internal database that serves neither traditional operational nor reporting functions in the conventional sense. Instead, their database functions as an application support repository containing logging information, application parameters, configuration data, and transient processing data.

Transient data management represents the primary operational use of PMT's database, particularly for complex processing workflows like end-of-day batch operations. During these processes, PMT may accumulate data throughout the day, use the database to build output files, and then transmit the completed files to downstream applications before purging the temporary data.

Data retention policy typically involves maintaining transient data for approximately seven days before purging, reflecting the temporary nature of most data stored in PMT's internal database. This short retention period indicates that the database serves processing support functions rather than long-term operational or reporting requirements.

Configuration and parameter storage includes application settings, interface configurations, routing tables, and other relatively static data required for PMT's integration operations. This data supports PMT's middleware functions rather than providing operational payment transaction storage.

No reporting database separation exists because PMT does not serve as a reporting platform. Instead, reporting data flows to specialized systems like COD where comprehensive reporting databases are maintained separately from operational processing systems.

The single-database approach reflects PMT's focused role as integration middleware where database requirements center on supporting integration operations rather than providing comprehensive transaction storage or analytical capabilities.

 15. Is your data being streamed anywhere? For ex. a warehouse like COD?

PMT actively streams data to COD (Corporate Online Data) warehouse systems through MQ (Message Queue) transmission protocols. This represents a key component of PNC's data warehousing strategy where transaction and integration data flows from operational systems to centralized analytical platforms.

MQ-based data transmission provides reliable, asynchronous data streaming that ensures COD receives comprehensive information about payment processing activities, integration events, and transaction status changes processed through PMT's middleware layer.

COD consumption and integration involves COD systems consuming the MQ messages from PMT and inserting the data into their database systems where it becomes available for reporting, analytics, business intelligence, and compliance monitoring purposes.

Data warehousing architecture enables PMT to focus on operational integration excellence while ensuring that comprehensive payment processing data remains available for analytical and reporting purposes through specialized warehouse systems designed for these functions.

Real-time data streaming means that COD receives near real-time updates about payment processing activities, enabling timely reporting and monitoring capabilities for business and operational stakeholders who rely on current information for decision-making and oversight.

The streaming relationship with COD represents PMT's contribution to PNC's broader data management strategy, ensuring that integration layer activities are captured and made available for enterprise-wide analytical and reporting capabilities.

 16. Is it possible for there to be a failure at your stage in the payments flow? If so, what happens if there is one?

PMT faces multiple types of potential failures given their central role as payment processing middleware, with different failure handling strategies for each type of service:

Real-time service failures are immediately communicated upstream to the calling payment engines, allowing GPP and other upstream systems to make appropriate decisions about payment processing continuation, alternative routing, or transaction rejection. The real-time nature of these integrations requires immediate failure notification to prevent payment processing delays or incorrect routing decisions.

Intraday service failures create a different challenge because downstream applications expect notifications but payment engines may not care about notification delivery failures. When intraday notification failures occur, PMT generates automated incidents that are monitored by PMT's run-the-bank operational team. These incidents trigger investigation and resolution procedures to restore notification capabilities and address any missed notifications.

End-of-day batch failures similarly generate automated incidents for operational team investigation. These failures can have significant downstream impact because mainframe applications and reconciliation systems depend on receiving complete and accurate batch files for their processing cycles.

Support service failures for applications like OIM extracts or PRS data feeds also generate incidents because these failures can impact payment engine capabilities and routing accuracy.

Incident management workflow involves PMT's operational team investigating failure root causes, determining whether issues are infrastructure-related (requiring infrastructure team involvement) or application-specific (requiring PMT development team attention), and implementing appropriate resolution procedures.

Failure escalation occurs when PMT cannot resolve issues independently, triggering involvement of downstream application teams, infrastructure specialists, or upstream payment engine teams depending on the failure type and scope.

The comprehensive failure handling approach ensures that payment processing disruptions are quickly identified, properly escalated, and resolved through coordinated team efforts across PNC's payment ecosystem.

 17. Do you do any negative tracking or volume tracking to account for expected transactions on a certain day?

PMT implements limited volume tracking that varies by service type and operational requirements:

General processing approach follows an event-driven model where PMT processes data when received and does not process when no data is available. This reflects their middleware role where transaction volume depends entirely on upstream payment engine activity rather than PMT-driven expectations.

End-of-day volume monitoring represents the primary exception to the general approach, where Raj (the run-the-bank manager) manually monitors batch processing volumes for unusual patterns. If end-of-day volumes appear significantly higher or lower than expected patterns, operational investigation may be initiated to ensure processing accuracy and identify potential issues.

Manual monitoring process rather than automated systems handles the volume tracking that does occur, indicating that comprehensive negative tracking is not implemented as a standard operational procedure.

Limited scope of volume tracking reflects PMT's position as middleware where transaction volumes are determined by upstream payment engines and client activity rather than PMT-specific processing requirements.

Future considerations suggest that more comprehensive volume tracking could be implemented if operational requirements change, but current architecture and operational procedures do not include systematic negative tracking or automated volume validation.

The selective approach to volume tracking balances operational oversight requirements with the practical realities of middleware positioning where transaction volumes are largely outside PMT's direct control or influence.

 18. Do you get any notifications from downstream systems if they don't receive a file or transaction from you?

PMT receives selective notifications from downstream systems, primarily from mainframe applications that have more sophisticated monitoring capabilities:

Mainframe application monitoring includes systems like CFE (Cash Flow Engine) and GL (General Ledger) related applications that have automated monitoring for missing files. These systems generate alerts and reach out to Raj's operational team when expected files are not received within established timeframes.

Automated mainframe tools provide better capabilities for monitoring missing files or transactions compared to other application types. Mainframe environments typically include comprehensive job scheduling and file monitoring tools that can detect when expected processing inputs are not received.

Manual notification process occurs when downstream application operational teams identify missing files or data and contact PMT's run-the-bank team for investigation and resolution. This manual escalation handles situations where automated monitoring may not exist or may not cover all integration scenarios.

Limited coverage means that not all downstream applications provide missing file notifications, particularly newer applications or those without sophisticated operational monitoring capabilities. Many applications simply wait for data to arrive rather than actively monitoring for missing transmissions.

Infrastructure-level monitoring may exist at the MQ or file transfer level to detect transmission failures, but business-level monitoring for missing content varies significantly across downstream applications.

The notification approach reflects the mixed technological environment across PNC's payment ecosystem, where mainframe applications provide more comprehensive monitoring capabilities than other application types, requiring PMT to maintain multiple approaches to failure detection and resolution.
