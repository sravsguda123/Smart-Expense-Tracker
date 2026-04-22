# data.py
# Handles all CSV storage and monthly analytics

import csv
import os
from collections import defaultdict
from config import CSV_FILE, FIELDNAMES, SALARY_CSV, SALARY_FIELDNAMES


# ══════════════════════════════════════════════════════════════════════════════
#  EXPENSE DATA
# ══════════════════════════════════════════════════════════════════════════════

def init_csv():
    """Create CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()


def load_expenses():
    """Return all expenses as a list of dicts."""
    init_csv()
    with open(CSV_FILE, newline="") as f:
        return list(csv.DictReader(f))


def save_expense(date, category, amount, description):
    """Append a single expense row to the CSV."""
    init_csv()
    with open(CSV_FILE, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow({
            "date": date,
            "category": category,
            "amount": amount,
            "description": description
        })


def delete_expense_by_index(index):
    """Delete the expense at the given list index and rewrite the CSV."""
    rows = load_expenses()
    rows.pop(index)
    with open(CSV_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(rows)


def get_monthly_summary(year, month):
    """
    Return a summary dict for the given year/month:
      - rows       : list of matching expense dicts
      - total      : total amount spent
      - cat_totals : dict of category -> total
      - top        : highest spending category
      - count      : number of transactions
    """
    key  = f"{year}-{month:02d}"
    rows = [r for r in load_expenses() if r["date"].startswith(key)]

    total      = sum(float(r["amount"]) for r in rows)
    cat_totals = defaultdict(float)
    for r in rows:
        cat_totals[r["category"]] += float(r["amount"])

    top = max(cat_totals, key=cat_totals.get) if cat_totals else "—"

    return {
        "rows":       rows,
        "total":      total,
        "cat_totals": dict(cat_totals),
        "top":        top,
        "count":      len(rows)
    }


# ══════════════════════════════════════════════════════════════════════════════
#  SALARY / INCOME DATA
# ══════════════════════════════════════════════════════════════════════════════

def _init_salary_csv():
    """Create salary CSV with headers if it doesn't exist."""
    if not os.path.exists(SALARY_CSV):
        with open(SALARY_CSV, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=SALARY_FIELDNAMES).writeheader()


def load_salaries():
    """Return all salary records as a list of dicts."""
    _init_salary_csv()
    with open(SALARY_CSV, newline="") as f:
        return list(csv.DictReader(f))


def save_salary(date, source, amount, note=""):
    """Append a single salary/income row to the CSV."""
    _init_salary_csv()
    with open(SALARY_CSV, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=SALARY_FIELDNAMES).writerow({
            "date": date,
            "source": source,
            "amount": amount,
            "note": note
        })


def delete_salary_by_index(index):
    """Delete the salary record at the given list index and rewrite the CSV."""
    rows = load_salaries()
    rows.pop(index)
    with open(SALARY_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SALARY_FIELDNAMES)
        w.writeheader()
        w.writerows(rows)


def get_monthly_salary(year, month):
    """
    Return a summary dict for salary/income for the given year/month:
      - rows          : list of matching salary dicts
      - total         : total income for the month
      - source_totals : dict of source -> total
      - count         : number of income entries
    """
    key  = f"{year}-{month:02d}"
    rows = [r for r in load_salaries() if r["date"].startswith(key)]

    total = sum(float(r["amount"]) for r in rows)
    source_totals = defaultdict(float)
    for r in rows:
        source_totals[r["source"]] += float(r["amount"])

    return {
        "rows":          rows,
        "total":         total,
        "source_totals": dict(source_totals),
        "count":         len(rows)
    }
