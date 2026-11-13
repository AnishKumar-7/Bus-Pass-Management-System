# Bus Pass Management System

[![Python 3](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status: Passed](https://img.shields.io/badge/Tests-5%2F5%20Passed-brightgreen.svg)]()

A robust, console-based Bus Pass Management System built with Python 3. It provides an end-to-end solution for issuing, renewing, searching, and managing commuter bus passes with automated fee calculation, student concession rules, and flat-file persistent storage.

---

## 📌 Features

1. **Issue New Pass:**
   - Automatically generates sequential alphanumeric identifiers starting from `BP101`, `BP102`, etc.
   - Computes base fee based on duration tier (`Monthly`, `Quarterly`, `Yearly`).
   - Automatically calculates and applies a **25% concession for students**.
   - Input validation for pass types and passenger categories (`General`, `Student`).
   - Persistent storage to `buspass.txt`.

2. **Renew Pass:**
   - Search for existing pass by ID.
   - Upgrade or renew the duration tier (`Monthly`, `Quarterly`, `Yearly`).
   - Recalculates fee with applicable student discount.
   - Atomic file update to preserve data consistency.

3. **Search Pass by ID:**
   - Instant search across issued passes.
   - Case-insensitive ID lookup (`bp101` $\rightarrow$ `BP101`).
   - Formatted output: `BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500`

4. **View All Passes:**
   - Displays all active passes with passenger details, routes, and validity.
   - Clean message if no passes are found.

5. **Data Persistence (`buspass.txt`):**
   - Automatically loads existing records on startup.
   - Saves updates atomically to prevent data corruption.

6. **Built-in Self-Test Suite:**
   - Run automated verification for normal, boundary, concession, and edge scenarios.

---

## 📊 Pass Tiers & Pricing Matrix

| Pass Tier | Validity Duration | Standard Fee (General) | Concession Fee (Student - 25% Off) |
| :--- | :--- | :--- | :--- |
| **Monthly** | 30 Days | Rs. 500 | **Rs. 375** |
| **Quarterly** | 90 Days | Rs. 1350 | **Rs. 1012.50** |
| **Yearly** | 365 Days | Rs. 4800 | **Rs. 3600** |

---

## 🛠️ Architecture & Data Structures

- **Dictionary for Pass Types:**
  ```python
  PASS_TYPES = {
      "Monthly": {"days": 30, "fee": 500},
      "Quarterly": {"days": 90, "fee": 1350},
      "Yearly": {"days": 365, "fee": 4800}
  }
  ```

- **List of Dictionaries for Stored Passes:**
  ```python
  passes = [
      {
          "id": "BP101",
          "name": "Riya",
          "route": "Route 5",
          "type": "Monthly",
          "category": "General",
          "fee": 500,
          "valid_days": 30
      }
  ]
  ```

- **Modular Functions:**
  - `load_passes(filename)`: Reads and parses records from file.
  - `save_passes(passes, filename)`: Writes updated records safely to disk.
  - `generate_next_id(passes)`: Generates sequential IDs (`BP101`, `BP102`, ...).
  - `calculate_fee(pass_type, category)`: Computes base fee and student discount.
  - `issue_pass(...)`: Handles new pass issuance and input validation.
  - `renew_pass(...)`: Updates existing pass duration and fee.
  - `search_pass(...)`: Searches and displays pass details by ID.
  - `view_all_passes(...)`: Displays all issued passes.
  - `run_self_tests()`: Built-in automated verification suite.

---

## 💻 How to Run

### Prerequisites
- Python 3.8 or higher installed on your system.

### Running the Application
```bash
python main.py
```

### Running Self-Tests
Inside the interactive menu, choose the self-test option or run:
```bash
python main.py --test
```

---

## 🧪 Verification Scenarios

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

## 📂 Project Structure
```text
Bus-Pass-Management-System/
├── main.py        # Complete Python 3 console application
├── buspass.txt    # Flat-file database for persistent storage
├── README.md      # Project documentation and run guide
└── summary.md     # Technical and architectural summary
```

---

## 👤 Author
- **Anish Kumar** - [@AnishKumar-7](https://github.com/AnishKumar-7)

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
