Payment System Monitoring Meeting Summary
 Executive Summary
 This meeting provided a comprehensive overview of the company's payment system monitoring
 infrastructure, discussing the evolution from the failed Axway project to the current LOT (Lifecycle of
 Transaction) system, and outlining future development plans for enhanced monitoring and
 dashboard capabilities.
 Background: The Axway Project Failure (7 years ago)
 Initial Vision
 Objective: Track every single transaction through the entire ecosystem
 Primary Focus: Wire transfers (customers call when wire problems occur)
 Proposed Solution: Axway tool with dashboard, alerts, email capabilities, and transaction
 deep-dive functionality
 Why Axway Failed
 1. No Universal Transaction ID: Applications lacked a single ID to track items across systems
 2. Technical Limitations:
 Axway attempted in-memory processing for distributed applications
 Only viable for small transaction volumes with single IDs
 Backend data association was "horrible" - represented 80-90% of project complexity
 3. Vendor Capabilities: Axway developers couldn't handle the data complexity
 4. Result: Axway was terminated, payments team attempted to build internally
 Post-Axway Developments
 COVID Impact: Internal development stalled
 Infrastructure Progress: Streaming processes were built during this period
 PPP Program: Built in COD during COVID period
 Current LOT System Architecture
 Core Philosophy
 Scope: Track steps from system to system (not full transaction lifecycle)
Method: Stream data from each system into database, run queries to identify mismatches
 Alert Strategy: Accept false positives rather than miss real issues
 Timing: Operations prefer 30 minutes of false alerts over 2-hour undetected issues
 System Components and Data Flow
 Sterling File Gateway (SFG) Layer
 Function: Entry point for files containing wires and ACH transactions
 Challenge: Files aren't unpacked at this level - contents unknown until downstream processing
 Tracking: File-level monitoring to various downstream systems
 Payment Staging Gateway (PSG) - Central Hub
 Role: Primary hub for payment processing
 Data Delivery: Pushes data via MQ topics (not pulled like other systems)
 Systems: Uses both DB2 and Oracle databases
 Limitations: Missing one transaction type causing daily false positives
 Current Monitored Flows
 1. SFG to PSG: Primary black hole that was eliminated - highest priority
 2. CPY to PSG: Automated monitoring replacing manual operations tracking
 3. EDI to PSG: Automated monitoring replacing manual operations tracking
 4. PSG to PME: Critical for payment execution
 5. PWW and PWA: Individual transaction level (Pinnacle Web Wire/ACH)
 Data Processing Methodology
 Raw Data: Stream into COD database tables (not creating model tables)
 Query Approach: Run simple queries against paired tables to find mismatches
 Alert Generation: Create email alerts with attachments for operations review
 Timing: Hourly query execution with 1-2.5 minute data delays
 Complex Data Association Challenges
 Multi-System Tracking Requirements
 SFG → EDI: Requires three-table lookup (SFG, OPS database for NDM data, EDI)
 Connect Direct: Captures file IDs during transfer process
EDI to Payments: No direct file association - uses three matching data attributes as
 workaround
 Current Gaps and Limitations
 ACH Tracking: Stops at EDI, resumes at COD transaction level
 DSP Integration: Attempted but PSG team didn't cooperate - project abandoned
 Swift Database: Previously proprietary/unreadable - potential future opportunity
 CAP System: Not currently integrated
 PRT Integration: Minimal current involvement
 Technical Infrastructure Details
 Database and Streaming Architecture
 Platform: Built on BDL (Big Data Lake)
 Data Sources: Multiple systems with varying collection methods
 PSG Integration: MQ-based push model every 10 minutes
 Other Systems: Pull-based with 1-minute batch queries
 Storage: Raw data tables, no intermediate modeling
 Current Data Assets
 PME Data: Already streaming for PSUI tool consumption
 PRT Data: Available in Minth tables
 IPF Data: Recently added (July) for archival - no alerts yet
 ACH Processing: 30 files daily from 3 ACH systems (10 files each)
 Executive Requirements and Management Expectations
 Senior Leadership Vision (Bobby/Chuka/Raj Saini)
 Dashboard Requirement: Executive-level payment visibility
 Real-time Monitoring: Streaming front-end interface
 Transaction-level Tracking: Monitor individual transactions across all systems
 Budget: Approximately $1 million allocated
 Operations Reality (Mary Sammy and Team)
 Practical Needs: Email alerts more valuable than dashboards
