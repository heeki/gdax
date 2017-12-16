import json
import logging
import requests


class GdaxClientPublic:
    def __init__(self, api_url="https://api.gdax.com"):
        self.url = api_url
        self.log = None
        self.set_logging("gdax-client")

    def set_logging(self, name):
        self.log = logging.getLogger(name)
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s '%(message)s'")
        handler_console = logging.StreamHandler()
        handler_console.setFormatter(formatter)
        # handler_file = logging.FileHandler("log/{}.log".format(name))
        # handler_file.setFormatter(formatter)
        self.log.setLevel(logging.INFO)
        if len(self.log.handlers) == 0:
            self.log.addHandler(handler_console)
            # self.log.addHandler(handler_file)

    def get(self, path, params=None):
        data = requests.get("{}/{}".format(self.url, path), timeout=1).json()
        # self.log.info("get: got {}".format(data))
        return data

    def get_product_ticker(self, product_id):
        return self.get("/products/{}/ticker".format(product_id))

    def get_product_trades(self, product_id):
        return self.get("/products/{}/trades".format(product_id))

    def get_product_stats(self, product_id):
        return self.get("/products/{}/stats".format(product_id))

    def get_time(self):
        return self.get("/time")

