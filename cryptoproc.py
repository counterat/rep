import hashlib
import hmac
import json


def sign(data: str, secret_key: str):
    secret_key = bytes(secret_key, "utf8")

    return hmac.new(secret_key, data.encode(), hashlib.sha256).hexdigest()

data = {
  "type": "long_term",
  "client_id": "123",
  "currency": "eth",
  "conversion_currency": "usdt",
  "callback_url": "https://example.com/crosspay_callback/order_123",
  "order_id_prefix": "crypto_order_",
  "attributes": {
    "blockchain_network": "erc20"
  }
}

payload = json.dumps(data)
signature = sign(payload, 'Iczsckf3OlKqE27RL2cgC3UvY9m0jD8H59vCB9uamPam8sAT')

print(signature)