# Grading Rubrics - CS 5374 Software Verification and Validation

> **Texas Tech University**
> Department of Computer Science
> Spring 2026

---

## Quiz 1: LangGraph Vague Specification Detection Agent

**Total Marks: 2**

### Overview

| Component | Max Marks |
|-----------|------------|
| Source Code | 1.0 |
| Execution Screenshots | 1.0 |
| **Total** | **2.0** |

---

### 1. Source Code (1.0 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **LangGraph Structure** | 0.3 | Proper StateGraph with nodes (check, fix, testcase) |
| **Vagueness Detection** | 0.3 | Logic correctly identifies vague vs. non-vague specs |
| **Test Case Generation** | 0.3 | Generates valid test case specifications |
| **Code Quality** | 0.1 | Clean, readable code with proper imports |

#### Grading Scale

| Grade | Description |
|-------|-------------|
| 1.0 | Complete, fully functional code |
| 0.7-0.9 | Minor issues, mostly functional |
| 0.4-0.6 | Partial implementation, some features missing |
| 0.1-0.3 | Significant missing functionality |
| 0.0 | No submission or completely non-functional |

---

### 2. Execution Screenshots (1.0 mark)

One screenshot per test case (0.2 marks each, 5 total):

| Test Case | Specification | Marks |
|-----------|---------------|-------|
| 1 | "The system shall allow for fast, easy data entry" | 0.2 |
| 2 | "Install high-quality flooring" | 0.2 |
| 3 | "The application must be secure" | 0.2 |
| 4 | "The report will include, as appropriate, investigation findings" | 0.2 |
| 5 | "The project will be completed in a timely manner" | 0.2 |

#### Screenshot Requirements

- Must show the agent's output for each specification
- Output format must include:
  - Vagueness determination (VAGUE / NOT_VAGUE)
  - Test case specification
  - For vague specs: clarified specification

---

## Assignment 1: Functional + Structural Testing + LangSmith

**Total Marks: 9 (On-Campus) / 10 (Distance)**

---

### Part A: Functional/Structural Testing (8 marks)

| # | Deliverable | Max Marks |
|---|-------------|------------|
| 1 | Installation & Execution | 1.0 |
| 2 | Execute Existing Tests | 1.0 |
| 3 | Baseline Coverage Measurement | 1.0 |
| 4 | Design 20 Functional Tests (EP) | 2.0 |
| 5 | Implement 20 Functional Tests | 1.0 |
| 6 | Coverage After Functional Tests | 0.5 |
| 7 | Structural Tests for 80% Coverage | 1.0 |
| 8 | Final Coverage Measurement | 0.5 |
| **Part A Total** | | **8.0** |

---

#### 1. Installation & Execution (1.0 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Repository Cloned | 0.3 | Git clone successful |
| Dependencies Installed | 0.3 | All pip packages installed |
| Code Executes | 0.4 | Main code runs without errors |

#### 2. Execute Existing Tests (1.0 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Tests Run | 0.5 | pytest/unittest executed |
| Results Documented | 0.5 | Output captured and shown |

#### 3. Baseline Coverage Measurement (1.0 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Coverage Run | 0.3 | coverage run -m pytest |
| Report Generated | 0.3 | coverage report produced |
| Baseline % Documented | 0.4 | Statement coverage percentage recorded |

#### 4. Design 20 Functional Tests - Equivalence Partitioning (2.0 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| EP Classes Identified | 0.5 | All equivalence classes identified |
| Test Case Table Complete | 0.5 | All 20 test cases in required format |
| Valid/Invalid Coverage | 0.5 | Both valid and invalid partitions covered |
| Expected Outputs | 0.5 | Correct expected outputs for each test |

**Required Table Format:**

| Source Code | TC# | EP Class | Valid/Invalid | Test Inputs | Expected Output | Status |
|-------------|-----|----------|---------------|-------------|-----------------|--------|

#### 5. Implement 20 Functional Tests (1.0 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Test Count | 0.3 | Exactly 20 tests implemented |
| Framework Used | 0.2 | unittest framework |
| Test Logic | 0.3 | Tests correctly validate expected behavior |
| Runnability | 0.2 | Tests execute without errors |

#### 6. Coverage After Functional Tests (0.5 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Coverage Measured | 0.3 | Coverage run after functional tests |
| Report Provided | 0.2 | Coverage report included |

#### 7. Structural Tests for 80% Coverage (1.0 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Gap Analysis | 0.3 | Uncovered statements identified |
| Test Design | 0.4 | Structural tests designed to cover gaps |
| Strategy Documented | 0.3 | Approach explained |

#### 8. Final Coverage Measurement (0.5 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Coverage ≥ 80% | 0.5 | Statement coverage at least 80% |

---

### Part B: LangSmith Tracing (2 marks)

| # | Deliverable | Max Marks |
|---|-------------|------------|
| 1 | Source Code with Tracing | 0.5 |
| 2 | Execution Screenshot | 0.5 |
| 3 | LangSmith Trace Report | 1.0 |
| **Part B Total** | | **2.0** |

---

#### 1. Source Code with Tracing (0.5 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| LangChain Implementation | 0.2 | Quiz 1 in LangChain |
| LangSmith Enabled | 0.2 | LANGCHAIN_TRACING_V2=true |
| API Key Configured | 0.1 | Proper environment setup |

#### 2. Execution Screenshot (0.5 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Quiz Output Visible | 0.5 | Screenshot shows agent execution |

#### 3. LangSmith Trace Report (1.0 mark)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Trace Screenshot(s) | 0.5 | LangSmith UI showing traces |
| Chain Count | 0.5 | Number of chains/LLM calls documented |

---

## Assignment Summary

| Component | On-Campus | Distance |
|-----------|-----------|----------|
| Part A: Functional/Structural Testing | 8.0 | 8.0 |
| Part B: LangSmith Tracing | 1.0 | 2.0 |
| **Total** | **9.0** | **10.0** |

---

## General Grading Guidelines

### Code Quality Expectations

- Code must be runnable without modification
- Clear variable and function names
- Proper error handling
- Comments where necessary

### Documentation Requirements

- All screenshots must be clear and readable
- File names must be descriptive
- Include any required tables in specified format

### Late Submission Policy

- Refer to course syllabus for late penalties
- Canvas submission only - email submissions not accepted

---

## Common Deductions

| Issue | Deduction |
|-------|-----------|
| Missing screenshots | 0.2 per missing |
| Incorrect output format | 0.1 per instance |
| Coverage < 80% (Part A #8) | Full deduction |
| Code doesn't run | Up to 0.5 |
| Missing required table format | 0.2 |

---

*Texas Tech University • Department of Computer Science • Spring 2026*
