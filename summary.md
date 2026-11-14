# Technical Summary: Bus Pass Management System

- **Course:** Programming Fundamentals and Logic Building Using Python (`RU-100-01-0021`)
- **Institution:** Rungta International Skills University, School of Computer Science & Engineering
- **Degree:** B.Tech Computer Science & Engineering (First Semester)
- **Author:** Anish Kumar
- **Implementation Language:** Python 3
- **Primary Data Structures:** Dictionaries, Lists, Flat-file I/O

---

## 1. System Overview

The Bus Pass Management System is a console application built to manage commuter bus passes. It replaces manual paper registers with an automated file-based workflow that supports issuing passes, applying student concessions, renewing existing passes, and searching records.

### Functional Capabilities:
- Sequential ID generation (`BP101`, `BP102`, etc.) based on existing stored records.
- Automatic 25% discount applied for verified student passengers.
- Multi-tier tariff schedules for Monthly, Quarterly, and Yearly passes.
- Direct flat-file storage in `buspass.txt` with pipe-delimited records.
- Input validation to reject invalid pass tiers and invalid categories.

---

## 2. Function Hierarchy and Modules

| Function | Purpose | Complexity |
| :--- | :--- | :--- |
| `load_passes(filename)` | Reads and parses `buspass.txt` into memory | O(N) |
| `save_passes(passes, filename)` | Writes active records back to disk | O(N) |
| `generate_next_id(passes)` | Scans existing records to compute the next sequential ID | O(N) |
| `calculate_fee(pass_type, category)` | Computes base fee and applies 25% student concession | O(1) |
| `issue_pass(...)` | Validates user input and creates a new pass record | O(1) |
| `renew_pass(...)` | Updates validity tier and fee for an existing ID | O(N) |
| `search_pass(...)` | Looks up a pass record by ID (case-insensitive) | O(N) |
| `view_all_passes(...)` | Displays all stored passes in a formatted table | O(N) |

---

## 3. Mathematical and Concession Models

### 3.1 Base Tariffs
- **Monthly Tier:** Rs. 500 (30 days validity)
- **Quarterly Tier:** Rs. 1350 (90 days validity)
- **Yearly Tier:** Rs. 4800 (365 days validity)

### 3.2 Student Concession (25% Discount)
For base tariff $F_{\text{base}}$:
$$\text{Fee}_{\text{Student}} = F_{\text{base}} \times (1 - 0.25) = F_{\text{base}} \times 0.75$$

- Monthly (Student): $500 \times 0.75 = \text{Rs. } 375$
- Quarterly (Student): $1350 \times 0.75 = \text{Rs. } 1012.50$
- Yearly (Student): $4800 \times 0.75 = \text{Rs. } 3600$

### 3.3 Alphanumeric ID Generation
$$\text{ID}_{k+1} = \text{"BP"} + \left(\max_{p \in \text{Passes}} \text{NumericSuffix}(p.\text{id}) + 1\right)$$
If no previous passes exist, generation begins at `BP101`.

---

## 4. Verification and Self-Test Results

The built-in self-test suite verifies all core system requirements:
1. **Pass Issuance:** Verifies ID generation, correct fee assignment, and file writing.
2. **Student Concession:** Verifies 25% discount across all tiers.
3. **Pass Renewal:** Validates tier switching and fee recalculation.
4. **Input Sanitation:** Verifies rejection of unsupported pass tiers.
5. **Data Persistence:** Verifies read/write consistency with `buspass.txt`.

---

## 5. Storage Format (`buspass.txt`)

Data is stored as pipe-delimited plaintext:
```text
BP101 | Riya | Route 5 | Monthly | Rs. 500
BP102 | Aman | Route 7 | Yearly | Rs. 3600
```
This format allows simple file inspection and robust backward-compatible parsing.
