from datetime import datetime


class Transaction:
    '''
    Transaction model.

    timestamp: datetime.datetime - transaction timestamp
    funding: float - deposit or withdrawal
    {
        deposit: +X in asset [U]
        withdrawal: -X in asset [U]
    }
    '''
    def __init__(self, timestamp: datetime, funding: float):
        self.timestamp = timestamp
        self.funding = funding
