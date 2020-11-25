from datetime import datetime, timedelta

from .investor import Investor


class ROICalculator:
    '''
    theory: https://www.investopedia.com/terms/r/returnoninvestment.asp

    ROICalculator.

    1. Create virtual pif __init_pif 
    {
        init shares = deposit quantity of asset[U]
        share price = 1
    }

    2. System go through 3 conditions while getting funding
    {
        Let funding X[U] was added to virtual pif at T;

        T - transaction timestamp,
        T0 = T - eps - timestamp before transaction
        T1 = T + eps - timestamp after transaction

        pif consisted of N SHARES with share price P_0[U] = NAV_T0[U] / N.

        Add X[U] to virtual pif: M = N + X[U] / P_0[U],
        where M - new shares amount

        Update share price P[U] = NAV_T1[U] / M

    }
    '''

    def __init__(self, investor: Investor, eps_hours=1):
        # eps is used while getting nav_before
        # and nav_after transaction
        self.investor = investor
        self.eps_hours = eps_hours
        self.__init_pif()

    def __init_pif(self):
        self.shares = self.investor.deposit
        self.share_price = 1

    def __calculate_shares(self, funding: float):
        self.shares += funding / self.share_price

    def __calculate_share_price(self, nav: float):
        self.share_price = nav / self.shares

    def __calculate_shares_by_timestamp(self, timestamp: datetime):

        # create virtual pif each time calculating shares
        self.__init_pif()

        for transaction in self.investor.transactions:
            if transaction.timestamp > timestamp:
                break

            # 1 condition: before transaction
            # T0
            timestamp_before_transtaction = transaction.timestamp - \
                timedelta(hours=self.eps_hours)

            if timestamp_before_transtaction < self.investor.investment_timestamp:
                nav_before = self.investor.deposit

            # NAV_T0
            try:
                nav_before = self.investor.get_nav_by_timestamp(
                    timestamp_before_transtaction)
            except Exception as e:
                print(e)

            # P0 = NAV_T0 / N
            self.__calculate_share_price(nav_before)

            # 2 condition: add funding to virtual pif
            # shares = M
            self.__calculate_shares(transaction.funding)

            # T1
            timestamp_after_transtaction = transaction.timestamp + \
                timedelta(hours=self.eps_hours)

            # NAV_T
            try:
                nav_after = self.investor.get_nav_by_timestamp(
                    timestamp_after_transtaction)
            except Exception as e:
                print(e)

            # update share price
            # P[U] = NAV_T1[U] / M
            self.__calculate_share_price(nav_after)

    def __calculate_share_price_by_timestamp(self, timestamp: datetime):
        # update shares N in self.shares
        self.__calculate_shares_by_timestamp(timestamp)

        # get NAV from data
        nav = self.investor.get_nav_by_timestamp(timestamp)

        # update share_price in self.share_price
        self.__calculate_share_price(nav)

    def get_share_price_perfomance(self, t0: datetime, t: datetime) -> float:
        '''
        t  - end_timestamp
        t0 - start_timestamp, t > t0

        t = datetime.utcnow(), t0 = investment_timestamp to get ROI
        '''
        self.__calculate_share_price_by_timestamp(t)
        # fix share_price at t
        k = self.share_price

        self.__calculate_share_price_by_timestamp(t0)
        # fix share_price at t0
        k0 = self.share_price

        return k / k0 - 1
