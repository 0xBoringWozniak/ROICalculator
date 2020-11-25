from datetime import datetime
from abc import ABC, abstractmethod

from typing import List

from .transaction import Transaction

Transactions = List[Transaction]


class Investor(ABC):
    '''
    Investor model.

    1. Attributes
    investment_timestamp: datetime.datetime - investment timestamp (deposit timestamp)
    deposit: float - deposit amount in asset [U]
    transactions: Transactions - list of transactions with fundings and timestamp

    2. get_nav_by_timestamp - investor's net asset value

    '''

    def __init__(self, investment_timestamp: datetime, deposit: float, transactions: Transactions, *args, **kwargs):
        self.investment_timestamp = investment_timestamp
        self.deposit = deposit

        # sort transactions by timestamp
        # from first transaction to last
        #
        # EXCEPT DEPOSIT TRANSACTION
        #
        self.transactions = sorted(
            transactions, key=lambda x: x.timestamp, reverse=False)

    @abstractmethod
    def get_nav_by_timestamp(self, timestamp: datetime) -> float:
        '''returns NAV'''
        raise NotImplementedError
