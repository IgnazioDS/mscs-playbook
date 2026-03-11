# Agents: Planning, Memory, and Evals

## Key Ideas

- Agentic systems combine language models with iterative planning, tool use, and memory so they can complete multi-step tasks rather than answer one prompt at a time.
- The main engineering challenge is control: budgets, stop conditions, permissions, and evaluation matter more than making the loop more autonomous.
- Planning decomposes a task into steps, while memory preserves relevant state across turns or actions; both must be bounded to avoid drift and contamination.
- Agents should usually be built from simpler reliable components rather than treated as one monolithic prompt.
- Evaluation for agents must measure task completion, safety, cost, and failure recovery across multi-step trajectories.

## 1. What Makes a System Agentic

A system becomes agentic when it can:

- interpret a goal
- choose intermediate actions
- call tools
- update state
- decide whether to continue or stop

That is different from a single-turn assistant, which only maps one prompt to one response.

## 2. Core Components

### 2.1 Planning

**Planning** means breaking a goal into executable steps or subgoals.

### 2.2 Memory

**Memory** can mean:

- short-term working context for the current task
- longer-term stored facts, preferences, or prior results

### 2.3 Controller

A **controller** enforces budgets, permissions, and stop conditions around the model loop.

## 3. Why Evals Are Harder for Agents

An agent can fail even if each individual response looks plausible. Failures include:

- extra unnecessary steps
- looping behavior
- wrong tool choice
- stale or contaminated memory
- partial success that still violates budget or policy

So agent evaluation must inspect the trajectory, not only the final sentence.

## 4. Worked Example: Simple Analyst Agent

Suppose an agent must answer:

```text
"What is (12 * 7) + 5?"
```

Available tools:

- `calculator(expression)`
- `search_docs(query)`

### 4.1 Good Plan

```text
step 1: detect this is arithmetic
step 2: call calculator("12*7+5")
step 3: return result and stop
```

### 4.2 Bad Plan

```text
step 1: search docs for "12 times 7 plus 5"
step 2: summarize search results
step 3: maybe call calculator
step 4: continue planning
```

The bad plan wastes cost, introduces irrelevant context, and increases the chance of drift.

Verification: the good plan selects one deterministic tool and terminates immediately after receiving the needed result, which is the desired agent behavior for this task.

## 5. Design Principles for Safer Agents

Useful controls include:

- step limits
- token and tool-call budgets
- memory isolation per user or task
- explicit termination rules
- trace logging for every action

A mature agent system is mostly careful orchestration around the model rather than blind trust in autonomy.

## 6. Common Mistakes

1. **Autonomy inflation.** Adding planning loops before the single-step workflow is reliable creates opaque failures; start with the simplest working assistant first.
2. **Unbounded loops.** Missing stop conditions or budget caps can cause cost blowups and drift; enforce hard limits on steps and tokens.
3. **Memory contamination.** Reusing memory across users or unrelated tasks leaks state and harms privacy; isolate and expire memory explicitly.
4. **Trajectory blindness.** Evaluating only final answers misses wasteful or unsafe intermediate behavior; inspect plans, actions, and tool traces.
5. **Tool overreach.** Giving agents broad action authority without policy checks turns model errors into system errors; keep permissions narrow and externally enforced.

## 7. Practical Checklist

- [ ] Prove the single-step workflow before adding planning loops.
- [ ] Enforce maximum steps, token budgets, and tool-call limits.
- [ ] Separate short-term scratchpad state from long-term stored memory.
- [ ] Log plan, action, observation, and stop reason for each run.
- [ ] Evaluate whole trajectories, not just final answers.
- [ ] Keep tool permissions and approvals outside the model loop.

## 8. References

- Yao, Shunyu, et al. "ReAct: Synergizing Reasoning and Acting in Language Models." 2023. <https://arxiv.org/abs/2210.03629>
- Wang, Lei, et al. "Plan-and-Solve Prompting." 2023. <https://arxiv.org/abs/2305.04091>
- Nakano, Reiichiro, et al. "WebGPT." 2022. <https://arxiv.org/abs/2112.09332>
- Mialon, Grégoire, et al. "Augmented Language Models: a Survey." 2023. <https://arxiv.org/abs/2302.07842>
- Anthropic. "Building effective agents." <https://docs.anthropic.com/>
- OpenAI. "Agents and tool-use documentation." <https://platform.openai.com/docs>
- OWASP. "Top 10 for Large Language Model Applications." <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
