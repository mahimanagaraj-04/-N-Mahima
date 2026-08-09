import csv
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

CSV_FILE = Path("transactions.csv")
FIELDS = ["date", "type", "category", "amount"]

class ExpenseTracker:
    def __init__(self, csv_file=CSV_FILE):
        self.csv_file = Path(csv_file)
        self._ensure_csv()

    def _ensure_csv(self):
        if not self.csv_file.exists():
            self.csv_file.parent.mkdir(parents=True, exist_ok=True)
            with self.csv_file.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()

    def _read_transactions(self):
        self._ensure_csv()
        transactions = []
        with self.csv_file.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row.get("date"):
                    continue
                transactions.append({
                    "date": row["date"],
                    "type": row["type"].lower(),
                    "category": row["category"],
                    "amount": float(row["amount"])
                })
        return transactions

    def add_transaction(self, transaction_date, transaction_type, category, amount):
        try:
            parsed_date = datetime.strptime(transaction_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date must use YYYY-MM-DD format.")

        if transaction_type not in ("income", "expense"):
            raise ValueError("Type must be income or expense.")

        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        with self.csv_file.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writerow({
                "date": parsed_date.isoformat(),
                "type": transaction_type,
                "category": category.strip(),
                "amount": f"{amount:.2f}"
            })

    def display_transactions(self):
        transactions = self._read_transactions()
        if not transactions:
            print("\nNo transactions found.")
            return

        print("\n" + "-" * 75)
        print(f"{'Date':<12}{'Type':<12}{'Category':<20}{'Amount':>12}")
        print("-" * 75)

        for item in transactions:
            print(
                f"{item['date']:<12}"
                f"{item['type']:<12}"
                f"{item['category']:<20}"
                f"₹{item['amount']:>10.2f}"
            )
        print("-" * 75)

    def monthly_summary(self, month=None):
        if month is None:
            month = date.today().strftime("%Y-%m")

        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            raise ValueError("Month must use YYYY-MM format.")

        transactions = [
            t for t in self._read_transactions()
            if t["date"].startswith(month)
        ]

        if not transactions:
            print(f"\nNo transactions found for {month}.")
            return

        income = sum(t["amount"] for t in transactions if t["type"] == "income")
        expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        balance = income - expense

        category_totals = defaultdict(float)
        for t in transactions:
            if t["type"] == "expense":
                category_totals[t["category"]] += t["amount"]

        print("\n" + "=" * 40)
        print(f"       {month} SUMMARY")
        print("=" * 40)
        print(f"Total Income   : ₹{income:,.2f}")
        print(f"Total Expense  : ₹{expense:,.2f}")
        print(f"Balance        : ₹{balance:,.2f}")
        print("\nExpense by Category")
        print("-" * 30)

        for category, amount in sorted(category_totals.items()):
            print(f"{category:<20} ₹{amount:,.2f}")

    def export_csv(self, output_path):
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        transactions = self._read_transactions()

        with output.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            for t in transactions:
                writer.writerow({
                    "date": t["date"],
                    "type": t["type"],
                    "category": t["category"],
                    "amount": f"{t['amount']:.2f}"
                })

    def export_excel(self, output_path):
        import pandas as pd

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        transactions = self._read_transactions()

        df = pd.DataFrame(transactions, columns=FIELDS)
        df.to_excel(output, index=False)

    def generate_charts(self):
        import matplotlib.pyplot as plt
        import pandas as pd

        output_dir = Path("charts")
        output_dir.mkdir(parents=True, exist_ok=True)

        transactions = self._read_transactions()
        if not transactions:
            print("No transactions available for charts.")
            return []

        df = pd.DataFrame(transactions)
        df["date"] = pd.to_datetime(df["date"])

        created = []

        expenses = df[df["type"] == "expense"]
        if not expenses.empty:
            category_data = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)
            plt.figure(figsize=(9, 5))
            category_data.plot(kind="bar")
            plt.title("Expenses by Category")
            plt.xlabel("Category")
            plt.ylabel("Amount")
            plt.xticks(rotation=30, ha="right")
            plt.tight_layout()
            path = output_dir / "expense_by_category.png"
            plt.savefig(path, dpi=150)
            plt.close()
            created.append(str(path))

        df["month"] = df["date"].dt.to_period("M").astype(str)
        monthly = df.pivot_table(
            index="month",
            columns="type",
            values="amount",
            aggfunc="sum",
            fill_value=0
        )

        for column in ("income", "expense"):
            if column not in monthly.columns:
                monthly[column] = 0

        monthly = monthly.sort_index()
        ax = monthly[["income", "expense"]].plot(kind="bar", figsize=(10, 5))
        ax.set_title("Monthly Income vs Expense")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount")
        ax.tick_params(axis="x", rotation=30)
        fig = ax.get_figure()
        fig.tight_layout()
        path = output_dir / "monthly_income_vs_expense.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        created.append(str(path))

        return created
