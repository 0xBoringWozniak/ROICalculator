# python3 ROI calculator

**General theory**

Let we have some investments in strategy and we want to calclulate ROI. If we don't make any withdrawals or deposits then it is easy to calculate ```ROI = NAV / initital investments - 1```. However, if we make potfolio rebalancing or new deposits/withdrawals we should account them and simple ROI formula is not enough here. 

For this purpose we can use following algorithm:

1. Create virtual pie with shares = deposited asset (in shares) and set share price ```P = 1```.

2. Any deposit or withrawal is equivalent to buying or selling some shares per share price ```P_T0```.

Let ```X``` was added to virtual pie at time ```T```, where ```X > 0``` when we make deposit, and ```X < 0``` when we make withdrawal;

```T0 = T - eps``` - timestamp before transaction
```T1 = T + eps``` - timestamp after transaction

Pie consisted of ```N``` SHARES with share price ```P_0 = NAV_T0 / N```.

New shares amount will be ```M = N + X / P_0```
Updated share price ```P_T1 = NAV_T1 / M```

3. So, for each moment we have our ```NAV_t```, virtual shares amount ```N_t``` and share price ```P_t = NAV_t / N_t``` and we can calculate ROI as ```P_t / P_t0 - 1```
Moreover we can calculate ROI at any period ```(t, t0)```, ```t > t0```.

[**Full theory**](https://www.investopedia.com/terms/r/returnoninvestment.asp)


# How to use? Example

1. Create own class ```Investor``` implemetned by Investor interface and redefine **```get_nav_by_timestamp```** - it can be ```pandas.Series``` with acess to NAV by timestamp or manual input like in the example **(not recommended)**

```python
lass ExampleInvestor(Investor):
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
```
2. In this example, there is a simple strategy model with 0.05% daily returns on investments. Let we have deposit at 2020/4/1 then our NAV = current_investments + PnL_before_deposit + PnL_after_deposit. 

Define transactions: 

```python
transaction = Transaction(datetime(2020, 4, 1), funding=200)
```

Create pie object:

```python
investor = ExampleInvestor(investment_timestamp=datetime(2020, 1, 1),
                           deposit=100, transactions=[transaction])

# create pie
pie = ROICalculator(investor)
```

3. Calculate ROI per period ```(t_0, t_1)```, **```t_1 > t_0```**
```python
# initial investment time
t_0 = pie.investor.investment_timestamp

#
# before transaction
#

t_1 = datetime(2020, 3, 31)
return_day_1 = pie.get_share_price_perfomance(t=t_1,
                                              t0=t_1 - timedelta(days=1))
print(f'1D return on {t_1.date()} = {return_day_1 * 100:.2f} %')

return_mtd_1 = pie.get_share_price_perfomance(t=t_1,
                                              t0=t_1.replace(day=1) - timedelta(hours=1))
print(f'MTD return on {t_1.date()} = {return_mtd_1 * 100:.2f} %')

return_ytd_1 = pie.get_share_price_perfomance(t=t_1, t0=t_0)
print(f'YTD return on {t_1.date()} = {return_ytd_1 * 100:.2f} %\n')

#
# after transaction
#

t_2 = datetime(2020, 4, 30)
return_day_2 = pie.get_share_price_perfomance(t=t_2,
                                              t0=t_2 - timedelta(days=1))
print(f'1D return on {t_2.date()} = {return_day_2 * 100:.2f} %')

return_mtd_2 = pie.get_share_price_perfomance(t=t_2,
                                              t0=t_2.replace(day=1) - timedelta(hours=1))
print(f'MTD return on {t_2.date()} = {return_mtd_2 * 100:.2f} %')

return_ytd_2 = pie.get_share_price_perfomance(t=t_2, t0=t_0)
print(f'YTD return on {t_2.date()} = {return_ytd_2 * 100:.2f} %\n')

```

Result:

```
1D return on 2020-03-31 = 0.05 %
MTD return on 2020-03-31 = 1.51 %
YTD return on 2020-03-31 = 4.50 %

1D return on 2020-04-30 = 0.05 %
MTD return on 2020-04-30 = 1.44 %
YTD return on 2020-04-30 = 6.01 %
```
