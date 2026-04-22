# charts.py
# Handles all matplotlib chart rendering inside a tkinter frame

import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import WHITE, CHART_COLORS, MUTED, FONT, FONT_BOLD


def draw_charts(parent_frame, cat_totals):
    """
    Clear parent_frame and draw a pie + bar chart side by side.
    Shows a 'no data' label if cat_totals is empty.
    """
    # Clear previous chart
    for widget in parent_frame.winfo_children():
        widget.destroy()

    if not cat_totals:
        tk.Label(parent_frame, text="No data for this month.",
                 font=FONT, bg=WHITE, fg=MUTED).pack(expand=True)
        return

    labels = list(cat_totals.keys())
    values = list(cat_totals.values())
    colors = CHART_COLORS[:len(labels)]

    fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(9, 4.2), facecolor=WHITE)
    fig.subplots_adjust(left=0.05, right=0.97, top=0.88, bottom=0.12, wspace=0.35)

    # ── Pie chart ─────────────────────────────────────────────────────────────
    wedges, _, autotexts = ax_pie.pie(
        values,
        labels=None,
        autopct=lambda p: f"{p:.1f}%" if p > 5 else "",
        colors=colors,
        startangle=140,
        pctdistance=0.75,
        wedgeprops={"linewidth": 2, "edgecolor": WHITE, "width": 0.6}
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight("bold")

    ax_pie.legend(
        wedges,
        [f"{l}  ₹{v:,.0f}" for l, v in zip(labels, values)],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=2, fontsize=9, frameon=False
    )
    ax_pie.set_title("Category Breakdown", fontsize=12, fontweight="bold", pad=10)

    # ── Bar chart ─────────────────────────────────────────────────────────────
    bars = ax_bar.barh(labels, values, color=colors, edgecolor=WHITE, height=0.6)
    for bar, val in zip(bars, values):
        ax_bar.text(
            val + max(values) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"₹{val:,.0f}",
            va="center", fontsize=9
        )
    ax_bar.set_xlim(0, max(values) * 1.25)
    ax_bar.set_title("Spending by Category", fontsize=12, fontweight="bold", pad=10)
    ax_bar.spines[["top", "right"]].set_visible(False)
    ax_bar.tick_params(labelsize=10)
    ax_bar.grid(axis="x", alpha=0.3)
    ax_bar.set_axisbelow(True)

    # Embed in tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
    plt.close(fig)
