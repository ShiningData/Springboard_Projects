Question 1: Where does your application/platform sit in the flow of payments (what do you receive from an upstream system, if any? What do you send downstream)?

PPO (Payments Platform Operations) sits as the central payment engine for lending money movement at PNC. According to the transcript, PPO is responsible for "lending money movement" which involves "withdrawing funds from a lending product and depositing those funds into a checking account." PPO serves as the system of record for payments and acts as three key functions: (1) the authorization engine that owns all business rules for whether a payment can or cannot be made, (2) the payment staging engine that holds payments until execution date, and (3) the execution engine that distributes files to downstream systems.

Upstream Systems: PPO receives payment requests from multiple channels including WBAML (mobile banking), WBB, IVR, and other channel systems. All upstream systems connect to PPO via APIs, specifically calling PPO's payment order API to get payments into the PPO system.

Downstream Systems: PPO sends data to multiple downstream systems depending on the lending product system of record:
- For ACLS, MSP, and FDR: CFE (files), ACH (files), Core/COSE (APIs), and DSP (APIs)
- For ACPS: PMT, AIS and Class (APIs), and DSP (APIs)
- PPO also publishes to DSP (Data Streaming Platform) for all flows

Question 2: In what format do receive transactions/files/information?

PPO does not receive files as input. Instead, PPO receives payment requests exclusively through API calls from upstream channel systems. The transcript specifically states that "they all leverage PPO APIs" and describes the process where upstream systems make API calls for payment evaluation (looking at from/to accounts, balances) and then call PPO's payment order API to submit the actual payment request.

Question 3: In what format do send transactions/files/information?

PPO sends information in two different formats depending on the downstream system:

File Formats:
- ACH: Files (for all off-us accounts)
- CFE: Files (for all on-us accounts) 
- The transcript explains: "Your off-us goes through ACH. So on-us and off-us, they those two files equate to that 2,000 that's going to ACLS for processing."

API Formats:
- DSP: APIs (publishes payment information)
- Core/COSE: APIs
- For ACPS flow: PMT, AIS and Class: APIs

The transcript notes that PPO performs ETL (Extract, Transform, Load) functions to "extract that data into file formats that are appropriate for whoever we're delivering it to next."

Question 4: Do you have any unique identifier that you add to the transactions from your system? Do you pass that to the next system in the step? Do you create a new one? If so, do you maintain an index?

Yes, PPO uses a confirmation number as the primary unique identifier for each payment. The transcript indicates there may also be other unique identifiers but the confirmation number is the main one referenced. 

Passing to Downstream Systems:
- The confirmation number is sent downstream to DSP and further downstream systems including DMG and WCI for letter communication and alerts
- For files sent to ACH and CFE, the transcript indicates uncertainty about whether the confirmation number is included or if a separate transaction ID is used instead
- The speaker noted they would need to "talk to tech" to confirm exactly what unique identifiers are used in the files versus APIs

Maintenance: PPO maintains the confirmation number in its database, and this identifier is considered unique within PPO's system of record.

Question 5: Do you have any reporting that captures the activity that takes place at your stop in the lifecycle of a transaction? If so, where is that hosted? Are there consumers for said report today?

PPO has multiple reporting and monitoring systems, but "nothing holistic," which is why the speaker was very interested in the dashboard project being discussed:

Dynatrace Dashboards: Monitor certain APIs and their functionality
Glass Box Dashboards: Look at errors occurring throughout the end-to-end customer journey  
Elastic Dashboards: Built off DSP data, but described as "not fully built" and only "directionally" useful
Tableau: Only available for PPO 1.0 (legacy agent-assisted payments), not for PPO 2.0 (modern system)

