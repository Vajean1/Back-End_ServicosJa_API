import requests
import time
from random import randint

while True:
    try:
        response = requests.get(
            "https://back-end-servicosja-api.onrender.com/api/redoc/", timeout=30
        )

        print(f"Resquest successful status {response.status_code}")

    except Exception as err:
        print(f"Error: {err}")
        break

    time.sleep(randint(40, 50))
