from datetime import datetime, timedelta

import numpy as np 

from investor import Investor
from transaction import Transaction
from ROICalculator import ROICalculator


class ExampleInvestor(Investor):
    '''

    Simple lending (static) strategy with 0.05% profit daily
    on investments without reinvestment

    '''

    def __init__(self, investment_timestamp, deposit, transactions):
        super().__init__(investment_timestamp, deposit, transactions)

    def lending_assets(self, timestamp):

        if timestamp <= datetime(2020, 4, 1):
            return 100

        elif timestamp <= datetime(2020, 8, 29):
            return 100 + 200

        elif timestamp <= datetime(2020, 9, 1):
            return 100 + 200 - 100

        elif timestamp <= datetime(2020, 10, 5):
            return 100 + 200 - 100 + 150

        else:
            return 100 + 200 - 100 + 200 - 120

    def get_nav_by_timestamp(self, timestamp):
        '''

        NAV = investments + PnL
        daily PnL = 0.0005 * investments =>
        total PnL = 0.0005 * sum(invesmetns_i * period_i)

        '''
        date = datetime(2020, 1, 1)
        pnl = 0
        for i in range(timestamp.day - date.day):
            pnl += self.coef[date.date()] * self.lending_assets(date)
            date += timedelta(days=1)

        return self.lending_assets(timestamp) + pnl

### Backtest 1 ###
# generate return per date in range 0.01% - 1%

coef = {}
date = datetime(2020, 1, 1)
coefs = np.random.random_sample((365,)) / 100
for i in range(365):
    coef[date.date()] = coefs[i]
    date += timedelta(days=1)

# create transactions
transaction1 = Transaction(datetime(2020, 4, 1), funding=200)
transaction2 = Transaction(datetime(2020, 8, 29), funding=-100)
transaction3 = Transaction(datetime(2020, 9, 1), funding=150)
transaction4 = Transaction(datetime(2020, 10, 5), funding=-120)

transactions = [transaction1, transaction2, transaction3, transaction4]

investor = ExampleInvestor(investment_timestamp=datetime(2020, 1, 1),
                           deposit=100, transactions=transactions)
investor.coef = coef

# create pie
pie = ROICalculator(investor)


# initial investment time
t_0 = pie.investor.investment_timestamp

#
# before transaction
#

for i in range(1, 12):
    t_1 = datetime(2020, i+1, 1) - timedelta(hours=1)
    print(pie.investor.get_nav_by_timestamp(t_1))
    return_day_1 = pie.get_share_price_perfomance(t=t_1,
                                                  t0=t_1 - timedelta(days=1))
    print(f'1D return on {t_1.date()} = {return_day_1 * 100:.2f} %')

    return_mtd_1 = pie.get_share_price_perfomance(t=t_1,
                                                  t0=t_1.replace(day=1))
    print(f'MTD return on {t_1.date()} = {return_mtd_1 * 100:.2f} %')

    return_ytd_1 = pie.get_share_price_perfomance(t=t_1, t0=t_0)
    print(f'YTD return on {t_1.date()} = {return_ytd_1 * 100:.2f} %\n')
