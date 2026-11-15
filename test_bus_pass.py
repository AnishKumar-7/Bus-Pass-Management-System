"""
================================================================================
Automated Verification Suite for Bus Pass Management System
Course: Programming Fundamentals and Logic Building Using Python (RU-100-01-0021)
Author: Anish Kumar (@AnishKumar-7)
Institution: Rungta International Skills University, School of CSE
================================================================================
Verifies all 4 official test cases from Project_Description_1K.pdf plus pass renewal:
  1. Test Case 1: Normal Input (Issue pass with standard fare)
  2. Test Case 2: Boundary / Minimum Input (Empty buspass.txt)
  3. Test Case 3: Invalid Input Rejection (Unsupported pass tier)
  4. Test Case 4: Existing File & Multi-Operation (Student discount & Search)
  5. Test Case 5: Pass Renewal (Tier switching & discount recalculation)
================================================================================
"""

import os
import io
import sys
import unittest
from contextlib import redirect_stdout

try:
    import main as bpm
except ImportError:
    import bus_pass_management as bpm

TEST_FILE = "test_buspass.txt"


class TestBusPassManagementSystem(unittest.TestCase):

    def setUp(self):
        # Clean up test file before each test
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def tearDown(self):
        # Clean up test file after each test
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_case_1_normal_input(self):
        """
        Test Case 1: Normal Input
        Input:
            Menu option 1 (Issue)
            Name: Riya
            Route: Route 5
            Type: Monthly
            Category: General
        Expected Output:
            Pass issued. ID: BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500 | Valid: 30 days
        """
        passes = []
        captured = io.StringIO()
        with redirect_stdout(captured):
            result = bpm.issue_pass(
                passes,
                name="Riya",
                route="Route 5",
                pass_type="Monthly",
                category="General",
                filename=TEST_FILE
            )

        output = captured.getvalue().strip()
        expected = "Pass issued. ID: BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500 | Valid: 30 days"
        self.assertIsNotNone(result)
        self.assertEqual(output, expected)
        self.assertEqual(result["id"], "BP101")
        self.assertEqual(result["fee"], 500)
        self.assertEqual(result["valid_days"], 30)

    def test_case_2_boundary_minimum_input(self):
        """
        Test Case 2: Boundary / Minimum Input
        Input:
            buspass.txt is empty
            Menu option 4 (View all)
        Expected Output:
            No passes issued yet.
        """
        # Create empty file
        open(TEST_FILE, "w").close()
        passes = bpm.load_passes(TEST_FILE)
        self.assertEqual(len(passes), 0)

        captured = io.StringIO()
        with redirect_stdout(captured):
            bpm.view_all_passes(passes)

        output = captured.getvalue().strip()
        expected = "No passes issued yet."
        self.assertEqual(output, expected)

    def test_case_3_invalid_input(self):
        """
        Test Case 3: Invalid Input
        Input:
            Menu option 1 (Issue)
            Name: Aman
            Route: Route 7
            Type: Weekly
            Category: General
        Expected Output:
            Invalid pass type. Choose Monthly, Quarterly or Yearly. Pass not issued.
        """
        passes = []
        captured = io.StringIO()
        with redirect_stdout(captured):
            result = bpm.issue_pass(
                passes,
                name="Aman",
                route="Route 7",
                pass_type="Weekly",
                category="General",
                filename=TEST_FILE
            )

        output = captured.getvalue().strip()
        expected = "Invalid pass type. Choose Monthly, Quarterly or Yearly. Pass not issued."
        self.assertIsNone(result)
        self.assertEqual(output, expected)
        self.assertEqual(len(passes), 0)

    def test_case_4_different_valid_scenario(self):
        """
        Test Case 4: Different Valid Scenario
        Precondition:
            buspass.txt has: BP101 | Riya | Route 5 | Monthly | Rs. 500
        Action (a):
            Menu option 1 (Issue): Aman, Route 7, Yearly, Student
        Expected Output (a):
            Pass issued. ID: BP102 | Aman | Route 7 | Yearly | Fee: Rs. 3600 | Valid: 365 days
        Action (b):
            Menu option 3 (Search): ID BP101
        Expected Output (b):
            BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500
        """
        # Set up precondition file
        with open(TEST_FILE, "w", encoding="utf-8") as f:
            f.write("BP101 | Riya | Route 5 | Monthly | Rs. 500\n")

        passes = bpm.load_passes(TEST_FILE)
        self.assertEqual(len(passes), 1)
        self.assertEqual(passes[0]["id"], "BP101")

        # Action (a): Issue Aman with Student discount on Yearly pass
        captured_a = io.StringIO()
        with redirect_stdout(captured_a):
            pass_a = bpm.issue_pass(
                passes,
                name="Aman",
                route="Route 7",
                pass_type="Yearly",
                category="Student",
                filename=TEST_FILE
            )

        output_a = captured_a.getvalue().strip()
        expected_a = "Pass issued. ID: BP102 | Aman | Route 7 | Yearly | Fee: Rs. 3600 | Valid: 365 days"
        self.assertIsNotNone(pass_a)
        self.assertEqual(output_a, expected_a)
        self.assertEqual(pass_a["id"], "BP102")
        self.assertEqual(pass_a["fee"], 3600)  # 4800 * 0.75 = 3600
        self.assertEqual(pass_a["valid_days"], 365)

        # Action (b): Search ID BP101
        captured_b = io.StringIO()
        with redirect_stdout(captured_b):
            search_res = bpm.search_pass(passes, pass_id="BP101")

        output_b = captured_b.getvalue().strip()
        expected_b = "BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500"
        self.assertIsNotNone(search_res)
        self.assertEqual(output_b, expected_b)

    def test_renew_pass_feature(self):
        """
        Verify renewing an existing pass updates validity and applies discounts.
        """
        passes = [
            {"id": "BP101", "name": "Riya", "route": "Route 5", "type": "Monthly",
             "category": "General", "fee": 500, "valid_days": 30}
        ]
        captured = io.StringIO()
        with redirect_stdout(captured):
            renewed = bpm.renew_pass(
                passes,
                pass_id="BP101",
                new_type="Quarterly",
                category="Student",
                filename=TEST_FILE
            )

        output = captured.getvalue().strip()
        # 1350 * 0.75 = 1012.5
        expected = "Pass renewed. ID: BP101 | Riya | Route 5 | Quarterly | Fee: Rs. 1012.5 | Valid: 90 days"
        self.assertIsNotNone(renewed)
        self.assertEqual(output, expected)
        self.assertEqual(renewed["type"], "Quarterly")
        self.assertEqual(renewed["valid_days"], 90)


if __name__ == "__main__":
    unittest.main()
