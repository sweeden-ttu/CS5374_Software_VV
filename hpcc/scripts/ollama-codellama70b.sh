#!/bin/bash
# Pulled from ~/hpcc. Update paths and mail-user for your cluster account (e.g. /lustre/work/YOUR_USERNAME/).
#SBATCH --job-name=ollama_codellama70b
#SBATCH -p toreador
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:a100:1
#SBATCH --time=01:00:00
#SBATCH --output=agent_%j.out
#SBATCH --error=agent_%j.err
#SBATCH --mail-user=sweeden@ttu.edu
#SBATCH --mail-type=BEGIN,END,FAIL,REQUEUE,ALL

# Environment: bashrc, modules, then conda (required before any python)
source ~/.bashrc
module load gcc/13.2.0 cuda/12.9.0 python/3.12.5
conda activate cs5374

# Get unique port for Ollama
export OLPORT=$(python3 -c "import socket; s = socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()")
export OLLAMA_HOST=127.0.0.1:$OLPORT
export OLLAMA_BASE_URL="http://localhost:$OLPORT"


echo "Starting Ollama server on port $OLPORT"
echo "OLLAMA compute node: ${SLURM_NODELIST}"
echo "Forward local port 55131: ssh -L 55131:${SLURM_NODELIST}:$OLPORT -q -i ~/.ssh/id_rsa sweeden@login.hpcc.ttu.edu"
echo "Then use OLLAMA at http://127.0.0.1:55131"

# Start Ollama server in background
$HOME/ollama-latest/bin/ollama serve > ollama_$OLPORT.log 2> ollama_$OLPORT.err &
OLLAMA_PID=$!

# Wait for server to start
sleep 8

# Check if server is running (fixed: use PID check instead of pgrep with spaces)
if kill -0 $OLLAMA_PID 2>/dev/null; then
    echo "Ollama server started successfully (PID: $OLLAMA_PID)"
else
    echo "Failed to start Ollama server"
    cat ollama_$OLPORT.err
    exit 1
fi

MODEL=${MODEL:-codellama:70b}
echo "Using model: $MODEL"

# Pull model if needed
echo "Ensuring model is available..."
$HOME/ollama-latest/bin/ollama pull $MODEL

# Check if we have a Python agent script to run
AGENT_SCRIPT=${AGENT_SCRIPT:-}
if [ -n "$AGENT_SCRIPT" ] && [ -f "$AGENT_SCRIPT" ]; then
    echo "Running agent script: $AGENT_SCRIPT"
    python3 "$AGENT_SCRIPT"
else
    # Get prompt from environment or use default
    PROMPT=${AGENT_PROMPT:-"Review the RUBRIC, SPECS, and PROJECTPLAN in the /lustre/work/sweeden/CS5374_SOFTWARE_VV/langsmith folder. If there are any outstanding code changes pending a git commit or git add, review the changes for any issues. If no issues are found commit outstanding changes, squash all commits and publish all changes to a new branch and/or new repository using the github command line interface.  Once all published changes are pushed to the main or default branch, check the status of any CI/CD commands in the github workflow actions.  If any actions are unsuccessful, debug the actions and fix the issues.  If all actions are successful, update the RUBRIC, test the SPECS, and update the PROJECTPLAN with the results of the tests.  If the tests are successful, update the RUBRIC, SPECS, and PROJECTPLAN with the results of the tests.  If the tests are unsuccessful, debug the tests and fix the issues.  If the tests are successful, update the RUBRIC, SPECS, and PROJECTPLAN with the results of the tests, and results of experiments in LangChain observables.  If the tests are unsuccessful, debug the tests and fix the issues.  If the tests are successful, update the RUBRIC, SPECS, and PROJECTPLAN with the results of the tests. Then kick off the LangGraph orchetration agennt. Remember all evidence and reuslts must be traceable so log observable evetns in LangChain, LangGraph, and LangSmith. All actions and results must be traceable and reproducible so log all actions and results in LangChain, LangGraph, and LangSmith."}
    echo "Running prompt: $PROMPT"
    $HOME/ollama-latest/bin/ollama run $MODEL "$PROMPT"
fi

echo "Agent execution completed"
