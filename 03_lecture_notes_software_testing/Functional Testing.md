# Functional Testing

> **CS 5374 – Software Verification and Validation**  
> Texas Tech University

---

## Overview

**Functional Testing** focuses on verifying that software meets its functional requirements (specifications). Also known as:

- Black-box testing
- Specification-based testing
- Behavioral testing

```mermaid
flowchart LR
    A[Specification] --> B[Test Design]
    B --> C[Test Cases]
    C --> D[Input Space]
    D --> E[System]
    E --> F[Outputs]
```

### Error Categories Targeted

| Category | Description |
|----------|-------------|
| 1 | Incorrect or missing functions |
| 2 | Interface errors |
| 3 | Data structure or external data access errors |
| 4 | Behavior or performance errors |
| 5 | Initialization and termination errors |

---

## Functional Testing Process

```mermaid
flowchart TB
    subgraph Input["Input Space"]
        I1[Valid Inputs]
        I2[Invalid Inputs]
    end
    
    subgraph System["System Under Test"]
        S[Processing]
    end
    
    subgraph Output["Output Space"]
        O1[Expected Outputs]
        O2[Anomalous Outputs]
    end
    
    I1 --> S
    I2 --> S
    S --> O1
    S --> O2
```

### Key Questions for Test Design

1. How is functional validity tested?
2. How is system behavior and performance tested?
3. What classes of input make good test cases?
4. How are data class boundaries isolated?

---

## Major Test Generation Methods

```mermaid
mindmap
  root((Functional Testing Methods))
    Equivalence Partitioning
      Input partitioning
      Output partitioning
    Boundary Value Analysis
      Edge cases
      Extreme values
    Error Guessing
      Experience-based
      GUI testing
    Pair-wise Combination
      IPO algorithm
      Coverage optimization
    Graph-based Testing
      Node coverage
      Link coverage
    Syntax Checking
      Token level
      Lexical level
```

---

## 1. Equivalence Partitioning (EP)

### Definition

**Equivalence Partitioning** divides input data into classes where each class should be treated identically by the software.

$$
\text{Input Domain} = \bigcup_{i=1}^{n} E_i \quad \text{where } E_i \cap E_j = \emptyset
$$

```mermaid
flowchart TB
    subgraph Partition["Input Domain"]
        V[Valid Inputs]
        I1[Invalid Class 1]
        I2[Invalid Class 2]
    end
    
    V --> S[System]
    I1 --> S
    I2 --> S
    S --> O[Outputs]
```

### Input Space Components

| Component | Examples |
|-----------|----------|
| **Sources of Inputs** | User input, GUI, disk files, network data |
| **Input Event Types** | Mouse movement, interrupts, pop-up menus |
| **Input Variables** | Phone numbers, names, license numbers |
| **Value Sets** | Valid ranges, invalid ranges |

### Value Set Examples

| Input | Valid Set | Invalid Sets |
|-------|-----------|--------------|
| Height | $\{x \mid x > 0\}$ | $\{x \mid x \leq 0\}$, non-numeric |
| City Name | alphabetic | alphanumeric, other |
| Unix filename | existing file | non-existent file |

> **Rule:** Number of invalid sets typically exceeds number of valid sets.

---

## EP Test Case Construction Rules

### Rule Summary

| Condition | Valid Classes | Invalid Classes |
|-----------|---------------|-----------------|
| **Range** $[a, b]$ | 1 | 2 |
| **Specific value** | 1 | 2 |
| **Set member** | 1 | 1 |
| **Boolean** | 1 | 1 |

### Detailed Guidelines

```mermaid
flowchart TB
    A["Input Condition"] --> B{Type?}
    B -->|Range| C["1 valid: [a,b]<br/>2 invalid: <a, >b"]
    B -->|Specific Value| D["1 valid: exact value<br/>2 invalid: wrong values"]
    B -->|Set Member| E["1 valid: in set<br/>1 invalid: not in set"]
    B -->|Boolean| F["1 valid: true<br/>1 invalid: false"]
```

### Example: Search Routine

**Specification:**

```
procedure Search (key: ELEM; T: SEQ of ELEM; 
                  Found: in out BOOLEAN; L: in out ELEM_INDEX);

Pre-condition: T^FIRST <= T^LAST
Post-condition: (Found and T(L) = Key) or (not Found and key not in T)
```

**Equivalence Partitions:**

