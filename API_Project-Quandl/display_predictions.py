 Embedded Finance (CAP): Dashboard Requirements Analysis

 1. Current Challenges and Gaps

 Limited Transaction Lifecycle Visibility
- No status change tracking: CAP doesn't capture the complete transaction lifecycle or status changes over time within their system
- 90-day audit limitation: Only maintains audit information for when customers made calls and data exchange, not actual payment progression
- Pass-through status model: Simply relays status from downstream systems without internal tracking of transaction progression

 Incomplete Downstream Monitoring
- Unknown missing transaction detection: Team unaware of systems monitoring whether downstream applications receive files/transactions from CAP
- Run-the-bank disconnect: Limited visibility into operational monitoring functions that would detect processing gaps
- Basic acknowledgment tracking: Only receives initial acknowledgments that downstream systems received requests, no ongoing status confirmation

 Client-Facing Visibility Gaps
- Reactive status checking: Clients must actively query for status updates using GET calls rather than receiving proactive failure notifications
- Webhook dependency: Status change notifications rely on downstream systems triggering webhooks, creating potential gaps if downstream systems fail silently
- Limited failure attribution: 400-level HTTP errors indicate failures but may not provide sufficient detail for clients to understand root causes

 Operational Monitoring Limitations
- Volume tracking without correlation: Monitor payment volumes for leadership reporting but lack correlation with processing success rates or failure patterns
- Single database architecture: Oracle Exadata serves both operational and audit functions without separation for performance optimization
- TAP data consumption opacity: Unclear how TAP leverages CAP data for broader payment ecosystem monitoring

 2. Recommendations

 Enhanced Transaction Lifecycle Tracking
- Internal status progression monitoring: Implement comprehensive tracking of payment status changes as they flow through CAP, not just audit logs of API calls
- Transaction correlation mapping: Create linkage between trace IDs, customer references, and downstream system responses for complete payment tracking
- Extended data retention: Consider longer retention periods for critical transaction lifecycle data beyond current 90-day audit window

 Proactive Downstream Integration Monitoring
- Systematic downstream health checks: Implement regular confirmation that PSG, PPS, PTT, and REC are receiving and acknowledging CAP transmissions
- Missing transaction alerting: Deploy automated detection when expected downstream acknowledgments aren't received within defined timeframes
- Run-the-bank integration: Establish systematic communication with operational monitoring teams to identify downstream processing gaps

 Dashboard Integration Requirements
- API performance metrics: Track response times, success rates, and failure patterns across all CAP API endpoints
- Client-specific monitoring: Monitor API usage patterns by client to identify anomalies or processing issues affecting specific customers
- Dual identifier correlation: Provide unified tracking using both PNC trace IDs and customer reference numbers for comprehensive payment monitoring
- Authentication and validation failure tracking: Monitor field-level validation failures and entitlement rejections to identify systematic issues

 Enhanced Client Experience Monitoring
- Proactive failure notification: Implement real-time alerts when payments fail at CAP level or downstream processing, not just reactive status checking
- Status change attribution: Provide detailed failure reasons and processing stage information to help clients understand payment issues
- Webhook reliability monitoring: Track webhook delivery success to ensure clients receive timely status notifications

 Operational Dashboard Components
- Real-time throughput monitoring: Track payment volumes and processing rates across different payment types (direct API, Pinnacle Connected)
- Format processing metrics: Monitor JSON processing efficiency and any legacy file-based integration performance
- Network and infrastructure health: Track F5, APG, and other network layer performance impacting API availability
- End-to-end processing correlation: Link CAP processing with downstream system performance for complete payment flow visibility
