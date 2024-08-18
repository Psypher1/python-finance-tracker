import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime

from data_entry import get_date, get_amount, get_category, get_description


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod  # has access to class but not instance of it
    def initialise_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        # use csv writer
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry created successfully!")

    @classmethod
    def delete_entry(cls, index):
        """Deletes a transaction entry from the CSV file."""
        try:
            df = pd.read_csv(cls.CSV_FILE)
            if df.empty:
                print("Nothing to delete")
                return
            if 0 <= index < len(df):
                df = df.drop(index).reset_index(drop=True)
                df.to_csv(cls.CSV_FILE, index=False)
                print("Entry deleted")
            else:
                print("Invalid index.")
        except FileNotFoundError:
            print("No data to delete")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.DATE_FORMAT)
        start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_date, cls.DATE_FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found")
        else:
            print(
                f"\nTransactions from {start_date.strftime(cls.DATE_FORMAT)} to {end_date.strftime(cls.DATE_FORMAT)}\n"
            )
            print(
                filtered_df.to_string(
                    index=False,
                    formatters={"date": lambda x: x.strftime(cls.DATE_FORMAT)},
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expenses = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()

            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expenses:.2f}")
            print(f"Net Savings: ${(total_income - total_expenses):.2f}")

        return filtered_df


def add():
    CSV.initialise_csv()
    date = get_date(
        "Enter the date of the transaction or ENTER for today: ", allow_default=True
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def delete():
    """Prompts the user to delete an existing transaction."""
    index = int(input("Enter the index of the transaction to delete: "))
    CSV.delete_entry(index)


def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income & Expense")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\nWhat would you like to do?")
        print("1. Add a transaction")
        print("2. View transactions with summary")
        print("3. Delete")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter start date: ")
            end_date = get_date("Enter end date: ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            delete()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()


# CSV.get_transactions("01-01-2024", "30-10-2024")
# add()
# CSV.initialise_csv()
# CSV.add_entry("20-07-2024", 40.00, "Income", "Movement task")
