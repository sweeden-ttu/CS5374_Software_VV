# HPCC / RedRaider integration

This directory contains **files pulled from `~/hpcc`** for running LLM workloads (OLLAMA, LangSmith, LangGraph) on the **Texas Tech RedRaider cluster**.

## Contents

| Path | Description |
|------|-------------|
| `scripts/` | SLURM job scripts for OLLAMA (e.g. `ollama-codellama70b.sh`) |
| `langsmith/` | Job scripts and agents for LangSmith/LangGraph on the cluster |
| `AGENTS.md` | Execution order, cluster paths, and OLLAMA notes for agents |

## Syncing from ~/hpcc

To refresh these files from your local `~/hpcc`:

```bash
# From repo root
cp ~/hpcc/scripts/*.sh hpcc/scripts/
cp ~/hpcc/langsmith/langsmith/*.sh hpcc/langsmith/
cp ~/hpcc/langsmith/langsmith/vague_spec_agent.py hpcc/langsmith/   # optional
cp ~/hpcc/AGENTS.md hpcc/   # optional, if you keep a full copy
```

Or use `rsync` to mirror selected subdirs:

```bash
rsync -av --include='*.sh' --include='*.py' --exclude='*' ~/hpcc/langsmith/langsmith/ hpcc/langsmith/
rsync -av ~/hpcc/scripts/ hpcc/scripts/
```

## Using these files on the cluster

1. **Upload** scripts to the cluster (replace `YOUR_ERAIDER` and cluster path):

   ```bash
   scp -i ~/.ssh/id_rsa hpcc/scripts/*.sh YOUR_ERAIDER@login.hpcc.ttu.edu:/lustre/work/YOUR_USERNAME/scripts/
   scp -i ~/.ssh/id_rsa hpcc/langsmith/*.sh YOUR_ERAIDER@login.hpcc.ttu.edu:/lustre/work/YOUR_USERNAME/langsmith/
   ```

2. **Edit paths** in the scripts: replace `/lustre/work/sweeden/` (or similar) with your cluster username and project path.

3. **Submit jobs** from the login node after SSH’ing in:

   ```bash
   ssh YOUR_ERAIDER@login.hpcc.ttu.edu
   cd /lustre/work/YOUR_USERNAME/langsmith
   sbatch vague_spec_job.sh
   ```

## Documentation

- **Connecting to RedRaider and running OLLAMA:** [docs/RedRaider_LLM_Ollama.md](../docs/RedRaider_LLM_Ollama.md)
- **TTU HPCC:** [Running Ollama on RedRaider](https://www.depts.ttu.edu/hpcc/userguides/application_guides/ollama.php)
