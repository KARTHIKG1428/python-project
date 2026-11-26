"""
Personal Finance CSV Reporter
Project #20 - LocalImpact Challenge
Run: python app.py
"""
import csv
import json
import os
from datetime import date, datetime
from collections import defaultdict

DATA_DIR = "data"
REPORT_DIR = "reports"
CSV_FILE = os.path.join(DATA_DIR, "transactions.csv")
JSON_FILE = os.path.join(DATA_DIR, "transactions.json")
FIELDS = ["date", "type", "category", "description", "amount"]

def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

def load_transactions():
    ensure_files()
    records = []
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            for row_num, row in enumerate(csv.DictReader(f), start=2):
                try:
                    kind = row["type"].strip().lower()
                    amount = float(row["amount"])
                    datetime.strptime(row["date"], "%Y-%m-%d")
                    if kind not in ("income", "expense") or amount <= 0:
                        raise ValueError("Invalid type or amount")
                    records.append({
                        "date": row["date"], "type": kind,
                        "category": row["category"].strip(),
                        "description": row["description"].strip(),
                        "amount": round(amount, 2)
                    })
                except (ValueError, KeyError) as e:
                    print(f"Skipping invalid CSV row {row_num}: {e}")
    except (OSError, csv.Error) as e:
        print("Could not read CSV:", e)
    return records

def save_transactions(records):
    ensure_files()
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)

def ask_amount(prompt="Amount (₹): "):
    while True:
        raw = input(prompt).strip().replace(",", "")
        try:
            value = float(raw)
            if value <= 0:
                print("Please enter an amount greater than zero.")
                continue
            return round(value, 2)
        except ValueError:
            print("Invalid amount. Enter a number, for example 250 or 1250.50.")

def ask_date():
    while True:
        raw = input("Date (YYYY-MM-DD, blank for today): ").strip()
        if not raw:
            return date.today().isoformat()
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")

def add_transaction(records):
    print("\n--- Add Transaction ---")
    while True:
        kind = input("Type (income/expense): ").strip().lower()
        if kind in ("income", "expense"):
            break
        print("Enter either income or expense.")
    category = input("Category (e.g. Salary, Food, Travel): ").strip()
    while not category:
        print("Category cannot be blank.")
        category = input("Category: ").strip()
    description = input("Description: ").strip() or "No description"
    records.append({
        "date": ask_date(), "type": kind, "category": category,
        "description": description, "amount": ask_amount()
    })
    save_transactions(records)
    print("Transaction saved successfully.")

def import_csv(records):
    path = input("Path to CSV file: ").strip().strip('"')
    if not os.path.isfile(path):
        print("File not found.")
        return
    added, rejected = 0, 0
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            missing = set(FIELDS) - set(reader.fieldnames or [])
            if missing:
                print("CSV is missing columns:", ", ".join(sorted(missing)))
                return
            for row in reader:
                try:
                    kind = row["type"].strip().lower()
                    amount = float(row["amount"])
                    datetime.strptime(row["date"], "%Y-%m-%d")
                    if kind not in ("income", "expense") or amount <= 0:
                        raise ValueError()
                    records.append({
                        "date": row["date"], "type": kind,
                        "category": row["category"].strip(),
                        "description": row["description"].strip(),
                        "amount": round(amount, 2)
                    })
                    added += 1
                except (ValueError, AttributeError, KeyError):
                    rejected += 1
        save_transactions(records)
        print(f"Import complete: {added} added, {rejected} invalid rows skipped.")
    except (OSError, csv.Error) as e:
        print("Import failed:", e)

def show_transactions(records):
    print("\n--- Transactions ---")
    if not records:
        print("No transactions found.")
        return
    print(f"{'DATE':<12} {'TYPE':<9} {'CATEGORY':<16} {'AMOUNT':>12}  DESCRIPTION")
    print("-" * 78)
    for r in sorted(records, key=lambda x: x["date"], reverse=True):
        print(f"{r['date']:<12} {r['type']:<9} {r['category'][:15]:<16} "
              f"{r['amount']:>12,.2f}  {r['description'][:25]}")

def summary(records):
    income = sum(r["amount"] for r in records if r["type"] == "income")
    expenses = sum(r["amount"] for r in records if r["type"] == "expense")
    balance = income - expenses
    print("\n========== FINANCIAL SUMMARY ==========")
    print(f"Total income   : ₹{income:,.2f}")
    print(f"Total expenses : ₹{expenses:,.2f}")
    print(f"Net balance    : ₹{balance:,.2f}")
    print(f"Transactions   : {len(records)}")
    print(f"Average amount : ₹{(sum(r['amount'] for r in records)/len(records)) if records else 0:,.2f}")
    print("Status         :", "Surplus" if balance >= 0 else "Overspending")
    print("=======================================")
    return income, expenses, balance

def search_transactions(records):
    term = input("Search by keyword or category: ").strip().lower()
    found = [r for r in records if term in r["category"].lower()
             or term in r["description"].lower() or term in r["type"].lower()]
    show_transactions(found)

def export_report(records):
    income, expenses, balance = summary(records)
    path = os.path.join(REPORT_DIR, "financial_report.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("PERSONAL FINANCE CSV REPORTER\n")
        f.write("==============================\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M}\n")
        f.write(f"Total income: ₹{income:,.2f}\n")
        f.write(f"Total expenses: ₹{expenses:,.2f}\n")
        f.write(f"Net balance: ₹{balance:,.2f}\n\n")
        for r in records:
            f.write(f"{r['date']} | {r['type']} | {r['category']} | ₹{r['amount']:.2f} | {r['description']}\n")
    print("Report exported to", path)

def create_chart(records):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib is not installed. Run: pip install matplotlib")
        return
    totals = defaultdict(float)
    for r in records:
        if r["type"] == "expense":
            totals[r["category"]] += r["amount"]
    if not totals:
        print("No expense records available to plot.")
        return
    labels, values = list(totals.keys()), list(totals.values())
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    os.makedirs(REPORT_DIR, exist_ok=True)
    output = os.path.join(REPORT_DIR, "expense_chart.png")
    plt.savefig(output, dpi=150)
    plt.show()
    print("Chart saved to", output)

def main():
    ensure_files()
    records = load_transactions()
    print("\n" + "=" * 48)
    print("       PERSONAL FINANCE CSV REPORTER")
    print("=" * 48)
    while True:
        print("\n1. Add transaction")
        print("2. Import transactions from CSV")
        print("3. View all transactions")
        print("4. Financial summary")
        print("5. Search transactions")
        print("6. Export text report")
        print("7. Generate expense chart")
        print("8. Exit")
        choice = input("\nChoose an option (1-8): ").strip()
        if choice == "1": add_transaction(records)
        elif choice == "2": import_csv(records)
        elif choice == "3": show_transactions(records)
        elif choice == "4": summary(records)
        elif choice == "5": search_transactions(records)
        elif choice == "6": export_report(records)
        elif choice == "7": create_chart(records)
        elif choice == "8":
            save_transactions(records)
            print("Your data is saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 to 8.")

if __name__ == "__main__":
    main()