| Array Size | Element Position | Test Case |
|------------|------------------|-----------|
| Single value | In sequence | `[17]`, key=17 |
| Single value | Not in sequence | `[17]`, key=0 |
| Multiple values | First element | `[17,29,21,23]`, key=17 |
| Multiple values | Last element | `[41,18,9,31,30,16,45]`, key=45 |
| Multiple values | Middle element | `[17,18,21,23,29,41,38]`, key=23 |
| Multiple values | Not in sequence | `[21,23,29,33,38]`, key=25 |

---

## 2. Boundary Value Analysis (BVA)

### Concept

BVA extends equivalence partitioning by focusing on data at the **edges** of each class.

```mermaid
flowchart LR
    subgraph InputSpace["Input Domain Space"]
        direction TB
        EC1[EC1] --> EC2[EC2]
        EC2 --> EC3[EC3]
        EC3 --> EC4[EC4]
        EC4 --> EC5[EC5]
        EC5 --> EC6[EC6]
        EC6 --> EC7[EC7]
    end
    
    B1[Boundary] --> B2[Boundary] --> B3[Boundary]
```

### Boundary Problem Types

| Problem | Description |
|---------|-------------|
| **Boundary Shift** | Where is the boundary between classes? |
| **Missing Boundary** | Does software implement the boundary? |
| **Extra Boundary** | Hidden boundaries not in spec? |
| **Closure Problem** | Which class contains boundary points? |

### BVA Guidelines

$$
\text{Boundary Tests} = \{a-1, a, a+1, b-1, b, b+1\}
$$

| Guideline | Test Values |
|-----------|-------------|
| Range $[a, b]$ | $a-1, a, a+1, b-1, b, b+1$ |
| Count $n$ | $n-1, n, n+1$ |
| Output range | Apply same to outputs |
| Data structures | Test array bounds |

### Example: Input Validation

**Specification:** Program accepts 4-10 inputs, each a 5-digit integer > 10000.

```mermaid
flowchart TB
    subgraph Count["Number of Inputs"]
        C1["< 4 (Invalid)"] --- C2["4 (Min)"]
        C2 --- C3["7 (Mid)"]
        C3 --- C4["10 (Max)"]
        C4 --- C5["> 10 (Invalid)"]
    end
```

| Test Dimension | Invalid Low | Valid Min | Valid Mid | Valid Max | Invalid High |
|----------------|-------------|-----------|-----------|-----------|--------------|
| **Count** | 3 | 4 | 7 | 10 | 11 |
| **Value** | 9999 | 10000 | 50000 | 99999 | 100000 |

---

## 3. Error Guessing (EG)

### Concept

Error guessing relies on **experience and intuition** to anticipate where errors might occur.

```mermaid
flowchart TB
    A[Experience] --> B[Error Guessing]
    C[Intuition] --> B
    D[Domain Knowledge] --> B
    B --> E[Test Cases]
```

### Common Error Patterns

| Category | Examples |
|----------|----------|
| **Data Structures** | Empty list, single element, full capacity |
| **Numeric Values** | Zero, negative, very large, very small |
| **Strings** | Empty, special characters, Unicode |
| **GUI** | Invalid input type in field, rapid clicks |

### Linked List Example

- Add node to empty list
- Delete first node, then add first
- Delete last node, then add last
- Delete all nodes, then rebuild

---

## 4. Pair-wise Combination Testing

### Problem

Exhaustive testing of parameter combinations is often infeasible:

$$
\text{Exhaustive} = \prod_{i=1}^{n} |V_i|
$$

For 3 parameters with 3 values each: $3 \times 3 \times 3 = 27$ test cases.

### Solution: In-Parameter Order (IPO)

Generate test cases that cover all **pairs** of parameter values.

```mermaid
flowchart LR
    subgraph Parameters["Parameters"]
        A["A: A1, A2, A3"]
        B["B: B1, B2, B3"]
        C["C: C1, C2, C3"]
    end
    
    subgraph Result["Pair-wise Coverage: 9 tests"]
        T["Each pair (Ai, Bj), (Ai, Ck), (Bj, Ck) covered"]
    end
    
    Parameters --> Result
```

### IPO Algorithm Result

| Test | A | B | C |
|------|---|---|---|
| 1 | A1 | B1 | C1 |
| 2 | A1 | B2 | C2 |
| 3 | A1 | B3 | C3 |
| 4 | A2 | B1 | C2 |
| 5 | A2 | B2 | C3 |
| 6 | A2 | B3 | C1 |
| 7 | A3 | B1 | C3 |
| 8 | A3 | B2 | C1 |
| 9 | A3 | B3 | C2 |

