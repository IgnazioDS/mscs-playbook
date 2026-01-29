# Adversarial Search: Minimax and Alpha-Beta

## Overview
Adversarial search models competitive settings using minimax and pruning to
select optimal actions under perfect play assumptions.

## Why it matters
Game playing and multi-agent planning rely on adversarial reasoning.

## Key ideas
- Minimax alternates maximizing and minimizing players
- Alpha-beta pruning reduces expanded nodes
- Evaluation functions approximate deep search
- Horizon effects require quiescence or depth tuning

## Practical workflow
- Define game state, actions, and terminal conditions
- Implement minimax with depth limits
- Add alpha-beta pruning and move ordering
- Tune evaluation heuristics and search depth

## Failure modes
- Poor evaluation functions cause blunders
- Exponential branching without pruning
- Horizon effect on tactical positions
- Non-deterministic behavior without fixed seeds

## Checklist
- Validate against known optimal moves
- Profile node expansions with and without pruning
- Add deterministic tie-breakers
- Track win/loss/draw rates across opponents

## References
- Minimax — https://en.wikipedia.org/wiki/Minimax
- Alpha-beta pruning — https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
