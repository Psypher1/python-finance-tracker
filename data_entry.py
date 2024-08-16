import pandas as pd
import csv
from datetime import datetime


class CSV:
    CSV_FILE = "finance_data.csv"

    @classmethod  # has access to class but not instance of it
    def initialise_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except:
            df = pd.DataFrame(columns=["date", "amount", "category", "description"])
            df.to_csv(cls.CSV_FILE, index=False)
