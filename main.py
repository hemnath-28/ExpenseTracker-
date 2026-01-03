import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from typing import Optional, List, Dict

# --- Configuration ---
USERS_FILE: str = "users.csv"
CSV_FILE_TEMPLATE: str = "expenses_{}.csv"
LOG_FILE: str = "change_log.txt"

# --- Global State ---
current_user: Optional[str] = None
CSV_FILE: Optional[str] = None

# --- Tkinter Setup (Hide the main window) ---
root = tk.Tk()
root.withdraw() 

def log_change(action: str) -> None:
    current_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode="a", newline="") as log_file:
        log_file.write(f"{current_time}: {action}\n")

def user_exists(username: str) -> bool:
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, mode="r") as file:
        reader = csv.reader(file)
        return any(row and row[0] == username for row in reader)

def register_user(username: str, password: str) -> None:
    with open(USERS_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    log_change(f"User registered: {username}")

def validate_user(username: str, password: str) -> bool:
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username and row[1] == password:
                log_change(f"User login successful: {username}")
                return True
    log_change(f"User login failed: {username}")
    return False

def set_user(username: str) -> None:
    global current_user, CSV_FILE
    current_user = username
    CSV_FILE = CSV_FILE_TEMPLATE.format(username)
    log_change(f"User set: {username}")

def save_entry(date: str, amount: float, category: str, description: str, 
               is_income: bool = False, is_recurring: bool = False) -> None:
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, description, str(is_income), str(is_recurring)])

def add_entry(amount: float, category: str, description: str, date: Optional[str] = None, 
              is_income: bool = False, is_recurring: bool = False) -> None:
    date = date if date else datetime.now().strftime("%Y-%m-%d")
    
    if not amount or not category:
        messagebox.showwarning("Warning", "Please fill in all required fields.")
        return

    save_entry(date, float(amount), category, description, is_income, is_recurring)
    log_change(f"Entry added: {category} - {amount} on {date}")
    messagebox.showinfo("Success", "Entry added successfully.")
    
    # Display updated savings
    savings: float = calculate_monthly_savings()
    print(f"Total Savings for the month: ${savings:.2f}")

