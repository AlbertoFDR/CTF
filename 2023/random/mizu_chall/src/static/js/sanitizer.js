class Sanitizer {
    // https://source.chromium.org/chromium/chromium/src/+/main:out/android-Debug/gen/third_party/blink/renderer/modules/sanitizer_api/builtins/sanitizer_builtins.cc;l=360
    DEFAULT_TAGS  = [ "a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "bgsound", "big", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "datalist", "dd", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "keygen", "label", "layer", "legend", "li", "link", "listing", "main", "map", "mark", "marquee", "menu", "meta", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "popup", "pre", "progress", "q", "rb", "rp", "rt", "rtc", "ruby", "s", "samp", "section", "select", "selectlist", "small", "source", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr" ];
    // https://source.chromium.org/chromium/chromium/src/+/main:out/android-Debug/gen/third_party/blink/renderer/modules/sanitizer_api/builtins/sanitizer_builtins.cc;l=481
    DEFAULT_ATTRS = [ "abbr", "accept", "accept-charset", "accesskey", "action", "align", "alink", "allow", "allowfullscreen", "alt", "anchor", "archive", "as", "async", "autocapitalize", "autocomplete", "autocorrect", "autofocus", "autopictureinpicture", "autoplay", "axis", "background", "behavior", "bgcolor", "border", "bordercolor", "capture", "cellpadding", "cellspacing", "challenge", "char", "charoff", "charset", "checked", "cite", "class", "classid", "clear", "code", "codebase", "codetype", "color", "cols", "colspan", "compact", "content", "contenteditable", "controls", "controlslist", "conversiondestination", "coords", "crossorigin", "csp", "data", "datetime", "declare", "decoding", "default", "defer", "dir", "direction", "dirname", "disabled", "disablepictureinpicture", "disableremoteplayback", "disallowdocumentaccess", "download", "draggable", "elementtiming", "enctype", "end", "enterkeyhint", "event", "exportparts", "face", "fetchpriority", "for", "form", "formaction", "formenctype", "formmethod", "formnovalidate", "formtarget", "frame", "frameborder", "headers", "height", "hidden", "high", "href", "hreflang", "hreftranslate", "hspace", "http-equiv", "id", "imagesizes", "imagesrcset", "impressiondata", "impressionexpiry", "incremental", "inert", "inputmode", "integrity", "invisible", "is", "ismap", "keytype", "kind", "label", "lang", "language", "latencyhint", "leftmargin", "link", "list", "loading", "longdesc", "loop", "low", "lowsrc", "manifest", "marginheight", "marginwidth", "max", "maxlength", "mayscript", "media", "method", "min", "minlength", "multiple", "muted", "name", "nohref", "nomodule", "nonce", "noresize", "noshade", "novalidate", "nowrap", "object", "open", "optimum", "part", "pattern", "ping", "placeholder", "playsinline", "policy", "poster", "preload", "pseudo", "readonly", "referrerpolicy", "rel", "reportingorigin", "required", "resources", "rev", "reversed", "role", "rows", "rowspan", "rules", "sandbox", "scheme", "scope", "scopes", "scrollamount", "scrolldelay", "scrolling", "select", "selected", "shadowroot", "shadowrootdelegatesfocus", "shape", "size", "sizes", "slot", "span", "spellcheck", "src", "srcdoc", "srclang", "srcset", "standby", "start", "step", "style", "summary", "tabindex", "target", "text", "title", "topmargin", "translate", "truespeed", "trusttoken", "type", "usemap", "valign", "value", "valuetype", "version", "virtualkeyboardpolicy", "vlink", "vspace", "webkitdirectory", "width", "wrap" ];

    constructor(config={}) {
        this.version = "2.0.0";
        this.creator = "@kevin_mizu";
        this.ALLOWED_TAGS = config.ALLOWED_TAGS
            ? config.ALLOWED_TAGS.concat([ "html", "head", "body" ]).filter(tag => this.DEFAULT_TAGS.includes(tag))
            : this.DEFAULT_TAGS;
        this.ALLOWED_ATTS = config.ALLOWED_ATTS
            ? config.ALLOWED_ATTS.filter(attr => this.DEFAULT_ATTRS.includes(attr))
            : this.DEFAULT_ATTRS;
    }

    // https://github.com/cure53/DOMPurify/blob/48bd850cc20190e3896cb6291367c2da2ed2bddb/src/purify.js#L924
    _isClobbered = function (elm) {
        return (
            elm instanceof HTMLFormElement &&
            (typeof elm.nodeName !== 'string' ||
            typeof elm.textContent !== 'string' ||
            typeof elm.removeChild !== 'function' ||
            !(elm.attributes instanceof NamedNodeMap) ||
            typeof elm.removeAttribute !== 'function' ||
            typeof elm.setAttribute !== 'function' ||
            typeof elm.namespaceURI !== 'string' ||
            typeof elm.insertBefore !== 'function' ||
            typeof elm.hasChildNodes !== 'function')
        )
    }

    // https://github.com/cure53/DOMPurify/blob/48bd850cc20190e3896cb6291367c2da2ed2bddb/src/purify.js#L1028
    removeNode = (currentNode) => {
        const parentNode = currentNode.parentNode;
        const childNodes = currentNode.childNodes;

        if (childNodes && parentNode) {
            const childCount = childNodes.length;

            for (let i = childCount - 1; i >= 0; --i) {
                parentNode.insertBefore(
                    childNodes[i].cloneNode(),
                    currentNode.nextSibling
                );
            }
        }

        currentNode.parentElement.removeChild(currentNode);
    }

    sanitize = (input) => {
        let currentNode;
        var dom_tree = new DOMParser().parseFromString(input, "text/html");
        var nodeIterator = document.createNodeIterator(dom_tree);

        while ((currentNode = nodeIterator.nextNode())) {

            // avoid DOMClobbering
            if (this._isClobbered(currentNode) || typeof currentNode.nodeType !== "number") {
                this.removeNode(currentNode);
                continue;
            }

            switch(currentNode.nodeType) {
                case currentNode.ELEMENT_NODE:
                    var tag_name   = currentNode.nodeName.toLowerCase();
                    var attributes = currentNode.attributes;

                    // avoid mXSS
                    if (currentNode.namespaceURI !== "http://www.w3.org/1999/xhtml") {
                        this.removeNode(currentNode);
                        continue;

                    // sanitize tags
                    } else if (!this.ALLOWED_TAGS.includes(tag_name)){
                        this.removeNode(currentNode);
                        continue;
                    }

                    // sanitize attributes
                    for (let i=0; i < attributes.length; i++) {
                        if (!this.ALLOWED_ATTS.includes(attributes[i].name)){
                            this.removeNode(currentNode);
                            continue;
                        }
                    }
            }
        }

        return dom_tree.body.innerHTML;
    }
}
