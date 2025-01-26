import json
from random import random, randint

import requests
import datetime

BASE_URL = "http://localhost:5040"
req = requests.post(
    url=f"{BASE_URL}/accept-payment",
    data={
        "timestamp": datetime.datetime.now().isoformat(),
        "card_number": "-".join(f"{randint(0, 9999):04}" for _ in range(4)),
        "card_security_code": f"{randint(1, 999):03}",
        "zip_code": f"80{randint(1, 999):03}",
        "amount": randint(50, 1000) + round(random(), 2),
        "name": "Jackson Harrison",
        "email": "jackson@gmail.com",
    },
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        # "Accept": "text/plain",
        "Accept": "application/json",
    }
)

response = req.json()
print(json.dumps(response, indent=2))

