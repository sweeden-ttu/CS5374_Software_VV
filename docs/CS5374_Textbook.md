# CS 5374 – Software Verification and Validation
## Textbook Documentation

**Texas Tech University • Department of Computer Science • Spring 2026**

This textbook consolidates and elevates all course markdown materials into a single, high-quality reference. It is organized in four parts: Foundations, Testing Techniques, LLM Tools and Project, and Assignments and Infrastructure.

---

# Table of Contents

**Part I — Foundations and Course Overview**
1. [Course Overview and Syllabus](#part-i-foundations-and-course-overview)
2. [Course Setup and Video Channel](#2-course-setup-and-video-channel)

**Part II — Software Testing Fundamentals**
3. [Introduction to Software Testing](#3-introduction-to-software-testing)
4. [Functional (Black-Box) Testing](#4-functional-black-box-testing)
5. [Defect Testing: Black-Box and White-Box Techniques](#5-defect-testing-black-box-and-white-box-techniques)
6. [Test Planning and the Economics of Testing](#6-test-planning-and-the-economics-of-testing)

**Part III — LLM Tools, LangSmith, and LangGraph**
7. [LangSmith Setup and Tracing](#7-langsmith-setup-and-tracing)
8. [LangGraph: Graph-Based LLM Workflows](#8-langgraph-graph-based-llm-workflows)
9. [LangSmith Prompt Iteration and Evaluation](#9-langsmith-prompt-iteration-and-evaluation)
10. [Open-Source Frameworks and Tools for LLM V&V](#10-open-source-frameworks-and-tools-for-llm-vv)

**Part IV — Assignments, Project, and Infrastructure**
11. [Assignments and Grading](#11-assignments-and-grading)
12. [Course Project: Trustworthy AI Legal Validator](#12-course-project-trustworthy-ai-legal-validator)
13. [Infrastructure: RedRaider Cluster and HPCC](#13-infrastructure-redraider-cluster-and-hpcc)

---

# Part I — Foundations and Course Overview

## 1. Course Overview and Syllabus

### 1.1 Purpose and Scope

This course provides a comprehensive treatment of **Software Verification and Validation (V&V)**. Students learn to answer two fundamental questions:

| Paradigm | Question | Focus |
|----------|----------|--------|
| **Validation** | "Are we building the right product?" | Testing, dynamic analysis, customer needs |
| **Verification** | "Are we building the product right?" | Formal methods, static analysis, process compliance |

$$
\text{Software Quality} = \text{Validation} + \text{Verification}
$$

### 1.2 Learning Objectives

Upon completion, students will be able to:

1. Apply black-box and white-box testing techniques
2. Generate test cases using adequacy criteria (equivalence partitioning, boundary value analysis, coverage)
3. Implement model-based and graph-based testing
4. Perform fault localization and fault-based testing
5. Apply formal verification methods, including model checking
6. Evaluate AI/ML systems and Large Language Models (LLMs) using LangSmith and related tools

### 1.3 Course Topics (Tentative Timeline)

| Week | Topic |
|------|--------|
| 1 | Introduction to V&V |
| 2 | Adequacy Criterion |
| 4 | Black-Box Testing |
| 5 | White-Box Testing |
| 6 | Model-Based Testing |
| 8 | Graph-Based Testing |
| 9 | Fault-Based Testing & Localization |
| 10 | Security Testing |
| 11–13 | Formal Verification, Model Checking |
| 15–16 | LangSmith Hands-on, AI/LLM/RL Evaluation |

### 1.4 Prerequisites and Resources

- **Prerequisites:** Programming experience; familiarity with software engineering practices
- **Primary textbook:** *Introduction to Software Testing* — Ammann & Offutt ([online slides](https://cs.gmu.edu/~offutt/softwaretest/))
- **Secondary:** *Software Testing and Analysis* (Pezze & Young); *Logic in Computer Science* (Huth & Ryan)
- **AI/LLM:** LangSmith documentation, LangSmith Cookbook, LangGraph documentation

### 1.5 Grading Policy

| Component | Weight (On-Campus) | Weight (Distance) |
|-----------|--------------------|-------------------|
| Project | 18% | 20% |
| Assignments | 27% | 30% |
| Quizzes / Participation | 10% | — |
| Midterm | 15% | 20% |
| Final Exam | 30% | 30% |

### 1.6 Instructor and Support

| Role | Name | Email |
|------|------|--------|
| Instructor | Dr. Akbar S. Namin | akbar.namin@ttu.edu |
| TA 1 | Sonali Singh | sonalsin@ttu.edu |
| TA 2 | Hasan Al-Qudah | halqudah@ttu.edu |

**Academic integrity:** All work must be your own. Plagiarism and cheating result in zero on the assignment and possible further action. See the Texas Tech Student Handbook.

---

## 2. Course Setup and Video Channel

### 2.1 MyMediasite (Video Content)

MyMediasite is the university platform for course video content.

- **Portal:** [engrmediacast.ttu.edu/mediasite/mymediasite](https://engrmediacast.ttu.edu/mediasite/mymediasite)
- **Locating shared folders:** Search by instructor name; use the star icon to favorite folders
- **Uploading presentations:** Choose File → select MP4 → name presentation → select destination → Create Presentation → wait for processing → adjust security (unlock for viewing)
- **Sharing:** Use "Share Presentation" or "Share" on a channel; copy the quick link for students

**Channel naming convention:** `CourseNumber-Section-Faculty-Semester` (e.g., `CS5374-D01-Namin-Spring2026`).

### 2.2 Module Index

| Module | Title | Description |
|--------|-------|-------------|
| 01 | Video Channel | MyMediasite setup (this section) |
| 02 | Outline & Syllabus | Policies and schedule |
| 03 | Lecture Notes | Introduction, Functional, Black-Box, Defect Testing |
| 04 | LangSmith Tutorial | Setup and LLM evaluation |
| 05 | Open Source Tools | Frameworks and projects |
| 06 | LangGraph Hands-on #1 | First LangGraph exercises |
| 07 | Tutorials & Exercises | Practice materials |
| 08 | LangGraph Hands-on #2 | Advanced LangGraph with LangSmith |
| 09 | LangSmith Tracing | Tracing and debugging LLM apps |
| 10 | LangSmith Prompt Iteration | Prompt optimization |

---

# Part II — Software Testing Fundamentals

## 3. Introduction to Software Testing

### 3.1 What Is Software Testing?

**Software testing** is the process of executing a program with the intent of finding errors. Once source code exists, testing is used to uncover and fix defects before delivery.

**Key objectives:**

- **What:** Systematic execution to uncover errors before delivery
- **Who:** Software engineers and testing specialists
- **Why:** Reviews and SQA are necessary but not sufficient
- **How:** Exercise requirements (functional) and internal logic (structural)
- **Work product:** Test cases with expected and actual results

### 3.2 Static vs. Dynamic Analysis

| Type | Description | When Applied |
|------|-------------|--------------|
| **Static analysis** | Inspecting code without executing it | Before runtime (formal methods, inspection, theorem proving) |
| **Dynamic analysis** | Inspecting code by executing it | During runtime (testing, debugging, profiling) |

### 3.3 Terminology: Error, Fault, Failure

| Term | Definition | Example |
|------|-------------|---------|
| **Error** | Mistake made by the programmer | Using `<` where `<=` was required |
| **Fault** | Problem in code that can cause failure | The incorrect `<` in the source |
| **Failure** | Incorrect observable behavior | Wrong output for an input |
| **Defect / Bug** | Informal terms for fault or failure | "There's a bug in the code" |

$$
\text{Error} \xrightarrow{\text{introduces}} \text{Fault} \xrightarrow{\text{execution}} \text{Failure}
$$

### 3.4 Test Cases and Test Infrastructure

A **test case** consists of:

$$
\text{Test Case} = \{\text{Test Input},\, \text{Expected Output},\, \text{Condition}\}
$$

- **Test oracle:** Source of expected results
- **Test driver:** Program that feeds inputs to the component under test and reports results
- **Test stub:** Dummy replacement for a subordinate module
- **Test harness:** Environment (drivers, stubs, data) used to run and monitor tests

### 3.5 Testing Approaches and Levels

| Approach | Basis | Source code required? |
|----------|-------|------------------------|
| **Black-box (functional)** | Specification | No |
| **White-box (structural)** | Code structure | Yes |
| **Gray-box** | Both | Partially |

**Testing levels:** Unit → Integration → System → Acceptance; **regression testing** applies across releases.

### 3.6 Verification vs. Validation

| Aspect | Verification (QA) | Validation (QC) |
|--------|--------------------|------------------|
| **Question** | "Are we building it right?" | "Are we building the right thing?" |
| **Focus** | Process compliance, specs | User requirements |
| **When** | End of each phase | Before delivery |

### 3.7 Adequacy Criterion

An **adequacy criterion** is a predicate on a program and a test suite:

$$
C(P, T) = \begin{cases} \text{True} & \text{if } T \text{ adequately tests } P \\ \text{False} & \text{otherwise} \end{cases}
$$

**Key takeaway:** Stopping criteria (when to stop testing) depend on the test plan, resources, coverage, and risk—an optimization and research problem.

---

## 4. Functional (Black-Box) Testing

### 4.1 Overview

**Functional testing** (black-box, specification-based, behavioral) verifies that the system satisfies its functional requirements. Test design is driven by the specification, not the code.

**Error categories targeted:** Incorrect or missing functions; interface errors; data structure or external data errors; behavior or performance errors; initialization and termination errors.

### 4.2 Equivalence Partitioning (EP)

Partition the input (and optionally output) space into **equivalence classes** such that the program is expected to treat all values in a class alike. One representative per class is tested.

$$
\text{Input Domain} = \bigcup_{i=1}^{n} E_i \quad \text{with } E_i \cap E_j = \emptyset
$$

**Rules:** For a range $[a,b]$ use one valid class and two invalid (below/above); for a specific value, one valid and two invalid; for set membership or Boolean, one valid and one invalid.

### 4.3 Boundary Value Analysis (BVA)

Focus on **boundaries** of equivalence classes, where many faults occur. For a range $[a,b]$ test:

$$
\{a-1,\, a,\, a+1,\, b-1,\, b,\, b+1\}
$$

Apply the same idea to counts, output ranges, and data structure limits.

### 4.4 Other Functional Methods

- **Error guessing:** Use experience and domain knowledge to add tests (empty lists, zero, negative, special characters, GUI edge cases).
- **Pair-wise (IPO):** Cover all pairs of parameter values to reduce test count while preserving interaction coverage.
- **Graph-based:** Model objects and relationships as a graph; use node and link coverage to derive tests.
- **Syntax checking:** Model input syntax (e.g., command-line options) as a state machine; generate valid and invalid sequences.

### 4.5 Summary

| Method | Focus | Best for |
|--------|-------|----------|
| EP | Input classes | Reducing test count |
| BVA | Edge values | Boundary faults |
| Error guessing | Experience | Exploratory testing |
| Pair-wise | Parameter combinations | Multi-parameter systems |
| Graph-based | Relationships | Complex data flows |
| Syntax | Input format | Parsers and CLI |

---

## 5. Defect Testing: Black-Box and White-Box Techniques

### 5.1 Black-Box Techniques (Recap and Examples)

**Equivalence partitioning:** Identify valid and invalid partitions for each input (and output). Example: exam mark $0$–$75$, coursework $0$–$25$; total grade A/B/C/D and fault message for out-of-range. Test one case per partition or minimize so one test covers multiple partitions.

**Boundary value analysis:** For each boundary (e.g., 0, 30, 50, 70, 75, 100) test just below, on, and just above. Include implementation-dependent boundaries (e.g., INT_MIN, INT_MAX) when relevant.

### 5.2 White-Box: Statement and Branch Coverage

**Statement coverage:** Percentage of executable statements executed by the test suite. Weakness: 100% statement coverage can miss branches (e.g., only one branch of an `if` exercised).

**Branch (decision) coverage:** Each decision must evaluate to both TRUE and FALSE. Stronger than statement coverage; required in many standards.

### 5.3 Condition Coverage: BCC, BCCC, MCDC

- **Branch Condition Coverage (BCC):** Each Boolean operand is evaluated to both TRUE and FALSE (e.g., 2 tests). Does not guarantee both outcomes of the decision.
- **Branch Condition Combination Coverage (BCCC):** All $2^n$ combinations of $n$ operands. Thorough but expensive.
- **Modified Condition/Decision Coverage (MCDC):** Each condition is shown to **independently** affect the decision outcome. Typically $n+1$ to $2n$ tests; required in avionics (e.g., DO-178).

**Short-circuit evaluation:** In languages that short-circuit (`&&`, `||`), some combinations may be infeasible; BCCC may not be fully achievable; MCDC remains applicable.

### 5.4 Coverage Hierarchy

$$
\text{Statement} \subset \text{Branch} \subset \text{MCDC} \subset \text{BCCC}
$$

---

## 6. Test Planning and the Economics of Testing

### 6.1 Test Plan Structure

A test plan should include: testing process; requirements traceability; test items; schedule; recording procedures; hardware/software requirements; constraints (staff, time, budget).

### 6.2 Test Case Quality

**Good test case:** Specific, repeatable, verifiable. Include preconditions, inputs, expected results. Poor tests are vague ("Player 1 rolls dice"); good tests specify preconditions, exact inputs, and expected outcomes.

### 6.3 Economics and Risk

Testing incurs cost (planning, development, execution, fault removal). Not testing incurs risk (customer loss, downtime, emergency fixes, reputation). Investment should be proportional to **risk and criticality** (e.g., safety-critical systems warrant much higher investment).

### 6.4 Types of Testing (Summary)

| Type | Specification | Scope | Opacity | Tester |
|------|---------------|-------|---------|--------|
| Unit | Low-level design, code | Single unit | White-box | Programmer |
| Integration | High/low-level design | Multiple units | Both | Programmer |
| Functional/System | Requirements | Whole product | Black-box | Independent |
| Acceptance | Requirements | Customer env. | Black-box | Customer |
| Regression | Changed docs | Any level | Both | Both |

---

# Part III — LLM Tools, LangSmith, and LangGraph

## 7. LangSmith Setup and Tracing

### 7.1 Prerequisites

- Python 3.10+ (3.11 recommended)
- Terminal (macOS/Linux/Windows)
- Optional: Ollama installed with a model (e.g., llama3.2:1b, granite-code:20b)
- LangSmith account and API key for cloud tracing

### 7.2 Environment Setup

1. Create project folder and virtual environment.
2. Install: `langgraph`, `langchain`, `langsmith`, `langchain-ollama`, `python-dotenv`, `typing_extensions`.
3. (Optional) Install and run Ollama; pull a model and verify with `ollama run <model> "Say hello."`

### 7.3 Enabling LangSmith Tracing

Set environment variables (e.g., in a `.env` file, not committed):

```
LANGCHAIN_TRACING=true
LANGCHAIN_API_KEY=lsv2_xxxxxxxxxxxxxxxxxxxxxxxx
LANGCHAIN_PROJECT=LangSmith
```

In Python, load before using LangChain/LangGraph:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 7.4 Running and Viewing Traces

Run your script (e.g., `python LangGraph_Demo2.py`). Open [smith.langchain.com](https://smith.langchain.com) → Tracing → select project → open a run to see the trace tree, node-level steps, and LLM calls.

### 7.5 LangSmith Tutorial (Full Setup)

For the full tutorial (react-agent, eli5, Jupyter): install Python 3.12+, Ollama, Miniconda; create LangSmith account and API key; update `.env` in each subproject; create conda env, `pip install -r requirements.txt`; run `langgraph dev` in react-agent and `jupyter lab` in eli5. See module 04 handouts for step-by-step and references.

---

## 8. LangGraph: Graph-Based LLM Workflows

### 8.1 What Is LangGraph?

**LangGraph** is a graph-based framework for building LLM applications. The workflow is a directed graph of **nodes** (functions) and **edges** (transitions), with explicit support for branching and conditional routing. Compared to pure LangChain agents, LangGraph offers more **deterministic control** and production-ready flow.

**Core concepts:**

- **State:** Shared data structure (e.g., `TypedDict`) passed between nodes.
- **Nodes:** Functions that take state and return updates (e.g., `extract_content`, `llm_route`, `beautify`).
- **Edges:** Connections between nodes; can be fixed or conditional.
- **Conditional edges:** A routing function returns a key (e.g., `"question"` or `"compliment"`); the graph maps keys to next nodes.

### 8.2 Building a Simple Graph (Customer Feedback)

**Workflow:** START → Extract content → Route (question vs. compliment) → Run question code OR Run compliment code → Beautify → END.

1. Define **State** (e.g., `payload`, `text`, `route`, `answer`).
2. Add nodes: `extract_content`, `run_question_code`, `run_compliment_code`, `beautify` (and optionally `llm_route`).
3. Add edges: `START → extract_content`; conditional edge from `extract_content` to `run_question_code` or `run_compliment_code`; both action nodes → `beautify`; `beautify → END`.
4. Implement each node to read state and return a dict of updates.
5. Compile with `graph_builder.compile()` and run with `graph.invoke({"payload": [{"customer_remark": "..."}]})`.

Routing can be heuristic (e.g., `"?" in text`) or LLM-based (prompt the model to return `"question"` or `"compliment"` in JSON). Beautify can be a fixed template or an LLM call.

### 8.3 Best Practices

- Draw the graph on paper first (bottom-up development).
- Use `add_node`, `add_edge`, `add_conditional_edges` with clear names.
- Keep node functions pure: input state, output updates.
- Use LangSmith tracing to debug runs and inspect node I/O.

---

## 9. LangSmith Prompt Iteration and Evaluation

### 9.1 Goal

Use LangSmith to **iterate on prompts** and evaluate LLM outputs systematically: run prompts on a dataset, evaluate results (accuracy, relevance, coherence, completeness), identify failures, modify the prompt, and re-run until acceptable.

### 9.2 Workflow

1. Configure LangSmith (API key, project).
2. Load or create a dataset (inputs and optional reference outputs).
3. Define an initial prompt template.
4. Run the prompt on the dataset; record runs in LangSmith.
5. Evaluate outputs (manually or with evaluators).
6. Identify issues, update the prompt, and repeat.

### 9.3 Running the Prompt Iteration Notebook

Install `langchain`, `langsmith`, and optionally `openai`. Set `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`. Open `updated_small_prompt_iteration.ipynb`, run cells in order, and review traces and metrics in the LangSmith dashboard.

---

## 10. Open-Source Frameworks and Tools for LLM V&V

The course references a curated collection of open-source tools (see `05_opensource_tools/Collection_of_frameworks_tools_projects.md`). Selected categories:

**LLM / AI evaluation and testing:**
DeepEval, promptfoo, Ragas, LangSmith, trulens, Phoenix (observability, hallucination detection), Langfuse, Opik, LLM Canary (security benchmarking).

**Adversarial and robustness:**
Adversarial Robustness Toolbox (ART), TextAttack, Foolbox, OpenAttack.

**Systematic testing and error analysis:**
Azimuth (text classification error analysis), CheckList (behavioral NLP testing), PiML, OpenXAI.

**Traditional ML validation:**
Deepchecks, OpenML.

**Collections and red-teaming:**
NVIDIA GARAK (Generative AI Red-teaming & Assessment Kit), Vulnhuntr, CAISI cyber evals; best-of-ml-python, awesome-llm-apps, best-of-mcp-servers.

Use these tools to support experiments, evaluation metrics, and security reviews (e.g., GARAK for prompt injection and red-team exercises).

---

# Part IV — Assignments, Project, and Infrastructure

## 11. Assignments and Grading

### 11.1 Quiz 1: LangGraph Vague Specification Agent

**Total: 2 marks.** Build a LangGraph agent that (1) checks if a specification is vague, (2) fixes vague specs, (3) generates test case specifications. Deliverables: source code (1 mark) and execution screenshots for five given specifications (1 mark, 0.2 each). Grading emphasizes LangGraph structure, vagueness logic, test case generation, and code quality. See `assignments/RUBRIC.md` and `assignments/Quiz1.md` for full criteria and test specs.

### 11.2 Assignment 1: Functional + Structural Testing + LangSmith

**Due:** February 28. **Marks:** 9 (on-campus) / 10 (distance).

**Part A — Functional/structural testing (8 marks):**
Use repository: [AutomationPanda/shopping-cart-unit-tests](https://github.com/AutomationPanda/shopping-cart-unit-tests). Deliverables: installation and execution; run existing tests; baseline coverage (Coverage.py); design 20 functional tests (equivalence partitioning); implement them; report coverage after functional tests; add structural tests to reach 80% statement coverage; final coverage report.

**Part B — LangSmith (1–2 marks):**
Integrate LangSmith tracing with a LangGraph or LangChain application and submit evidence (e.g., screenshots, project name). See `assignments/Assignment1-CS5374-Spring2026.md` and `assignments/RUBRIC.md` for detailed breakdown and point allocation.

### 11.3 Grading Rubrics

Rubrics define criteria and weights for source code, execution evidence, test design, coverage, and documentation. Always refer to the latest `assignments/RUBRIC.md` for exact requirements.

---

## 12. Course Project: Trustworthy AI Legal Validator

### 12.1 Objective

Build a **Trustworthy AI validation pipeline** that verifies legal and governmental content (news, officials, elections, laws, court documents, templates) against **authoritative sources** so that only verified content is presented to users, with clear provenance.

### 12.2 Proposal and Plan

- **Proposal:** [submissions/PROJECT_PROPOSAL.md](../submissions/PROJECT_PROPOSAL.md) — Defines scope, hypothesis, experiments (baseline hallucination, pipeline effectiveness, validator vs. post-hoc, security red-team), deliverables, and references.
- **Plan (Texas data + tools):** [submissions/PROJECT_PLAN.md](../submissions/PROJECT_PLAN.md) — Same structure but uses **Texas Open Data** ([data.texas.gov](https://data.texas.gov), [data.capitol.texas.gov](https://data.capitol.texas.gov)) as authoritative sources and integrates open-source tools (DeepEval, Ragas, GARAK, promptfoo, Phoenix, etc.) into experiments and deliverables.

### 12.3 Milestones

1. **Phase 1:** Design document, threat model, validator modules (news, judges, officials), LangGraph prototype with pass/fail routing, unit and integration tests.
2. **Phase 2:** Full validator suite, integration with at least one authoritative source per content type, end-to-end RAG pipeline with validation gates.
3. **Phase 3:** Security review (red-team results), evaluation report, and experiment results.

---

## 13. Infrastructure: RedRaider Cluster and HPCC

### 13.1 Connecting to RedRaider

- **Browser:** [HPCC OnDemand Portal](https://ondemand.hpcc.ttu.edu/) → RedRaider Cluster Shell Access.
- **SSH:** `ssh YOUR_ERAIDER@login.hpcc.ttu.edu` (use your key and username).

### 13.2 Running OLLAMA on RedRaider

OLLAMA runs on the **Matador GPU partition**. One-time setup: create `~/ollama-latest`, download the Linux AMD64 tarball from [ollama.com](https://ollama.com), unpack. For each session: request an interactive GPU job (e.g., `interactive -c 20 -g 1 -p matador`), load modules (`gcc/13.2.0 cuda/12.9.0 python/3.12.5`), choose a dynamic port, set `OLLAMA_HOST` and `OLLAMA_BASE_URL`, start `~/ollama-latest/bin/ollama serve` in the background, then use `ollama run <model>`. Use batch jobs for long runs. See [TTU HPCC: Running Ollama on RedRaider](https://www.depts.ttu.edu/hpcc/userguides/application_guides/ollama.php).

### 13.3 Using Cluster OLLAMA from LangChain/LangGraph

- **Same node:** Set `OLLAMA_HOST` and `OLLAMA_BASE_URL` in the session; `ChatOllama` will use them.
- **From your laptop:** SSH port-forward to the worker node and port (e.g., `ssh -L 55131:NODE:OLPORT USER@login.hpcc.ttu.edu`); point the client to `http://127.0.0.1:55131`.

### 13.4 HPCC Files in This Repository

The **hpcc/** directory contains job scripts and agent notes pulled from `~/hpcc`: SLURM scripts for OLLAMA and LangSmith/LangGraph jobs, plus execution order and path notes. Upload scripts to your Lustre work directory and edit paths/usernames before submitting. See [hpcc/README.md](../hpcc/README.md) and [docs/RedRaider_LLM_Ollama.md](RedRaider_LLM_Ollama.md).

---

# Appendix: Source Module Reference

| Textbook Part / Chapter | Primary Source Modules |
|-------------------------|-------------------------|
| Ch 1–2 | README.md, 02_outline_syllabus, 01_video_channel |
| Ch 3–4 | 03_lecture_notes (Introduction to Testing, Functional Testing) |
| Ch 5–6 | 03 & 07 (BlackBox, 12_Defect_Testing_handout) |
| Ch 7–9 | 04_langsmith_tutorial, 09_langsmith_tracing, 10_langsmith_prompt_iteration |
| Ch 8 | 06_langgraph_hands_on_1, 08_langgraph_hands_on_2 |
| Ch 10 | 05_opensource_tools |
| Ch 11–12 | assignments (RUBRIC, Quiz1, Assignment1), submissions (PROJECT_PROPOSAL, PROJECT_PLAN) |
| Ch 13 | docs/RedRaider_LLM_Ollama.md, hpcc/README.md, hpcc/AGENTS.md |

---

*This textbook is derived from all markdown materials in the CS5374 Software V&V repository. For the latest assignment due dates, rubrics, and project milestones, always refer to the course Canvas site and the linked files above.*

**Texas Tech University • Department of Computer Science • Spring 2026**
