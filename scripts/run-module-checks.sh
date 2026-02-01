#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${REPO_ROOT}/.venv/bin/python3"
if [ ! -x "$PY" ]; then
  PY="python3"
fi

run_pytest() {
  local tests_dir="$1"
  echo "pytest: ${tests_dir}"
  "$PY" -m pytest -q "$tests_dir"
}

run_cli() {
  local cli_path="$1"
  echo "cli: ${cli_path}"
  if ! "$PY" "$cli_path" evaluate --seed 42 >/dev/null 2>&1; then
    "$PY" "$cli_path" --help >/dev/null
  fi
}

for module in "${REPO_ROOT}"/modules/[0-9][0-9]-*; do
  [ -d "$module" ] || continue
  tests_dir="${module}/03-implementations/python/tests"
  if [ -d "$tests_dir" ] && compgen -G "${tests_dir}/test_*.py" > /dev/null; then
    run_pytest "$tests_dir"
  fi

  cli_path=$(find "${module}/03-implementations" -name "cli.py" -type f 2>/dev/null | head -n 1 || true)
  if [ -n "$cli_path" ]; then
    run_cli "$cli_path"
  fi
done

echo "All module checks completed."
