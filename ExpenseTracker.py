import argparse
import json
import os
import datetime
import re

from tabulate import tabulate


EXPENSE_FILE = "expenses.json"

def load_data():
    if not os.path.exists(EXPENSE_FILE):
        return []
    with open(EXPENSE_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_data(expenses):
    with open(EXPENSE_FILE, "w") as file:
        json.dump(expenses,file, indent=4)

def add_expense(description, amount):
    #load expenses
    expenses = load_data()

    #create new id
    last_id = expenses[-1]['id'] if expenses else 0
    new_id = last_id + 1

    date = datetime.datetime.now().strftime("%d/%m/%Y")

    #add new expense
    new_expense = {
        "id" : new_id,
        "date" : date,
        "description" : description,
        "amount" : amount
    }

    expenses.append(new_expense)
    save_data(expenses)

    print(f"Expense added successfully (ID: {new_id})")

def delete_expense(expense_id):
    expenses = load_data()
    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
    save_data(expenses)
    print(f"expense deleted successfully")

def view_expenses():
    expenses = load_data()
    print(tabulate(expenses, headers="keys"))

def total_expense():
    expenses = load_data()
    sum = 0
    for expense in expenses:
        sum += expense["amount"]
    print(f" Total expenses: {sum}")

def view_month_expense():
    expenses = load_data()
    sum = 0
    for expense in expenses:
        if expense["date"] == re.search("^/../$", expense["date"]):
            sum += expense["amount"]
    print(f" Total expenses: {sum}")

def args():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add subcommand
    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("--description", type=str, required=True)
    add_parser.add_argument("--amount", type=float, required=True)

    # Delete subcommand
    del_parser = subparsers.add_parser("delete", help="Delete an expense")
    del_parser.add_argument("--id", type=int, required=True)

    #view expenses
    subparsers.add_parser("list", help="list expenses")

    #view expense summary
    expenses = subparsers.add_parser("summary", help='summarize expenses')
    expenses.add_argument("--month", type=str, help="month of expense")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "list":
        view_expenses()
    elif args.command == "summary":
        total_expense()

if __name__ == "__main__":
    args()


