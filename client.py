import json
from random import random, randint

import requests
import datetime

BASE_URL = "http://localhost:5040"  # URL for the server.
MERCHANT_ID = "db3da37d-edef-4c99-aea0-86c297feff0f"

# Send a POST request to the server.
http_response = requests.post(
    url=f"{BASE_URL}/accept-payment",
    data={
        "merchant_id": MERCHANT_ID,
        "timestamp": datetime.datetime.now().isoformat(),
        "card_number": "-".join(f"{randint(0, 9999):04}" for _ in range(4)),  # Randomized card number.
        "card_security_code": f"{randint(1, 999):03}",  # Randomized security code.
        "zip_code": f"80{randint(1, 999):03}",  # Randomized zip code.
        "amount": randint(50, 1000) + round(random(), 2),  # Randomized transaction amount.
        "name": "Jackson Harrison",
        "email": "jackson@gmail.com",
    },
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        # "Accept": "text/plain",  # This would cause a 406 error.
        "Accept": "application/json",
    }
)

# Get the response back as json and print it out.
response_body = http_response.json()
print("HEADERS:", json.dumps(dict(http_response.headers), indent=2))
print("BODY:", json.dumps(response_body, indent=2))

