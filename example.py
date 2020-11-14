from datetime import datetime, timedelta

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
        # before transaction
        if timestamp <= datetime(2020, 4, 1):
            return 100
        # after transaction
        else:
            return 300

    def get_nav_by_timestamp(self, timestamp):
        '''

        NAV = investments + PnL
        daily PnL = 0.0005 * investments =>
        total PnL = 0.0005 * sum(invesmetns_i * period_i)

        '''
        if timestamp < datetime(2020, 4, 1):
            pnl = 0.0005 * \
                self.lending_assets(timestamp) * \
                (timestamp - self.investment_timestamp).days
            return self.lending_assets(timestamp) + pnl

        elif timestamp > datetime(2020, 4, 1):
            # redefine investments_i and daily PnL
            transaction_timestamp = datetime(2020, 4, 1)
            acc_pnl_before_transaction = 0.0005 * self.lending_assets(
                transaction_timestamp) * (transaction_timestamp - self.investment_timestamp).days
            pnl =  0.0005 * self.lending_assets(timestamp) * (timestamp - transaction_timestamp).days +\
                acc_pnl_before_transaction

            return self.lending_assets(timestamp) + pnl

# # # Example.
# initial investment = 100$
# deposit on strategy 200$ at 2020/4/1
# daily pnl = 0.5%

transaction = Transaction(datetime(2020, 4, 1), funding=200)
investor = ExampleInvestor(investment_timestamp=datetime(2020, 1, 1),
                           deposit=100, transactions=[transaction])

# create pif
pif = ROICalculator(investor)

# initial investment time
t_0 = pif.investor.investment_timestamp

#
# before transaction
#

t_1 = datetime(2020, 3, 31)
return_day_1 = pif.get_share_price_perfomance(t=t_1,
                                              t0=t_1 - timedelta(days=1))
print(f'1D return on {t_1.date()} = {return_day_1 * 100:.2f} %')

return_mtd_1 = pif.get_share_price_perfomance(t=t_1,
                                              t0=t_1.replace(day=1) - timedelta(hours=1))
print(f'MTD return on {t_1.date()} = {return_mtd_1 * 100:.2f} %')

return_ytd_1 = pif.get_share_price_perfomance(t=t_1, t0=t_0)
print(f'YTD return on {t_1.date()} = {return_ytd_1 * 100:.2f} %\n')

#
# after transaction
#

t_2 = datetime(2020, 4, 30)
return_day_2 = pif.get_share_price_perfomance(t=t_2,
                                              t0=t_2 - timedelta(days=1))
print(f'1D return on {t_2.date()} = {return_day_2 * 100:.2f} %')

return_mtd_2 = pif.get_share_price_perfomance(t=t_2,
                                              t0=t_2.replace(day=1) - timedelta(hours=1))
print(f'MTD return on {t_2.date()} = {return_mtd_2 * 100:.2f} %')

return_ytd_2 = pif.get_share_price_perfomance(t=t_2, t0=t_0)
print(f'YTD return on {t_2.date()} = {return_ytd_2 * 100:.2f} %\n')
