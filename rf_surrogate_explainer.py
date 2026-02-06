Treasury Management Pricing Process Overview
PNC pricing team meeting with external consultants to review current deal approval workflow

Key participants: Ben (discussion leader), Patrick, Mike, McKenzie, Joe, Megan, Colin, Engin (lead data scientist)

Goal: identify automation opportunities and improve efficiency in pricing review process

Current process involves multiple disconnected tools requiring manual data integration

Current Pricing Workflow Process
Treasury Management Officers (TMOs) initiate deal quotes in CPQ system

Process varies by client type (existing vs new) and service type (existing vs new products)

New clients require bank statement analysis using statement translator tool

Volume estimation critical first step - uses existing client statements from current providers

Express approval process auto-approves deals meeting specific criteria:

Customer-level discount ≤30%

Monthly discount <$2,500

Bypasses pricing team review for qualifying deals

Volume Accuracy Challenges
Most critical bottleneck in pricing process

Common issues: fat-finger errors, misinterpreted data fields

Example: confusion between total items vs OCR reads (1M items could be 200K items × 5 fields)

Statement translator tool covers limited bank formats

Pricing Assistant Tool (PATH) only covers 30% of products

Volume dependencies between transaction codes not systematically managed

Multi-Tool Data Analysis Requirements
CPQ: contract dashboards, cost reports, historical quote approvals

TAP: profitability reports, transaction code pricing benchmarks, 24-month client trends

Tableau: client summaries, historical analysis via Time Machine

Edge: profitability data, relationship-level margin analysis

Seismic: product reference guides and documentation

McKinsey Portfolio Navigator: industry benchmarking across 18 banks

Manual spreadsheet consolidation required for comprehensive analysis

Decision-Making Methodology Inconsistencies
No standardized rules-based system for pricing decisions

Different analysts may use different data sources for same deal type

Evaluation methods vary by situation:

Existing client behavior analysis (primary method)

Margin analysis using finance cost spreadsheets

Competitive benchmarking via McKinsey data

Internal portfolio positioning via TAP reports

Lack of systematic approach to applying decision criteria

Technology Integration Gaps
All analysis happens outside CPQ in separate systems

Requires multiple monitors for effective workflow

Manual data export/import between systems

No centralized dashboard combining all data sources

Final pricing decisions manually entered back into CPQ

Communication tracking through Chatter system for documentation

Process Improvement Opportunities
Single integrated interface combining all data sources

Automated volume validation and dependency checking

Standardized decision support without full automation

Enhanced express approval criteria using historical accuracy data

Model-based pricing suggestions requiring human review

Streamlined data flow reducing 4-hour process to 30 minutes

Next Steps
Evaluate feasibility of integrated dashboard solution

Identify highest-value data source integrations for Phase 1

Consider expanding Pricing Assistant Tool coverage beyond current 30%

Assess McKinsey benchmarking data integration possibilities
