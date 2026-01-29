# Agentic Data Analyst

## Problem and constraints
- Answer business questions using warehouse data and dashboards
- Generate reproducible queries and charts
- Respect data access controls and cost budgets

## Architecture (components and data flow)
- User asks a question in natural language
- Planner builds a multi-step plan and selects tools
- Tools execute SQL, fetch metrics, and render charts
- Final response includes query results, charts, and assumptions

## Prompting and tool design
- System prompt requires explicit assumptions and citations to tables
- Tool: run_sql(query, warehouse) with read-only access
- Tool: chart(data, spec) returns chart metadata and URL

## Evaluation plan and metrics
- Offline: replay known questions with expected metrics
- Metrics: query correctness, result accuracy, time to answer, cost per query
- Online: manual review for high-impact reports

## Failure modes and mitigations
- Incorrect joins or filters: add query linting and unit tests
- Excessive query costs: enforce row limits and use sampling
- Unsafe data access: row-level security and scoped credentials

## Security and privacy considerations
- Enforce least-privilege data roles
- Log queries and approvals for audits
- Mask sensitive fields in outputs

## Cost and latency levers
- Cache query results for repeated questions
- Use materialized views for heavy joins
- Stop after a maximum number of tool calls

## What I would ship checklist
- [ ] Read-only service account with RLS
- [ ] Query validator and cost estimator
- [ ] Audit logs for tool calls and outputs
- [ ] Guardrails for sensitive data exposure
- [ ] Evals for top 20 business questions
