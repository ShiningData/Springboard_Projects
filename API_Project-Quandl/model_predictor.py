Based on the meeting transcript about Online Banking (WBB/WBA systems), here are the answers to the key questions:

## 1. Reports that exist today
- **Activity logs**: All customer activities (including payments) are logged and sent to mainframe every 3-4 hours via batch jobs
- **Adapt team reports**: The adapt team reads mainframe data and creates Tableau dashboards for stakeholders
- **Generic logging**: Not payment-specific - covers all online banking activities including logins, account activities, etc.
- **No payment-specific reporting**: All activities flow to one combined log file without payment differentiation

## 2. Who each group interacts with and what notifications exist currently

**Two different system flows:**
- **WBB (Legacy system):**
  - Internal transfers → Transfer Warehouse (TWH) via MQ services/APIs
  - External transfers → Cashish
  - Bill pay → Pfizer (via APIs)
  - Some lending transactions → PPO (handled by separate lending team)

- **WBA (Modern system):**
  - External transfers → PPO
  - WBE transactions → Pfizer (direct API integration)

**Current notifications:**
- Real-time API responses for transaction validation
- No downstream notification system - all interactions are real-time
- Risk team may contact customers for suspicious transaction patterns

## 3. Payment traceability (unique ID existence)
**Limited unique identification:**
- **No specific transaction IDs** attached by online banking
- **Customer ALK (Alternate Key)**: Primary identifier, usually SSN or alternate for customers without SSN
- **Subscriber ID**: Used for Pfizer interactions (also maps to customer ALK)
- **Payee IDs**: May exist but interconnected to customer ALK
- **Multiple ALKs possible**: One customer can have multiple ALKs/profiles

**Gap identified:** No unified transaction tracking ID across payment lifecycle

## 4. Data streaming accessibility
**Current data destinations:**
- **Mainframe files**: Raw log data stored but not easily readable
- **Adapt team**: Processes mainframe data for reporting
- **Transfer Warehouse (TWH)**: Only known data repository mentioned

**Limited accessibility:** No direct data warehouse or streaming identified beyond the adapt team processing

## 5. What happens if an issue arises
**Current process:**
- **Real-time validation**: Immediate error display on web page for invalid submissions
- **No batch processing issues**: Since all transactions are real-time API calls
- **No proactive monitoring**: No volume tracking or expected transaction monitoring
- **Risk monitoring**: Some backend risk processes monitor suspicious patterns
- **No downstream failure handling**: No notifications if downstream systems don't receive expected transactions

## 6. Client file status checking
**Available options:**
- **Real-time status**: Customers can see payment status (pending/completed) directly in online banking
- **Immediate feedback**: Errors shown instantly on submission
- **No confirmation numbers**: Generally no confirmation numbers provided (except for disputes)
- **Self-service**: All status checking done through online banking interface

## Key Opportunities for Enhancement

**Critical gaps identified:**
1. **Transaction traceability**: No unique transaction IDs beyond customer ALK linkage
2. **Payment-specific reporting**: All activity logs mixed together without payment differentiation  
3. **Downstream visibility**: No awareness of what happens after API calls to external systems
4. **Proactive monitoring**: No volume or pattern-based alerting system
5. **Confirmation tracking**: Limited confirmation number system for customer reference
6. **Data accessibility**: Payment data buried in generic activity logs processed by adapt team

**Recommended initiative focus:**
- Implement unique transaction IDs for end-to-end tracking
- Create payment-specific logging and reporting separate from general activity logs
- Establish downstream status monitoring beyond initial API response
- Develop proactive transaction volume and pattern monitoring
- Create centralized payment status dashboard combining real-time and historical data
- Improve data accessibility for payment operations teams

**System modernization note:** The coexistence of WBB (legacy) and WBA (modern) systems creates additional complexity in payment tracking and reporting that should be addressed in any comprehensive payment monitoring solution.
