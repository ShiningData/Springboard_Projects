Question 1: Where does your application/platform sit in the flow of payments (what do you receive from an upstream system, if any? What do you send downstream)?

DSP (Data Streaming Platform) sits at the very end of the payment processing flow and serves as a data repository rather than a processing engine. DSP is not a system of record like core banking systems but instead receives data from multiple systems of record after payments have already been fully processed. Payments are already completely processed by the time they reach DSP, and DSP does not change or further process this data. DSP then makes this data available to various banking channels like mobile banking (WBA) and online banking for customer presentation through APIs. DSP appears to be the final destination for payment data storage and access, with no further downstream systems receiving data directly from DSP.

Question 2: In what format do receive transactions/files/information?

DSP receives data from various systems of record through streaming mechanisms. All system of records send their data to DSP, which houses the information either in Kafka topics or in backend databases. The platform utilizes Kafka and streaming applications as part of their technology infrastructure to manage this incoming data flow. The specific data format details are not elaborated upon in the discussion, but the emphasis on topics suggests stream-based data ingestion.

Question 3: In what format do send transactions/files/information?

DSP provides data access exclusively through APIs that enable banking channels to present information to customers. These APIs allow other teams and channels to access payment data for presentation to customers through various interfaces including mobile banking and online banking platforms. DSP focuses on providing quick and easy data access using modern streaming technology rather than file-based data distribution. The platform does not send traditional files but rather provides real-time data access through API endpoints.

Question 4: Do you have any unique identifier that you add to the transactions from your system? Do you pass that to the next system in the step? Do you create a new one? If so, do you maintain an index?

This aspect of DSP operations was not discussed during the meeting. No information was provided regarding unique identifiers, transaction IDs, or indexing mechanisms that DSP might use or create for the payment data they manage.

Question 5: Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction? If so, where is that hosted? Are there consumers for said report today?

DSP maintains limited reporting capabilities that focus primarily on platform health rather than payment-specific analytics. The platform does not specifically monitor or report on individual payments but instead concentrates on ensuring the overall health of the streaming platform and verifying data integrity. DSP performs reconciliation activities to ensure that received data matches what should be present and compares information across data centers to maintain synchronization. The team mentioned establishing a reporting database, but this contains only certain tables rather than comprehensive operational transaction data.

Question 6: Is your data being streamed (KAFKA stream, etc) anywhere? For example, a warehouse like COD.

DSP itself serves as the streaming platform using Kafka technology and streaming applications to manage data flow. The platform houses data in Kafka topics and utilizes streaming infrastructure, but DSP does not feed data into other data warehouses or downstream analytical systems. While individual systems of record may send data to various warehouses, DSP operates as an endpoint for streaming data rather than a source for further data warehousing activities. DSP focuses on providing real-time access to payment data rather than batch processing for analytical purposes.

Question 7: What happens if a file dies at your step in the process?

Error handling and file processing failure procedures at the DSP level were not discussed during the meeting. No information was provided regarding how DSP manages processing failures or data ingestion issues.

Question 8: What do you do if you didn't get a file or transaction that you were expecting to get on a certain day?

DSP does not perform volume-based monitoring or alerting for missing transactions or unusual payment volumes. The platform does not specifically monitor payment flows or generate reports based on payment volume expectations. DSP's monitoring efforts focus entirely on platform health and data integrity rather than tracking transaction volumes, timing patterns, or identifying missing payment data. The platform operates as a passive recipient of data from systems of record rather than actively monitoring payment processing patterns.

Question 9: Can a client check on the status of their file?

Customer access to payment status information through DSP was not directly addressed in the discussion. While DSP enables banking channels to present payment data to customers through API access, the meeting did not specify what level of payment detail, status information, or transaction tracking capabilities are made available to customers through these channels.

Question 10: Do you get a notification if your downstream system doesn't receive a file from you?

This question does not apply to DSP's operational model since the platform serves as the endpoint of the data flow rather than sending data to downstream processing systems. DSP provides data access through APIs to banking channels but does not push data files to other systems that would require delivery confirmation or failure notification processes.

Question 11: Others

Access and Security Management: DSP maintains strict production database access controls to protect customer-facing infrastructure. The platform avoids providing direct database access for analytical purposes to prevent performance overhead and potential disruptions to production operations. Teams requiring data access must establish their own pipelines and work through proper channels to access DSP data for customer-facing functionality.

Business Scope Definition: DSP primarily handles retail payment data rather than commercial corporate payments, though the platform includes some small business payment information since small business operations typically fall under retail banking categories. The team confirmed their focus remains on retail payment processing channels.

Platform Architecture Philosophy: DSP operates without business logic or payment processing capabilities, serving purely as a data access and storage layer. The platform functions as a data holder that facilitates channel access for customer presentation rather than performing any payment processing, validation, or transformation activities.

Data Integrity Operations: DSP performs comprehensive reconciliation processes to ensure data consistency and accuracy across their infrastructure. These reconciliation activities compare incoming data against stored information and synchronize data across multiple data centers to maintain platform reliability and data integrity.

Technology Infrastructure: DSP utilizes modern streaming technology including Kafka and streaming applications to provide real-time data access capabilities to various banking channels, enabling quick customer data presentation and supporting multiple concurrent access patterns for different banking services.
