"""
================================================================================
Bus Pass Management System
Author: Anish Kumar (@AnishKumar-7)
Course: Programming Fundamentals and Logic Building Using Python
================================================================================
"""

import os

# Project folder and data file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "buspass.txt")


# ------------------------------------------------------------------------------
# 1. FEE CALCULATION
# ------------------------------------------------------------------------------
def calculate_fee(pass_type, category):
    """
    Calculates fee and validity days.
    Students get a 25% discount.
    """
    if pass_type == "Monthly":
        fee = 500
        days = 30
    elif pass_type == "Quarterly":
        fee = 1350
        days = 90
    elif pass_type == "Yearly":
        fee = 4800
        days = 365
    else:
        return 0, 0

    # 25% discount for student
    if category.lower() == "student":
        fee = fee * 0.75
        if fee.is_integer():
            fee = int(fee)

    return fee, days


# ------------------------------------------------------------------------------
# 2. NEXT ID GENERATOR
# ------------------------------------------------------------------------------
def generate_next_id(passes):
    """
    Generates next sequential pass ID: BP101, BP102, BP103...
    """
    if len(passes) == 0:
        return "BP101"

    highest = 100
    for p in passes:
        pass_id = p["id"]
        if pass_id.startswith("BP"):
            number_part = pass_id[2:]
            if number_part.isdigit():
                num = int(number_part)
                if num > highest:
                    highest = num

    next_num = highest + 1
    return "BP" + str(next_num)


# ------------------------------------------------------------------------------
# 3. FILE OPERATIONS (LOAD & SAVE)
# ------------------------------------------------------------------------------
def load_passes(filename=FILE_NAME):
    """
    Reads all passes from buspass.txt into a list.
    """
    passes = []
    if not os.path.exists(filename):
        return passes

    file = open(filename, "r", encoding="utf-8")
    for line in file:
        line = line.strip()
        if line == "":
            continue

        parts = line.split("|")
        if len(parts) >= 4:
            pass_id = parts[0].strip()
            name = parts[1].strip()
            route = parts[2].strip()
            pass_type = parts[3].strip()

            fee = 0
            category = "General"
            if len(parts) >= 5:
                fee_text = parts[4].replace("Fee:", "").replace("Rs.", "").replace("Rs", "").strip()
                try:
                    val = float(fee_text)
                    fee = int(val) if val.is_integer() else val
                except ValueError:
                    pass

            # Detect category based on fee
            if pass_type == "Monthly" and fee == 375:
                category = "Student"
            elif pass_type == "Quarterly" and fee == 1012.5:
                category = "Student"
            elif pass_type == "Yearly" and fee == 3600:
                category = "Student"

            # Get validity days
            if pass_type == "Monthly":
                days = 30
            elif pass_type == "Quarterly":
                days = 90
            else:
                days = 365

            passes.append({
                "id": pass_id,
                "name": name,
                "route": route,
                "type": pass_type,
                "category": category,
                "fee": fee,
                "valid_days": days
            })

    file.close()
    return passes


def save_passes(passes, filename=FILE_NAME):
    """
    Saves all passes to buspass.txt.
    """
    file = open(filename, "w", encoding="utf-8")
    for p in passes:
        line = f"{p['id']} | {p['name']} | {p['route']} | {p['type']} | Rs. {p['fee']}\n"
        file.write(line)
    file.close()


# ------------------------------------------------------------------------------
# 4. MAIN FEATURES: ISSUE, RENEW, SEARCH, VIEW ALL
# ------------------------------------------------------------------------------
def issue_pass(passes, name=None, route=None, pass_type=None, category=None, filename=FILE_NAME):
    """
    1. Issue New Pass
    """
    # Ask inputs from user if not provided
    if name is None:
        name = input("Name: ")
    if route is None:
        route = input("Route: ")
    if pass_type is None:
        pass_type = input("Type: ")
    if category is None:
        category = input("Category: ")

    # Clean inputs
    name = name.replace("Name:", "").strip()
    route = route.replace("Route:", "").strip()
    pass_type = pass_type.replace("Type:", "").strip().capitalize()
    category = category.replace("Category:", "").strip().capitalize()

    # Validation
    if name == "":
        print("Name cannot be empty. Pass not issued.")
        return None
    if route == "":
        print("Route cannot be empty. Pass not issued.")
        return None
    if pass_type not in ["Monthly", "Quarterly", "Yearly"]:
        print("Invalid pass type. Choose Monthly, Quarterly or Yearly. Pass not issued.")
        return None
    if category not in ["General", "Student"]:
        print("Invalid category. Choose Student or General. Pass not issued.")
        return None

    # Create new pass
    pass_id = generate_next_id(passes)
    fee, valid_days = calculate_fee(pass_type, category)

    new_pass = {
        "id": pass_id,
        "name": name,
        "route": route,
        "type": pass_type,
        "category": category,
        "fee": fee,
        "valid_days": valid_days
    }

    passes.append(new_pass)
    save_passes(passes, filename)

    print(f"Pass issued. ID: {pass_id} | {name} | {route} | {pass_type} | Fee: Rs. {fee} | Valid: {valid_days} days")
    return new_pass


