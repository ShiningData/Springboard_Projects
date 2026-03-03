1. Executive Summary
This project plan outlines the end-to-end execution of a Treasury Management (TM) Pricing Decision Dashboard — a Shiny-based application designed to replace the existing fragmented, manual Excel workbook process used by the TM Pricing team when evaluating customer quotes.

Currently, pricing analysts must manually download quote line items from Edge (Salesforce/CPQ), paste them into a workbook, run cost lookups, and separately cross-reference TAP reports for relationship context. This project automates and unifies that workflow into a single, interactive, filterable, and iterative tool — targeting the insight that 80% of U.S. revenue growth is driven by pricing decisions.

2. Project Context & Objectives
2.1 Business Problem
•	Manual, fragmented quote evaluation process across multiple disconnected tools
•	No unified view of historical relationship context alongside a live quote
•	Pricing decisions made in isolation — no cross-functional visibility into Liquidity or Card
•	Process bottlenecks create time pressure on approvals; risk of inconsistent decisions

2.2 Primary Objectives
•	Automate cost/margin calculation at the quote line item (train code) level
•	Surface historical TAP relationship data alongside each quote in real time
•	Integrate profitability benchmarking (percentile by segment) to inform approval thresholds
•	Build an iterative UI: adjust price points and immediately see impact on deal and relationship margin
•	Lay data architecture groundwork for future NPV modeling, McKinsey benchmarking, and cross-TM decisioning

2.3 Success Criteria
•	Analyst can select a quote and receive pre-populated cost, margin, and relationship context within 30 seconds
•	Price point edits propagate to summary views in real time (no manual re-calculation)
•	Dashboard replaces the manual workbook process for Megan and team within pilot phase
•	All three data sources (Edge, TAP, Profit Fact) successfully queried and joined on MDM/Power ID

