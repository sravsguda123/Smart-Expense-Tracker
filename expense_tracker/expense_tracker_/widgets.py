# widgets.py
# Reusable popup widgets: CalendarPopup and MonthPopup

import tkinter as tk
import calendar
from datetime import datetime

from config import (WHITE, DARK, BORDER, MUTED, ACCENT,
                    FONT_BOLD, FONT_SMALL)


class CalendarPopup(tk.Toplevel):
    """
    Popup date picker. Opens below anchor_widget.
    Calls on_select(date_str) with format 'YYYY-MM-DD' when a day is clicked.
    """
    def __init__(self, root, anchor_widget, on_select, initial=None):
        super().__init__(root)
        self.on_select = on_select
        self.overrideredirect(True)
        self.configure(bg=BORDER)
        self.grab_set()

        try:
            d = datetime.strptime(initial, "%Y-%m-%d")
        except Exception:
            d = datetime.now()
        self._y, self._m = d.year, d.month

        self._frame = tk.Frame(self, bg=WHITE, padx=2, pady=2)
        self._frame.pack(padx=1, pady=1)
        self._draw()

        # Position below anchor, clamp if near screen bottom
        self.update_idletasks()
        ax = anchor_widget.winfo_rootx()
        ay = anchor_widget.winfo_rooty() + anchor_widget.winfo_height() + 2
        if ay + self.winfo_reqheight() > self.winfo_screenheight() - 40:
            ay = anchor_widget.winfo_rooty() - self.winfo_reqheight() - 2
        self.geometry(f"+{ax}+{ay}")

        self.bind("<FocusOut>", lambda e: self.destroy())
        self.focus_set()

    def _draw(self):
        for w in self._frame.winfo_children():
            w.destroy()

        # Header with month/year and nav arrows
        hdr = tk.Frame(self._frame, bg=DARK)
        hdr.pack(fill="x")
        tk.Button(hdr, text=" ◀ ", bg=DARK, fg=WHITE, bd=0, font=FONT_BOLD,
                  cursor="hand2", activebackground="#333",
                  command=self._prev).pack(side="left")
        tk.Label(hdr, text=datetime(self._y, self._m, 1).strftime("%B %Y"),
                 font=FONT_BOLD, bg=DARK, fg=WHITE,
                 width=16, anchor="center").pack(side="left", expand=True)
        tk.Button(hdr, text=" ▶ ", bg=DARK, fg=WHITE, bd=0, font=FONT_BOLD,
                  cursor="hand2", activebackground="#333",
                  command=self._next).pack(side="right")

        # Day-of-week headers
        dow = tk.Frame(self._frame, bg=WHITE)
        dow.pack(fill="x", padx=6, pady=(6, 2))
        for d in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            tk.Label(dow, text=d, font=FONT_SMALL, bg=WHITE, fg=MUTED,
                     width=4, anchor="center").pack(side="left")

        # Day buttons grid
        body = tk.Frame(self._frame, bg=WHITE)
        body.pack(padx=6, pady=(0, 6))
        today = datetime.now()
        for week in calendar.monthcalendar(self._y, self._m):
            row = tk.Frame(body, bg=WHITE)
            row.pack()
            for day in week:
                if day == 0:
                    tk.Label(row, text="", width=4, bg=WHITE,
                             font=FONT_SMALL).pack(side="left", pady=2)
                else:
                    is_today = (day == today.day and
                                self._m == today.month and
                                self._y == today.year)
                    tk.Button(
                        row, text=str(day), width=4, font=FONT_SMALL,
                        bg=ACCENT if is_today else WHITE,
                        fg=WHITE if is_today else DARK,
                        relief="flat", bd=0, cursor="hand2",
                        activebackground=ACCENT, activeforeground=WHITE,
                        command=lambda d=day: self._pick(d)
                    ).pack(side="left", padx=1, pady=2)

    def _prev(self):
        self._m -= 1
        if self._m == 0:
            self._m, self._y = 12, self._y - 1
        self._draw()

    def _next(self):
        self._m += 1
        if self._m == 13:
            self._m, self._y = 1, self._y + 1
        self._draw()

    def _pick(self, day):
        self.on_select(f"{self._y}-{self._m:02d}-{day:02d}")
        self.destroy()


class MonthPopup(tk.Toplevel):
    """
    Popup month picker. Opens below anchor_widget.
    Calls on_select(month_str) with format 'YYYY-MM' when a month is clicked.
    """
    def __init__(self, root, anchor_widget, on_select, initial=None):
        super().__init__(root)
        self.on_select = on_select
        self.overrideredirect(True)
        self.configure(bg=BORDER)
        self.grab_set()

        try:
            self._y = int(initial.split("-")[0])
        except Exception:
            self._y = datetime.now().year

        self._frame = tk.Frame(self, bg=WHITE, padx=2, pady=2)
        self._frame.pack(padx=1, pady=1)
        self._draw()

        # Position below anchor, clamp if near screen bottom
        self.update_idletasks()
        ax = anchor_widget.winfo_rootx()
        ay = anchor_widget.winfo_rooty() + anchor_widget.winfo_height() + 2
        if ay + self.winfo_reqheight() > self.winfo_screenheight() - 40:
            ay = anchor_widget.winfo_rooty() - self.winfo_reqheight() - 2
        self.geometry(f"+{ax}+{ay}")

        self.bind("<FocusOut>", lambda e: self.destroy())
        self.focus_set()

    def _draw(self):
        for w in self._frame.winfo_children():
            w.destroy()

        # Year nav header
        hdr = tk.Frame(self._frame, bg=DARK)
        hdr.pack(fill="x")
        tk.Button(hdr, text=" ◀ ", bg=DARK, fg=WHITE, bd=0, font=FONT_BOLD,
                  cursor="hand2", activebackground="#333",
                  command=lambda: self._yr(-1)).pack(side="left")
        tk.Label(hdr, text=str(self._y), font=FONT_BOLD, bg=DARK, fg=WHITE,
                 width=10, anchor="center").pack(side="left", expand=True)
        tk.Button(hdr, text=" ▶ ", bg=DARK, fg=WHITE, bd=0, font=FONT_BOLD,
                  cursor="hand2", activebackground="#333",
                  command=lambda: self._yr(1)).pack(side="right")

        # Month grid (4 rows x 3 cols)
        grid = tk.Frame(self._frame, bg=WHITE, padx=10, pady=10)
        grid.pack()
        now = datetime.now()
        names = ["Jan","Feb","Mar","Apr","May","Jun",
                 "Jul","Aug","Sep","Oct","Nov","Dec"]
        for i, name in enumerate(names):
            r, c = divmod(i, 3)
            is_cur = (i + 1 == now.month and self._y == now.year)
            tk.Button(
                grid, text=name, width=7, font=FONT_SMALL,
                bg=ACCENT if is_cur else "#F2F2F2",
                fg=WHITE if is_cur else DARK,
                relief="flat", bd=0, cursor="hand2",
                activebackground=ACCENT, activeforeground=WHITE,
                pady=8,
                command=lambda m=i+1: self._pick(m)
            ).grid(row=r, column=c, padx=4, pady=4)

    def _yr(self, delta):
        self._y += delta
        self._draw()

    def _pick(self, month):
        self.on_select(f"{self._y}-{month:02d}")
        self.destroy()
