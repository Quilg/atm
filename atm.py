import tkinter as tk
import sqlite3
from tkinter import messagebox

conn = sqlite3.connect('accounts.db')
db = conn.cursor()

db.execute("""CREATE TABLE IF NOT EXISTS accounts (
             account_number INTEGER PRIMARY KEY,
             pin INTEGER,
             balance REAL
             )""")

conn.commit()

def check_credentials():
    account_number = int(account_number_entry.get())
    pin = int(pin_entry.get())

    db.execute("SELECT * FROM accounts WHERE account_number = ? AND pin = ?", (account_number, pin))
    account = db.fetchone()

    if not account:
        incorrect_label.config(text="Incorrect account number or PIN.")
        incorrect_label.grid(row=5, column=0)
        return False
    else:
        view_balance_button.grid(row=2, column=0)
        deposit_button.grid(row=2, column=1)
        withdraw_button.grid(row=3, column=0)
        exit_button.grid(row=3, column=1)
        account_number_label.grid_forget()
        account_number_entry.grid_forget()
        pin_label.grid_forget()
        pin_entry.grid_forget()
        login_button.grid_forget()
        incorrect_label.grid_forget()
        
        return True

def view_balance():

    account_number = int(account_number_entry.get())
    db.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    balance = db.fetchone()[0]
    balance_label.config(text="Balance: $%.2f" % balance)
    view_balance_button.grid_forget()
    deposit_button.grid_forget()
    withdraw_button.grid_forget()
    exit_button.grid_forget()
    back_button.grid(row=3, column=0)
    balance_label.grid(row=2, column=0)


def back():
    view_balance_button.grid(row=2, column=0)
    deposit_button.grid(row=2, column=1)
    withdraw_button.grid(row=3, column=0)
    exit_button.grid(row=3, column=1)
    back_button.grid_forget()
    amount_label.grid_forget()
    amount_entry.grid_forget()
    balance_label.grid_forget()

        
def exit():
    reset_ui()
    
def reset_ui():
    account_number_entry.delete(0, 'end')
    pin_entry.delete(0, 'end')
    balance_label.grid_forget()
    deposit_button.grid_forget()
    withdraw_button.grid_forget()
    view_balance_button.grid_forget()
    back_button.grid_forget()
    amount_label.grid_forget()
    amount_entry.delete(0, 'end')
    login_button.grid(row=2, column=1)
    account_number_label.grid(row=0, column=0)
    account_number_entry.grid(row=0, column=1)
    pin_label.grid(row=1, column=0)
    pin_entry.grid(row=1, column=1)
    incorrect_label.grid_forget()
    exit_button.grid_forget()
    
def deposit():
    account_number = int(account_number_entry.get())
    db.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    balance = db.fetchone()[0]
    balance_label.config(text="Balance: $%.2f" % balance)
    view_balance_button.grid_forget()
    deposit_button.grid_forget()
    withdraw_button.grid_forget()
    exit_button.grid_forget()
    back_button.grid(row=3, column=0)
    balance_label.grid(row=2, column=0)
    amount_label.grid(row=4, column=0)
    amount_entry.grid(row=4, column=1)
    submit_button = tk.Button(root, text="Submit", command=lambda: update_balance(account_number, balance, amount_entry.get(), 'deposit', submit_button))
    submit_button.grid(row=5, column=0)
    back_button.grid(row=5, column=1)

def withdraw():
    account_number = int(account_number_entry.get())
    db.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    balance = db.fetchone()[0]
    balance_label.config(text="Balance: $%.2f" % balance)
    view_balance_button.grid_forget()
    deposit_button.grid_forget()
    withdraw_button.grid_forget()
    exit_button.grid_forget()
    back_button.grid(row=3, column=0)
    balance_label.grid(row=2, column=0)
    amount_label.grid(row=4, column=0)
    amount_entry.grid(row=4, column=1)
    submit_button = tk.Button(root, text="Submit", command=lambda: update_balance(account_number, balance, amount_entry.get(), 'withdraw', submit_button))
    submit_button.grid(row=5, column=0)
    back_button.grid(row=5, column=1)

def update_balance(account_number, balance, amount, transaction_type, submit_button):
    if not amount:
        return
    try:
        amount = float(amount)
    except ValueError:
        return
    if transaction_type == 'deposit':
        new_balance = balance + amount
    else:
        if amount > balance:
            messagebox.showerror("Error", "Withdrawal amount exceeds current balance")
            return
        new_balance = balance - amount
    db.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
    conn.commit()
    balance_label.config(text="Balance: $%.2f" % new_balance)
    amount_label.grid_forget()
    amount_entry.grid_forget()
    submit_button.grid_forget()
    back_button.grid(row=3, column=0)


root = tk.Tk()
root.title("Bank ATM")

account_number_label = tk.Label(root, text="Account Number:")
account_number_label.grid(row=0, column=0)
account_number_entry = tk.Entry(root)
account_number_entry.grid(row=0, column=1)

pin_label = tk.Label(root, text="PIN:")
pin_entry = tk.Entry(root, show="*")
pin_entry.grid(row=1, column=1)


login_button = tk.Button(root, text="Login", command=check_credentials)
login_button.grid(row=2, column=1)

balance_label = tk.Label(root, text="")
deposit_button = tk.Button(root, text="Deposit", command=deposit)
withdraw_button = tk.Button(root, text="Withdraw", command=withdraw)
view_balance_button = tk.Button(root, text="View Balance", command=view_balance)


amount_label = tk.Label(root, text="Amount:")
amount_entry = tk.Entry(root)

incorrect_label = tk.Label(root, text="")

exit_button = tk.Button(root, text="Exit", command=exit)
back_button = tk.Button(root, text="Back", command=back)

account_number_label.grid(row=0, column=0)
account_number_entry.grid(row=0, column=1)
pin_label.grid(row=1, column=0)
pin_entry.grid(row=1, column=1)
login_button.grid(row=2, column=1)
incorrect_label.grid(row=3, column=1)

root.mainloop()
