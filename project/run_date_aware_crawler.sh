#!/usr/bin/env bash
# Run date_aware_crawler.py; saves posts to legal-luminary/_posts.
# Use a terminal where playwright is installed (e.g. conda activate agent-pipeline).
# From project root: ./run_date_aware_crawler.sh   or   bash run_date_aware_crawler.sh

set -e
cd "$(dirname "$0")"

if ! python3 -c "import playwright" 2>/dev/null; then
  echo "Playwright not found. Activate your env first, e.g.:"
  echo "  conda activate agent-pipeline"
  exit 1
fi

echo "Running date_aware_crawler -> legal-luminary/_posts"
python3 src/agent/date_aware_crawler.py
