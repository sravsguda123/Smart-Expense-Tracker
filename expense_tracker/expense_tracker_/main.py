# main.py
# Entry point — builds the UI and wires everything together

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from config import (BG, WHITE, DARK, MUTED, ACCENT, GREEN, RED, BORDER,
                    CATEGORIES, INCOME_SOURCES, CURRENCY,
                    FONT, FONT_BOLD, FONT_H1, FONT_H2, FONT_SMALL)
from data    import (load_expenses, save_expense, delete_expense_by_index,
                     get_monthly_summary,
                     load_salaries, save_salary, delete_salary_by_index,
                     get_monthly_salary)
from charts  import draw_charts
from widgets import CalendarPopup, MonthPopup


class ExpenseTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("1100x750")
        self.configure(bg=BG)
        self.resizable(True, True)

        self._filter_month = tk.StringVar(value=datetime.now().strftime("%Y-%m"))
        self._date_var     = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        self._build()
        self._refresh()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build(self):
        # Style notebook and treeview globally
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", font=FONT_BOLD, padding=[16, 8],
                        background=BORDER, foreground=MUTED)
        style.map("TNotebook.Tab",
                  background=[("selected", DARK)],
                  foreground=[("selected", WHITE)])
        style.configure("Treeview", rowheight=36, font=FONT,
                        background=WHITE, fieldbackground=WHITE, foreground=DARK)
        style.configure("Treeview.Heading", font=FONT_BOLD,
                        background=BORDER, foreground=DARK, relief="flat")
        style.map("Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", WHITE)])

        # Header bar
        hdr = tk.Frame(self, bg=DARK, pady=18)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Expense Tracker", font=FONT_H1,
                 bg=DARK, fg=WHITE).pack(side="left", padx=28)
        tk.Label(hdr, text="Track · Analyse · Save", font=FONT_SMALL,
                 bg=DARK, fg=MUTED).pack(side="left", padx=4)

        # Body: left form | right panel
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=16)

        left = tk.Frame(body, bg=BG, width=350)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.pack_propagate(False)

        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        self._build_form(left)
        self._build_right(right)

    # ── Left: Add Expense form + Salary form + View Month picker ──────────────
    def _build_form(self, parent):
        # ── View Month card ───────────────────────────────────────────────
        mcard = tk.Frame(parent, bg=WHITE, highlightthickness=1,
                         highlightbackground=BORDER)
        mcard.pack(fill="x", pady=(0, 12), ipady=4)
        mpad = tk.Frame(mcard, bg=WHITE)
        mpad.pack(fill="x", padx=20, pady=16)

        tk.Label(mpad, text="View Month", font=FONT_H2,
                 bg=WHITE, fg=DARK).pack(anchor="w", pady=(0, 8))
        self._month_btn = tk.Button(
            mpad, textvariable=self._filter_month,
            font=FONT, bg="#F2F2F2", fg=DARK,
            relief="solid", bd=1, anchor="w", padx=10, pady=7,
            cursor="hand2", activebackground="#E8E8E8",
            command=self._open_month
        )
        self._month_btn.pack(fill="x")

        # ── Input Forms Notebook ──────────────────────────────────────────
        self._input_nb = ttk.Notebook(parent)
        self._input_nb.pack(fill="both", expand=True)

        tab_exp = tk.Frame(self._input_nb, bg=BG)
        tab_sal = tk.Frame(self._input_nb, bg=BG)
        
        self._input_nb.add(tab_exp, text="  + Expense  ")
        self._input_nb.add(tab_sal, text="  + Salary  ")

        # ── Add Expense card ──────────────────────────────────────────────
        card = tk.Frame(tab_exp, bg=WHITE, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(fill="x", pady=(12, 0), ipady=4)
        pad = tk.Frame(card, bg=WHITE)
        pad.pack(fill="x", padx=20, pady=16)

        # Date — calendar button
        tk.Label(pad, text="Date", font=FONT_SMALL, bg=WHITE, fg=MUTED).pack(anchor="w")
        self._date_btn = tk.Button(
            pad, textvariable=self._date_var,
            font=FONT, bg="#F2F2F2", fg=DARK,
            relief="solid", bd=1, anchor="w", padx=10, pady=7,
            cursor="hand2", activebackground="#E8E8E8",
            command=self._open_cal
        )
        self._date_btn.pack(fill="x", pady=(3, 10))

        # Amount
        tk.Label(pad, text=f"Amount ({CURRENCY})", font=FONT_SMALL, bg=WHITE, fg=MUTED).pack(anchor="w")
        self._amt_var = tk.StringVar()
        tk.Entry(pad, textvariable=self._amt_var, font=FONT,
                 bg="#F2F2F2", relief="solid", bd=1).pack(fill="x", pady=(3, 10))

        # Category
        tk.Label(pad, text="Category", font=FONT_SMALL, bg=WHITE, fg=MUTED).pack(anchor="w")
        self._cat_var = tk.StringVar(value=CATEGORIES[0])
        ttk.Combobox(pad, textvariable=self._cat_var, values=CATEGORIES,
                     state="readonly", font=FONT).pack(fill="x", pady=(3, 10))

        # Description
        tk.Label(pad, text="Description", font=FONT_SMALL, bg=WHITE, fg=MUTED).pack(anchor="w")
        self._desc_var = tk.StringVar()
        tk.Entry(pad, textvariable=self._desc_var, font=FONT,
                 bg="#F2F2F2", relief="solid", bd=1).pack(fill="x", pady=(3, 10))

        # Submit button
        tk.Button(pad, text="Add Expense", font=FONT_BOLD,
                  bg=ACCENT, fg=WHITE, relief="flat", pady=10,
                  cursor="hand2", activebackground="#e55a26",
                  command=self._add).pack(fill="x", pady=(4, 0))

        self._status_lbl = tk.Label(pad, text="", font=FONT_SMALL, bg=WHITE, fg=GREEN)
        self._status_lbl.pack(pady=(6, 0))

        # ── Add Salary card ───────────────────────────────────────────────
        sal_card = tk.Frame(tab_sal, bg=WHITE, highlightthickness=1,
                            highlightbackground=BORDER)
        sal_card.pack(fill="x", pady=(12, 0), ipady=4)
        sal_pad = tk.Frame(sal_card, bg=WHITE)
        sal_pad.pack(fill="x", padx=20, pady=16)

        # Salary date
        tk.Label(sal_pad, text="Pay Date", font=FONT_SMALL, bg=WHITE, fg=MUTED).pack(anchor="w")
        self._sal_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self._sal_date_btn = tk.Button(
            sal_pad, textvariable=self._sal_date_var,
            font=FONT, bg="#F2F2F2", fg=DARK,
            relief="solid", bd=1, anchor="w", padx=10, pady=7,
            cursor="hand2", activebackground="#E8E8E8",
            command=self._open_sal_cal
        )
        self._sal_date_btn.pack(fill="x", pady=(3, 10))

        # Salary amount
        tk.Label(sal_pad, text=f"Amount ({CURRENCY})", font=FONT_SMALL, bg=WHITE, fg=MUTED).pack(anchor="w")
        self._sal_amt_var = tk.StringVar()
        tk.Entry(sal_pad, textvariable=self._sal_amt_var, font=FONT,
                 bg="#F2F2F2", relief="solid", bd=1).pack(fill="x", pady=(3, 10))

        # Source
        tk.Label(sal_pad, text="Source", font=FONT_SMALL, bg=WHITE, fg=MUTED).pack(anchor="w")
        self._sal_src_var = tk.StringVar(value=INCOME_SOURCES[0])
        ttk.Combobox(sal_pad, textvariable=self._sal_src_var, values=INCOME_SOURCES,
                     state="readonly", font=FONT).pack(fill="x", pady=(3, 10))

        # Note
        tk.Label(sal_pad, text="Note", font=FONT_SMALL, bg=WHITE, fg=MUTED).pack(anchor="w")
        self._sal_note_var = tk.StringVar()
        tk.Entry(sal_pad, textvariable=self._sal_note_var, font=FONT,
                 bg="#F2F2F2", relief="solid", bd=1).pack(fill="x", pady=(3, 10))

        # Submit salary button
        tk.Button(sal_pad, text="Add Salary", font=FONT_BOLD,
                  bg="#34C759", fg=WHITE, relief="flat", pady=10,
                  cursor="hand2", activebackground="#2da648",
                  command=self._add_salary).pack(fill="x", pady=(4, 0))

        self._sal_status_lbl = tk.Label(sal_pad, text="", font=FONT_SMALL, bg=WHITE, fg=GREEN)
        self._sal_status_lbl.pack(pady=(6, 0))

    # ── Right: stat cards + tabbed Expenses/Salary/Chart ──────────────────────
    def _build_right(self, parent):
        # Stat cards row
        self._stat_bar = tk.Frame(parent, bg=BG)
        self._stat_bar.pack(fill="x", pady=(0, 12))

        nb = ttk.Notebook(parent)
        nb.pack(fill="both", expand=True)

        self._tab_exp     = tk.Frame(nb, bg=WHITE)
        self._tab_salary  = tk.Frame(nb, bg=WHITE)
        self._tab_chart   = tk.Frame(nb, bg=WHITE)
        nb.add(self._tab_exp,    text="  Expenses  ")
        nb.add(self._tab_salary, text="  💵 Salary  ")
        nb.add(self._tab_chart,  text="  Chart  ")

        self._build_table(self._tab_exp)
        self._build_salary_table(self._tab_salary)

        # Chart frame (draw_charts from charts.py renders into this)
        self._chart_frame = tk.Frame(self._tab_chart, bg=WHITE)
        self._chart_frame.pack(fill="both", expand=True)

    def _build_table(self, parent):
        cols = ("Date", "Category", "Amount", "Description")
        f = tk.Frame(parent, bg=WHITE)
        f.pack(fill="both", expand=True, padx=2, pady=2)

        self._tree = ttk.Treeview(f, columns=cols, show="headings", selectmode="browse")
        for col, w in zip(cols, [120, 140, 110, 300]):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, minwidth=60, anchor="w")

        sb = ttk.Scrollbar(f, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._tree.pack(fill="both", expand=True)
        self._tree.tag_configure("odd", background="#FAFAFA")

        tk.Button(parent, text="Delete Selected", font=FONT_SMALL,
                  bg=RED, fg=WHITE, relief="flat", pady=6, padx=12,
                  cursor="hand2", command=self._delete).pack(pady=8)

    def _build_salary_table(self, parent):
        """Build the salary/income history treeview tab."""
        cols = ("Date", "Source", "Amount", "Note")
        f = tk.Frame(parent, bg=WHITE)
        f.pack(fill="both", expand=True, padx=2, pady=2)

        self._sal_tree = ttk.Treeview(f, columns=cols, show="headings", selectmode="browse")
        for col, w in zip(cols, [120, 160, 120, 300]):
            self._sal_tree.heading(col, text=col)
            self._sal_tree.column(col, width=w, minwidth=60, anchor="w")

        sb = ttk.Scrollbar(f, orient="vertical", command=self._sal_tree.yview)
        self._sal_tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._sal_tree.pack(fill="both", expand=True)
        self._sal_tree.tag_configure("odd", background="#F0FFF0")

        # Summary label at bottom
        self._sal_summary = tk.Label(parent, text="", font=FONT_SMALL,
                                     bg=WHITE, fg=GREEN)
        self._sal_summary.pack(pady=(4, 0))

        tk.Button(parent, text="Delete Selected", font=FONT_SMALL,
                  bg=RED, fg=WHITE, relief="flat", pady=6, padx=12,
                  cursor="hand2", command=self._delete_salary).pack(pady=8)

    # ── Popup openers ─────────────────────────────────────────────────────────
    def _open_cal(self):
        CalendarPopup(
            self, self._date_btn,
            on_select=lambda d: self._date_var.set(d),
            initial=self._date_var.get()
        )

    def _open_sal_cal(self):
        CalendarPopup(
            self, self._sal_date_btn,
            on_select=lambda d: self._sal_date_var.set(d),
            initial=self._sal_date_var.get()
        )

    def _open_month(self):
        def on_pick(ym):
            self._filter_month.set(ym)
            self._refresh()
        MonthPopup(
            self, self._month_btn,
            on_select=on_pick,
            initial=self._filter_month.get()
        )

    # ── Stat cards ────────────────────────────────────────────────────────────
    def _draw_stats(self, total, count, top, income, savings):
        for w in self._stat_bar.winfo_children():
            w.destroy()
        sav_color = GREEN if savings >= 0 else RED
        for label, val, color in [
            ("Total Spent",   f"{CURRENCY}{total:,.2f}",   ACCENT),
            ("Transactions",  str(count),                  DARK),
            ("Top Category",  top,                         GREEN),
            ("💵 Income",     f"{CURRENCY}{income:,.2f}",  "#007AFF"),
            ("🏦 Savings",    f"{CURRENCY}{savings:,.2f}", sav_color),
        ]:
            c = tk.Frame(self._stat_bar, bg=WHITE, highlightthickness=1,
                         highlightbackground=BORDER, padx=18, pady=14)
            c.pack(side="left", expand=True, fill="both", padx=(0, 10))
            tk.Label(c, text=label, font=FONT_SMALL, bg=WHITE, fg=MUTED).pack(anchor="w")
            tk.Label(c, text=val, font=("Georgia", 16, "bold"),
                     bg=WHITE, fg=color).pack(anchor="w")

    # ── Refresh: reload data → update stats, table, chart ─────────────────────
    def _refresh(self):
        try:
            y, m = map(int, self._filter_month.get().split("-"))
        except Exception:
            messagebox.showerror("Error", "Invalid month format"); return

        data = get_monthly_summary(y, m)
        sal_data = get_monthly_salary(y, m)

        income  = sal_data["total"]
        savings = income - data["total"]

        self._draw_stats(data["total"], data["count"], data["top"], income, savings)

        # Refresh expense table
        for row in self._tree.get_children():
            self._tree.delete(row)
        for i, r in enumerate(reversed(data["rows"])):
            self._tree.insert("", "end", values=(
                r["date"], r["category"],
                f"{CURRENCY}{float(r['amount']):,.2f}", r["description"]
            ), tags=("odd" if i % 2 else "",))

        # Refresh salary table
        for row in self._sal_tree.get_children():
            self._sal_tree.delete(row)
        for i, r in enumerate(reversed(sal_data["rows"])):
            self._sal_tree.insert("", "end", values=(
                r["date"], r["source"],
                f"{CURRENCY}{float(r['amount']):,.2f}", r.get("note", "")
            ), tags=("odd" if i % 2 else "",))
        self._sal_summary.configure(
            text=f"{sal_data['count']} record(s)  •  Total Income: {CURRENCY}{sal_data['total']:,.2f}"
        )

        draw_charts(self._chart_frame, data["cat_totals"])

    # ── Add expense ───────────────────────────────────────────────────────────
    def _add(self):
        date = self._date_var.get().strip()
        amt  = self._amt_var.get().strip()
        cat  = self._cat_var.get()
        desc = self._desc_var.get().strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            self._set_status(self._status_lbl, "✗ Invalid date", RED); return

        try:
            amount = float(amt)
            assert amount > 0
        except Exception:
            self._set_status(self._status_lbl, "✗ Enter a valid amount", RED); return

        save_expense(date, cat, amount, desc)
        self._amt_var.set("")
        self._desc_var.set("")
        self._set_status(self._status_lbl, f"✓ Added {CURRENCY}{amount:,.2f} in {cat}", GREEN)
        self._refresh()

    # ── Add salary ────────────────────────────────────────────────────────────
    def _add_salary(self):
        date   = self._sal_date_var.get().strip()
        amt    = self._sal_amt_var.get().strip()
        source = self._sal_src_var.get()
        note   = self._sal_note_var.get().strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            self._set_status(self._sal_status_lbl, "✗ Invalid date", RED); return

        try:
            amount = float(amt)
            assert amount > 0
        except Exception:
            self._set_status(self._sal_status_lbl, "✗ Enter a valid amount", RED); return

        save_salary(date, source, amount, note)
        self._sal_amt_var.set("")
        self._sal_note_var.set("")
        self._set_status(self._sal_status_lbl, f"✓ Added {CURRENCY}{amount:,.2f} — {source}", GREEN)
        self._refresh()

    # ── Delete selected expense ───────────────────────────────────────────────
    def _delete(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a row to delete."); return
        if not messagebox.askyesno("Delete", "Delete this expense?"): return

        vals = self._tree.item(sel[0])["values"]
        for i, r in enumerate(load_expenses()):
            if (r["date"] == vals[0] and r["category"] == vals[1] and
                    abs(float(r["amount"]) - float(
                        str(vals[2]).replace("₹", "").replace(",", ""))) < 0.01):
                delete_expense_by_index(i)
                break
        self._refresh()

    # ── Delete selected salary ────────────────────────────────────────────────
    def _delete_salary(self):
        sel = self._sal_tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a salary record to delete."); return
        if not messagebox.askyesno("Delete", "Delete this salary record?"): return

        vals = self._sal_tree.item(sel[0])["values"]
        for i, r in enumerate(load_salaries()):
            if (r["date"] == vals[0] and r["source"] == vals[1] and
                    abs(float(r["amount"]) - float(
                        str(vals[2]).replace("₹", "").replace(",", ""))) < 0.01):
                delete_salary_by_index(i)
                break
        self._refresh()

    def _set_status(self, label, msg, color):
        label.configure(text=msg, fg=color)
        self.after(3000, lambda: label.configure(text=""))


if __name__ == "__main__":
    ExpenseTracker().mainloop()
