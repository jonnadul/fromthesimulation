#!/usr/bin/env python3
"""Convert a Medium export (posts/*.html) into Jekyll posts/drafts.

Matches the conventions already used by the Substack import:
  - front matter: layout/title/subtitle/date/published
  - images self-hosted under assets/img/raw and referenced with
    {{ '/assets/img/raw/NAME' | relative_url }} so GitHub Pages baseurl works

Published posts  -> _posts/YYYY-MM-DD-slug.md
Drafts (no date) -> _drafts/slug.md
"""
import os, re, html, json, sys, unicodedata

SRC = r"C:/Users/jonna/Downloads/medium-export-1fd04de1e27644ea14035a260fd0779a6d66e5772f0fe6fbe0298a34109430d8/posts"
SITE = r"C:/Users/jonna/fromthesimulation"
POSTS = os.path.join(SITE, "_posts")
DRAFTS = os.path.join(SITE, "_drafts")
RAW = "assets/img/raw"

os.makedirs(POSTS, exist_ok=True)
os.makedirs(DRAFTS, exist_ok=True)

imgmap = json.load(open(os.path.join(SITE, "tools", "medium_img_map.json")))


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-") or "untitled"


def clean_text(node_html):
    """Strip tags to plain text, unescaping entities and normalising space."""
    t = re.sub(r"<br\s*/?>", " ", node_html)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def inline(node_html):
    """Convert inline HTML (links, em, strong, code) to Markdown."""
    s = node_html
    s = re.sub(r"<br\s*/?>", "\n", s)
    # anchors (incl. inside <pre>)
    s = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", s, flags=re.S)
    s = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return s.strip()


def get_body(h):
    """Return the e-content body HTML."""
    m = re.search(r'<section data-field="body"[^>]*>(.*?)<footer>', h, re.S)
    if not m:
        m = re.search(r'<section data-field="body"[^>]*>(.*)', h, re.S)
    return m.group(1)


def parse(h):
    """Walk Medium 'graf' blocks in document order, emit markdown lines.

    Medium wraps everything in nested <section>/<div> scaffolding, so instead
    of matching wrapper tags we select elements carrying a `graf graf--*`
    class (p, h2, h3, h4, pre, figure, li, ...) and walk them in DOM order.
    """
    from bs4 import BeautifulSoup
    body = get_body(h)
    soup = BeautifulSoup(body, "html.parser")
    out = []
    seen_figs = set()

    for el in soup.find_all(class_=re.compile(r"\bgraf\b")):
        cls = " ".join(el.get("class") or [])
        tag = el.name

        # --- headings ---
        if tag in ("h1", "h2", "h3", "h4"):
            t = clean_text(str(el))
            if not t:
                continue
            # drop the duplicated cover title/subtitle block
            if "graf--title" in cls or "graf--subtitle" in cls:
                continue
            out.append(f"{'#' * int(tag[1])} {t}\n")

        # --- paragraphs / captions ---
        elif tag == "p":
            if "graf--sectionCaption" in cls:
                t = clean_text(str(el))
                if t:
                    out.append(f"*{t}*\n")
                continue
            t = inline(str(el))
            if t:
                out.append(t + "\n")

        # --- code blocks ---
        elif tag == "pre":
            code = str(el)
            code = re.sub(r"<br\s*/?>", "\n", code)
            code = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"\2", code, flags=re.S)
            code = re.sub(r"<[^>]+>", "", code)
            code = html.unescape(code)
            out.append("```\n" + code.strip() + "\n```\n")

        # --- figures (images + mixtape embeds) ---
        elif tag == "figure":
            im = el.find("img")
            if im and im.get("src", "").startswith("https://cdn-images-"):
                fn = imgmap.get(im["src"])
                if fn:
                    out.append(f"![]({{{{ '/{RAW}/{fn}' | relative_url }}}})\n")
            elif "mixtapeEmbed" in cls:
                a = el.find("a", href=True)
                if a:
                    out.append(f"[{clean_text(str(a))}]({a['href']})\n")
            cap = el.find("figcaption")
            if cap:
                c = clean_text(str(cap))
                if c:
                    out.append(f"*{c}*\n")

        # --- list items (Medium emits them as standalone <li>) ---
        elif tag == "li":
            t = inline(str(el))
            if t:
                out.append(f"- {t}")

        # --- pullquotes / blockquotes ---
        elif tag == "blockquote":
            t = clean_text(str(el))
            if t:
                out.append("> " + t + "\n")

    md = "\n".join(out)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def fm_escape(s):
    return s.replace('"', '\\"')


def main():
    made = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".html"):
            continue
        h = open(os.path.join(SRC, fn), encoding="utf-8").read()
        title_m = re.search(r'<h1 class="p-name">(.*?)</h1>', h, re.S)
        title = clean_text(title_m.group(1)) if title_m else ""
        sub_m = re.search(r'<section data-field="subtitle"[^>]*>(.*?)</section>', h, re.S)
        subtitle = clean_text(sub_m.group(1)) if sub_m else ""
        dt_m = re.search(r'<time class="dt-published" datetime="([^"]+)"', h)
        is_draft = fn.startswith("draft_") or not dt_m

        body_md = parse(h)
        if not title:
            title = "Untitled"
        if not body_md.strip():
            print(f"  SKIP (empty body): {fn}")
            continue

        lines = ["---", "layout: post", f'title: "{fm_escape(title)}"']
        if subtitle:
            lines.append(f'subtitle: "{fm_escape(subtitle)}"')
        if dt_m:
            d = dt_m.group(1)[:10]
            lines.append(f"date: {d} 12:00:00")
        if not is_draft:
            lines.append("published: true")
        lines.append("---\n")
        content = "\n".join(lines) + body_md

        if is_draft:
            path = os.path.join(DRAFTS, slugify(title) + ".md")
        else:
            d = dt_m.group(1)[:10]
            path = os.path.join(POSTS, f"{d}-{slugify(title)}.md")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        made.append((os.path.basename(path), is_draft))
        print(f"  {'draft' if is_draft else 'post '}: {os.path.basename(path)}")

    print(f"\nconverted {len(made)} files")
    print("  posts :", sum(1 for _, d in made if not d))
    print("  drafts:", sum(1 for _, d in made if d))


if __name__ == "__main__":
    main()
