import json
import time

import requests

req = requests.get('http://localhost:8000')

print(req.text)

for i in range(10):
    if i % 2:
        data = json.dumps({"on": False})
    else:
        data = json.dumps({"off": True})
    req = requests.post('http://localhost:8000/led', json=data)
    time.sleep(1)
    print(req.text)
