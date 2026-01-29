# Agents: Planning, Memory, and Evals

## Overview
Agents combine iterative planning, tool use, and memory to complete multi-step
tasks with minimal human intervention.

## Why it matters
Agentic workflows enable automation for complex tasks but require strong safety
and evaluation scaffolding.

## Key ideas
- Planning breaks goals into executable steps
- Memory can be short-term (scratchpad) or long-term (vector store)
- Tool use should be gated by policies and budgets
- Evals guard against regressions and unsafe behavior

## Practical workflow
- Start with a single-step assistant and add planning loops
- Separate task memory from user data for privacy
- Use a controller to enforce budgets and stop conditions
- Add evals for task success, latency, and safety

## Failure modes
- Goal drift from poor stop criteria
- Cost blowups from unbounded loops
- Memory contamination across users or tasks
- Unsafe actions due to weak tool policies

## Checklist
- Define maximum steps, tokens, and tool calls
- Add per-user memory isolation and retention rules
- Log plans, actions, and results for audits
- Run evals on critical tasks before release

## References
- ReAct: Synergizing Reasoning and Acting — https://arxiv.org/abs/2210.03629
- Plan-and-Solve Prompting — https://arxiv.org/abs/2305.04091
