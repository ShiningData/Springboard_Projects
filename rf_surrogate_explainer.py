Based on the meeting transcript provided, here are the detailed answers to each question:

**1. Where does your application/platform sit in the flow of payments? (Beginning, middle, end)**

The application sits at the beginning of the payments flow. The team operates as the customer client-facing application where clients call the API, which comes to them first. They perform initial validations and then send requests to backend applications for processing. Their CAP APIs allow clients to directly send payments through two methods: API directly to payments infrastructure or API to Pinnacle Connected payments.

**2. What are your downstream applications for originations?**

For originations, they have three downstream systems: Payment Staging (PSG) for regular payments, PPS for Pinnacle Connected payments (Itic), and PTT for direct to debit payments.

**3. What are your downstream applications for receivables?**

For receivables, the downstream application is REC (receivables platform), and they pull information from Pinnacle. The team clarified that they are just returning information, as the receivables platform receives all the payments information and they pull the data back to the client.

**4. What are your upstream applications for originations?**

For originations, they have direct clients calling the APIs, and also have three-legged clients who come through their platforms PIF and PIK (Pinnacle Connect platforms) which then call CAP. There are also some network layers at the top of CAP including F5 and APG.

**5. What are your upstream applications for receivables?**

For receivables, PIF calls PIF as the upstream application.

**6. Of those downstream applications, which do you receive acknowledgments or notifications from?**

When the initial request goes through, they receive an acknowledgement that the downstream applications have received the request.

**7. Of those upstream applications, which do you receive acknowledgments or notifications from?**

They send acknowledgments to upstream systems. When payments come in through Pinnacle Connect, the platforms call CAP and they provide a status of that payment. They operate as a pass-through where whatever they receive back from the backend downstream applications gets sent up to their clients and the platforms.

**8. In what format do you receive transactions/files/data?**

They receive data in JSON format through JSON-based data structures and JSON-based REST APIs. They do have some limited integration with integrated payables file spec for Pinnacle Connect, and some file-based payments for legacy systems.

**9. In what format do you send transactions/files/data?**

They send data in JSON format. All their downstream systems support JSON-based REST integration, so the JSON data remains the same throughout the flow from user to CAP to downstream with some internal configurations or mapping.

**10. Do you have any unique identifier that you add to the transactions from your system? Do you pass that to the next system in the flow? If not are you receiving a unique ID from a downstream application that you continue to pass upstream?**

They utilize two unique identifiers: a trace ID which is a PNC-generated end-to-end ID, and a customer reference which is client-supplied. The trace ID is generated within the CAP application for payments API, and for Pinnacle Connected payments, the PPS or Pinnacle system generates the trace ID.

**11. Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction? If so, where is that hosted? Who are the consumers for said reporting?**

They store data in CAP databases and it is consumed by TAP. However, they do not capture the complete lifecycle of a transaction in terms of status changes over time within CAP. They do capture audit information for approximately 90 days showing when customers made calls and what data went in and out, but not the actual lifecycle of status changes.

**12. Can a client check on the status of their payment?**

Clients can check payment status through two methods: they can use unique identifiers (trace ID and customer reference) to make a GET call to see the latest status of transactions, and there is a webhook capability where they send notifications to clients when status changes occur, allowing clients to then make a GET call to see what changed.

**13. What sort of data management are you doing? What type of database do you use?**

They use an Oracle database, specifically Oracle Exadata for their data management.

**14. Is your database split between operational and reporting databases?**

They maintain just one database that primarily performs auditing functions for a period of approximately 90 days to track when payments were made and when status check requests were made.

**15. Is your data being streamed anywhere? For ex. a warehouse like COD?**

The data currently resides in Oracle Exadata. TAP consumes data from CAP databases, but specific details about streaming to other warehouses were not provided.

**16. Is it possible for there to be a failure at your stage in the payments flow? If so, what happens if there is one?**

Failures can occur at their stage through several mechanisms. They perform field-level validations when receiving initial requests, and there can be service network-level issues at the API level, and authentication checks. If someone lacks access to certain entitlements, they can reject those calls, and they perform account and operator-level checks. When failures occur, clients receive a 400-level HTTP status code with an error response indicating the failure, and they are asked to resend the payment after correcting the errors.

**17. Do you do any negative tracking or volume tracking to account for expected transactions on a certain day?**

They have reporting mechanisms in place that they share with leadership regarding volume for their products. They capture volume data so that if there is a negative impact resulting in less volume in a certain week or month, they can investigate what is occurring.

**18. Do you get any notifications from downstream systems if they don't receive a file or transaction from you?**

The team was not aware of any systems currently in place for this type of monitoring and suggested it would require follow-up with the run-the-bank team, as they are not closely aligned with that monitoring function.
