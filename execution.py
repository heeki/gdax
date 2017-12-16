import argparse
import gdax_client_public
import gdax_client_auth
import os
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)


def get_auth_client():
    # api_url = "https://api.gdax.com"
    api_url = "https://api-public.sandbox.gdax.com"
    gdax_key = os.getenv("GDAX_KEY")
    gdax_secret = os.getenv("GDAX_SECRET")
    gdax_passphrase = os.getenv("GDAX_PASSPHRASE")
    client = gdax_client_auth.GdaxClientAuth(gdax_key, gdax_secret, gdax_passphrase, api_url=api_url)
    return client


def usage():
    print "usage: execution.py"
    print "--accounts"
    print "--orders"
    print "--buy"
    print "--sell"
    print "--price="
    print "--product_id="
    print "--size="
    sys.exit(1)


def get_order_detail(data):
    return "{}, {}, {}@{}, {}-{}".format(data["id"], data["product_id"], data["size"], data["price"], data["status"], data["side"])


def main():
    # test_public()
    # test_auth()
    parser = argparse.ArgumentParser()
    parser.add_argument("--accounts", nargs="?")
    parser.add_argument("--account", nargs="?")
    parser.add_argument("--orders", nargs="?")
    parser.add_argument("--order", nargs="?")
    parser.add_argument("--buy", nargs="?")
    parser.add_argument("--sell", nargs="?")
    parser.add_argument("--cancel", nargs="?")
    parser.add_argument("--cancel_all", nargs="?")
    parser.add_argument("--price", nargs="?")
    parser.add_argument("--size", nargs="?")
    args = parser.parse_args()
    pp.pprint(args)

    client = get_auth_client()
    if args.buy:
        client.log.info("submitting buy order for {}".format(args.buy))
        data = client.buy(price=args.price, size=args.size, product_id=args.buy)
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


if __name__ == '__main__':
    main()
