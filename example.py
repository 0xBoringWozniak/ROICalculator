from datetime import datetime, timedelta

from investor import Investor
from transaction import Transaction
from SharePricePerfomanceCalculator import SharePricePerfomanceCalculator


class ExampleInvestor(Investor):
    '''

    Simple static strategy with 0.5% profit daily
    on investments without reinvestment

    '''

    def __init__(self, investment_timestamp, deposit, transactions):
        super().__init__(investment_timestamp, deposit, transactions)

    def lending_assets(self, timestamp):
        if timestamp <= datetime(2020, 4, 1):
            return 100
        else:
            return 300

    def get_nav_by_timestamp(self, timestamp):
        if timestamp < datetime(2020, 4, 1):
            pnl = 0.0005 * self.lending_assets(timestamp) * (timestamp - self.investment_timestamp).days
            return self.lending_assets(timestamp) + pnl

        elif timestamp > datetime(2020, 4, 1):
            transaction_timestamp = datetime(2020, 4, 1)
            acc_pnl_before_transaction = 0.0005 * self.lending_assets(transaction_timestamp) * (transaction_timestamp - self.investment_timestamp).days
            pnl =  0.0005 * self.lending_assets(timestamp) * (timestamp - transaction_timestamp).days +\
                   acc_pnl_before_transaction

            return self.lending_assets(timestamp) + pnl

# Example.
# initial investment = 100K$
# deposit on strategy 200K$ at 2020/4/1

transaction = Transaction(datetime(2020, 4, 1), funding=200)
investor = ExampleInvestor(investment_timestamp=datetime(2020, 1, 1),
                        deposit=100, transactions=[transaction])

pie = SharePricePerfomanceCalculator(investor)

# before transaction
t_1 = datetime(2020, 3, 31)
t_0 = pie.investor.investment_timestamp
return_ytd_1 = pie.get_share_price_perfomance(t=t_1, t0=t_0)
print(f'YTD on {t_1.date()} = {return_ytd_1 * 100:.2f} %')
return_mtd_1 = pie.get_share_price_perfomance(t=t_1,
                                              t0=t_1.replace(day=1) - timedelta(hours=1))
print(f'MTD on {t_1.date()} = {return_mtd_1 * 100:.2f} %')

# after transaction
t_2 = datetime(2020, 4, 30)
return_ytd_2 = pie.get_share_price_perfomance(t=t_2, t0=t_0)
print(f'YTD on {t_2.date()} = {return_ytd_2 * 100:.2f} %')

return_mtd_2 = pie.get_share_price_perfomance(t=t_2,
                                              t0=t_2.replace(day=1) - timedelta(hours=1))
print(f'MTD on {t_2.date()} = {return_mtd_2 * 100:.2f} %')
