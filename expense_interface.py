from expense_tracker_db import ExpenseTrackerDb
import sqlite3
import datetime

class ExpenseInterface:
    def __init__(self):
        try:
            self.tracker = ExpenseTrackerDb("expenses.db")
        except sqlite3.Error as e:
            print("Error initializing database:", e)


    def create_expense(self):
        try:
            description = input("Enter expense description: ").strip()
            category = input("Enter expense category: ").strip()
            price = input("Enter price: ").strip()
            date_input = input("Enter date (YYYY-MM-DD): ").strip()

            # Check if any of the fields are empty
            if not description or not category or not price or not date_input:
                raise ValueError("All fields must be filled out.")

            # Check if price is a valid float
            try:
                price = float(price)
            except ValueError:
                raise ValueError("Price must be a valid number.")

            # Check if date is a valid date in YYYY-MM-DD format
            try:
                date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

            self.tracker.add_expense(description, category.capitalize(), price, date)
            print("Expense added successfully.")
        except ValueError as e:
            print("Error adding expense:", e)


    def view_all_expenses(self):
        try:
            expenses = self.tracker.view_expenses()
            if expenses:
                print("All Expenses: ")
                print("Id | Description | Category | Price | Date")
                for expense in expenses:
                    print(expense)
            else:
                print("No expenses found.")
        except sqlite3.Error as e:
            print("Error viewing all expenses:", e)


    def view_expenses_by_month(self):
        try:
            year = input("Enter year: ")
            month = input("Enter month (01-12): ")
            expenses = self.tracker.fetch_expenses_by_month(year, month)
            if expenses:
                print(f"Expenses for {month}-{year}:")
                for expense in expenses:
                    print(expense)
            else:
                print("No expenses found for this month.")
        except sqlite3.Error as e:
            print("Error fetching expenses by month:", e)


    def view_expenses_by_category(self):
        try:
            category = input("Enter category: ")
            expenses = self.tracker.fetch_expenses_by_category(category.capitalize())
            if expenses:
                print(f"Expenses for {category}:")
                for expense in expenses:
                    print(expense)
            else:
                print("No expenses found for this category.")
        except sqlite3.Error as e:
            print("Error fetching expenses by category:", e)


    def delete_expense_by_id(self):
        try:
            self.view_all_expenses()
            expense_id_input = input("Enter the ID of the expense you want to delete: ")

            # Check if the provided expense ID is empty
            if not expense_id_input:
                raise ValueError("Expense ID must be filled out.")
            
            # Check if the provided expense ID is numeric
            if not expense_id_input.isdigit():
                raise ValueError("Expense ID must be a number.")

            expense_id = int(expense_id_input)

            # Check if the provided expense ID exists before attempting to delete
            expenses = self.tracker.view_expenses()
            expense_ids = [expense[0] for expense in expenses]
            if expense_id not in expense_ids:
                raise ValueError("Expense ID does not exist.")

            self.tracker.delete_expense(expense_id)
            print("Expense deleted successfully.")
        except ValueError as e:
            print("Error deleting expense:", e)
        except sqlite3.Error as e:
            print("Database error:", e)


    def close_tracker(self):
        try:
            self.tracker.close()
            print("Expense tracker closed.")
        except sqlite3.Error as e:
            print("Error closing expense tracker:", e)


# usage
if __name__ == "__main__":
    interface = ExpenseInterface()
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Expenses by Month")
        print("4. View Expenses by Category")
        print("5. Delete Expense by ID")
        print("6. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            interface.create_expense()
        elif choice == "2":
            interface.view_all_expenses()
        elif choice == "3":
            interface.view_expenses_by_month()
        elif choice == "4":
            interface.view_expenses_by_category()
        elif choice == "5":
            interface.delete_expense_by_id()
        elif choice == "6":
            interface.close_tracker()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
