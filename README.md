# Smart Expense Tracker

A modern, user-friendly Python desktop application to track your daily expenses, manage your incomes/salaries, and gain visual insights into your spending habits. Built using Python's Tkinter library, it features a clean graphical user interface and persists your data locally.

## Features

- **Dashboard Insights**: View your total spent, number of transactions, top category, total income, and net savings at a glance.
- **Expense Tracking**: Easily log daily expenses with date, amount, category, and a brief description.
- **Salary Tracking**: Add and manage your income sources (e.g., Salary, Freelance, etc.) via a dedicated Salary tab.
- **Visual Analytics**: Automatically generated pie charts and visualizations to help you understand your spending distribution across different categories.
- **Monthly Filtering**: Select specific months to view relevant expenses, incomes, and charts.
- **Data Persistence**: Data is safely saved locally in simple CSV files (`expenses.csv` and `salary.csv`).
- **Data Management**: View your records in a structured table format and delete entries easily if you make a mistake.

## Project Structure

- `main.py`: The entry point of the application. It builds the layout, tabs, and wires all the components together.
- `data.py`: Handles all data persistence logic. It reads, writes, and deletes records in the CSV files and aggregates monthly summaries.
- `charts.py`: Contains the logic for rendering analytical charts (e.g., spending by category).
- `config.py`: Stores application constants, configuration values, color palettes, and fonts.
- `widgets.py`: Custom UI widgets such as the Calendar popup and View Month picker.
- `expenses.csv` & `salary.csv`: Local databases storing your tracked financial records.

## Requirements

- Python 3.x
- Tkinter (Usually included with standard Python installations)

## Getting Started

1. **Clone or Download** this repository.
2. Ensure you have **Python 3** installed on your system.
3. Open a terminal or command prompt and navigate to the project directory:
   ```bash
   cd expense_tracker_
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage

- **Adding an Expense**: Go to the `+ Expense` tab, pick a date from the popup calendar, enter the amount, choose a category, optionally add a description, and click "Add Expense".
- **Adding Salary**: Go to the `+ Salary` tab, select the pay date, enter the amount, select the income source, add a note, and click "Add Salary".
- **Viewing Records**: Switch between the "Expenses" and "Salary" tabs on the right to see a list of your transactions for the selected month.
- **Visuals**: Click on the "Chart" tab to view a breakdown of your expenses for the month.
- **Deleting a Record**: Select an item from either the Expenses or Salary table and click the "Delete Selected" button at the bottom.
