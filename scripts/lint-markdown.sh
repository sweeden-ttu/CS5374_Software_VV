#!/usr/bin/env bash
# Lint and optionally fix markdown in this repo. Requires Node.js/npx.
set -e
cd "$(dirname "$0")/.."
echo "Running markdownlint --fix..."
npx markdownlint-cli@latest "**/*.md" --fix
echo "Running markdownlint (report only)..."
npx markdownlint-cli@latest "**/*.md"
