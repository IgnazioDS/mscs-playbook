#!/usr/bin/env bash
set -euo pipefail

# Bootstrap script for `mscs-playbook`.
# Goal: ensure the repository skeleton exists and is consistent with the current roadmap.
# This script is idempotent: it only creates missing folders/files and never overwrites existing content.

echo "Bootstrapping mscs-playbook repository structure…"

ensure_dir() {
  mkdir -p "$1"
}

ensure_file() {
  local path="$1"
  local content="$2"
  if [[ ! -f "$path" ]]; then
    ensure_dir "$(dirname "$path")"
    printf "%s" "$content" > "$path"
  fi
}

# -----------------------------------------------------------------------------
# Top-level structure
# -----------------------------------------------------------------------------
ensure_dir ".github/workflows"
ensure_dir "docs/tracks"
ensure_dir "modules"
ensure_dir "projects"
ensure_dir "tools/templates"

ensure_file "modules/README.md" $'# Modules\n\nThis directory contains curriculum-aligned modules. Each module includes concepts, cheat sheets, implementations, case studies, exercises, and notes.\n'
ensure_file "projects/README.md" $'# Projects\n\nThis directory contains flagship, end-to-end projects that integrate multiple modules.\n'
ensure_file "docs/README.md" $'# Docs\n\nDocumentation hub for learning tracks and navigation.\n'
ensure_file "docs/index.md" $'# mscs-playbook — Docs\n\n## Learning Tracks\n\n- [CS Fundamentals](tracks/cs-fundamentals.md)\n- [Systems Engineering](tracks/systems-engineering.md)\n- [AI Engineer](tracks/ai-engineer.md)\n- [Autonomy and Robotics](tracks/autonomy-robotics.md)\n- [Responsible Computing](tracks/responsible-computing.md)\n\n## References\n\n- [References](references.md)\n'
ensure_file "docs/references.md" $'# References\n\nAdd books, papers, standards, and high-quality links here.\n'

ensure_file "docs/tracks/cs-fundamentals.md" $'# Track — CS Fundamentals\n\nFoundations → Algorithms.\n'
ensure_file "docs/tracks/systems-engineering.md" $'# Track — Systems Engineering\n\nNetworking → Big Data Architecture → OO Design.\n'
ensure_file "docs/tracks/ai-engineer.md" $'# Track — AI Engineer\n\nMachine Learning → NLP → Computer Vision → Generative AI.\n'
ensure_file "docs/tracks/autonomy-robotics.md" $'# Track — Autonomy and Robotics\n\nAutonomous Systems → Reinforcement Learning → Robotics.\n'
ensure_file "docs/tracks/responsible-computing.md" $'# Track — Responsible Computing\n\nEthics → HCI → AI implications.\n'

# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------
ensure_dir "tools/templates/module-template"
ensure_dir "tools/templates/concept-template"
ensure_dir "tools/templates/case-study-template"
ensure_dir "tools/templates/mini-project-template"

ensure_file "tools/README.md" $'# Tools\n\nScripts, utilities, and templates for maintaining consistent structure and quality.\n'

ensure_file "tools/templates/module-template/README.md" $'# Module Template\n\n## Required Sections\n\n- Overview\n- Prerequisites\n- Concepts (links)\n- Cheat Sheet (link)\n- Implementations (how to run)\n- Case Studies (link)\n- Exercises\n- Notes\n- Testing and Verification\n- Status\n'

ensure_file "tools/templates/concept-template/README.md" $'# Concept Page Template\n\n## Structure\n\n- What it is\n- Why it matters\n- Core idea (intuition)\n- Formal definition (lightweight)\n- Patterns / techniques\n- Complexity notes\n- Pitfalls\n- References\n'

ensure_file "tools/templates/case-study-template/README.md" $'# Case Study Template\n\n## Structure\n\n- Context\n- Problem statement\n- Constraints\n- Options considered\n- Decision and rationale\n- Implementation notes\n- Verification\n- Failure modes\n- Takeaways\n'

ensure_file "tools/templates/mini-project-template/README.md" $'# Mini-Project Template\n\n## Structure\n\n- Goal\n- Requirements\n- Inputs/outputs\n- Implementation plan\n- How to run\n- How to test\n- Extensions\n'