**Coverage Guarantee:** All $(A_i, B_j)$, $(A_i, C_k)$, $(B_j, C_k)$ pairs covered.

---

## 5. Graph-Based Testing

### Concept

Model relationships between data objects and program objects as a graph.

```mermaid
flowchart LR
    A[Object A] -->|"Directed Link<br/>(weight)"| B[Object B]
    A ---|"Undirected Link"| C[Object C]
    C ==>|"Parallel Links"| B
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#f3e5f5
```

### Graph Components

| Component | Description |
|-----------|-------------|
| **Nodes** | Objects (data, screens, modules) |
| **Links** | Relationships between objects |
| **Node Weight** | Properties of a node |
| **Link Weight** | Characteristics of a link |

### Coverage Criteria

```mermaid
flowchart TB
    A[Graph Coverage] --> B[Node Coverage]
    A --> C[Link Coverage]
    
    B --> B1["Every node exercised"]
    C --> C1["Every link exercised"]
```

### Example: File Editor

```mermaid
flowchart LR
    A["Edit Menu"] -->|"Menu select open<br/>(time < 2 sec)"| B["Document Window"]
    B --> C["Document Text"]
    C --> D["Attributes:<br/>type, etc."]
```

**Test Cases Derived:**
1. Select Edit → Open
2. Verify window opens < 2 seconds
3. Check document attributes

### Relationship Properties

| Property | Test Requirement |
|----------|------------------|
| **Transitivity** | $x R y, y R z \implies x R z$ |
| **Symmetry** | $x R y \implies y R x$ (bidirectional) |
| **Reflexivity** | $x R x$ (null/no action) |

---

## 6. Syntax Checking

### Concept

Test syntax validation at two levels:

| Level | Focus |
|-------|-------|
| **Token** | Keywords, numbers, operators |
| **Lexical** | Individual characters |

### Process

```mermaid
flowchart LR
    A[Identify Syntax] --> B[Draw State Machine]
    B --> C[Generate Valid Tests]
    B --> D[Generate Invalid Tests]
```

### Example: Unix `wc` Command

**Syntax:** `wc [-c | -m | -C] [-l] [-w] filename ...`

```mermaid
stateDiagram-v2
    [*] --> s0
    s0 --> s1: wc
    s1 --> s2: -c/-m/-C
    s1 --> s3: -l
    s1 --> s4: -w
    s2 --> s3: -l
    s2 --> s4: -w
    s3 --> s4: -w
    s4 --> s5: filename
    s5 --> s5: filename
    s5 --> [*]
```

### Valid Syntax Testing

**All Transitions:**
- `wc foo`
- `wc foo1 foo2`
- `wc foo1 foo2 foo3`

**All Transition Pairs:**
- `wc -c foo`
- `wc -C -l foo`
- `wc -m -w foo`
- `wc -w foo`

### Invalid Syntax Testing

**Reaching Strings:** Strings that reach each state.

| State | Reaching String |
|-------|-----------------|
| s1 | `wc` |
| s2 | `wc -m` |
| s3 | `wc -l` |
| s4 | `wc -w` |

**Invalid Test Cases:**
- `wc -x -l -w foo` (invalid option -x)
- `wc -c -P foo` (invalid option -P)
- `wc -m -l -X foo` (invalid option -X)

### Lexical Level Testing

**Valid:** `wc`  
**Invalid:** `w`, `wcc`, `wcp`, `wc` (with special chars)

---

## Summary Comparison

| Method | Focus | Best For |
|--------|-------|----------|
| **EP** | Input classes | Reducing test count |
| **BVA** | Edge values | Finding boundary errors |
| **EG** | Experience-based | Exploratory testing |
| **Pair-wise** | Combinations | Multi-parameter systems |
| **Graph-based** | Relationships | Complex data flows |
| **Syntax** | Input validation | Command parsers |

---

## Key Takeaways

1. **Functional testing** is specification-based, not code-based
2. **Equivalence partitioning** reduces test cases while maintaining coverage
3. **Boundary values** are where errors cluster
4. **Error guessing** complements systematic methods
5. **Pair-wise testing** efficiently handles parameter combinations
6. **Graph-based testing** models complex relationships
7. **Syntax checking** validates input/output formats

---

*CS 5374 – Software Verification and Validation | Texas Tech University*
