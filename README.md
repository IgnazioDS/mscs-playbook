# mscs-playbook

`mscs-playbook` is a graduate-level computer science learning repository built as both a structured curriculum and a proof-of-work portfolio.

It is designed to be useful in two ways:

1. as a concept-first MSCS study path with ordered readings across major CS domains
2. as an engineering portfolio with runnable implementations and project briefs tied to those domains

## What the repo offers today

The current repository already provides:

- 18 numbered curriculum modules under [`modules/`](modules/)
- ordered concept sequences across the full curriculum from foundations through quantum computing
- module-level navigation for concepts, cheatsheets, implementations, case studies, exercises, and notes
- 12 portfolio-oriented project directories under [`projects/`](projects/)
- a clear separation between curriculum content, portfolio projects, navigation docs, and tooling

The practical value of the repo today is not only that it lists topics. It already gives a coherent reading order across the curriculum and ties many areas to concrete implementation or project surfaces.

## Repository Structure

The repository is organized around four top-level areas:

```text
mscs-playbook/
  docs/       # Lightweight navigation docs
  modules/    # Curriculum modules and learning content
  projects/   # Portfolio-style project briefs aligned to modules
  tools/      # Templates and supporting utilities
```

Supporting references:

- [Repository Structure](STRUCTURE.md)
- [Docs Index](docs/README.md)
- [Modules Index](modules/README.md)
- [Projects Index](projects/README.md)

## Current Curriculum

The module sequence currently covers:

- `00` Foundations
- `01` Algorithms
- `02` Network Systems
- `03` Machine Learning
- `04` Ethics
- `05` Autonomous Systems
- `06` Big Data Architecture
- `07` Data Mining
- `08` Robotics with Webots
- `09` Object-Oriented Analysis and Design
- `10` Natural Language Processing
- `11` Generative AI
- `12` Computer Vision
- `13` Artificial Intelligence
- `14` Reinforcement Learning
- `15` Human-Computer Interaction
- `16` Cryptography and Number Theory
- `17` Quantum Computing

Each module is intended to be read through its numbered concept pages in order. The most reliable source of truth for any module's maturity is that module's own `README.md`.

## What Is Standardized Across Modules

The repo has been normalized around a common documentation shape:

- numbered concept pages reflecting prerequisite order
- module-level `README.md` navigation
- subdirectories for concepts, cheatsheets, implementations, case studies, exercises, and notes

Not every module currently offers the same implementation depth. Some modules are concept-heavy, while others already include richer implementation and mini-project surfaces. The root README should therefore describe the repository as a structured curriculum with uneven but growing implementation depth, not as a fully uniform course pack.

## Projects Layer

The repository also includes project briefs under [`projects/`](projects/), including:

- `p0` Algorithms Toolkit
- `p1` Networking Lab Suite
- `p2` Big Data Mini Platform
- `p3` ML Evaluation Suite
- `p4` Data Mining Pipeline
- `p5` NLP System
- `p6` CV Inference Pipeline
- `p7` GenAI RAG Agent App
- `p8` RL Playground
- `p9` Autonomous Verification Demo
- `p10` Webots Robotics Suite
- `p11` HCI Ethics Case Studies

These projects are currently positioned as portfolio-aligned briefs with purpose, scope, module dependencies, and run/test guidance.

## How To Use The Repo

If you want a study path:

- start in [`modules/00-foundations`](modules/00-foundations/)
- continue to [`modules/01-algorithms`](modules/01-algorithms/)
- then branch into systems, AI, autonomy, human-centered computing, or advanced topics based on your goals

If you want portfolio-facing work:

- browse [`projects/`](projects/)
- use the linked module READMEs as the concept and implementation backplane for each project

If you want the fastest repo-wide orientation:

- read [`modules/README.md`](modules/README.md)
- skim a target module `README.md`
- follow the numbered concept files inside that module

## Getting Started

Clone the repository:

```bash
git clone https://github.com/IgnazioDS/mscs-playbook.git
cd mscs-playbook
```

Then enter the module or project you care about and follow its local setup instructions. There is no single root-level workflow that applies uniformly to every module.

Common commands you will encounter in module and project READMEs include:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pytest -q <path-to-tests>
```

and, for service-backed work:

```bash
docker compose up
```

## Current Value Proposition

The repo's value is strongest in these areas:

- a broad, ordered graduate CS reading path
- concept pages written to a consistent structure
- module-level navigation that makes the curriculum traversable
- project briefs that connect curriculum areas to applied engineering outputs

The root README should reflect that current value directly. It should not promise missing global docs, contribution guides, or roadmap files as if they already exist.

## License

See [LICENSE](LICENSE).

## Author

Built and maintained by **Ignazio De Santis**.