def load_entries() -> List[List[str]]:
    entries: List[List[str]] = []
    if not CSV_FILE or not os.path.exists(CSV_FILE):
        return entries
        
    try:
        with open(CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row: # Check for empty rows
                    entries.append(row)
    except FileNotFoundError:
        pass
    return entries

def plot_monthly_expenses() -> None:
    entries = load_entries()
    if not entries:
        print("No data available to plot.")
        return

    monthly_totals: Dict[str, float] = {}

    for entry in entries:
        try:
            date = entry[0]
            amount = float(entry[1])
            is_income = entry[4] == "True"
            if not is_income:
                month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m")
                monthly_totals[month] = monthly_totals.get(month, 0) + amount
        except (ValueError, IndexError):
            continue

    months: List[str] = list(monthly_totals.keys())
    totals: List[float] = list(monthly_totals.values())

    plt.figure(figsize=(10, 6))
    plt.bar(months, totals, color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Total Expense ($)')
    plt.title('Monthly Expenses')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    log_change("Monthly expenses plot generated.")

def plot_expenses_by_category() -> None:
    entries = load_entries()
    if not entries:
        print("No data available to plot.")
        return

    category_totals: Dict[str, float] = {}

    for entry in entries:
        try:
            amount = float(entry[1])
            category = entry[2]
            is_income = entry[4] == "True"
            
            if not is_income:
                category_totals[category] = category_totals.get(category, 0) + amount
        except (ValueError, IndexError):
            continue

    categories: List[str] = list(category_totals.keys())
    totals: List[float] = list(category_totals.values())

    plt.figure(figsize=(8, 8))
    plt.pie(totals, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("Expenses by Category")
    plt.show()
    log_change("Expenses by category plot generated.")

def search_expenses_by_date(start_date: str, end_date: str) -> None:
    entries = load_entries()
    filtered_entries: List[List[str]] = []
    
    for entry in entries:
        date = entry[0]
        if start_date <= date <= end_date:
            filtered_entries.append(entry)

    if filtered_entries:
        for entry in filtered_entries:
            print(entry)
    else:
        print("No entries found in this date range.")

    log_change(f"Expenses searched between {start_date} and {end_date}.")

def export_data() -> None:
    entries = load_entries()
    export_file: str = f"exported_data_{current_user}.csv"
    with open(export_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Amount", "Category", "Description", "Is Income", "Is Recurring"])
        for entry in entries:
            writer.writerow(entry)
    print(f"Data exported to {export_file}.")
    messagebox.showinfo("Export", f"Data exported successfully to {export_file}")
    log_change("User data exported to CSV.")

def display_expense_summary() -> None:
    entries = load_entries()
    category_totals: Dict[str, float] = {}
    
    for entry in entries:
        try:
            amount = float(entry[1])
            category = entry[2]
            is_income = entry[4] == "True"
            
            if not is_income:
                category_totals[category] = category_totals.get(category, 0) + amount
        except (ValueError, IndexError):
            continue
    
    if not category_totals:
        print("No expenses recorded yet.")
    else:
        for category, total in category_totals.items():
            print(f"Total spent on {category}: ${total:.2f}")

    log_change("Expense summary displayed by category.")

def set_budget() -> None:
    try:
        budget_input = input("Enter your budget amount for the month: ")
        budget_amount: float = float(budget_input)
        with open(f"{current_user}_budget.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([budget_amount])
        print(f"Budget of ${budget_amount} has been set.")
        log_change(f"Budget of ${budget_amount} set for {current_user}.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        log_change("Failed to set budget due to invalid input.")

def load_budget() -> Optional[float]:
    try:
        if not os.path.exists(f"{current_user}_budget.csv"):
            return None
        with open(f"{current_user}_budget.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                return float(row[0])
    except (FileNotFoundError, ValueError, IndexError):
        return None
    return None

def calculate_monthly_savings() -> float:
    entries = load_entries()
    current_month = datetime.now().strftime("%Y-%m")
    total_income: float = 0.0
    total_expenses: float = 0.0
    
    for entry in entries:
        try:
            if entry[0].startswith(current_month):
                amount = float(entry[1])
                is_income = entry[4] == "True"
                if is_income:
                    total_income += amount
                else:
                    total_expenses += amount
        except (ValueError, IndexError):
            continue
            
    return total_income - total_expenses

def check_budget_alerts() -> None:
    budget: Optional[float] = load_budget()
    if budget:
        try:
            expenses: float = sum(float(entry[1]) for entry in load_entries() if entry[4] == "False")
            if expenses >= budget:
                messagebox.showwarning("Budget Alert", "Warning: You have reached or exceeded your budget!")
                print("Warning: You have reached or exceeded your budget!")
            else:
                print(f"Current expenses: ${expenses}. Remaining budget: ${budget - expenses:.2f}")
        except ValueError:
            pass
        log_change("Budget alert checked.")
    else:
        print("No budget set.")

def delete_entry() -> None:
    entries = load_entries()

    if not entries:
        print("No entries found.")
        return

    print("\n--- All Entries ---")
    for i, entry in enumerate(entries, start=1):
        print(f"{i}. Date: {entry[0]}, Amount: {entry[1]}, Category: {entry[2]}, Description: {entry[3]}, Income: {entry[4]}")

    entry_index = input("Enter the number of the entry to delete (or press Enter to cancel): ")
    if entry_index.strip() == "":
        print("Deletion cancelled.")
        return
    
    try:
        index = int(entry_index) - 1
        if 0 <= index < len(entries):
            deleted_entry = entries.pop(index)
            
            with open(CSV_FILE, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(entries)
            
            print("Entry deleted successfully.")
            messagebox.showinfo("Deleted", "Entry deleted successfully.")
            log_change(f"Entry deleted: {deleted_entry}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def main():
    while True:
        print("\n--- Financial Management System ---")
        if current_user:
            print(f"Logged in as: {current_user}")
        
        print("1. Register")
        print("2. Login")
        print("3. Set Budget")
        print("4. Add Expense Entry")
        print("5. Add Income Entry")
        print("6. View Expense Summary")
        print("7. Plot Monthly Expenses")
        print("8. Plot Expenses by Category")
        print("9. Search Expenses by Date")
        print("10. Export Data")
        print("11. Check Budget Alerts")
        print("12. Delete Entry")
        print("13. Exit")
        
        choice = input("Enter your choice: ")

        # --- Public Options (No Login Required) ---
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if not user_exists(username):
                register_user(username, password)
                print("Registration successful!")
            else:
                print("Username already exists.")
            continue
        
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if validate_user(username, password):
                set_user(username)
                print(f"Welcome, {username}!")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
            continue

        elif choice == "13":
            print("Exiting system.")
            break

        # --- Restricted Options (Login Required) ---
        if current_user is None:
            print("\n[!] Please LOGIN (Option 2) before accessing this feature.\n")
            continue

        if choice == "3":
            set_budget()
        
        elif choice == "4":
            try:
                amount_str = input("Enter amount: ")
                amount = float(amount_str)
                category = input("Enter category: ")
                description = input("Enter description: ")
                add_entry(amount, category, description, is_income=False)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        elif choice == "5":
            try:
                amount_str = input("Enter amount: ")
                amount = float(amount_str)
                category = input("Enter category: ")
                description = input("Enter description: ")
                add_entry(amount, category, description, is_income=True)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        elif choice == "6":
            display_expense_summary()
        
        elif choice == "7":
            plot_monthly_expenses()
        
        elif choice == "8":
            plot_expenses_by_category()
        
        elif choice == "9":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            search_expenses_by_date(start_date, end_date)
        
        elif choice == "10":
            export_data()
        
        elif choice == "11":
            check_budget_alerts()
        
        elif choice == "12":
            delete_entry()
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
