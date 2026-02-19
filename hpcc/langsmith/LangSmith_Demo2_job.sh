#!/bin/bash
# Pulled from ~/hpcc. Update cd path and config.env path for your cluster account (e.g. /lustre/work/YOUR_USERNAME/langsmith).
#SBATCH --job-name=langsmith_demo2
#SBATCH --partition=matador
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --gres=gpu:v100:1
#SBATCH --time=06:00:00
#SBATCH --output=langsmith_demo2_%j.out
#SBATCH --error=langsmith_demo2_%j.err

# Environment: bashrc, modules, then conda (required before any python)
source ~/.bashrc
module load gcc/13.2.0 cuda/12.9.0 python/3.12.5
conda activate cs5374

cd /lustre/work/sweeden/CS5374_SOFTWARE_VV/langsmith

export OLPORT=55131
export OLLAMA_HOST=127.0.0.1:$OLPORT
export OLLAMA_BASE_URL="http://localhost:$OLPORT"
export MODEL=granite-code:34b

source ~/config.env

echo "Starting Ollama on port $OLPORT"
$HOME/ollama-latest/bin/ollama serve > ollama_$OLPORT.log 2> ollama_$OLPORT.err &
sleep 8

echo "Running LangSmith_Demo2.py..."

python LangSmith_Demo2.py

echo "Done"
