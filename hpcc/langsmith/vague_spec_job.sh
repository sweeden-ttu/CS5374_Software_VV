#!/bin/bash
# Pulled from ~/hpcc. Update cd path for your cluster account (e.g. /lustre/work/YOUR_USERNAME/langsmith).
#SBATCH --job-name=vague_spec_agent
#SBATCH --partition=matador
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --gres=gpu:v100:1
#SBATCH --time=06:00:00
#SBATCH --output=vague_spec_%j.out
#SBATCH --error=vague_spec_%j.err

# Environment: bashrc, modules, then conda (required before any python/pip)
source ~/.bashrc
module load gcc/13.2.0 cuda/12.9.0 python/3.12.5
conda activate cs5374

cd /lustre/work/sweeden/CS5374_SOFTWARE_VV/langsmith

export OLPORT=$(python3 -c "import socket; s = socket.socket(); s.bind((\"\", 0));print(s.getsockname()[1]);s.close()")
export OLLAMA_HOST=127.0.0.1:$OLPORT
export OLLAMA_BASE_URL="http://localhost:$OLPORT"

echo "Starting Ollama on port $OLPORT"

$HOME/ollama-latest/bin/ollama serve > ollama_$OLPORT.log 2> ollama_$OLPORT.err &
OLLAMA_PID=$!

sleep 8

if ! ps -p $OLLAMA_PID > /dev/null 2>&1; then
    echo "ERROR: Ollama failed to start"
    cat ollama_$OLPORT.err
    exit 1
fi

echo "Ollama started PID $OLLAMA_PID"

$HOME/ollama-latest/bin/ollama pull granite-code:4b

echo "Running agent..."
python3 vague_spec_agent.py

kill $OLLAMA_PID 2>/dev/null
echo "Done"
