#!/usr/bin/env bash
# Run cleanup_summarize.py using the Miniconda agent-pipeline environment.
# Requires: conda installed, and env created with: conda env create -f environment.yml

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Find conda: use CONDA_EXE if set, else common Miniconda locations
if [ -n "$CONDA_EXE" ] && [ -x "$CONDA_EXE" ]; then
  _conda="$CONDA_EXE"
elif [ -x "$HOME/miniconda3/bin/conda" ]; then
  _conda="$HOME/miniconda3/bin/conda"
elif [ -x "$HOME/opt/miniconda3/bin/conda" ]; then
  _conda="$HOME/opt/miniconda3/bin/conda"
elif [ -x "/opt/homebrew/Caskroom/miniconda/base/bin/conda" ]; then
  _conda="/opt/homebrew/Caskroom/miniconda/base/bin/conda"
else
  _conda="$(command -v conda 2>/dev/null)" || true
fi

if [ -z "$_conda" ] || [ ! -x "$_conda" ]; then
  echo "Conda not found. Install Miniconda or ensure conda is in PATH."
  exit 1
fi

# Source conda for this shell
_conda_root="$("$_conda" info --base 2>/dev/null)"
if [ -z "$_conda_root" ]; then
  echo "Could not get conda base path."
  exit 1
fi
# shellcheck source=/dev/null
. "$_conda_root/etc/profile.d/conda.sh"
conda activate agent-pipeline

# Optional: override posts dir via env
export LEGAL_LUMINARY_POSTS="${LEGAL_LUMINARY_POSTS:-/Volumes/RepoPart1/legal-luminary/_posts}"

echo "Using Python: $(which python)"
echo "Posts dir: $LEGAL_LUMINARY_POSTS"
echo "---"
python src/agent/cleanup_summarize.py
