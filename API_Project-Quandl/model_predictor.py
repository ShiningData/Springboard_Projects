Question 1: Where does your application/platform sit in the flow of payments (what do you receive from an upstream system, if any? What do you send downstream)?

DSP (Data Streaming Platform) sits at the very end of the payment processing flow and serves as a data repository rather than a processing engine. DSP is explicitly "not a system of record like core or cause." Instead, DSP receives data from multiple systems of record after payments have already been fully processed. The transcript states: "we're at the very end. The payments are already being processed. Whatever process the payment goes through, it is already gone through that and it doesn't change when it gets to us." DSP then makes this data available to channels like WBA (mobile banking) and online banking for customer presentation. There's no mention of DSP sending data further downstream - it appears to be the final destination for payment data storage and access.

Question 2: In what format do receive transactions/files/information?

DSP receives data from various systems of record, but the specific format is not detailed in this transcript. The transcript mentions that "all these system of records will send us their data" and that DSP houses it "either in topics or and or um a database in the back end." The mention of "topics" suggests they may receive data through Kafka topics or similar streaming mechanisms, and the transcript references "Kafka and streaming apps" as part of their technology stack.

Question 3: In what format do send transactions/files/information?

DSP provides data access through APIs to enable channels to present information to customers. The transcript states DSP provides "APIs to get to the data, uh, to present back to the customer" and enables "other teams to uh channels to access that data, um, to present to the customer, you know, whether it's, you know, WBA or online banking." The specific API formats are not detailed in the transcript.

Question 4: Do you have any unique identifier that you add to the transactions from your system? Do you pass that to the next system in the step? Do you create a new one? If so, do you maintain an index?

This question is not addressed in the DSP transcript. There's no discussion of unique identifiers, transaction IDs, or indexing mechanisms that DSP might use or create.

Question 5: Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction? If so, where is that hosted? Are there consumers for said report today?

DSP has limited reporting capabilities focused on platform health rather than payment-specific analytics. The transcript mentions they have "some reporting" but clarifies "we don't specifically monitor payments or report on payments." Their monitoring is "mostly around the health of the platform and make sure the data um is what it should be, everything's present." They do perform reconciliation to ensure data integrity and synchronization across data centers. The transcript mentions they were "standing up the reporting database" but notes it's not comprehensive operational data, just "certain tables."

Question 6: Is your data being streamed (KAFKA stream, etc) anywhere? For example, a warehouse like COD.

DSP itself is the streaming platform using Kafka technology. The transcript explains DSP uses "Kafka and streaming apps" and houses data "in topics." However, DSP does not feed into other data warehouses - the speaker states "I don't think we do" when asked about feeding data warehouses, clarifying that "System of records do" but DSP doesn't. DSP appears to be the endpoint for streaming data rather than a source for further data warehousing.

Question 7: What happens if a file dies at your step in the process?

This question is not addressed in the DSP transcript. There's no discussion of file processing failures or error handling procedures at the DSP level.

Question 8: What do you do if you didn't get a file or transaction that you were expecting to get on a certain day?

DSP does not perform volume-based monitoring or alerting for missing transactions. The transcript states: "we don't do anything specific to, you know, they certainly function um or um, you know, for example, payments. We don't specifically monitor payments or report on payments." Their monitoring focuses on platform health and data integrity rather than transaction volume or timing expectations.

Question 9: Can a client check on the status of their file?

This question is not directly addressed in the DSP transcript. However, since DSP enables channels to present payment data to customers through APIs, it's implied that customers can view their payment information through banking channels, but the transcript doesn't specify what level of detail or status information is available.

Question 10: Do you get a notification if your downstream system doesn't receive a file from you?

This question is not applicable to DSP since they appear to be at the end of the data flow rather than sending data to downstream systems. DSP provides data access through APIs but doesn't appear to push data to other systems.

Question 11: Others

Access and Security Concerns: DSP maintains strict access controls for their production databases. They explicitly state they prefer not to provide direct database access for analytics purposes because "this is production, customer facing, um, infrastructure that we don't want, you know, any uh quote unquote noise nor no uh putting overhead on on the databases."

Scope Clarification: DSP primarily handles retail payments rather than commercial corporate payments, though they indicated some small business data may be included since small business "technically fall under retail."

No Business Logic: DSP emphasizes they don't perform business logic or payment processing - they're purely a data access layer. As stated: "there's no really business logic per se, um, within DSP, we're really um... the holders of the data and and to help with those channels to present to the customer."

Data Integrity Focus: DSP performs reconciliation activities to ensure data consistency, comparing what they're receiving against what they have and synchronizing across data centers to maintain data integrity.

Technology Stack: DSP uses modern streaming technology including Kafka and streaming applications to provide real-time data access capabilities to various banking channels.
