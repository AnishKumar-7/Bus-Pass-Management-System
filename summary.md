# Bus Pass Management System - Technical Summary

**Project Title**: Bus Pass Management System  
**Author**: Anish Kumar ([@AnishKumar-7](https://github.com/AnishKumar-7))  
**Language**: Python 3  
**Data Structures**: Lists, Dictionaries, File I/O  

---

## 1. Executive Summary & Architecture

The **Bus Pass Management System** is a lightweight, efficient console application designed to automate the lifecycle of public commuter bus passes. It replaces manual registers with an auditable, persistent file-based management system.

### Key Capabilities:
- Automated alphanumeric ID generation (`BP101`, `BP102`, ...).
- Concession enforcement (automatic 25% discount for verified student passengers).
- Multi-tier tariff scheduling (`Monthly`, `Quarterly`, `Yearly`).
- Direct file serialization and deserialization via flat-file database (`buspass.txt`).
- Search and renewal modules with full input sanitation.

---

## 2. Core Functional Modules

| Module / Function | Purpose | Complexity |
| :--- | :--- | :--- |
| `load_passes(filename)` | Deserializes `buspass.txt` into in-memory dictionary objects | $O(N)$ |
| `save_passes(passes, filename)` | Serializes all active passes to disk atomically | $O(N)$ |
| `generate_next_id(passes)` | Finds highest existing ID and generates next sequential pass ID | $O(N)$ |
| `calculate_fee(pass_type, category)` | Applies discount rules and returns calculated tariff | $O(1)$ |
| `issue_pass(...)` | Validates input, constructs record, and appends to storage | $O(1)$ |
| `renew_pass(...)` | Updates validity tier, recalculates fee, and persists changes | $O(N)$ |
| `search_pass(...)` | Performs case-insensitive lookup by pass ID | $O(N)$ |
| `view_all_passes(...)` | Displays all issued passes in formatted table | $O(N)$ |

---

## 3. Mathematical & Concession Formulations

### 3.1 Base Tariff Schedule
- **Monthly Tier**: $T_{\text{Monthly}} = \text{Rs. } 500$ (Validity: 30 days)
- **Quarterly Tier**: $T_{\text{Quarterly}} = \text{Rs. } 1350$ (Validity: 90 days)
- **Yearly Tier**: $T_{\text{Yearly}} = \text{Rs. } 4800$ (Validity: 365 days)

### 3.2 Student Concession Formula (25% Discount)
For a selected pass tier with base fee $F_{\text{base}}$:
$$\text{Fee}_{\text{Student}} = F_{\text{base}} \times (1 - 0.25) = F_{\text{base}} \times 0.75$$

- **Monthly (Student)**: $500 \times 0.75 = \text{Rs. } 375$
- **Quarterly (Student)**: $1350 \times 0.75 = \text{Rs. } 1012.50$
- **Yearly (Student)**: $4800 \times 0.75 = \text{Rs. } 3600$

### 3.3 Sequential Alphanumeric ID Increment Logic
$$\text{ID}_{k+1} = \text{"BP"} + \left(\max_{p \in \text{Passes}} \text{NumericSuffix}(p.\text{id}) + 1\right)$$
Where the default baseline identifier is $\text{"BP101"}$.

---

## 4. Verification & Testing

The system includes automated tests verifying the following scenarios:
1. **Pass Issuance**: Correct ID generation, fee computation, and field persistence.
2. **Student Discount**: Validation of 25% discount application across all duration tiers.
3. **Pass Renewal**: Proper transition across duration tiers and fee recalculation.
4. **Input Sanitation**: Rejection of invalid pass types or unsupported categories.
5. **Persistence**: Consistency of reads and writes against `buspass.txt`.

---

## 5. File Persistence Format (`buspass.txt`)

Data is stored in clean pipe-delimited format:
```text
BP101 | Riya | Route 5 | Monthly | Rs. 500
BP102 | Aman | Route 7 | Yearly | Rs. 3600
```
This ensures high readability and backward-compatible parsing.
