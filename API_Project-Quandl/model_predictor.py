Based on the meeting transcript provided, here are the detailed answers to each question:

1. Where does your application/platform sit in the flow of payments? (Beginning, middle, end)

The application sits in the middle of the payments flow. According to the transcript, it operates "after the deposits have been collected for the providers or for the customer bank customers" and they do "reporting on all the collections activities that we have in the bank for various healthcare providers." The team clarified that they are "not in the payments flow in terms of what gets debited or credited, but we do report on the resulting collections."

2. What are your downstream applications for originations?

The application does not handle originations. As stated in the transcript, "we only work receivables work. Only receivables work."

3. What are your downstream applications for receivables?

For receivables, they have feeds to Pinnacle. Additionally, everything else is "either presented through a user interface to the client or transmitted in a file to the client."

4. What are your upstream applications for originations?

The application does not handle originations, only receivables work.

5. What are your upstream applications for receivables?

The upstream applications include lockbox, ACH from the bank, and they receive direct transmissions from payers for X12 835s. They also get a feed from PNC e-payments to create two types of refund files for healthcare clients so they can post for patient refunds.

6. Of those downstream applications, which do you receive acknowledgments or notifications from?

They do not receive acknowledgments or notifications from downstream applications like Pinnacle.

7. Of those upstream applications, which do you receive acknowledgments or notifications from?

They do not receive acknowledgments or notifications from upstream applications. File completeness is dictated by successful completion of jobs on the mainframe side that interact with lockbox and ACH.

8. In what format do you receive transactions/files/data?

They receive data in multiple formats: Nacha format, X12 format, and a variety of BAI formats from lockbox (basically CSV files).

9. In what format do you send transactions/files/data?

For Pinnacle, they interact directly with the database through web servers that present content using Pinnacle's security models. For other outputs, they typically send files in X12 835 format.

10. Do you have any unique identifier that you add to the transactions from your system? Do you pass that to the next system in the flow? If not are you receiving a unique ID from a downstream application that you continue to pass upstream?

They do not add unique identifiers or do tokenization. The significant identifier used to tie transactions together with payments and remits is the trace number included in either the ACH trace number or the X12 trace number. This is used in their "reassociation" process to match payments with remittance advice.

11. Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction? If so, where is that hosted? Who are the consumers for said reporting?

Yes, they provide various reports available through the UI that summarize daily activity, areas of particular interest, and situations where clients receive adjustments to their bill amounts. They provide reporting on rejection codes and reasons for payers to providers. The reports flow through the UI and are usually spreadsheet representations of actual pages that are printed. The consumers are their healthcare provider clients.

12. Can a client check on the status of their payment?

Based on the transcript, clients can access information through the user interface and can ask about missing files when they receive deposits but don't get corresponding remittance advice. Clients can see when they receive deposits and anticipate receiving remittance advice that describes those deposits.

13. What sort of data management are you doing? What type of database do you use?

They use an Oracle database for their data management.

14. Is your database split between operational and reporting databases?

No, it is not split between operational and reporting databases. It's "different schema, but it's one server."

15. Is your data being streamed anywhere? For ex. a warehouse like COD?

They are consumers from COD, but they are not streaming data anywhere. The information they manage is "essentially for information that we do not share."

16. Is it possible for there to be a failure at your stage in the payments flow? If so, what happens if there is one?

They do not interact with the payments flow from origination to deposit, so failures at their stage don't affect the actual flow of dollars. However, they do communicate to customers when payments have been received and can affect their client's posting of data. Since payment and remittance are separate, they can receive remittance characteristics days or weeks in advance of actual settlement, and this time lag can impact client posting but not dollar flow.

17. Do you do any negative tracking or volume tracking to account for expected transactions on a certain day?

They have operations groups that monitor general throughput and payer relations teams that monitor payer connection health. However, they don't systematically monitor each payer's relationship for timely delivery because payer frequency varies (some daily, some weekly, some twice monthly). They do volume tracking from a claims-based perspective and monitor if they haven't seen data from certain payers for a couple of days, but it's "best efforts monitoring" based on SME knowledge within their operations group.

18. Do you get any notifications from downstream systems if they don't receive a file or transaction from you?

Yes, when providers receive deposits, they anticipate receiving remittance advice describing those deposits. If they don't receive the remittance advice, they contact the team asking "Hey, where's our file?" This typically happens within a few days tolerance, as there can be a window between when payment is received and when remittance detail is provided.
