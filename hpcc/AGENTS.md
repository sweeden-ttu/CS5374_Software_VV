# HPCC / RedRaider — Agent execution order

This file is pulled from `~/hpcc/AGENTS.md` and summarizes the execution order and OLLAMA setup for agents running on the Texas Tech RedRaider cluster. Replace `sweeden` (or similar) with your cluster username where applicable.

---

## Cluster paths (Lustre)

| Purpose        | Path on cluster                    |
|----------------|------------------------------------|
| User work root | `/lustre/work/sweeden/`      |
| LangSmith etc. | `/lustre/work/sweeden/CS5374_SOFTWARE_VV` |

Code and data under `/lustre/work/sweeden/CS5374_SOFTWARE_VV/hpcc` persist across sessions.

**Scripts:** Upload job scripts to the cluster before submitting (e.g. via `scp` to `/lustre/work/sweeden/CS5374_SOFTWARE_VV/hpcc/scripts/` or `.../langsmith/`).

---

## Execution order (do not skip)

1. **Check existing jobs**  
   `squeue -u YOUR_USERNAME`  
   If OLLAMA/Jupyter/batch is already running, wait or reuse that allocation.

2. **SSH to login node**  
   `ssh -q -i ~/.ssh/id_rsa YOUR_USERNAME@login.hpcc.ttu.edu`

3. **Environment**  
   `source ~/.bashrc` then confirm access to your paths.

4. **Project directory**  
   `cd /lustre/work/YOUR_USERNAME/<project>`

5. **Conda (if used)**  
   `conda activate <environment>`

6. **Modules (required before Python/GPU)**  
   - Python: `module load Python/3.12.0` (or version on cluster)  
   - GPU: `module load gcc/13.2.0 cuda/12.9.0 python/3.12.5`

7. **Compute allocation**  
   - CPU: `interactive -c <cores> -t <time> -p nocona`  
   - GPU: `interactive -c 20 -g 1 -p matador` (or `-g 2 -c 40` for 2 GPUs)  
   - Batch: `sbatch <script.sh>`

8. **Run workload** — only after steps 1–7.

9. **Port forwarding (Jupyter/OLLAMA)**  
   - Jupyter: `ssh -L 8888:127.0.0.1:8888 ... YOUR_USERNAME@login.hpcc.ttu.edu`  
   - OLLAMA: use dynamic `$OLPORT`; forward e.g. `ssh -L 55131:NODE:OLPORT ...` (see [docs/RedRaider_LLM_Ollama.md](../docs/RedRaider_LLM_Ollama.md)).

---

## OLLAMA on RedRaider

- **Official guide:** [Running Ollama on RedRaider](https://www.depts.ttu.edu/hpcc/userguides/application_guides/ollama.php)
- **Partition:** `matador` for GPU; `gpu-build` when matador is busy.
- **Modules:** `module load gcc/13.2.0 cuda/12.9.0 python/3.12.5`
- **Install:** Linux AMD64 tarball in `~/ollama-latest`.
- **Port:** Use a dynamic port in each session:
  ```bash
  export OLPORT=$(python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()")
  export OLLAMA_HOST=127.0.0.1:$OLPORT
  ~/ollama-latest/bin/ollama serve >ollama_$OLPORT.log 2>&1 &
  ```
- **Access from laptop:** `ssh -L 55131:127.0.0.1:$OLPORT ...` (or to worker node; see main doc).
- Prefer **batch** for production; exit interactive sessions when done.

---

## Job script template

```bash
#!/bin/bash
#SBATCH -p matador
#SBATCH -t 02:00:00
#SBATCH --gres=gpu:1
#SBATCH -c 20

source ~/.bashrc
module load gcc/13.2.0 cuda/12.9.0 python/3.12.5
conda activate myenv   # if needed

cd /lustre/work/YOUR_USERNAME/<project>
python train.py
```

---

Full integration instructions: [docs/RedRaider_LLM_Ollama.md](../docs/RedRaider_LLM_Ollama.md).
