# config.py
# All constants: colors, fonts, categories

# ── Data ──────────────────────────────────────────────────────────────────────
CSV_FILE          = "expenses.csv"
SALARY_CSV        = "salary.csv"
CATEGORIES        = ["Food","Travel","Bills","Shopping","Health","Education","Entertainment","Other"]
FIELDNAMES        = ["date","category","amount","description"]
SALARY_FIELDNAMES = ["date","source","amount","note"]
INCOME_SOURCES    = ["Monthly Salary","Freelance","Bonus","Investment Returns",
                     "Rental Income","Part-time Job","Gift","Other"]
CURRENCY          = "₹"

# ── Colors ────────────────────────────────────────────────────────────────────
BG     = "#F7F5F0"
WHITE  = "#FFFFFF"
DARK   = "#1C1C1E"
MUTED  = "#8E8E93"
ACCENT = "#FF6B35"
GREEN  = "#34C759"
RED    = "#FF3B30"
BORDER = "#E5E5EA"
CHART_COLORS = ["#FF6B35","#FFB347","#4ECDC4","#45B7D1","#96CEB4","#DDA0DD","#F7DC6F","#82E0AA"]

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT       = ("Georgia", 14)
FONT_BOLD  = ("Georgia", 14, "bold")
FONT_H1    = ("Georgia", 28, "bold")
FONT_H2    = ("Georgia", 18, "bold")
FONT_SMALL = ("Georgia", 13)