Response Preference: 1-hour detection acceptable vs. constant false alerts
 Usage Pattern: Rarely access dashboards without email alerts prompting investigation
 Collaboration: Strong partners but need guidance on technical requirements
 Requirements Development Challenge
 Executive Level: High-level vision without detailed specifications
 Operations Level: Practical needs but limited technical specification capability
 Solution Approach: LOT team historically created solutions based on assumed needs, then
 gained approval
 Future Development Strategy
 Elastic Search Integration Plan
 Current Progress
 ACH to Elastic: Daily batch process implemented
 Real-time Goal: Working toward 30 files/day streaming via Confluent Kafka
 Aaron's Team: Developing automation for real-time data flow
 Migration Strategy
 1. Phase 1: Move existing LOT alerts to Elastic Search front-end
 2. Phase 2: Enhance with real-time ACH streaming
 3. Phase 3: Migrate money movement dashboard functionality
 4. Phase 4: Add remaining payment systems
 Advantages of Elastic Search Approach
 Quick Implementation: Leverage existing streaming infrastructure
 Rich Front-end: Cool dashboards, graphs, and visualization capabilities
 Alert Capabilities: Built-in email and alert functionality
 Cost Effective: Avoid building new web applications from scratch
 Iterative Development: Can transition to custom application later if needed
 Data Enhancement Requirements
 Customer Information Enrichment
CDM Integration: Pull customer table data to enrich ACH information
 Bank Name Mapping: Routing number to clean bank name associations
 Multiple Source Integration: Combine various production sources for comprehensive
 coverage
 System Expansion Opportunities
 1. DSP Integration: Retail-side payment data
 2. CAP System: Additional payment rail coverage
 3. Swift Modernization: If database becomes accessible
 4. ACH Tracking: Fill gaps between EDI and COD transaction level
 5. Transaction-level Monitoring: Expand beyond current file-level tracking
 Technical Implementation Recommendations
 Short-term Quick Wins
 Elastic Search Migration: Move existing LOT functionality to visual interface
 Money Movement Integration: Combine with existing dashboard capabilities
 Real-time ACH: Complete streaming implementation
 Alert Enhancement: Improve current email-based alerting
 Medium-term Enhancements
 Transaction-level Tracking: Implement for PWW/PWA and PSG systems
 Data Enrichment: Add customer and bank information
 Additional Systems: Integrate DSP, CAP, and other payment rails
 Dashboard Development: Executive-level real-time visibility
 Long-term Considerations
 Custom Application: Potentially migrate from Elastic Search to purpose-built solution
 Complete Transaction Lifecycle: Full end-to-end tracking capabilities
 Customer-facing Features: Provide transaction status to external customers
 Transaction Lifecycle Limitations
 Current Reality
Backward Association: Can only provide lifecycle information after transaction reaches
 destination system
 File Processing: Cannot track individual transactions within files until unpacked
 Timing Dependencies: Must wait for batch processing completion before associating
 transactions to source files
 Customer Information: Limited ability to provide real-time status during processing
 Technical Constraints
 File Unpacking: Major project required to unpack files at SFG level
 Batch Processing: EDI and CPY systems have complex timing dependencies
 Alert Complexity: Individual transaction alerts would be extremely difficult due to variable
 processing times (24-48 hours possible)
 Team Structure and Responsibilities
 Proposed Division of Labor
 Data Analytics Team: Provide leadership for outcomes and requirements definition
 COD Team: Handle data processing and streaming infrastructure
 Collaborative Approach: Joint ownership with complementary expertise
 Key Personnel
 Mike Humans: Former LOT architect (no longer available) - documented significant system
 knowledge
 Aaron: Leading current streaming implementation efforts
 Mary Sammy: Operations lead with extensive payment system experience
 Narayan: Current data analytics team member
 Knowledge Transfer Needs
 System Documentation: Mike Humans' documentation available for reference
 Query Analysis: Existing queries contain data association logic
 Architecture Understanding: Current team will need to understand complex system
 interdependencies
 Risk Assessment and Mitigation
 Technical Risks
Data Complexity: Payment system integration complexity historically underestimated
 System Dependencies: Multiple vendor systems with varying cooperation levels
 Performance Concerns: Real-time processing requirements vs. system capabilities
 Business Risks
 Scope Creep: Executive vision may exceed practical implementation possibilities
 Resource Allocation: $1 million budget may be insufficient for complete vision
 Timeline Pressure: September 2024 target for initial COD to RLO implementation
 Mitigation Strategies
 Phased Approach: Start with Elastic Search quick wins
 Expectation Management: Educate leadership on technical constraints
 Incremental Value: Deliver functional improvements while building toward larger vision
 Success Metrics and Outcomes
 Immediate Success Indicators
 Alert Reduction: Decrease false positive rates while maintaining detection capability
 Response Time: Maintain or improve current 1-hour issue detection
 Operations Satisfaction: Positive feedback from Mary Sammy's team
 Long-term Success Measures
 Executive Dashboard Adoption: Regular use of real-time payment visibility tools
 System Coverage: Comprehensive monitoring across all payment rails
 Issue Prevention: Proactive identification and resolution of payment system problems
 Organizational Impact
 Subject Matter Expertise: Team becomes company's payment system architecture experts
 Operational Efficiency: Reduced manual monitoring and faster issue resolution
 Strategic Positioning: Foundation for future payment system enhancements and customer
facing features
