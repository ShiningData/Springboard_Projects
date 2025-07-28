Based on the meeting transcript, here are the answers to the key questions about the CPY (payments processing group) workflow:

 1. Reports that exist today
- SystemWare reports: Primary reporting system accessible to anyone at PNC for transaction data
- COD system: Contains comprehensive logging data from CPY operations (set up by retired employee Mike Yoman)
- Tableau reports: Used by operations team for transmission information from SFG
- Pinnacle Integrated Payables module: Client-facing system where 99% of clients can view their payment status and rejections

 2. Who each group interacts with and what notifications exist currently

Input sources: Multiple internal systems feed into CPY (detailed architectural diagram mentioned to be shared)
Output destinations:
- ACH platforms (domestic, Canadian via RBC)
- Wire systems (staging/PME)
- Card processors 
- Check print centers
- SFG for external transmissions

Current notifications:
- Email summaries sent to clients showing transaction counts and accept/reject status
- Handshake confirmations received from wire staging, card processors, and check print centers
- No confirmations received from domestic ACH or PEP systems

 3. Payment traceability (unique ID existence)
Limited traceability: Once payments leave CPY, there's no unified tracking ID. Each system uses its own identifiers:
- CPY uses "sender ID" for client identification
- ACH uses batch headers
- Wire uses SRF field with sender ID
- Each downstream system converts to their own identification schemes

Data retention: Payment table maintains data for 730 days, but mainframe file retention limited to 255 versions

 4. Data streaming accessibility
Current data destinations:
- COD system: Receives all CPY input data and some downstream information
- SystemWare: Contains transaction reporting data
- Mainframe tables: Payment data accessible for 2 years

Gap identified: Inconsistent downstream data capture - unclear what information flows to COD from payment processing systems

 5. What happens if an issue arises
Current process:
- No proactive monitoring or alerts for expected vs. actual volumes
- Clients must contact EC operations staff for reject information
- Operations team uses Tableau to investigate transmission issues via SFG
- Manual investigation required to trace payments across systems
- "All hands" approach when major issues occur (identified as inefficient)

 6. Client file status checking
Available options:
- Pinnacle portal: 99% of clients have access to check payment status and view rejections
- Email notifications: Automatic summaries of processed transactions
- Phone support: Clients can call EC operations for detailed reject information

 Key Opportunities for Enhancement

Critical gaps identified:
1. End-to-end traceability: No unified tracking ID across the payment lifecycle
2. Proactive monitoring: No alerts for volume anomalies or missing expected files  
3. Downstream visibility: Limited insight into what happens after CPY processing
4. Real-time status: Current systems are largely batch-oriented rather than real-time
5. Integrated alerting: No centralized notification system for operational issues

Recommended initiative focus:
- Implement unified transaction tracking across all payment channels
- Establish proactive monitoring with volume-based alerts
- Create centralized operational dashboard combining CPY, COD, and downstream system data
- Develop real-time status capabilities for faster issue resolution
