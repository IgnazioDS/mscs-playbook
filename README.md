
# mscs-playbook

A structured, master’s-level Computer Science playbook that combines **deep concepts**, **tested implementations**, **real-world case studies**, and **flagship projects**.

This repository is designed to be both:

1) a high-quality educational resource for students and professionals, and
2) a proof-of-work portfolio demonstrating real engineering and AI capability.

---

## Why this repo exists

Many learning resources are either:

- too theoretical (hard to apply), or
- too practical (no depth, weak foundations, limited rigor).

**mscs-playbook** bridges that gap:

- Concepts are explained with clarity and depth
- Implementations are clean, reproducible, and tested
- Each topic is connected to real-world engineering tradeoffs
- Projects integrate multiple modules to demonstrate applied mastery

---

## What you’ll find inside

The repository is organized into two primary layers:

- **Modules (`modules/`)**: structured learning content (concepts, implementations, case studies)
- **Projects (`projects/`)**: portfolio-grade, end-to-end proof of work

```
mscs-playbook/
  modules/        # Concepts, notes, implementations, case studies
  projects/       # Flagship projects (end-to-end)
  docs/           # Learning tracks, navigation hub, references
  tools/          # Templates, scripts, utilities
```

---

## Curriculum map

Each module mirrors a core area commonly covered in a rigorous MS in Computer Science.

### 00 — Foundations

Essential math and CS fundamentals that support the rest of the repository.

### 01 — Foundations of Data Structures and Algorithms

Dynamic programming, greedy algorithms, approximation algorithms, linear programming, advanced data structures, RSA, and introductory quantum algorithms.

### 02 — Network Systems: Principles and Practice

Linux networking and cloud networking foundations with reproducible labs.

### 03 — Machine Learning

Supervised learning, unsupervised learning, and deep learning foundations with proper evaluation practices.

### 04 — Computing, Ethics, and Society

Professional ethics, responsible computing, and applied ethics case studies.

### 05 — Autonomous Systems

Modeling, requirement specification, verification, and synthesis of autonomous systems.

### 06 — Software Architecture for Big Data

Architecture fundamentals, big-data patterns, and applied system design.

### 07 — Data Mining Foundations and Practice

End-to-end data mining pipeline, methods, and a project-based component.

### 08 — Introduction to Robotics with Webots

Odometry, mapping, trajectory generation, path planning, and task execution.

### 09 — Object-Oriented Analysis & Design

OO principles, design patterns, architecture, and practical refactoring.

### 10 — Natural Language Processing

NLP fundamentals, deep NLP, and systematic model/error analysis.

### 11 — Generative AI

Modern GenAI applications (RAG, tool use, evaluation) and advanced techniques.

### 12 — Computer Vision

CV fundamentals, deep learning for vision, and multimodal understanding.

### 13 — Artificial Intelligence

Intelligent agents, search, knowledge representation, and reasoning under uncertainty.

### 14 — Reinforcement Learning

Classic RL, deep RL, reward design, efficiency, and safety considerations.

### 15 — Human-Computer Interaction

Prototyping, usability testing, and emerging topics including VR/AR and AI interfaces.

---

## Module format (standard)

Every module is built to be readable, teachable, and maintainable.

Each module should contain:

- **Concept pages** (structured explanations)
- **Cheat sheet** (one-page summary)
- **Implementations** (clean reference code)
- **Tests** (correctness and regression)
- **Real-world case studies** (engineering relevance)
- **Exercises** (optional but preferred)

A module is considered **complete** only when it includes:

- 5–10 concept pages
- 1 cheat sheet / summary
- 1 implementation folder (code + tests)
- 1 real-world case study
- 1 mini-project or contribution to a flagship project
- module-level `README.md` with navigation

---

## Learning tracks

For navigation, the repo can be approached through curated tracks:

- **Track A — CS Fundamentals**: Foundations → Algorithms
- **Track B — Systems Engineering**: Networking → Big Data Architecture → OO Design
- **Track C — AI Engineer**: ML → NLP → CV → GenAI
- **Track D — Autonomy & Robotics**: Autonomous Systems → RL → Robotics
- **Track E — Responsible Computing**: Ethics → HCI → AI implications

A track index will live under `docs/`.

---

## Flagship projects (proof of work)

The `projects/` directory contains end-to-end, portfolio-grade projects designed to integrate multiple modules.

Examples include:

- Algorithms toolkit (library + benchmarks)
- Linux and cloud networking lab suite
- Big data architecture mini-platform
- ML evaluation suite
- NLP retrieval + classification system with error analysis
- Computer vision embeddings + inference pipeline
- GenAI application (RAG + tools) with evaluation harness
- Reinforcement learning playground (classic → deep RL)
- Autonomous systems verification / synthesis demo
- Webots robotics suite (odometry → planning)

---

## Getting started

Clone the repository:

```bash
git clone https://github.com/<ignaziods>/mscs-playbook.git
cd mscs-playbook
```

Each module or project may have its own setup instructions.

---

## Running code (recommended conventions)

This repository may contain implementations in multiple languages (primarily **Python** and **TypeScript/JavaScript**).

Common commands you will see:

- Python tests:

  ```bash
  python -m pytest
  ```

- Node tests:

  ```bash
  npm test
  ```

- Service-backed projects:

  ```bash
  docker compose up
  ```

As the repository evolves, a root-level command runner (e.g., `Makefile`) may unify these workflows.

---

## Contributing

Contributions are welcome from students, engineers, and researchers.

Please follow these principles:

- Keep explanations rigorous and structured
- Prefer correctness and clarity over complexity
- Include tests for implementations when applicable
- Avoid copying copyrighted or paid material
- Cite papers and public references when helpful

A full contribution guide will live in `CONTRIBUTING.md`.

---

## Progress and roadmap

The complete plan (modules, standards, and flagship projects) lives in:

- `ROADMAP.md`

---

## License

Recommended licensing structure:

- **MIT** for code
- Optional: **CC BY 4.0** for documentation and written educational content

Add the chosen license(s) to the repository root once finalized.

---

## Author

Built and maintained by **Ignazio De Santis**.

If you find this repository useful, feel free to fork it, reference it, or contribute improvements.
