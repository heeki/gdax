import json
import requests
from gdax_client_public import GdaxClientPublic
from gdax_auth import GdaxAuth


class GdaxClientAuth(GdaxClientPublic):
    def __init__(self, key, b64secret, passphrase, api_url="https://api.gdax.com"):
        GdaxClientPublic.__init__(self, api_url)
        self.auth = GdaxAuth(key, b64secret, passphrase)

    def get_accounts(self):
        return requests.get("{}/accounts".format(self.url), auth=self.auth, timeout=30).json()

    def get_account(self, account_id):
        return requests.get("{}/accounts/{}".format(self.url, account_id), auth=self.auth, timeout=30).json()

    def get_account_ledger(self, account_id):
        return requests.get("{}/accounts/{}/ledger".format(self.url, account_id), auth=self.auth, timeout=30).json()

    def buy(self, **kwargs):
        kwargs["side"] = "buy"
        if "product_id" not in kwargs:
            kwargs["product_id"] = self.product_id
        r = requests.post(self.url + '/orders',
                          data=json.dumps(kwargs),
                          auth=self.auth,
                          timeout=30)
        return r.json()

    def sell(self, **kwargs):
        kwargs["side"] = "sell"
        r = requests.post(self.url + '/orders',
                          data=json.dumps(kwargs),
                          auth=self.auth,
                          timeout=30)
        return r.json()

    def cancel_order(self, order_id):
        r = requests.delete(self.url + '/orders/' + order_id, auth=self.auth, timeout=30)
        # r.raise_for_status()
        return r.json()

    def cancel_all(self, product_id=''):
        url = self.url + '/orders/'
        if product_id:
            url += "?product_id={}&".format(str(product_id))
        r = requests.delete(url, auth=self.auth, timeout=30)
        # r.raise_for_status()
        return r.json()

    def get_order(self, order_id):
        r = requests.get(self.url + '/orders/' + order_id, auth=self.auth, timeout=30)
        # r.raise_for_status()
        return r.json()

    def get_order(self, order_id):
        r = requests.get(self.url + '/orders/' + order_id, auth=self.auth, timeout=30)
        # r.raise_for_status()
        return r.json()

    def get_orders(self, product_id='', status=[]):
        result = []
        url = self.url + '/orders/'
        params = {}
        if product_id:
            params["product_id"] = product_id
        if status:
            params["status"] = status
        r = requests.get(url, auth=self.auth, params=params, timeout=30)
        # r.raise_for_status()
        result.append(r.json())
        if 'cb-after' in r.headers:
            self.paginate_orders(product_id, status, result, r.headers['cb-after'])
        return result

    def paginate_orders(self, product_id, status, result, after):
        url = self.url + '/orders'

        params = {
            "after": str(after),
        }
        if product_id:
            params["product_id"] = product_id
        if status:
            params["status"] = status
        r = requests.get(url, auth=self.auth, params=params, timeout=30)
        # r.raise_for_status()
        if r.json():
            result.append(r.json())
        if 'cb-after' in r.headers:
            self.paginate_orders(product_id, status, result, r.headers['cb-after'])
        return result

