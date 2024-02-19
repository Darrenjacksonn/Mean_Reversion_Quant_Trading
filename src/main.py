from config import ALPACA_KEY, ALPACA_SECRET_KEY
#import config_example
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream



client = TradingClient(ALPACA_KEY, ALPACA_SECRET_KEY)


# account = dict(client.get_account())

# for k,v in account.items():
#     print(f"{k:30}{v})")


order_details = MarketOrderRequest(
    symbol = "SPY",
    notional = 100,
    side = 'buy',
    time_in_force = 'day'
)

order = client.submit_order(order_details)

trades = TradingStream(ALPACA_KEY, ALPACA_SECRET_KEY, paper = True)

async def trade_status(data):
    print(data)

trades.subscribe_trade_updates(trade_status)
trades.run()