Additional Monitoring Tools:
- Humio (though the speaker wasn't sure of the boundaries between tools)
- Log Scale
- Various monitoring on both channel side and PPO side APIs

The transcript emphasizes that monitoring exists "on both sides of the house" because "you can have a channel API failing, like an outer API, or you can have a PPO API failing."

Question 6: Is your data being streamed (KAFKA stream, etc) anywhere? For example, a warehouse like COD.

Yes, PPO streams data to DSP (Data Streaming Platform). The transcript explains that PPO is "both a consumer and a publisher" with DSP:

As a Publisher: "After we add a payment to the database, we publish that to DSP, because then when a customer logs back in afterwards, we have to be able to present that payment."

As a Consumer: PPO leverages DSP APIs for functions like CPS (Customer Product Service) API to understand account ownership and get account lists.

Technical Implementation: The communication uses APIs, but "behind them are like their topics, Kafka streams, whatever." The speaker confirmed this includes Kafka streams and similar streaming technologies.

Data Warehouse: PPO itself serves as the data warehouse, with the speaker stating "PPO is essentially, in my opinion, that's the data warehouse. PPO is all the databases that hold all of the information around the payments and we just published to DSP. There's no other data warehouses outside of it."

Question 7: What happens if a file dies at your step in the process?

If file generation fails during PPO's ETL process, ServiceNow incidents are automatically opened. The transcript explains: "If ETL were to fail, couldn't like perform that action and build that file, then we would have, you know, um, service now incidents opened because we were not successful, right, to extract the data and put it into a file format, um, that would be consumable for the next step of the journey."

Downstream File Issues: PPO also faces challenges when files are successfully sent but encounter problems at downstream systems. The transcript provides a specific example: "there was a syntax error, some kind of like symbol or something like that in one of the records... ACH, as soon as it's got that that error, that character, or whatever, it stopped before, it stopped, um, there. It didn't like, it the, it did not perform any additional ACHs right after that character... So anyways, so even though we were supposed to have 10,000 payments processed, we only, you know, received the funds for 4,000 of them."

Monitoring Gaps: The speaker acknowledged gaps in monitoring, stating they have mechanisms to monitor file receipt and timing, but "I think we're still missing like uh being 100% crisp on how we need to monitor the reconcilement and the receiving of those files uh throughout the the steps."

Question 8: What do you do if you didn't get a file or transaction that you were expecting to get on a certain day?

This question was directly addressed in the follow-up session. PPO does have time-based monitoring for expected file delivery, but not volume-based monitoring:

Time-Based Alerts: If files are not received by downstream systems within expected timeframes, ServiceNow incidents are opened. The example given was: "if we, um, um, you know, we are, you know, processing a file or sending a file, let's say, to be received by MSP or MSD, that typically is received by, let's say, 9:00. If it's not received by like 9:15, then, uh, a service now incident would be opened."

No Volume Monitoring: PPO does not track if file volumes are lower than anticipated. As stated: "Not if the volume's lower. If the file doesn't get received or doesn't get received within a certain time frame... If the volume is lower than anticipated. Like, there's not thresholds built around the volumes thing."

Question 9: Can a client check on the status of their file?

No, clients cannot check on the status of their files or payments in transit. The transcript clearly states "No" when asked "can clients like check on the status of their file now? Like to see where it is in like transition or something like that?"

Question 10: Do you get a notification if your downstream system doesn't receive a file from you?

The monitoring works in reverse - it's actually the downstream systems that check and alert if they don't receive expected files from PPO within specified timeframes. The transcript clarifies: "It's actually them, sorry. It's actually them, like MSP or whomever the hop is, which would be checking to make sure that they've gotten it in that... Not us checking. Um, but I'm on the receiving end."

However, PPO does have some mechanisms in place to monitor file delivery success, as mentioned: "we have things in place to say, did you receive the file? And did you receive it successfully? Did it get received on time?" But the primary alerting mechanism relies on downstream systems notifying PPO of missing files rather than PPO proactively detecting delivery failures.

11. Other:

PPO System Architecture - Multiple Versions: PPO operates two versions: PPO 1.0 (described as "old antiquated" used for "agent assisted payments") and PPO 2.0 (the more modern version). The speaker focused discussion on PPO 2.0 as the modern system.
Four Different Systems of Record: PPO handles lending payments across four different core systems because lending products sit on four different platforms:

FDR: Credit card and minimal personal business lines of credit
ACLS: Auto, personal, business loans and lines of credit
MSP: Mortgage (first mortgage) and home equity loans and lines of credit
ACBS: Commercial, small business, and private banking loans and lines of credit

Database Technology and Migration Plans: PPO currently uses MySQL databases but will be migrating to Oracle "sometime within the next year." This contrasts with retail deposits which has one system of record while lending has four.

Wire Capability Limitations: PPO does not currently support wire transfers for lending payments/payoffs, though this functionality "will happen likely in the next year to two years." Currently, customers wanting to wire payments must go through other channels like calling the bank.
ACBS Different Processing Model: For ACBS (commercial/private banking), PPO operates differently - it's "just a pass-through or informational, like, uh, uh, the authorization engine" rather than being the actual payment engine. AIS and Class serve as the payment engines for ACBS, while PPO is the payment engine for the other three systems.
Comprehensive Documentation Available: The speaker referenced detailed process maps available in Confluence that show "upstream, downstream" flows for all payment types, organized as a matrix covering "payments on ACLS, advances on ACLS, uh, payments on FDR, Advances on FDR, MSP payments and advances, ACPS" with the caveat that there are "some flaws in them, um, but directionally it's pretty good."

Balance Verification Approach: PPO goes directly to Systems of Record (SORs) for real-time balance checks rather than using DSP, because "we're money movement and because there's always a risk of delayed balances."
Team Enthusiasm for Dashboard Project: The PPO representative expressed strong support for the health dashboard initiative, stating "this is something we need wholeheartedly and something I've been asking for for a good period of time" and "I'm super excited for this conversation."
