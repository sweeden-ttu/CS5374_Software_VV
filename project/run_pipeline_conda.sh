#!/usr/bin/env bash
# Run the crawl pipeline using the conda environment.
# From project root: ./run_pipeline_conda.sh
# Or: bash run_pipeline_conda.sh

set -e
cd "$(dirname "$0")"

ENV_NAME="${CONDA_PIPELINE_ENV:-agent-pipeline}"

if ! conda run -n "$ENV_NAME" python -c "import langgraph" 2>/dev/null; then
  echo "Conda env '$ENV_NAME' missing or missing deps. Create with:"
  echo "  conda env create -f environment.yml"
  echo "  conda activate $ENV_NAME"
  echo "  playwright install chromium"
  exit 1
fi

echo "Running pipeline (conda env: $ENV_NAME)..."
echo "Output: legal-luminary/_posts and legal-luminary/_data/important_articles.json"
echo ""

PYTHONPATH=src conda run -n "$ENV_NAME" python run_crawl_pipeline.py
