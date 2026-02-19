# Texas Legal Dataset Validator Specifications

## Overview

This document outlines the validator specifications for the Texas Legal Datasets (texas_legal_datasets_langgraph.json). The validators are designed to improve data quality, enable model evaluation, and ensure reproducibility.

## Data Schema

Based on the current `texas_legal_datasets_langgraph.json`:

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "category": "string",
  "tags": ["string"],
  "viewCount": "integer",
  "downloadCount": "integer",
  "createdAt": "timestamp",
  "updatedAt": "timestamp",
  "displayType": "string",
  "url": "string"
}
```

## RUBRIC Goals

The validators must address these RUBRIC requirements:

1. **Citation Accuracy >= 98%** - Ensure URLs are valid and point to authoritative Texas sources
2. **Temporal Validity >95%** - Verify timestamps are valid and within reasonable ranges
3. **Outcome Label Correctness >= 99%** - Ensure category classifications are accurate
4. **Coverage >= 90%** - Ensure coverage across top statutes and issue types

## Validator Specifications

### Priority 1: Core Validators (Must Implement)

#### 1.1 Schema Validator
- **Type**: Deterministic
- **Description**: Validates field presence, types, and basic normalization
- **Input Fields**: All fields from dataset record
- **Pass Criteria**: All required fields present with correct types
- **Severity**: ERROR
- **Test Cases**:
  - Valid dataset with all fields → PASS
  - Missing required field (id, name, url) → FAIL
  - Invalid type (viewCount as string) → FAIL

#### 1.2 URL Authority Checker
- **Type**: Deterministic + Lookup
- **Description**: Verify URLs map to authoritative Texas legal domains
- **Input Fields**: url
- **Pass Criteria**: URL domain matches allowlist (config/allowlist.json)
- **Severity**: ERROR
- **Test Cases**:
  - URL: "https://data.texas.gov/dataset/xyz" → PASS
  - URL: "https://bellcountytx.gov" → PASS
  - URL: "https://unknown-site.com" → FAIL

#### 1.3 Temporal Validity Checker
- **Type**: Deterministic
- **Description**: Verify timestamps are valid Unix timestamps and within reasonable range
- **Input Fields**: createdAt, updatedAt
- **Pass Criteria**: 
  - Both timestamps exist
  - updatedAt >= createdAt
  - Both within 2000-2030 range
- **Severity**: WARNING
- **Test Cases**:
  - createdAt: 1768997508, updatedAt: 1768997717 → PASS
  - updatedAt < createdAt → FAIL
  - Invalid timestamp format → FAIL

#### 1.4 Category Consistency Checker
- **Type**: Deterministic + ML (optional)
- **Description**: Ensure category matches content based on keywords
- **Input Fields**: category, name, description, tags
- **Pass Criteria**: Category aligns with content keywords
- **Severity**: WARNING
- **Test Cases**:
  - Category: "LAW_VERIFICATION", tags: ["tdcj", "prison"] → PASS
  - Category: "NEWS", name: "School Nutrition" → FAIL

### Priority 2: Quality Validators

#### 2.1 Description Quality Checker
- **Type**: Deterministic
- **Description**: Validate description length and quality
- **Input Fields**: description
- **Pass Criteria**: 
  - Description length >= 50 characters
  - Not just URL or boilerplate text
- **Severity**: INFO
- **Test Cases**:
  - Description: "This dataset contains..." (50+ chars) → PASS
  - Description: "" or < 50 chars → WARNING

#### 2.2 Tag Quality Checker
- **Type**: Deterministic
- **Description**: Validate tags are present and meaningful
- **Input Fields**: tags
- **Pass Criteria**: At least 2 tags present
- **Severity**: INFO
- **Test Cases**:
  - tags: ["tdcj", "inmates", "prison"] → PASS
  - tags: [] → WARNING

#### 2.3 Engagement Validation
- **Type**: Deterministic
- **Description**: Validate view/download counts are non-negative
- **Input Fields**: viewCount, downloadCount
- **Pass Criteria**: Both >= 0
- **Severity**: ERROR
- **Test Cases**:
  - viewCount: 152, downloadCount: 132 → PASS
  - viewCount: -5 → FAIL

### Priority 3: Advanced Validators (ML-based)

#### 3.1 Content Relevance Checker
- **Type**: LLM/NLI
- **Description**: Use NLI to check if name/description relates to category
- **Input Fields**: name, description, category
- **Pass Criteria**: LLM confirms relevance > 0.9 threshold
- **Severity**: INFO
- **Test Cases**:
  - Category "CRIMINAL_JUSTICE", description about inmates → PASS
  - Category mismatch detected → FAIL

#### 3.2 Duplicate Detection
- **Type**: Deterministic + Semantic (optional)
- **Description**: Detect duplicate datasets by URL or name similarity
- **Input Fields**: url, name
- **Pass Criteria**: No exact URL duplicates, name similarity < 0.8
- **Severity**: ERROR
- **Test Cases**:
  - Same URL appears twice → FAIL
  - Nearly identical names → WARNING

#### 3.3 Robustness Test (Paraphrase Invariance)
- **Type**: LLM
- **Description**: Test if category remains consistent under paraphrasing
- **Input Fields**: name, description, category
- **Pass Criteria**: Category unchanged after paraphrase
- **Severity**: INFO

## Implementation Mapping

| Validator | Node Type | Complexity | RUBRIC Goal |
|-----------|-----------|------------|--------------|
| Schema Validator | Deterministic | Low | All |
| URL Authority Checker | Deterministic | Low | Citation Accuracy |
| Temporal Validity | Deterministic | Low | Temporal Validity |
| Category Consistency | Deterministic/ML | Medium | Label Correctness |
| Description Quality | Deterministic | Low | Coverage |
| Tag Quality | Deterministic | Low | Coverage |
| Engagement Validation | Deterministic | Low | Data Quality |
| Content Relevance | LLM | High | Label Correctness |
| Duplicate Detection | Deterministic | Medium | Data Quality |
| Robustness Test | LLM | High | Model Evaluation |

## Dependencies

1. **config/allowlist.json** - For URL authority checking
2. **LangGraph** - For node orchestration
3. **NLI Model** (optional) - For content relevance checking
4. **Texas Statutes API** (future) - For citation validation

## Metrics to Track

- **Pass Rate**: % of records passing all validators
- **False Positive Rate**: Valid records flagged as invalid
- **False Negative Rate**: Invalid records passing validation
- **Coverage**: % of records with all fields populated
- **Runtime**: Average validation time per record

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| URL allowlist outdated | Medium | High | Regular allowlist updates |
| Overfitting to current data | High | Medium | Keep validators reversible |
| False positives blocking valid data | Medium | High | Human review fallback |
| Temporal edge cases | Low | Medium | Extended date range validation |

## Implementation Plan

### Phase 1 (Week 1)
1. Schema Validator
2. URL Authority Checker  
3. Temporal Validity Checker
4. Engagement Validation

### Phase 2 (Week 2)
1. Category Consistency Checker
2. Description Quality Checker
3. Tag Quality Checker
4. Duplicate Detection

### Phase 3 (Week 3-4)
1. Content Relevance (LLM-based)
2. Robustness Testing
3. Test harness and reporting

## Test Cases Summary

Each validator should have 3-5 test cases:
- Happy path (valid input)
- Edge cases (boundary values)
- Failure cases (invalid input)
- Edge case: Empty/missing optional fields

## Fallback Strategies

- If URL checker fails → Flag for manual review
- If NLI model unavailable → Skip to deterministic checks
- If temporal validation uncertain → Set to WARNING not ERROR
