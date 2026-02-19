# CS 5374 – Software Verification and Validation

> **Texas Tech University**  
> Department of Computer Science  
> Spring 2026

---

## Course Overview

This course covers software verification and validation (V&V) techniques, including black-box and white-box testing, with a focus on modern AI/LLM evaluation using LangSmith and LangGraph.

### Learning Objectives

| Objective | Description |
|-----------|-------------|
| **Validation** | Testing techniques to ensure software meets requirements |
| **Verification** | Formal methods to prove correctness |
| **AI/LLM Evaluation** | Modern approaches to testing AI-powered applications |

---

## Module Index

| Module | Title | Description |
|--------|-------|-------------|
| 01 | Video Channel | MyMediasite setup guide |
| 02 | Outline & Syllabus | Course policies and schedule |
| 03 | Lecture Notes | Core testing concepts (Black-Box, White-Box) |
| 04 | LangSmith Tutorial | LLM evaluation framework |
| 05 | Open Source Tools | Testing frameworks and projects |
| 06 | LangGraph Hands-on #1 | First LangGraph exercises |
| 07 | Tutorials & Exercises | Practice materials |
| 08 | LangGraph Hands-on #2 | Advanced LangGraph with LangSmith |
| 09 | LangSmith Tracing | Tracing and debugging LLM apps |
| 10 | LangSmith Prompt Iteration | Prompt optimization |

---

## Key Topics

- **Testing Foundations:** Black-Box Testing, White-Box Testing, Test Case Generation, Coverage Criteria
- **Testing Techniques:** Equivalence Partitioning, Boundary Value Analysis, Statement/Branch Coverage, MCDC
- **Modern Tools:** LangSmith, LangGraph, AI/LLM Debugging
- **Project Work:** Team Projects, Individual Assignments, Hands-on Exercises

---

## Assignments

| Assignment | Description | Due Date |
|------------|-------------|----------|
| Assignment 1 | Functional + Structural Testing | Feb 28 |
| Quiz 1 | LangGraph Vague Spec Agent | Completed |
| Project | Trustworthy AI Legal Validator | See milestones |

---

## Grading Distribution

| Component | Weight |
|-----------|--------|
| Project | 18% |
| Assignments | 27% |
| Quizzes | 10% |
| Midterm | 15% |
| Final | 30% |

---

## Contact Information

| Role | Name | Email |
|------|------|-------|
| Instructor | Dr. Akbar S. Namin | akbar.namin@ttu.edu |
| TA 1 | Sonali Singh | sonalsin@ttu.edu |
| TA 2 | Hasan Al-Qudah | halqudah@ttu.edu |

---

## Resources

### Textbook
- **Introduction to Software Testing** — Paul Ammann & Jeff Offutt  
  [https://cs.gmu.edu/~offutt/softwaretest/](https://cs.gmu.edu/~offutt/softwaretest/)

### AI/LLM Resources
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Cookbook](https://github.com/langchain-ai/langsmith-cookbook)

### RedRaider cluster (Texas Tech HPCC)
- **[Connecting to LLMs and running OLLAMA on RedRaider](docs/RedRaider_LLM_Ollama.md)** — Connect to the cluster, run OLLAMA in batch or interactive sessions, and point LangChain/LangGraph at cluster LLMs (including port forwarding from your laptop).
- **hpcc/** — Job scripts and agent notes pulled from `~/hpcc` for running LangSmith/LangGraph and OLLAMA on the cluster. See [hpcc/README.md](hpcc/README.md).

---

## Project: Trustworthy AI Legal and Governmental Content Validator

This course includes a major project on building a validation pipeline that verifies legal and governmental content against authoritative sources to reduce LLM hallucination rates.

### Project Milestones

1. **Phase 1:** Design document, basic validators, LangGraph prototype
2. **Phase 2:** Full validator suite, RAG integration
3. **Phase 3:** Security review, experiment results

### Project plan (Texas data + open-source tools)

**[PROJECT_PLAN.md](submissions/PROJECT_PLAN.md)** — Integrated project plan that meets the [PROJECT_PROPOSAL](submissions/PROJECT_PROPOSAL.md) guidelines, uses **Texas Open Data** ([data.texas.gov](https://data.texas.gov), [data.capitol.texas.gov](https://data.capitol.texas.gov)) as authoritative legal/governmental sources instead of federal, and integrates the **open-source frameworks and tools** from [05_opensource_tools/Collection_of_frameworks_tools_projects.md](05_opensource_tools/Collection_of_frameworks_tools_projects.md) (DeepEval, Ragas, LangSmith, GARAK, promptfoo, Phoenix, TextAttack, etc.) into experiments, deliverables, and security review.

---

*Texas Tech University • Department of Computer Science • Spring 2026*
