import pandas as pd
import csv
from datetime import datetime

from data_entry import get_date, get_amount, get_category, get_description


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

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


def add():
    CSV.initialise_csv()
    date = get_date(
        "Enter the date of the transaction or ENTER for today: ", allow_default=True
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


add()
# CSV.initialise_csv()
# CSV.add_entry("20-07-2024", 40.00, "Income", "Movement task")
