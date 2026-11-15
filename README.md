# Bus Pass Management System

A production-grade, zero-dependency console application in Python 3 for commuter bus pass issuance, renewal, ID lookup, and flat-file persistent storage.

---

## Architecture & System Design

The system is designed with a strict separation between domain state, tariff calculation engines, input validation pipelines, and terminal presentation:

```
┌────────────────────────────────────────────────────────┐
│                   CLI Controller                       │
│    (Session dispatcher, command routing, exit handler) │
└───────────────────────────┬────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌────────────────────────┐      ┌────────────────────────┐
│  Validation Layer      │      │  Domain & State Layer  │
│  - Pass tier checking  │      │  - In-memory passes    │
│  - Category validation │◄────►│  - Sequential ID (BP)  │
│  - ID format parsing   │      │  - Tariff & discount   │
└────────────────────────┘      └───────────┬────────────┘
                                            │
                                            ▼
                                ┌────────────────────────┐
                                │   Persistence Layer    │
                                │   - buspass.txt        │
                                │   - Atomic file writes │
                                └────────────────────────┘
```

### Key Architectural Characteristics
* **Flat-File Atomic Persistence**: Records are saved in pipe-delimited plaintext to `buspass.txt`. File updates use atomic temp-file substitution (`os.replace`) to ensure zero file corruption during unexpected termination.
* **$O(1)$ Tariff Lookups**: The pass tariff catalog uses a hash map (`dict`) with constant-time lookup for duration days and pricing schedules.
* **Sequential Alphanumeric ID Engine**: Generates unique identifiers (`BP101`, `BP102`, ...) dynamically computed from existing storage to eliminate collision risks.
* **Pure Financial Calculation**: `calculate_fee()` operates as a deterministic function with exact concession rate application and clean integer rounding.

---

## Business Rules & Tariff Schedule

### Pass Tiers and Pricing Matrix
| Pass Tier | Validity Duration | Standard Fee (General) | Concession Fee (Student - 25% Off) |
|:---:|:---:|:---:|:---:|
| **Monthly** | 30 Days | Rs. 500 | Rs. 375 |
| **Quarterly** | 90 Days | Rs. 1350 | Rs. 1012.50 |
| **Yearly** | 365 Days | Rs. 4800 | Rs. 3600 |

### Financial & Concession Engine
$$\text{Fee}_{\text{General}} = F_{\text{base}}$$
$$\text{Fee}_{\text{Student}} = F_{\text{base}} \times (1 - 0.25) = F_{\text{base}} \times 0.75$$
$$\text{ID}_{k+1} = \text{"BP"} + \left(\max_{p \in \text{Passes}} \text{NumericSuffix}(p.\text{id}) + 1\right)$$

---

## Project Structure

```
Bus-Pass-Management-System/
├── main.py                # Core application, domain logic & interactive console
├── test_bus_pass.py       # Automated unittest suite (5 acceptance test cases)
├── buspass.txt            # Persistent flat-file storage database
├── buspass.csv            # Tabular CSV database export with column headers
├── README.md              # System architecture, user guide & verification matrix
├── summary.md             # Technical design document & test verification report
├── test_cases_pass.png    # Primary test pass verification graphic
├── screenshots/           # VS Code integrated terminal execution captures
│   ├── test_case_1_normal.png
│   ├── test_case_2_boundary.png
│   ├── test_case_3_invalid.png
│   ├── test_case_4_multi_operation.png
│   ├── test_case_5_renewal.png
│   ├── test_case_all_pass_vscode.png
│   └── vscode_full_ide_test_pass.png
└── .gitignore             # Standard Python gitignore
```

---

## Getting Started

### Prerequisites
* Python 3.7+ (Standard library only; zero external pip dependencies).

### Run the Application
Launch the interactive bus pass console from the terminal:
```bash
python main.py
```

### Run the Automated Test Suite
Run acceptance tests directly via CLI:
```bash
python main.py --test
# or
python -m unittest test_bus_pass.py -v
```

### Interactive Commands
* **Option 1 (Issue):** Issues a new bus pass with automated sequential ID and fee calculation.
* **Option 2 (Renew):** Upgrades or updates the duration tier and discount for an existing pass ID.
* **Option 3 (Search):** Looks up and prints record details by pass ID (`BP101`).
* **Option 4 (View All):** Lists all active passes in formatted tabular format.
* **Option 5 (Exit):** Safely saves and detaches from the application.
* **Option 6 (Reset DB):** Truncates `buspass.txt` to test boundary conditions (empty file).
* **Option 7 (Pre-seed DB):** Initializes `buspass.txt` with record `BP101` for test scenario 4.

### Example Console Session
```text
=======================================================
             BUS PASS MANAGEMENT SYSTEM
=======================================================
1. Issue New Pass
2. Renew Existing Pass
3. Search Pass by ID
4. View All Passes
5. Exit
=======================================================
Enter your choice (1-7): 1
Name: Riya
Route: Route 5
Type: Monthly
Category: General
Pass issued. ID: BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500 | Valid: 30 days
```

---

## Verification Matrix

The system is validated across normal operations, boundary limits, concession rules, and input rejection guardrails:

| Test Scenario | Scope | Input Vector | Expected Output | Status |
|---|---|---|---|:---:|
| **Test Case 1** | Normal pass issuance | Riya, Route 5, Monthly, General | `Pass issued. ID: BP101 \| Riya \| Route 5 \| Monthly \| Fee: Rs. 500 \| Valid: 30 days` | **PASS** |
| **Test Case 2** | Boundary / Minimum input | `buspass.txt` is empty, Option 4 (View all) | `No passes issued yet.` | **PASS** |
| **Test Case 3** | Invalid pass tier rejection | Aman, Route 7, Weekly, General | `Invalid pass type. Choose Monthly, Quarterly or Yearly. Pass not issued.` | **PASS** |
| **Test Case 4(a)** | Student concession discount | Aman, Route 7, Yearly, Student | `Pass issued. ID: BP102 \| Aman \| Route 7 \| Yearly \| Fee: Rs. 3600 \| Valid: 365 days` | **PASS** |
| **Test Case 4(b)** | Search by pass ID | ID BP101 | `BP101 \| Riya \| Route 5 \| Monthly \| Fee: Rs. 500` | **PASS** |
| **Test Case 5** | Pass renewal & recalculation | BP101, Quarterly, Student | `Pass renewed. ID: BP101 \| Riya \| Route 5 \| Quarterly \| Fee: Rs. 1012.5 \| Valid: 90 days` | **PASS** |
| **Persistence Integrity** | Atomic write verification | Modify & reload `buspass.txt` | Pipe-delimited records match in-memory state | **PASS** |

---

## Author & Academic Details
- **Author:** Anish Kumar ([@AnishKumar-7](https://github.com/AnishKumar-7))
- **Course:** Programming Fundamentals and Logic Building Using Python (`RU-100-01-0021`)
- **Institution:** Rungta International Skills University, School of Computer Science & Engineering
