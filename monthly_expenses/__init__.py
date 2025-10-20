"""MonthlyExpenses extension for Fava.

This is a simple example of Fava's extension reports system.
"""

from fava.ext import FavaExtensionBase

try:
    from beancount.query.query import run_query
    from beancount.query.numberify import numberify_results
except ModuleNotFoundError:
    #beancount v3 support
    from beanquery.query import run_query
    from beanquery.numberify import numberify_results

import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class MonthlyExpenses(FavaExtensionBase):  # pragma: no cover
    """Sample Extension Report that just prints out an Portfolio List."""

    report_title = "Monthly Expenses"

    def get_all_report(self):
        return [self.build_report_for_account(account) for account in self.config['accounts']]

    def get_valid_month_number(self):
        account = self.config['account_used_to_get_valid_month']
        print("options", self.ledger.options)
        print("config", self.config)

        entries = self.ledger.all_entries
        opts = self.ledger.options

        cols, rows = run_query(entries, opts,
                               "SELECT year, month, account, COUNT(position)\
                                WHERE account ~ '{}'\
                                GROUP BY year, month, account\
                                ORDER BY year, month, account".format(account))
        cols, rows = numberify_results(cols, rows)
        month_count = {}
        for row in rows:
            month_count[row[0]] = 0
        for row in rows:
            if row[3] > 0:
                month_count[row[0]] = month_count[row[0]] + 1
        return cols, month_count

    def build_report_for_account(self, account):
        print("building report for ", account)
        entries = self.ledger.all_entries
        opts = self.ledger.options
        if "operating_currency" not in opts or len(opts["operating_currency"]) == 0:
            return "", "", "" ,account, "missing operating_currency"
        currency = opts["operating_currency"][0]
        cols, rows = run_query(entries, opts,
                               f"SELECT account, YEAR(date) AS year, convert(sum(position),'{currency}') AS amount\
                                WHERE account ~ '{account}'\
                                GROUP BY account, year ORDER BY account, year")
        cols, rows = numberify_results(cols, rows)

        month_count = self.get_valid_month_number()[1]

        # Converting Result Rows to a Pandas Dataframe
        df = pd.DataFrame(rows, columns=[k[0] for k in cols])
        df['month_count'] = df['year']
        df = df.replace({'month_count': month_count})
        print(df)
        if df.empty:
            return "" ,"" ,"" ,account , "no transaction under this account"
        df[f'amount ({currency})'] = df[f'amount ({currency})'] / df['month_count']
        df = df.drop(columns=['month_count'])
        df.rename(columns={"account": "Account", "year": "Year", f"amount ({currency})": f"Amount ({currency})"}, inplace=True)
        df = df.astype({"Account": str, "Year": int, "Amount ({})".format(currency): np.float64})

        # Pivoting a Table by Year
        df = df.pivot_table(index="Account", columns=['Year']).fillna(0).reset_index()
        # Creating Multi-Level Accounts
        n_levels = df["Account"].str.count(":").max() + 1

        if n_levels == account.count(":") + 1:
            return "", "", "", account, "no finer level under this account"

        cols = ["Account_L{}".format(k) for k in range(n_levels)]
        df[cols] = df["Account"].str.split(':', n=n_levels - 1, expand=True)
        df = df.fillna('').drop(columns="Account", level=0).set_index(cols)

        selected_levels = len(account.split(":")) + 1
        groups_name = ["Account_L{}".format(i) for i in range(selected_levels)]

        # expenses table
        a = df.groupby(groups_name).sum().round(decimals=2).to_html()
        # monthly sum table
        b = df.groupby(groups_name).sum().sum().to_frame().to_html()
        # month count table
        c = pd.DataFrame(month_count.items(), columns=['Year', 'count']).to_html()
        return a, b, c, account, "ok"
