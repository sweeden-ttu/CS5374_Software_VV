# An Introduction to Software Testing

> **CS 5374 – Software Verification and Validation**
> Texas Tech University

---

## What is Software Testing?

Software testing is the process of executing a program with the intent of finding errors. Once source code is available, software must be tested to uncover and fix possible errors before delivery to the customer.

```mermaid
flowchart LR
    subgraph Goal["Testing Goal"]
        A[Source Code] --> B[Test Execution]
        B --> C{Errors Found?}
        C -->|Yes| D[Debug & Fix]
        C -->|No| E[Confidence]
        D --> B
    end
```

### Key Objectives

$$
\text{Testing Goal} = \max_{\text{test cases}} P(\text{finding errors})
$$

| Question | Answer |
|----------|--------|
| **What is it?** | Systematic execution to uncover errors before delivery |
| **Who does it?** | Software engineers and testing specialists |
| **Why is it important?** | Reviews and SQA are necessary but not sufficient |
| **What are the steps?** | Exercise requirements (functional) and internal logic (structural) |
| **What is the work product?** | Test cases with expected and actual results |

---

## Two Types of Program Analysis

```mermaid
flowchart TB
    subgraph Analysis["Program Analysis"]
        A[Program] --> B{Run Code?}
        B -->|No| C[Static Analysis]
        B -->|Yes| D[Dynamic Analysis]

        C --> C1[Formal Methods]
        C --> C2[Code Inspection]
        C --> C3[Theorem Proving]

        D --> D1[Software Testing]
        D --> D2[Debugging]
        D --> D3[Profiling]
    end
```

| Type | Description | When Applied |
|------|-------------|--------------|
| **Static Analysis** | Inspecting code without executing it | Before runtime |
| **Dynamic Analysis** | Inspecting code by executing it | During runtime |

---

## The Testing Process

```mermaid
flowchart LR
    A["1. Prepare Test Plan"] --> B["2. Develop Test Cases"]
    B --> C["3. Run Executable Code"]
    C --> D["4. Record Behavior"]
    D --> E["5. Add More Cases?"]
    E -->|Yes| B
    E -->|No| F["6. Analyze Results"]
    F --> G{Acceptable?}
    G -->|No| H[Debug]
    H --> C
    G -->|Yes| I[Release]
```

### The Major Question: When to Stop?

$$
\text{Stopping Criteria} = f(\text{Test Plan}, \text{Resources}, \text{Coverage}, \text{Risk})
$$

This is fundamentally an **optimization problem** and an active research direction.

---

## Testing Terminology

### Core Definitions

```mermaid
flowchart TB
    A[Programmer makes] --> B[Error]
    B -->|causes| C[Fault]
    C -->|triggers| D[Failure]
    D -->|observed as| E[Defect/Bug]

    style B fill:#ffeb3b
    style C fill:#ff9800
    style D fill:#f44336,color:#fff
```

| Term | Definition | Example |
|------|------------|---------|
| **Error** | Mistake programmer made | Thinking `<` was correct when `<=` needed |
| **Fault** | Problem in code causing failure | Using `<` instead of `<=` |
| **Failure** | Incorrect program behavior | Producing wrong output |
| **Bug** | Informal term for fault/failure | "There's a bug in the code" |
| **Defect** | General term for any problem | Issues in specs, design, or code |

### Mathematical Relationship

$$
\text{Error} \xrightarrow{\text{introduces}} \text{Fault} \xrightarrow{\text{execution}} \text{Failure}
$$

---

## Test Case Components

A **test case** is the fundamental unit of testing:

$$
\text{Test Case} = \{\text{Test Input}, \text{Expected Output}, \text{Condition}\}
$$

```mermaid
flowchart TB
    subgraph TestCase["Test Case Structure"]
        A[Test Input] --> B[Condition]
        B --> C[Execution]
        C --> D[Actual Output]
        D --> E{Compare}
        E --> F[Expected Output]
    end
```

