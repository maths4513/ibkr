import pandas as pd
from ib_insync import IB, Stock, util

def fetch_data(symbol="AAPL", exchange="SMART", currency="USD", duration="1 Y", barSize="1 day"):
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    contract = Stock(symbol, exchange, currency)
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr=duration,
        barSizeSetting=barSize,
        whatToShow='TRADES',
        useRTH=True
    )
    ib.disconnect()
    df = util.df(bars)
    df.set_index("date", inplace=True)
    return df