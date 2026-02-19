# Connecting to LLMs and Running OLLAMA on the Texas Tech RedRaider Cluster

This guide integrates the CS5374 Software V&V repository with the **Texas Tech High Performance Computing Center (HPCC)** RedRaider cluster for running OLLAMA and connecting LangChain/LangGraph applications to LLMs on the cluster.

---

## 1. Connecting to RedRaider

### Option A: Web browser (Open OnDemand)

1. Go to the [HPCC OnDemand Portal](https://ondemand.hpcc.ttu.edu/).
2. Log in with your **eRaider** username and password.
3. Open a shell:
   - From **Clusters** → **RedRaider Cluster Shell Access**, or
   - From **Pinned Apps** → **RedRaider Cluster Shell Access**.

Direct link: [Open OnDemand HPCC Shell](https://ondemand.hpcc.ttu.edu/pun/sys/shell/ssh/login.hpcc.ttu.edu).

### Option B: SSH from your machine

```bash
ssh -q -i ~/.ssh/id_rsa sweeden@login.hpcc.ttu.edu
```

Replace `YOUR_ERAIDER` with your eRaider username. Use your actual key path if different from `~/.ssh/id_rsa`.

---

## 2. Running OLLAMA on RedRaider

OLLAMA runs in an **interactive or batch session on the Matador GPU partition**. CPU-only (nocona/quanah) is possible but very slow except for the smallest models.

**Important:** Use the minimum resources you need. Exit interactive sessions when done. Prefer batch jobs for long or production runs.

### 2.1 One-time setup (on login or any node)

1. Create a directory and download the Linux AMD64 tarball:

```bash
mkdir -p ~/ollama-latest && cd ~/ollama-latest
wget https://ollama.com/download/ollama-linux-amd64.tgz -O ollama-linux-amd64.tgz
tar -zxvf ollama-linux-amd64.tgz
```

To pin a specific version (e.g. 0.12.3), use:

```bash
wget "https://ollama.com/download/ollama-linux-amd64.tgz?version=0.12.3" -O ollama-linux-amd64.tgz
```

2. (Optional) Add OLLAMA to your PATH:

```bash
export PATH=~/ollama-latest/bin:$PATH
which ollama   # verify
```

### 2.2 Get a GPU session (Matador)

Load CUDA before running OLLAMA. Request an interactive session:

**Single GPU (1–20 CPUs):**

```bash
interactive -c 20 -g 1 -p matador
```

**Dual GPU (1–40 CPUs):**

```bash
interactive -c 40 -g 2 -p matador
```

Then load modules:

```bash
module load gcc/13.2.0 cuda/12.9.0 python/3.12.5
```

Check GPUs: `nvidia-smi`.

### 2.3 Start OLLAMA in the session

In the **same** interactive (or batch) session:

```bash
# Dynamic port (avoids collisions with other users)
export OLPORT=$(python3 -c "import socket; s = socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()")
export OLLAMA_HOST=127.0.0.1:$OLPORT
export OLLAMA_BASE_URL="http://localhost:$OLPORT"

# Load modules if not already loaded
module load gcc/13.2.0 cuda/12.9.0

# Start server in background
~/ollama-latest/bin/ollama serve > ollama_$OLPORT.log 2> ollama_$OLPORT.err &
```

Use the client in that session:

```bash
~/ollama-latest/bin/ollama run granite-code:34b --verbose
```

Or pull a model first:

```bash
~/ollama-latest/bin/ollama pull granite-code:20b
~/ollama-latest/bin/ollama run granite-code:20b "Say hello in one sentence."
```

The server stops when you exit the session or the batch job ends.

### 2.4 Batch jobs

For long or repeated runs, use SLURM batch scripts. Example job scripts are in this repo under **`hpcc/`** (pulled from `~/hpcc`):

- `hpcc/scripts/ollama-codellama70b.sh` – OLLAMA on GPU (toreador partition)
- `hpcc/langsmith/LangSmith_Demo2_job.sh` – LangSmith Demo2 with OLLAMA
- `hpcc/langsmith/vague_spec_job.sh` – Vague-spec agent with OLLAMA

Submit from the login node after uploading scripts:

```bash
cd /lustre/work/sweeden/CS5374_SOFTWARE_VV/langsmith   # or your project path
sbatch vague_spec_job.sh
```

See [TTU Job Submission Guide](https://www.depts.ttu.edu/hpcc/userguides/JobSubmission.php) for details.

---

## 3. Connecting LangChain/LangGraph to cluster OLLAMA

### 3.1 From a process on the same node (e.g. batch job)

If your Python code runs in the **same** session where OLLAMA is serving (same node, same `OLLAMA_HOST`):

- Set before starting OLLAMA (as above):
  - `OLLAMA_HOST=127.0.0.1:$OLPORT`
  - `OLLAMA_BASE_URL="http://localhost:$OLPORT"`
- Use `ChatOllama` as usual; it will use `OLLAMA_HOST` / `OLLAMA_BASE_URL`:

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="granite-code:20b", temperature=0)
response = llm.invoke("Hello, world!")
```

### 3.2 From your laptop (port forwarding)

To use the cluster’s OLLAMA from your **local** machine (e.g. Jupyter or scripts on your laptop):

1. On the cluster, in the session where OLLAMA is running, note `$OLPORT` (or read it from the job output/log).
2. In a **new local terminal**, forward a local port to that node and port. If the job runs on a worker node, you must forward through the login node to the worker (replace `NODE_NAME` with the worker hostname from `SLURM_NODELIST` or job output):

```bash
# Replace NODE_NAME and OLPORT with values from your job
ssh -L 55131:NODE_NAME:OLPORT -q -i ~/.ssh/id_rsa YOUR_ERAIDER@login.hpcc.ttu.edu
```

For an **interactive** session where you start OLLAMA on the **login node** (not recommended for heavy use), you can use:

```bash
ssh -L 55131:127.0.0.1:$OLPORT -q -i ~/.ssh/id_rsa YOUR_ERAIDER@login.hpcc.ttu.edu
```

3. On your laptop, point LangChain to the forwarded port:

```python
import os
from langchain_ollama import ChatOllama

# Use forwarded port (e.g. 55131)
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:55131"
llm = ChatOllama(model="granite-code:20b", temperature=0, base_url="http://127.0.0.1:55131/v1")
```

Or with the OpenAI-compatible API (e.g. for notebooks):

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:55131/v1", api_key="ollama")
# use client as usual
```

---

## 4. Cluster paths and uploading this repo / hpcc files

- **Work directory (Lustre):** Use `/lustre/work/YOUR_USERNAME/` for persistent code and data.
- **Upload scripts:** Copy job scripts from this repo’s `hpcc/` (or from `~/hpcc`) to the cluster, then submit from there:

```bash
scp -i ~/.ssh/id_rsa hpcc/scripts/*.sh YOUR_ERAIDER@login.hpcc.ttu.edu:/lustre/work/YOUR_USERNAME/scripts/
scp -i ~/.ssh/id_rsa hpcc/langsmith/*.sh YOUR_ERAIDER@login.hpcc.ttu.edu:/lustre/work/YOUR_USERNAME/langsmith/
```

- **Paths in scripts:** The copied scripts may reference paths like `/lustre/work/sweeden/`. Edit them to use your own username and project paths before running.

---

## 5. References

| Resource | URL |
|----------|-----|
| Running OLLAMA on RedRaider | https://www.depts.ttu.edu/hpcc/userguides/application_guides/ollama.php |
| Shell access (Open OnDemand) | https://www.depts.ttu.edu/hpcc/userguides/OpenOnDemand/Shell_Access.php |
| Job submission | https://www.depts.ttu.edu/hpcc/userguides/JobSubmission.php |
| HPCC user guides | https://www.depts.ttu.edu/hpcc/userguides/index.php |
| OLLAMA releases | https://github.com/ollama/ollama/releases |
| Support | hpccsupport@ttu.edu |

---

*This document integrates official TTU HPCC instructions with CS5374 course materials. Job scripts and execution order are aligned with the files pulled from `~/hpcc` into the `hpcc/` directory of this repository.*