| Component | Description | Example |
|-----------|-------------|---------|
| **Test Input** | Data to run a test | `-l` in `ls -l` |
| **Expected Output** | What should happen | Long format listing |
| **Condition** | Precondition for test | Valid directory path |

### Test Outcomes

| Outcome | Definition |
|---------|------------|
| **Passing Test Case** | Software behaves as expected |
| **Failing Test Case** | Software behaves incorrectly |

---

## Test Organization

```mermaid
flowchart TB
    subgraph Pool["Test Pool']
        A["Test Suite A"]
        B["Test Suite B"]
    end

    A --> A1["Test Case 1"]
    A --> A2["Test Case 2"]
    A --> A3["Test Case 3"]

    B --> B1["Test Case n-1"]
    B --> B2["Test Case n"]
```

| Term | Definition |
|------|------------|
| **Test Suite** | A set of related test cases |
| **Test Pool** | All test cases developed |

---

## Test Equivalence

Two test cases are **test equivalent** if the software fails (or passes) on both.

### Equivalence Relation Properties

$$
\forall t_1, t_2, t_3 : t_1 \equiv t_2 \equiv t_3 \implies \text{same outcome}
$$

| Property | Mathematical Form | Meaning |
|----------|-------------------|---------|
| **Reflexivity** | $t R t$ | A test case is equivalent to itself |
| **Symmetry** | $t_1 R t_2 \implies t_2 R t_1$ | If $t_1$ fails, $t_2$ fails and vice versa |
| **Transitivity** | $t_1 R t_2 \land t_2 R t_3 \implies t_1 R t_3$ | Chain of equivalence |

---

## Test Infrastructure

### Test Oracle

A **test oracle** is a source of expected results for a test case.

### Test Driver

A "main program" that:
1. Accepts test case data
2. Passes data to the component under test
3. Prints relevant results

### Test Stub

A dummy subprogram that:
1. Replaces subordinate modules
2. Performs minimal data manipulation
3. Prints verification of entry
4. Returns control to the module under test

```mermaid
flowchart TB
    subgraph Testing["Testing Environment"]
        D[Driver] --> M[Module Under Test]
        M --> S1[Stub 1]
        M --> S2[Stub 2]
        D -->|Test Cases| M
        M -->|Results| D
    end

    style D fill:#e1f5fe
    style M fill:#fff3e0
    style S1 fill:#f3e5f5
    style S2 fill:#f3e5f5
```

### Test Harness

A collection of software and test data configured to test a program unit under varying conditions while monitoring behavior.

---

## Testing Approaches

```mermaid
flowchart TB
    subgraph Approaches["Testing Approaches"]
        B[Black Box<br/>Functional] --> G[Gray Box]
        W[White Box<br/>Structural] --> G
    end

    B --> B1[Specs-based]
    B --> B2[No source code needed]

    W --> W1[Code-based]
    W --> W2[Source code required]

    G --> G1[Combined approach]
```

| Approach | Basis | Source Code |
|----------|-------|-------------|
| **Black Box (Functional)** | Specs, design docs, user manual | Not required |
| **White Box (Structural)** | Internal code structure | Required |
| **Gray Box** | Combination of both | Partial |

---

## Testing Levels

```mermaid
flowchart LR
    A[Unit Testing] --> B[Integration Testing]
    B --> C[System Testing]
    C --> D[Acceptance Testing]
    D --> E[Release]

    E --> F[Regression Testing]
    F --> E
```

| Level | Scope | Purpose |
|-------|-------|---------|
| **Unit Testing** | Modules, routines, classes | Test individual components |
| **Integration Testing** | Multiple units | Test interactions |
| **System Testing** | Whole program | Test as complete system |
| **Acceptance Testing** | Complete system | Client approval |
| **Regression Testing** | Multiple releases | Ensure fixes don't break existing functionality |