# -----------------------------------------------------------------------------
# Modules scaffold (matches the current roadmap)
# -----------------------------------------------------------------------------
modules=(
  "00-foundations"
  "01-algorithms"
  "02-network-systems"
  "03-machine-learning"
  "04-ethics"
  "05-autonomous-systems"
  "06-big-data-architecture"
  "07-data-mining"
  "08-robotics-webots"
  "09-ooad"
  "10-nlp"
  "11-generative-ai"
  "12-computer-vision"
  "13-artificial-intelligence"
  "14-reinforcement-learning"
  "15-hci"
)

for m in "${modules[@]}"; do
  base="modules/${m}"
  ensure_dir "${base}/01-concepts"
  ensure_dir "${base}/02-cheatsheets"
  ensure_dir "${base}/03-implementations/python/src"
  ensure_dir "${base}/03-implementations/python/tests"
  ensure_dir "${base}/03-implementations/typescript/src"
  ensure_dir "${base}/03-implementations/typescript/tests"
  ensure_dir "${base}/04-case-studies"
  ensure_dir "${base}/05-exercises"
  ensure_dir "${base}/06-notes"

  ensure_file "${base}/README.md" $"# ${m}\\n\\nModule overview and navigation.\\n"
  ensure_file "${base}/01-concepts/README.md" $'# Concepts\n\nConcept pages live here.\n'
  ensure_file "${base}/02-cheatsheets/README.md" $'# Cheat Sheets\n\nQuick references and summaries live here.\n'
  ensure_file "${base}/04-case-studies/README.md" $'# Case Studies\n\nReal-world scenarios and decision tradeoffs live here.\n'
  ensure_file "${base}/05-exercises/README.md" $'# Exercises\n\nPractice problems and mini-project prompts live here.\n'
  ensure_file "${base}/06-notes/README.md" $'# Notes\n\nScratch notes and supplementary material live here.\n'

  ensure_file "${base}/03-implementations/python/README.md" $'# Python Implementations\n\nPlace Python reference implementations under `src/` and tests under `tests/`.\n'
  ensure_file "${base}/03-implementations/typescript/README.md" $'# TypeScript Implementations\n\nPlace TypeScript reference implementations under `src/` and tests under `tests/`.\n'

done

# -----------------------------------------------------------------------------
# Projects scaffold (flagship portfolio layer)
# -----------------------------------------------------------------------------
projects=(
  "p0-algorithms-toolkit"
  "p1-networking-lab-suite"
  "p2-big-data-mini-platform"
  "p3-ml-evaluation-suite"
  "p4-data-mining-pipeline"
  "p5-nlp-system"
  "p6-cv-inference-pipeline"
  "p7-genai-rag-agent-app"
  "p8-rl-playground"
  "p9-autonomous-verification-demo"
  "p10-webots-robotics-suite"
  "p11-hci-ethics-case-studies"
)

for p in "${projects[@]}"; do
  base="projects/${p}"
  ensure_dir "${base}/docs"
  ensure_dir "${base}/src"
  ensure_dir "${base}/tests"
  ensure_dir "${base}/scripts"
  ensure_dir "${base}/docker"

  ensure_file "${base}/README.md" $"# ${p}\\n\\n## Purpose\\n\\n## Modules Used\\n\\n## How to Run\\n\\n## Testing\\n\\n## Milestones\\n"

done

# -----------------------------------------------------------------------------
# Root-level optional files (only created if missing)
# -----------------------------------------------------------------------------
ensure_file "ROADMAP.md" $'# ROADMAP\n\nSee repository roadmap and completion checklists here.\n'
ensure_file "CONTRIBUTING.md" $'# Contributing\n\nGuidelines for contributors will live here.\n'
ensure_file "STRUCTURE.md" $'# Repository Structure\n\nHigh-level structure and design philosophy for mscs-playbook.\n'

cat << 'OUT'
Bootstrap complete.

Notes:
- This script is safe to re-run; it does not overwrite existing files.
- If you want to regenerate content, edit files manually rather than relying on bootstrap.
OUT
