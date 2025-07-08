Based on the SFG team transcript, here are detailed answers to your specific questions:

 1. Where does SFG sit in the payment flow?

Position: SFG operates as the central file routing infrastructure between external entities and internal PNC systems.

Upstream Sources: SFG receives files from approximately 6,000 external partners, including direct corporate customers and third-party service providers. These files arrive through multiple security layers including external firewalls, F5 load balancers, secure proxy layers, and internal firewalls before reaching SFG.

Downstream Recipients: Files are routed to approximately 250 internal PNC applications, with payment-related applications including PSG, PMT, PME, HCA, and CPY systems.

Bidirectional Flow: The system handles both inbound files (external partners to internal apps) and outbound files (internal apps to external partners).

 2. Format they receive transactions/files/information:

Format Agnostic Processing: SFG operates without any knowledge of file formats or contents. The system treats all incoming files as opaque binary objects regardless of whether they contain payment data, marketing information, or other business content.

File-Based Architecture: All data arrives as discrete files rather than real-time transaction streams or API calls.

No Content Inspection: The platform deliberately avoids examining file contents for security and operational simplicity reasons.

 3. Format they send transactions/files/information:

Unchanged File Transmission: SFG maintains complete file integrity by passing files to downstream systems without any content modification or format transformation.

Protocol Standardization: Internal delivery uses Connect Direct protocol consistently across all receiving applications.

Optional File Renaming: The system can rename files during the routing process when external partner naming conventions don't match internal application requirements, but file contents remain unchanged.

 4. Unique identifiers:

No Identifier Creation: SFG does not generate or append any unique tracking identifiers to files during the routing process.

File Name Based Routing: The system relies on predefined file naming conventions combined with partner authentication credentials to determine routing destinations.

No Cross-Reference Tracking: Since no unique identifiers are created, SFG maintains no index or cross-reference tables linking files across the routing process.

Rename Capability: When file renaming occurs, both original and destination file names are recorded but no additional tracking identifiers are generated.

 5. Reporting on activity:

Comprehensive Analytics Platform: SFG maintains extensive reporting through Tableau dashboards that provide real-time visibility into file transfer operations.

Multi-Database Architecture: Reporting draws from several Oracle databases including the main SFG application database, workflow database, and ICC database.

Temporal Reporting Options: The system provides both 7-day and 31-day historical views, with the shorter timeframe used more frequently due to performance considerations.

Current Usage: The SFG team actively uses these reports for operational monitoring, and some downstream applications have been granted access for their own monitoring needs.

Metrics Captured: Reports include file names, transfer timestamps, originating partners, destination applications, success/failure status, and file routing paths.

 6. Data streaming to warehouses:

No Data Warehouse Integration: SFG does not stream or archive data to enterprise data warehouses such as COD or similar systems.

Operational Database Focus: All data remains in operational Oracle databases with limited retention periods rather than being moved to long-term analytical storage.

No Reporting Database: The system lacks a separate reporting database and runs analytical queries directly against operational systems using optimized query structures.

 7. What happens if a file dies at SFG:

Automated Incident Creation: Failed file routing automatically generates events in the Big Panda monitoring application.

24/7 Support Escalation: These events are immediately routed to Level 1 support teams who monitor systems around the clock.

Multi-Party Coordination: Support teams coordinate resolution efforts involving the originating external partner, the intended receiving application, and potentially SFG technical staff.

Resend Requirement: Failed files must be retransmitted by the external partner with corrected naming or credentials to successfully complete routing.

Root Cause Categories: Failures typically result from incorrect file naming, credential mismatches, or downstream application unavailability.

 8. Missing expected files:

No Proactive Monitoring: SFG deliberately avoids negative monitoring for expected but missing files due to the scale and variability of partner file transmission patterns.

Volume Challenges: With 50,000-60,000 daily files from 6,000 partners, predicting expected file arrivals is considered operationally unfeasible.

Application Responsibility: Individual downstream applications are expected to monitor their own expected file arrivals and initiate investigations when files don't arrive as scheduled.

SRC Coordination: When applications identify missing files, they coordinate with the Service Request Center to investigate whether files arrived at SFG but failed to route properly.

Business Context Limitations: SFG cannot distinguish between missing critical files and normal variations in partner transmission schedules.

 9. Client status checking:

Limited Direct Access: External partners do not have direct access to SFG operational databases or real-time monitoring systems.

SRC Mediated Inquiries: Status inquiries from external partners are handled through the Service Request Center rather than direct system access.

Internal Application Access: Some internal PNC applications may have Tableau dashboard access with appropriate entitlements, allowing them to track their own file flows.

Real-Time Data Availability: When accessed through proper channels, file status information is available in real-time as the Tableau reports refresh upon each access.

 10. Downstream system notifications:

No Acknowledgment Architecture: SFG operates on a fire-and-forget principle where successful Connect Direct initiation marks completion of SFG responsibilities.

Connection Failure Detection: The system can detect if it cannot establish initial connection to a downstream application, which would generate monitoring alerts.

Processing Failure Blindness: Once a file transfer begins successfully, SFG has no visibility into downstream processing failures, storage issues, or application-level problems.

Downstream Responsibility: Individual applications must implement their own monitoring and alerting for files they fail to receive or process successfully.

 11. Additional Operational Details:

 Traffic Patterns and Scale:
SFG processes between 50,000 and 60,000 files daily with significant variation in partner transmission frequency. Some partners transmit multiple files per day while others may only send weekly transmissions.

 Partner Ecosystem Complexity:
The 6,000 external partners include both direct PNC customers and third-party service providers who aggregate multiple end customers. This creates complexity in understanding the true business impact of any individual file routing issue.

 Authentication and Security:
Every external partner operates with unique PNC LDAP credentials that must match specific file naming patterns for successful routing. This creates a secure but rigid routing framework.

 Data Retention Policies:
Historical data retention is intentionally limited to prevent database bloat, making long-term trend analysis or historical issue investigation challenging.

 Performance Optimization:
The system uses highly optimized database queries to handle the reporting load, but would face performance degradation if hundreds of users accessed reports simultaneously.

 Break Glass Procedures:
Emergency access to file contents exists through tightly controlled procedures, but this capability is rarely used due to security and operational policies.

 Real-Time Operations:
File routing occurs in near real-time with minimal delays between receipt and forwarding, making SFG essentially a pass-through layer rather than a processing or queuing system.

 Error Pattern Analysis:
The majority of routing failures stem from file naming convention violations or credential mismatches rather than technical infrastructure problems.

 Business Logic Separation:
SFG deliberately maintains no business logic or payment-specific intelligence, operating purely as technical infrastructure to maximize reliability and minimize complexity.
