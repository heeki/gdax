# GDAX Trading Helper
The objective of this simple code package is to enable a user to perform simple trade executions on GDAX:
buy, sell, cancel. It also enables the user to query status on orders and get listings of account ids.

## Installation
This code package was developed with Python 2.7.

```commandline
git clone https://github.com/heeki/gdax.git
```

First, environment variables need to be setup with your GDAX key, secret, and passphrase. This script uses those
environment variables for performing authenticated calls to GDAX. To create those, go to the upper right corner
of the GDAX UI and select API. From there, create an API key with the following permissions: View, Trade.

For Mac users:
```commandline
GDAX_PASSPHRASE=abcdefghijk
GDAX_KEY=abcdefghijklmnopqrstuvwxyz123456
GDAX_SECRET=abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890
```

For Windows users:
```commandline
set GDAX_PASSPHRASE=abcdefghijk
set GDAX_KEY=abcdefghijklmnopqrstuvwxyz123456
set GDAX_SECRET=abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890
```

Note that GDAX has both its production/live API and a Sandbox API. This script is currently setup to point to the
Sandbox API for testing. When you have tested with the Sandbox API and feel ready to use the production/live API,
we will need to change the `get_auth_client()` method in execution.py to point to the public API. To do so, comment
out the `api-public.sandbox.gdax.com` line and uncomment the `api.gdax.com line`.

```python
    # api_url = "https://api.gdax.com"
    api_url = "https://api-public.sandbox.gdax.com"
```

Caution! Be very careful when moving over to the production/live API. The script is very basic and does not do
any validation against your trades. Erroneous script execution could lead to serious financial loss. Proceed with use
at your own risk.

## Usage
To check outstanding orders, execute the following. The parameter must be a valid trading pair on GDAX.
```commandline
python execution.py --orders="BTC-USD"
```

To execute a buy/sell order, execute the following. The buy/sell paramter must be a valid trading pair on GDAX.
The price is your target limit price. The size is the number of coins for the order.
```commandline
python execution.py --buy="BTC-USD" --price="100.00" --size="0.01"
python execution.py --sell="BTC-USD" --price="30000.00" --size="0.01"
```

To cancel a buy/sell order, execute the following. The paramter must be the order that was returned when entering the
buy/sell order.
```commandline
python execution.py --cancel="655fafe4-26fc-4e70-ab2a-b038e7fe6683"
python execution.py --cancel="2c4bd190-2026-45b5-9c57-c949f62a1ca2"
python execution.py --cancel_all="BTC-USD"
```

## Credit
Credit largely goes to [https://github.com/danpaquin/gdax-python](https://github.com/danpaquin/gdax-python), as I have taken the majority of the core code
from that repository. Most of what I have written is a wrapper for simple command line execution of trades.