### Alpha vs. Beta Testing

| Type | Location | Users |
|------|----------|-------|
| **Alpha Testing** | Developer's site | Real users |
| **Beta Testing** | User's site | Real users |

---

## Adequacy Criterion

A **test adequacy criterion** is a predicate that evaluates whether testing is sufficient:

$$
C: (\text{Program} \times \text{Test Suite}) \rightarrow \{\text{True}, \text{False}\}
$$

$$
C(P, T) = \begin{cases}
\text{True} & \text{if } T \text{ adequately tests } P \\
\text{False} & \text{otherwise}
\end{cases}
$$

---

## Verification vs. Validation

```mermaid
flowchart TB
    subgraph V["V&V Process"]
        V1[Verification<br/>Quality Assurance]
        V2[Validation<br/>Quality Control]
    end

    V1 -->|"Are we building it right?"| V1A[Internal Process]
    V1 -->|"Compliance with specs"| V1B[End of each phase]

    V2 -->|"Are we building the right thing?"| V2A[Customer Needs]
    V2 -->|"Acceptance & suitability"| V2B[Before Delivery]
```

| Aspect | Verification (QA) | Validation (QC) |
|--------|-------------------|-----------------|
| **Question** | "Are we building it right?" | "Are we building the right thing?" |
| **Focus** | Process compliance | User requirements |
| **When** | End of each phase | Before delivery |
| **Audience** | Internal | External (customers) |

---

## V&V Planning Timeline

```mermaid
flowchart TB
    subgraph Development["Development Phases"]
        R[Requirements<br/>Specification]
        S[System<br/>Specification]
        D[System Design]
        DD[Detailed Design]
        C[Code]
    end

    subgraph Testing["Test Plans"]
        R --> AP[Acceptance<br/>Test Plan]
        S --> SP[System Integration<br/>Test Plan]
        D --> SS[Subsystem<br/>Integration Test Plan]
        DD --> MP[Module & Unit<br/>Test Plan]
    end
```

---

## Software Test Plan Structure

A comprehensive test plan should include:

| Section | Content |
|---------|---------|
| **Testing Process** | Description of major testing phases |
| **Requirements Traceability** | Mapping of requirements to test cases |
| **Tested Items** | Products to be tested |
| **Testing Schedule** | Timeline and resource allocation |
| **Test Recording Procedures** | How results are documented |
| **Hardware/Software Requirements** | Tools and resources needed |
| **Constraints** | Staff, time, budget limitations |

---

## Simple Testing Process Flow

```mermaid
flowchart LR
    A["Design<br/>Test Cases"] --> B["Prepare<br/>Test Data"]
    B --> C["Run Program<br/>with Test Data"]
    C --> D["Compare Results<br/>to Test Cases"]
    D --> E["Test Reports"]
```

| Phase | Output |
|-------|--------|
| Design test cases | Test case specifications |
| Prepare test data | Test data sets |
| Run program | Test results |
| Compare results | Pass/Fail status |
| Document | Test reports |

---

## Summary: Test Case Generation Approaches

```mermaid
mindmap
  root((Test Generation))
    Functional Testing
      Specification-based
      Black-box techniques
      Requirements-driven
    Structural Testing
      Code-based
      White-box techniques
      Coverage-driven
```

| Approach | Source | Techniques |
|----------|--------|------------|
| **Functional** | Program specification | Equivalence partitioning, Boundary analysis |
| **Structural** | Internal program logic | Statement, branch, path coverage |

---

## Key Takeaways

1. **Testing is essential** — Reviews alone are not sufficient
2. **Systematic approach** — Use disciplined techniques for thorough testing
3. **Multiple levels** — Unit → Integration → System → Acceptance
4. **Dual perspectives** — Functional (black-box) and Structural (white-box)
5. **Adequacy matters** — Define criteria to know when testing is complete

---

*CS 5374 – Software Verification and Validation | Texas Tech University*
