import argparse
import gdax_client_auth
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)


def get_auth_client(production=False):
    if production:
        api_url = "https://api.gdax.com"
    else:
        api_url = "https://api-public.sandbox.gdax.com"
    gdax_key = os.getenv("GDAX_KEY")
    gdax_secret = os.getenv("GDAX_SECRET")
    gdax_passphrase = os.getenv("GDAX_PASSPHRASE")
    client = gdax_client_auth.GdaxClientAuth(gdax_key, gdax_secret, gdax_passphrase, api_url=api_url)
    return client


def get_order_detail(data):
    return "{}, {}, {}@{}, {}-{}".format(data["id"], data["product_id"], data["size"], data["price"], data["status"], data["side"])


def main():
    # test_public()
    # test_auth()
    parser = argparse.ArgumentParser(
        description="GDAX Trading Helper"
    )
    parser.add_argument("--accounts", nargs="?", help="")
    parser.add_argument("--account", nargs="?", help="--account=[account_id]")
    parser.add_argument("--buy", nargs="?", help="--buy=[trading_pair] --price=[price_usd] --size=[qty]")
    parser.add_argument("--sell", nargs="?", help="--sell=[trading_pair] --price=[price_usd] --size=[qty]")
    parser.add_argument("--cancel", nargs="?", help="--cancel=[order_id]")
    parser.add_argument("--cancel_all", nargs="?", help="--cancel_all=[trading_pair]")
    parser.add_argument("--orders", nargs="?", help="")
    parser.add_argument("--order", nargs="?", help="--order=[order_id]")
    parser.add_argument("--price", nargs="?", help="used in conjunction with --buy/sell")
    parser.add_argument("--size", nargs="?", help="used in conjunction with --buy/sell")
    parser.add_argument("--ticker", nargs="?", help="--ticker=[trading_pair]")
    parser.add_argument("--tickers", nargs="?", help="")
    parser.add_argument("--production", nargs="?", help="enables trading against live exchange")
    args = parser.parse_args()
    pp.pprint(args)

    if args.production:
        client = get_auth_client(production=True)
    else:
        client = get_auth_client(production=False)

    if args.buy:
        client.log.info("submitting buy order for {}".format(args.buy))
        data = client.buy(price=args.price, size=args.size, product_id=args.buy)
        # pp.pprint(data)
        client.log.info(get_order_detail(data))
        print data["id"]
    elif args.sell:
        client.log.info("submitting sell order for {}".format(args.sell))
        data = client.sell(price=args.price, size=args.size, product_id=args.sell)
        client.log.info(get_order_detail(data))
        print data["id"]
    elif args.cancel:
        client.log.info("cancelling order {}".format(args.cancel))
        pp.pprint(client.cancel_order(args.cancel))
    elif args.cancel_all:
        client.log.info("cancelling all orders {}".format(args.cancel_all))
        pp.pprint(client.cancel_all(args.cancel_all))
    elif args.order:
        client.log.info("getting order for {}".format(args.order))
        pp.pprint(client.get_order(args.order))
    elif args.orders:
        client.log.info("getting orders for {}".format(args.orders))
        data = client.get_orders(args.orders)
        for row in data[0]:
            client.log.info(get_order_detail(row))
    elif args.accounts:
        client.log.info("getting account information")
        accounts = dict()
        for row in client.get_accounts():
            accounts[row["currency"]] = row["id"]
            client.log.info("currency={}, id={}".format(row["currency"], row["id"]))
        pp.pprint(client.get_account(accounts["BTC"]))
        pp.pprint(client.get_account_ledger(accounts["BTC"]))
    elif args.ticker:
        client.log.info("getting ticker info on {}".format(args.ticker))
        data = client.get_product_ticker(args.ticker)
        pp.pprint(data)
        print data["price"]
    elif args.tickers:
        client.log.info("getting ticker info on all")
        coins = ["BTC-USD", "ETH-USD", "LTC-USD"]
        for coin in coins:
            data = client.get_product_ticker(coin)
            print "{},,{}".format(coin, data["price"])


if __name__ == '__main__':
    main()