3. Scope
3.1 In Scope — MVP (Must-Have)
•	Quote selection (filter/search by quote number)
•	Entity-level summary: segment, market, RRM, TMO, Power ID / MDM ID
•	Historical TM trend view (5-year) from TAP — revenue, volume, price growth toggles
•	Profitability summary from Profit Fact (gross revenue, expense, profit by CNIB solution)
•	Quote line items: train code, description, volume, standard price, editable approved price
•	Cost lookup per train code from Profit Fact finance table (unit cost × volume = total cost)
•	Before/after margin view: current relationship vs. proposed deal impact
•	Percentile benchmarking by segment (P×V revenue, # products, card, balances)
•	Implementation fee flag: display separately from ongoing revenue/cost
•	Multi-tab Shiny layout: Tab 1 – Relationship Summary | Tab 2 – Quote Detail | Tab 3 – Line Items

3.2 Nice-to-Have — v2.0
•	Net Present Value (NPV) calculator with configurable term, hurdle rate, revenue/cost growth inputs
•	Benchmark margin comparison: deal margin vs. average portfolio margin for same segment
•	Contract tracking: expiration date, composite contract, new vs. renewal

3.3 Stretch Goals — v3.0
•	McKinsey external benchmarking integration
•	Liquidity profitability inputs (balance × revenue rate − interest cost)
•	Card profitability inputs (spend × rate)
•	Push-back workflow: submit adjusted quote to CPQ/Edge for official approval
•	YTD TM revenue trends vs. budget; break-even analysis

3.4 Out of Scope
•	Real-time Edge API integration (overnight batch constraint) — workaround: manual upload
•	Flagging/resolving inaccurate quote TCs and volumes (separate high-priority exercise)
•	Production deployment infrastructure (IT/DevOps scope — separate workstream)

4. Technical Architecture & Data Sources
4.1 Platform Decision: Shiny App
Shiny was selected over Tableau based on must-have requirements for reactive user inputs and iterative price editing. Key technical considerations:
•	Reactive inputs: price point edits must trigger real-time recalculation of margin and summary views
•	Filterable train code grid: potentially hundreds of line items per quote; needs sort/filter/search
•	Real-time workaround: Edge is an overnight batch process; solution is manual CSV upload of quote line items at session start
•	Multi-tab layout achievable natively in Shiny with shinydashboard or bs4Dash

4.2 Data Sources
Source 1: Edge (Salesforce / CPQ)
•	Access method: manual CSV export (pending IAM/OIM role assignment — 2 weeks overdue)
•	Primary key: Power ID or MDM ID (to be confirmed with team)
•	Key tables: Quote, Opportunity, Entity/Account
•	Key fields: quote number, composite contract, override expiration date, line items (train code, volume, standard price)
•	Entity fields: entity name, segment, market, RRM, TMO domestic primary

Source 2: TAP (Historical TM Data Warehouse)
•	Access method: direct DB query (credentials available)
•	Primary table: TM Time Machine — 5+ year history at product family level
•	Key metrics: revenue, volume, price trend by product family
•	Benchmarking view: existing Pentagon viz — percentile by segment for P×V revenue, products, card, balances
•	Segment benchmarks to configure: Middle Market (avg $94K), Corporate Finance (avg $400K)

Source 3: Profitability Fact Table ("Profit Fact" — existing Tableau/DB source)
•	Table name: profit_fact (confirmed by Colin)
•	Primary key: MDM ID
•	Contains: gross revenue, expense, profit by CNIB solution; drill-down to product family → train code
•	Finance cost sub-table: unit cost per train code (fixed + overhead + variable)
•	Implementation fee flag: boolean field at train code level

4.3 Data Join Architecture
The central join key flows as follows:
•	User selects Quote Number →
◦	Edge: Quote → Opportunity → Entity → Power ID / MDM ID
◦	TAP: Entity MDM ID → TM Time Machine (historical product family revenue)
◦	TAP: Entity MDM ID → Pentagon benchmarking view (percentile by segment)
◦	Profit Fact: MDM ID → profitability summary (revenue, expense, profit)
◦	Profit Fact: Train Code → finance cost table (unit cost lookup)
•	Implementation fee train codes: flag join from Profit Fact; displayed as separate sub-total
•	Quote line items (uploaded CSV): joined to cost table on train code for margin calculation

5. Project Phases & Task Breakdown

Phase 0	Environment Setup & Access Resolution	Weeks 1–2

Establish access, tools, and working data connections before writing any application code. No dashboard development begins until Phase 0 is complete.

Task	Owner	Dependencies	Status	Priority
Obtain Edge IAM / OIM sales access role (not CPQ)	Joe + Engin	—	In Progress	Critical
Verify TAP TM Time Machine table access and query structure	Engin	TAP credentials	Not Started	Critical
Confirm Profit Fact table name, MDM ID join key, cost sub-table structure	Engin + Colin	DB access	Not Started	Critical
Confirm MDM ID vs. Power ID as active primary key in Edge	Engin + Ben	Edge access	Not Started	High
Receive and review Joe's Excel cost workbook (Quote 72986 example)	Engin	Joe to send	In Progress	High
Ben + Megan: identify contract fields in Edge (quote vs. entity level)	Ben + Megan	Edge access	Not Started	Medium
Set up Shiny project repo and local dev environment (R + shinydashboard)	Engin	—	Not Started	High
Document confirmed field names and table schemas for all 3 sources	Engin	All access above	Not Started	High

Phase 1	Data Pipeline — SQL Scripts & Query Development	Weeks 2–4

Build and validate all SQL/R queries that will power the dashboard. Each query corresponds to a specific dashboard view. Validate against known quote examples (72986) before dashboard integration.

Task	Owner	Dependencies	Status	Priority
Query 1: Quote line items from Edge CSV upload (train code, volume, std price)	Engin	Edge access	Not Started	Critical
Query 2: Entity metadata from Edge (segment, market, RRM, TMO, MDM ID)	Engin	Edge access	Not Started	Critical
Query 3: Unit cost per train code from Profit Fact finance table	Engin	Profit Fact access	Not Started	Critical
Query 4: Profitability summary from profit_fact (revenue, expense, profit by CNIB solution)	Engin	Profit Fact access	Not Started	Critical
Query 5: 5-year TM history from TAP TM Time Machine (product family, revenue, volume, price)	Engin	TAP access	Not Started	High
Query 6: Percentile benchmarking from TAP (P×V, products, card, balances by segment)	Engin	TAP access	Not Started	High
Query 7: Implementation fee flag — join train codes to Profit Fact flag field	Engin	Profit Fact access	Not Started	Medium
Validate all queries against Quote 72986 expected outputs from Joe's workbook	Engin + Ben	Queries 1–7	Not Started	Critical
Document final query/script file per data source with column mapping	Engin	Queries validated	Not Started	Medium

Phase 2	Shiny App — Tab 1: Relationship Summary	Weeks 4–6

Build the first tab of the Shiny app: the high-level relationship view. This is the context panel that anchors all downstream pricing decisions. Get Ben's sign-off before proceeding to Tab 2.

Tab 1 Components
•	Quote selector input (text input or dropdown — pulls from uploaded CSV or typed quote number)
•	Entity info card: entity name, segment, market, RRM, TMO, MDM/Power ID, composite contract
•	Profitability summary table: CNIB solutions × revenue / expense / profit (from Profit Fact)
•	5-year revenue trend chart: toggle between Total / Volume-driven / Price-driven growth
•	Percentile panel: radar/pentagon chart or bar chart showing customer vs. segment benchmark
•	Relationship size metric: current monthly P×V revenue + percentile rank in segment

Task	Owner	Dependencies	Status	Priority
Scaffold Shiny app with multi-tab layout (bs4Dash or shinydashboard)	Engin	Phase 0 complete	Not Started	High
Implement quote input + entity info card (Edge data)	Engin	Query 1, 2	Not Started	Critical
Build profitability summary table (Profit Fact → CNIB solutions)	Engin	Query 4	Not Started	High
Build 5-year revenue trend chart with growth-type toggle (ggplot2 / plotly)	Engin	Query 5	Not Started	High
Build percentile benchmarking panel (TAP Pentagon logic)	Engin	Query 6	Not Started	High
Ben review of Tab 1 — sign off before Tab 2 begins	Ben	Tab 1 complete	Not Started	Critical

Phase 3	Shiny App — Tab 2: Quote Detail & Tab 3: Line Items	Weeks 7–10

Build the deal evaluation and iterative editing core of the application. This phase delivers the primary workflow replacing Megan's manual workbook.

Tab 2 — Quote Detail
•	Quote-level summary: current monthly revenue vs. proposed, change in volume, change in revenue
•	Before/after product family margin table: current relationship + new deal → blended future state
•	Implementation fee sub-total (flagged train codes displayed separately)
•	Benchmark margin indicator: deal margin vs. average portfolio margin for segment

Tab 3 — Train Code Line Items
•	Filterable, sortable data grid: train code, description, volume, unit cost, standard price, approved price (editable)
•	Editable approved price field: reactive — changes propagate to Tab 2 summary views instantly
•	Margin % per line item, calculated automatically
•	Implementation fee rows visually distinguished (separate section or flag column)
•	Export/download button for adjusted line items (for quote submission workflow)

Task	Owner	Dependencies	Status	Priority
Build Tab 2: before/after product family summary table	Engin	Query 1, 3, 4	Not Started	Critical
Build Tab 2: quote-level revenue waterfall (current → proposed)	Engin	Query 1	Not Started	High
Build Tab 2: benchmark margin panel (segment avg vs. deal margin)	Engin	Query 6	Not Started	High
Build Tab 3: filterable/sortable DT datatable with editable approved price column	Engin	Query 1, 3	Not Started	Critical
Implement Shiny reactivity: Tab 3 price edits → Tab 2 margin recalculation	Engin	Tab 2 + Tab 3 built	Not Started	Critical
Implementation fee display: flag separation + sub-total in Tab 2 and Tab 3	Engin	Query 7	Not Started	Medium
Add download button for adjusted line items (CSV export)	Engin	Tab 3 complete	Not Started	Medium
Ben + Megan review of Tab 2 + Tab 3 — functional sign-off	Ben + Megan	Tabs 2–3 complete	Not Started	Critical

Phase 4	Integration, Testing & Pilot	Weeks 11–13

Integrate all tabs into a cohesive, stable application. Conduct user acceptance testing with the pricing team using live quotes before rolling out to operations.

Task	Owner	Dependencies	Status	Priority
End-to-end integration test: select quote → Tab 1 → Tab 2 → edit prices → Tab 3 export	Engin	Phases 2–3 complete	Not Started	Critical
Test with 3+ real quotes from Ben/Megan (variety: new, renewal, exception pricing)	Engin + Ben + Megan	Integration test pass	Not Started	High
Performance test: quotes with 200+ line items — ensure grid + reactivity is responsive	Engin	Tab 3 built	Not Started	High
Edge upload workaround QA: confirm CSV format, field mapping, upload → display flow	Engin	Tab 3 + upload module	Not Started	High
Fix bugs from UAT round 1; iterate on UX feedback from Ben/Megan	Engin	UAT complete	Not Started	High
Joe executive review: high-level demo of Tab 1 relationship summary	Engin + Ben	UAT pass	Not Started	Medium
Finalize data source documentation + data dictionary for all fields	Engin	All queries finalized	Not Started	Medium
Confirm contract fields in Edge (Ben + Megan deliverable from Phase 0)	Ben + Megan	Phase 0 pending	Not Started	Medium

Phase 5	v2.0 Enhancements — NPV & Benchmark Margin	Week 14+

Following successful pilot of MVP, implement v2.0 nice-to-have features based on team feedback and usage patterns.

Task	Owner	Dependencies	Status	Priority
NPV Calculator: inputs (term, hurdle rate, revenue growth %, cost growth %) → DCF output	Engin	MVP pilot stable	Backlog	Medium
Benchmark margin panel: compute avg margin by segment from Profit Fact + TAP	Engin	Query 6 extended	Backlog	Medium
Contract tracking: display expiration, composite contract, new vs. renewal flag	Engin	Ben/Megan field confirm	Backlog	Medium
Stretch: Liquidity + Card basic profitability input panels	Engin + Joe	v2.0 feedback	Backlog	Low

6. Timeline Summary

Phase	Focus	Key Deliverable	Duration	End of Week
Phase 0	Access & Setup	All 3 sources confirmed + schemas documented	2 weeks	Week 2
Phase 1	Data Pipeline	All SQL queries validated vs. Quote 72986	2 weeks	Week 4
Phase 2	Tab 1 Build	Relationship Summary tab signed off by Ben	2 weeks	Week 6
Phase 3	Tab 2 & 3 Build	Quote detail + editable line items, Ben/Megan sign-off	4 weeks	Week 10
Phase 4	Integration & Pilot	UAT complete, Joe demo, production-ready	3 weeks	Week 13
Phase 5	v2.0 Enhancements	NPV calc + benchmark margin deployed	Ongoing	Week 14+

7. Risks & Mitigations

Risk	Impact	Likelihood	Mitigation
Edge IAM access not resolved — blocks Phases 1–3 (2 weeks overdue)	High	High	Joe to identify correct sales OIM role (not CPQ) this week; escalate if not resolved by Phase 0 end
MDM ID vs. Power ID primary key mismatch across Edge, TAP, Profit Fact	High	Medium	Confirm correct active key in Phase 0; build join logic to handle both during transition period
Profit Fact finance cost table structure differs from Excel workbook assumptions	High	Medium	Validate cost table against Quote 72986 known outputs from Joe's Excel workbook in Phase 1
Quote CSV upload format inconsistent (sales team exports vary)	Medium	Medium	Define and document standard export format in Phase 0; add validation/error messaging in upload module
Shiny reactivity performance degrades with 200+ train code rows	Medium	Medium	Use DT datatable with server-side processing; benchmark in Phase 4 before UAT
Ben/Megan unavailable for iterative review check-ins	Medium	Low	Schedule standing 30-min check-ins weekly; Engin stops by desk as agreed
TAP benchmarking query logic unclear — percentile calculation not documented	Medium	Medium	Review existing Pentagon report with Joe/Colin; reverse-engineer percentile calc from existing Tableau DB
Contract field locations in Edge unresolved (quote vs. entity level)	Low	Medium	Scoped as v2.0; Ben+Megan to resolve in parallel — doesn't block MVP

8. Roles & Responsibilities

Stakeholder	Role	Responsibilities
Engin	Lead Data Scientist	All SQL queries, Shiny app development, data architecture, iterative builds, check-ins with Ben
Ben	Project Lead / Pricing Team	Project decisions, iterative review sign-offs, contract field research with Megan, primary stakeholder for all tab approvals
Joe	Executive Sponsor / SME	Edge IAM access resolution, Excel workbook delivery, high-level review of Tab 1, kept informed of progress
Megan	Pricing Analyst / UAT	UAT testing with live quotes, contract field identification in Edge, real-world workflow validation
Colin	Data Platform	Profit Fact table confirmation and access support

9. Immediate Action Items (This Week)

#	Action	Owner	Deadline
1	Joe: send Engin the Excel quote cost workbook (Quote 72986 with cost/margin calcs)	Joe	ASAP
2	Joe: identify and provide correct Edge IAM/OIM sales access role (not CPQ)	Joe	ASAP — 2 wks overdue
3	Ben: work with Megan to map contract fields in Edge (quote vs. entity level)	Ben + Megan	End of week
4	Ben: prepare 2–3 sample relationships for contract field testing	Ben	End of week
5	Engin: confirm MDM ID vs. Power ID as active primary key in current Edge setup	Engin + Ben	Phase 0
6	Engin: verify TAP TM Time Machine query structure and confirm access	Engin	Phase 0
7	Engin: confirm implementation fee flag field at train code level in Profit Fact	Engin + Colin	Phase 0
8	Joe: locate and share link to existing Edge contract dashboard	Joe	End of week
9	Ben: confirm contract expiration (override expiration date) is at quote or opportunity level	Ben	Phase 0
