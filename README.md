# Personal Finance Manager 💰

A Python-based CLI (Command Line Interface) application designed to help users track their income and expenses, visualize spending habits, and manage monthly budgets effectively.

This project demonstrates core Computer Science concepts including **File Handling (CSV)**, **Data Visualization (Matplotlib)**, and **User Authentication**.

## 🚀 Features

* **User System:** Secure Registration and Login functionality (Multi-user support).
* **Transaction Tracking:** Add income and expense entries with categories and descriptions.
* **Data Persistence:** Uses CSV files to store user credentials and financial data locally.
* **Visual Analytics:**
    * 📊 **Monthly Expenses:** Bar chart visualization.
    * 🥧 **Category Breakdown:** Pie chart visualization.
* **Budget Management:** Set monthly budgets and receive alerts (via Tkinter popups) when limits are exceeded.
* **Search & Export:** Search transactions by date range and export data to external CSV files.
* **Log System:** Tracks all changes and activities in a `change_log.txt` file for auditing.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Libraries:**
    * `matplotlib` (For generating graphs)
    * `tkinter` (For GUI alerts and message boxes)
    * `csv` (For data storage and retrieval)
    * `datetime` (For timestamping entries)

## 📂 Project Structure

```text
├── finance_manager.py   # Main application script
├── requirements.txt     # List of dependencies
├── users.csv            # Stores user credentials (auto-generated)
├── change_log.txt       # System activity log (auto-generated)
└── README.md            # Project documentation
