#!/usr/bin/env bash

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"

chmod +x \
  "${repo_root}/.githooks/commit-msg" \
  "${repo_root}/.github/skills/conventional-commit/scripts/sanitize-ai-attribution.sh" \
  "${repo_root}/.github/skills/conventional-commit/scripts/setup-git-hooks.sh"

git -C "${repo_root}" config core.hooksPath .githooks

echo "Git hooks configurados em .githooks (commit-msg -> sanitize-ai-attribution.sh)"
