# Bus Pass Management System

A console-based bus pass management system built in Python 3. It handles issuing, renewing, searching, and managing commuter bus passes with automated fee calculation, student concession rules, and flat-file persistent storage.

---

## Features

1. **Issue New Pass:**
   - Generates sequential pass IDs (`BP101`, `BP102`, etc.).
   - Computes base fee based on duration (`Monthly`, `Quarterly`, `Yearly`).
   - Applies an automatic 25% discount for students.
   - Validates pass types and categories before saving to `buspass.txt`.

2. **Renew Pass:**
   - Looks up existing pass by ID.
   - Updates the validity period and recalculates fee with applicable student concession.
   - Updates the storage file atomically to maintain data integrity.

3. **Search Pass by ID:**
   - Case-insensitive search across issued passes.
   - Formatted record output: `BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500`

4. **View All Passes:**
   - Displays all active passes in a clean tabular view.

5. **Data Persistence (`buspass.txt`):**
   - Automatically loads existing records on startup.
   - Writes updates back to disk after every change.

6. **Automated Test Suite:**
   - Self-test suite verifying normal issuance, concessions, renewals, and invalid input handling.

---

## Pass Tiers and Pricing Matrix

| Pass Tier | Validity Duration | Standard Fee (General) | Concession Fee (Student - 25% Off) |
| :--- | :--- | :--- | :--- |
| **Monthly** | 30 Days | Rs. 500 | Rs. 375 |
| **Quarterly** | 90 Days | Rs. 1350 | Rs. 1012.50 |
| **Yearly** | 365 Days | Rs. 4800 | Rs. 3600 |

---

## Architecture and Data Structures

### Pass Configuration
```python
PASS_TYPES = {
    "Monthly": {"days": 30, "fee": 500},
    "Quarterly": {"days": 90, "fee": 1350},
    "Yearly": {"days": 365, "fee": 4800}
}
```

### Stored Pass Record Format
```python
{
    "id": "BP101",
    "name": "Riya",
    "route": "Route 5",
    "type": "Monthly",
    "category": "General",
    "fee": 500,
    "valid_days": 30
}
```

### Core Functions
- `load_passes(filename)`: Reads records from file into memory.
- `save_passes(passes, filename)`: Saves updated records to disk.
- `generate_next_id(passes)`: Generates next sequential pass ID.
- `calculate_fee(pass_type, category)`: Computes base fee and applies student discount.
- `issue_pass(...)`: Handles new pass issuance and input validation.
- `renew_pass(...)`: Updates existing pass duration and fee.
- `search_pass(...)`: Searches and displays pass details by ID.
- `view_all_passes(...)`: Displays all issued passes.
- `run_self_tests()`: Automated verification suite.

---

## How to Run

### Run Interactive Console
```bash
python main.py
```

### Run Self-Test Suite
```bash
python main.py --test
```

---

## Verification Scenarios

### Scenario 1: Issue New Pass (General)
```text
Menu Option: 1 (Issue)
Name: Riya
Route: Route 5
Type: Monthly
Category: General

Output:
Pass issued. ID: BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500 | Valid: 30 days
```

### Scenario 2: Issue Pass with Student Discount
```text
Menu Option: 1 (Issue)
Name: Aman
Route: Route 7
Type: Yearly
Category: Student

Output:
Pass issued. ID: BP102 | Aman | Route 7 | Yearly | Fee: Rs. 3600 | Valid: 365 days
```

### Scenario 3: Search by ID
```text
Menu Option: 3 (Search)
ID: BP101

Output:
BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500
```

### Scenario 4: Validation on Invalid Input
```text
Menu Option: 1 (Issue)
Name: Aman
Route: Route 7
Type: Weekly
Category: General

Output:
Invalid pass type. Choose Monthly, Quarterly or Yearly. Pass not issued.
```

---

## Project Structure
```text
Bus-Pass-Management-System/
├── main.py        # Python 3 console application and test runner
├── buspass.txt    # Flat-file database for persistent storage
├── README.md      # Project overview and run instructions
└── summary.md     # Technical and architectural summary
```

---

## Author & Academic Details
- **Student Name:** Anish Kumar
- **Course:** Programming Fundamentals and Logic Building Using Python (`RU-100-01-0021`)
- **Institution:** Rungta International Skills University, School of Computer Science & Engineering
