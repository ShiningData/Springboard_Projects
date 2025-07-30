The Payment Gateway Architecture
PNC's commercial payment ecosystem centers around Pinnacle, which serves as the primary gateway for all payment transactions entering the bank through various channels. Think of Pinnacle as the central command center that initiates and orchestrates payments within PNC's broader payment infrastructure.
Two Main Processing Channels
The system operates through two distinct but interconnected channels, each designed to serve different customer segments and payment types:
Channel 1: Pinnacle Funds Transfer (PFT)
This channel primarily serves retail and business customers who need to handle wire payments, real-time payments (RTP), and ACH transactions. Customers interact with this system through user-friendly web interfaces where they can:

Manually enter payment details
Set up scheduled and recurring payments
Upload payment files using template-based import functionality that supports multiple input formats

Channel 2: Pinnacle Commercial Experience (Comex)
This specialized channel focuses exclusively on commercial clients and their complex business payment requirements. It operates through a separate but integrated platform that processes commercial payments alongside the PFT system.
The Payment Processing Journey
Once payments enter through either channel, they follow a sophisticated routing system:
Step 1: Initial Processing
Payment files can be sent directly to SFG (Stored File Gateway), which acts as the critical intermediary infrastructure connecting external partners with PNC's internal payment processing systems.
Step 2: Message Queue Distribution
From Pinnacle, payments flow to PSG (Payments Staging Group) via a Message Queue system using a Request-Response Model. PSG then intelligently distributes these payment files to various downstream processing locations, including:

CPY (Payables Advantage)
EDI (Electronic Data Interchange)
PSG and PMT (Payment Services Data)

All processed data ultimately gets stored in SFG's dedicated Oracle database for record-keeping and audit purposes.
Specialized Processing Systems
CPY: The Translation Engine
CPY functions as a sophisticated middleware translation service that PNC charges clients to use. Its primary role is converting client payment data into the specific formats required for different payment types:

ACH payments
Card transactions
Check payments
Wire transfers

Once the translation is complete, payments are automatically routed to the appropriate processing system based on their payment type.
EDI: The Dual-Purpose Platform
EDI operates as both a customer-facing interface and a critical middleware system:
Customer-Facing Functions:

Direct customer interaction portal
File reception from SFG and ARS systems
Critical intermediary processing for both payment origination and receivables transactions

Backend Processing:

Processes files from SFG containing various payment instructions
Handles files from internal applications through mainframe transactions
Manages both origination processes (outgoing payments) and receivables transactions (incoming payments)

Specialized Payment Flows
Lockbox Operations
EDI processes files from lockbox operations, while ARS (Accounts Receivable System) handles ACH transactions. Wire data flows into EDI specifically for remittance processing, representing a growing segment of transaction volume.
Merchant Services Integration
EDI also receives merchant services data for card transactions and processes monthly CAA (Customer Account Analysis) data from various internal systems, providing comprehensive transaction analysis and reporting capabilities.
System Integration and Data Flow
The entire system demonstrates sophisticated integration between multiple platforms, ensuring that payment data flows seamlessly from initial customer input through final processing and settlement. Each component serves a specific function while maintaining connectivity with the broader payment ecosystem, creating a robust and scalable commercial payment processing infrastructure.
This architecture allows PNC to handle diverse payment types efficiently while providing customers with multiple access points and processing options based on their specific business needs and transaction volumes.
