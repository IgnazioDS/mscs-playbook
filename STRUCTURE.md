# Repository Structure

This repository separates curriculum content, portfolio-oriented projects, lightweight navigation docs, and support utilities so the study path and the proof-of-work layer do not collapse into the same directory.

The current structure is organized around a small number of stable top-level areas.

## Top-Level Layout

```text
.
├── README.md
├── STRUCTURE.md
├── LICENSE
├── bootstrap.sh
├── docs/
├── modules/
├── projects/
├── scripts/
├── tools/
└── .github/
```

## Directory Roles

- `README.md`: top-level explanation of the repository's current value and navigation
- `STRUCTURE.md`: concise explanation of how the repository is organized
- `docs/`: lightweight documentation hub pointing readers to the main navigation surfaces
- `modules/`: the curriculum layer, organized as numbered modules from `00` through `17`
- `projects/`: portfolio-facing project briefs that synthesize multiple modules
- `scripts/`: repository-level helper scripts
- `tools/`: templates and supporting utilities
- `.github/`: workflow and repository automation configuration

## Modules Layer

The `modules/` directory is the main learning path. Each module corresponds to a numbered curriculum area such as foundations, algorithms, machine learning, networking, reinforcement learning, or quantum computing.

The current module set is:

- `00-foundations`
- `01-algorithms`
- `02-network-systems`
- `03-machine-learning`
- `04-ethics`
- `05-autonomous-systems`
- `06-big-data-architecture`
- `07-data-mining`
- `08-robotics-webots`
- `09-object-oriented-analysis-and-design`
- `10-natural-language-processing`
- `11-generative-ai`
- `12-computer-vision`
- `13-artificial-intelligence`
- `14-reinforcement-learning`
- `15-human-computer-interaction`
- `16-cryptography-and-number-theory`
- `17-quantum-computing`

### Standard Module Shape

Modules are normalized around a consistent internal pattern:

```text
modules/<nn>-<topic>/
├── README.md
├── 01-concepts/
├── 02-cheatsheets/
├── 03-implementations/
├── 04-case-studies/
├── 05-exercises/
└── 06-notes/
```

Important conventions:

- numbered concept pages inside `01-concepts/` reflect reading order
- the module `README.md` is the source of truth for that module's scope and navigation
- implementation depth varies by module, so the shared shape should not be interpreted as uniform completeness

## Projects Layer

The `projects/` directory contains integration-oriented project briefs rather than additional module content.

Current projects include:

- `p0-algorithms-toolkit`
- `p1-networking-lab-suite`
- `p2-big-data-mini-platform`
- `p3-ml-evaluation-suite`
- `p4-data-mining-pipeline`
- `p5-nlp-system`
- `p6-cv-inference-pipeline`
- `p7-genai-rag-agent-app`
- `p8-rl-playground`
- `p9-autonomous-verification-demo`
- `p10-webots-robotics-suite`
- `p11-hci-ethics-case-studies`

Each project README defines:

- purpose
- scope
- modules used
- run instructions
- test instructions
- expected output

Projects are meant to synthesize modules, not replace them.

## Docs Layer

The `docs/` directory is intentionally lightweight. It is not a second full documentation system. Its role is to point readers toward:

- the root README
- the modules index
- the projects index
- any lightweight track or navigation aids

## Support Layer

Two support directories sit alongside the curriculum and project layers:

- `scripts/` for repository-level helper scripts
- `tools/` for templates and reusable utilities

These exist to support the content structure rather than to define a separate product surface.

## Reading Guidance

For concept-first use:

1. start at `README.md`
2. move to `modules/README.md`
3. enter a target module and follow its numbered concept files

For portfolio-first use:

1. start at `projects/README.md`
2. choose a project brief
3. use its listed modules as the theory and implementation backplane
