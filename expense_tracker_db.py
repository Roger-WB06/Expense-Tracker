import sqlite3

class ExpenseTrackerDb:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create expenses table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            description TEXT,
            category TEXT,
            price REAL,
            date TEXT
            )''')
        self.conn.commit()

    def add_expense(self, description, category, price, date):
        # Add an expense to the database
        self.cursor.execute("INSERT INTO expenses (description, category, price, date) VALUES (?, ?, ?, ?)",
        (description, category, price, date))
        self.conn.commit()

    def view_expenses(self):
        # View all expenses
        self.cursor.execute("SELECT * FROM expenses")
        expenses = self.cursor.fetchall()
        return expenses

    def fetch_expenses_by_month(self, year, month):
        # Fetch expenses for a specific month of a year
        self.cursor.execute("SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ?", (year + "-" + month,))
        expenses = self.cursor.fetchall()
        return expenses

    def fetch_expenses_by_category(self, category):
        # Fetch expenses by category
        self.cursor.execute("SELECT * FROM expenses WHERE `category` = ?",(category,))
        expenses = self.cursor.fetchall()
        return expenses
    
    def delete_expense(self, expense_id):
        # Delete an expense by its ID
        self.cursor.execute("DELETE FROM expenses WHERE `id` = ?", (expense_id,))
        self.conn.commit()

    def close(self):
        # Close the database connection
        self.conn.close()