def renew_pass(passes, pass_id=None, new_type=None, category=None, filename=FILE_NAME):
    """
    2. Renew Existing Pass
    """
    if pass_id is None:
        pass_id = input("Enter Pass ID to renew: ")

    pass_id = pass_id.replace("ID:", "").strip().upper()
    if pass_id == "":
        print("Pass ID cannot be empty. Pass not renewed.")
        return None

    # Search existing pass
    target_pass = None
    for p in passes:
        if p["id"].upper() == pass_id:
            target_pass = p
            break

    if target_pass is None:
        print(f"Pass ID {pass_id} not found.")
        return None

    # Ask for new type and category
    if new_type is None:
        new_type = input(f"Enter Pass Type (Monthly/Quarterly/Yearly) [Current: {target_pass['type']}]: ")
    if category is None:
        category = input(f"Enter Category (General/Student) [Current: {target_pass['category']}]: ")

    # Keep existing if user pressed Enter
    new_type = new_type.strip()
    if new_type == "":
        new_type = target_pass["type"]

    category = category.strip()
    if category == "":
        category = target_pass["category"]

    new_type = new_type.capitalize()
    category = category.capitalize()

    # Validation
    if new_type not in ["Monthly", "Quarterly", "Yearly"]:
        print("Invalid pass type. Choose Monthly, Quarterly or Yearly. Pass not renewed.")
        return None
    if category not in ["General", "Student"]:
        print("Invalid category. Choose Student or General. Pass not renewed.")
        return None

    # Update pass
    fee, valid_days = calculate_fee(new_type, category)
    target_pass["type"] = new_type
    target_pass["category"] = category
    target_pass["fee"] = fee
    target_pass["valid_days"] = valid_days

    save_passes(passes, filename)

    print(f"Pass renewed. ID: {target_pass['id']} | {target_pass['name']} | {target_pass['route']} | {new_type} | Fee: Rs. {fee} | Valid: {valid_days} days")
    return target_pass


def search_pass(passes, pass_id=None):
    """
    3. Search Pass by ID
    """
    if pass_id is None:
        pass_id = input("Enter Pass ID: ")

    pass_id = pass_id.replace("ID:", "").strip().upper()
    if pass_id == "":
        print("Pass ID cannot be empty.")
        return None

    for p in passes:
        if p["id"].upper() == pass_id:
            print(f"{p['id']} | {p['name']} | {p['route']} | {p['type']} | Fee: Rs. {p['fee']}")
            return p

    print(f"Pass with ID {pass_id} not found.")
    return None


def view_all_passes(passes):
    """
    4. View All Passes
    """
    if len(passes) == 0:
        print("No passes issued yet.")
        return

    for p in passes:
        print(f"{p['id']} | {p['name']} | {p['route']} | {p['type']} | Fee: Rs. {p['fee']}")


# ------------------------------------------------------------------------------
# 5. CONSOLE MENU & PROGRAM ENTRY
# ------------------------------------------------------------------------------
def main():
    passes = load_passes()

    while True:
        print("\n=======================================================")
        print("             BUS PASS MANAGEMENT SYSTEM")
        print("=======================================================")
        print("1. Issue New Pass")
        print("2. Renew Existing Pass")
        print("3. Search Pass by ID")
        print("4. View All Passes")
        print("5. Exit")
        print("=======================================================")

        try:
            choice = input("Enter your choice (1-5): ").replace("\ufeff", "").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting application. Goodbye!")
            break

        if choice == "1":
            print("\n--- Issue New Pass ---")
            issue_pass(passes)
        elif choice == "2":
            print("\n--- Renew Pass ---")
            renew_pass(passes)
        elif choice == "3":
            print("\n--- Search Pass by ID ---")
            search_pass(passes)
        elif choice == "4":
            print("\n--- View All Passes ---")
            view_all_passes(passes)
        elif choice == "5":
            print("\nThank you for using Bus Pass Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
