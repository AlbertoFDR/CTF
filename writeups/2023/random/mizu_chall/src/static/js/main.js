const render = (html, allowed_tags, allowed_attrs) => {
    const output = document.getElementById("output");
    const s = new Sanitizer({
        ALLOWED_TAGS: allowed_tags,
        ALLOWED_ATTS: allowed_attrs
    });
    output.innerHTML = s.sanitize(html);
}

window.onload = () => {
    // Onload rendering
    const query = new URLSearchParams(location.search);
    const html = query.get("html");
    if (html) {
        const allowed_tags = query.get("allowed_tags") ? query.get("allowed_tags").split(",") : null;
        const allowed_attrs = query.get("allowed_attrs") ? query.get("allowed_attrs").split(",") : null;
        render(html, allowed_tags, allowed_attrs);
    }

    // Setup options
    const s = new Sanitizer();

    const tags = document.getElementById("tags");
    s.DEFAULT_TAGS.forEach(tag => {
        const opt = document.createElement("option");
        opt.value = tag;
        opt.text = tag;
        tags.appendChild(opt);
    })
    tags.addEventListener("mousedown", (e) => {
        e.preventDefault();
        const t = e.target;
        if (t.tagName === "OPTION") {
            t.selected = !t.selected;
            return false;
        }
    });

    const attrs = document.getElementById("attrs");
    s.DEFAULT_ATTRS.forEach(attr => {
        const opt = document.createElement("option");
        opt.value = attr;
        opt.text = attr;
        attrs.appendChild(opt);
    })
    attrs.addEventListener("mousedown", (e) => {
        e.preventDefault();
        const t = e.target;
        if (t.tagName === "OPTION") {
            t.selected = !t.selected;
            return false;
        }
    });

    // Render html
    document.getElementById("sanitize").onclick = () => {
        const html = document.getElementById("html").value;
        var allowed_tags = document.getElementById("tags").selectedOptions;
        allowed_tags = Array.from(allowed_tags).map(opt => opt.value);
        var allowed_attrs = document.getElementById("attrs").selectedOptions;
        allowed_attrs = Array.from(allowed_attrs).map(opt => opt.value);

        allowed_tags  = allowed_tags.length  !== 0 ? allowed_tags : null
        allowed_attrs = allowed_attrs.length !== 0 ? allowed_attrs : null

        render(html, allowed_tags, allowed_attrs);
    }
}
