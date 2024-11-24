import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker (Presented by RITIK SHARMA)")
        self.root.geometry("600x400")
        self.create_gradient_background()
        self.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        self.create_input_fields()
        self.create_table()

    def create_gradient_background(self):
        canvas = tk.Canvas(self.root, width=600, height=400)
        canvas.pack(fill="both", expand=True)
        for i in range(256):
            color = f"#{255-i:02x}{0:02x}{255:02x}"
            canvas.create_rectangle(0, i * 2, 600, (i + 1) * 2, fill=color, outline=color)
        canvas.place(x=0, y=0)

    def create_input_fields(self):
        frame = tk.Frame(self.root, bg="#3399ff", relief="ridge", bd=2)
        frame.place(x=10, y=10, width=580, height=180)
        tk.Label(frame, text="Date (YYYY-MM-DD):", bg="#4da6ff").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Category:", bg="#4da6ff").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(frame)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frame, text="Amount:", bg="#4da6ff").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(frame, text="Description:", bg="#4da6ff").grid(row=3, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(frame)
        self.description_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Button(frame, text="Add Expense", command=self.add_expense, bg="#4da6ff").grid(row=1, column=3, pady=10, padx=5)
        tk.Button(frame, text="Generate Report", command=self.generate_report, bg="#4da6ff").grid(row=2, column=3, pady=10, padx=5)

    def create_table(self):
        table_frame = tk.Frame(self.root, bg="#4da6ff")
        table_frame.place(x=10, y=180, width=580, height=200)
        self.tree = ttk.Treeview(table_frame, columns=("Date", "Category", "Amount", "Description"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        description = self.description_entry.get()
        if not date or not category or not amount:
            messagebox.showerror("Input Error", "Please fill in all fields!")
            return
        try:
            amount = float(amount)
            new_entry = pd.DataFrame({
                "Date": [date],
                "Category": [category],
                "Amount": [amount],
                "Description": [description]
            })
            self.expenses = pd.concat([self.expenses, new_entry], ignore_index=True)
            self.tree.insert("", "end", values=(date, category, amount, description))
            self.date_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number!")

    def generate_report(self):
        if self.expenses.empty:
            messagebox.showwarning("No Data", "No expenses to analyze!")
            return
        category_totals = self.expenses.groupby("Category")["Amount"].sum()
        category_totals.plot(kind="pie", autopct="%1.1f%%", startangle=90, title="Expenses by Category")
        plt.ylabel("")
        plt.show()
        self.expenses["Date"] = pd.to_datetime(self.expenses["Date"])
        daily_totals = self.expenses.groupby(self.expenses["Date"].dt.date)["Amount"].sum()
        daily_totals.plot(kind="bar", title="Daily Expenses", ylabel="Amount", xlabel="Date")
        plt.xticks(rotation=45)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
