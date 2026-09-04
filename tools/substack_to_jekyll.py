"""Convert a Substack HTML export into Jekyll posts with localized images.

- Reads posts.csv for metadata (date, title, subtitle, published state).
- Reads posts/*.html for body content.
- Downloads/rewrites remote <img> to local assets.
  (Images were pre-downloaded to assets/img/raw by tools/dl_images.py)
- Emits clean Markdown to _posts/YYYY-MM-DD-slug.md with YAML front matter.
"""
import csv
import html
import os
import re
import sys
from html.parser import HTMLParser

SRC = r"C:\Users\jonna\Downloads\qSkDtWMjSxqYJZaKe1U4Fg"
SITE = r"C:\Users\jonna\blog"
POSTS_OUT = os.path.join(SITE, "_posts")
IMG_DIR = os.path.join(SITE, "assets", "img")
RAW_DIR = os.path.join(IMG_DIR, "raw")

os.makedirs(POSTS_OUT, exist_ok=True)

# Tags that are block-level and should get surrounding blank lines.
BLOCK = {
    "p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li",
    "blockquote", "pre", "hr", "figure", "figcaption", "table", "tr",
}

# Substack wraps code in <pre><code><code> ... </code></code></pre>
CODE_RE = re.compile(r"<pre[^>]*>(.*?)</pre>", re.S | re.I)
IMG_RE = re.compile(r"<img[^>]*>", re.I)
SRC_RE = re.compile(r'src="([^"]+)"')
ALT_RE = re.compile(r'alt="([^"]*)"')
HR_RE = re.compile(r"<div>\s*<hr>\s*</div>", re.I)
LINK_RE = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S | re.I)


def slugify(text, fallback="post"):
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:70] or fallback


def unescape_deep(s):
    """HTML-unescape repeatedly (Substack double-escapes code blocks)."""
    prev = None
    out = s
    for _ in range(4):
        if out == prev:
            break
        prev = out
        out = html.unescape(out)
    return out


class Converter(HTMLParser):
    """Streaming HTML -> Markdown converter."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.list_stack = []       # stack of 'ul'/'ol'
        self.li_open = False
        self.skip_depth = 0
        self.in_pre = 0
        self.in_code = 0
        self.pre_buf = []
        self.blocks = 0

    # --- helpers -------------------------------------------------
    def emit(self, text, block=False):
        if block:
            if self.out and self.out[-1] != "\n":
                self.out.append("\n")
            self.out.append("\n")
        self.out.append(text)

    def heading(self, level):
        self.emit("#" * level + " ", block=True)

    # --- handlers ------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("br",):
            self.out.append("  \n")
        elif tag == "hr":
            self.emit("---", block=True)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heading(int(tag[1]))
        elif tag == "p":
            self.emit("", block=True)
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "code" and self.in_pre == 0:
            self.out.append("`")
        elif tag == "a":
            self._href = a.get("href", "")
            self._atext = []
            self._ina = True
            self._a_has_img = False
        elif tag == "img":
            # Substack wraps images in an <a> lightbox link. In that case the
            # image markdown is emitted directly and the wrapper link dropped.
            if getattr(self, "_ina", False):
                self._a_has_img = True
            self._img(a)
        elif tag == "ul":
            self.emit("", block=True)
            self.list_stack.append(("ul", 0))
        elif tag == "ol":
            self.emit("", block=True)
            self.list_stack.append(("ol", 0))
        elif tag == "li":
            depth = len(self.list_stack)
            indent = "  " * (depth - 1)
            if self.list_stack and self.list_stack[-1][0] == "ol":
                self.list_stack[-1] = ("ol", self.list_stack[-1][1] + 1)
                marker = "%d." % self.list_stack[-1][1]
            else:
                marker = "-"
            self.out.append(indent + marker + " ")
            self.li_open = True
        elif tag == "blockquote":
            self.emit("", block=True)
            self._bq = True
        elif tag == "pre":
            self.in_pre += 1
            self.pre_buf = []
        elif tag in ("script", "style"):
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.emit("", block=True)
        elif tag == "p":
            self.emit("", block=True)
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "code" and self.in_pre == 0:
            self.out.append("`")
        elif tag == "a":
            text = "".join(getattr(self, "_atext", []) or [])
            href = getattr(self, "_href", "")
            is_img_link = getattr(self, "_a_has_img", False)
            # Drop Substack's lightbox <a> wrappers around images: the image
            # markdown was already emitted, so only emit text links.
            if is_img_link or not text.strip():
                if text.strip() and not is_img_link:
                    self.out.append(text)
            elif href:
                self.out.append("[%s](%s)" % (text.strip(), href))
            else:
                self.out.append(text)
            self._ina = False
            self._a_has_img = False
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self.emit("", block=True)
        elif tag == "li":
            self.out.append("\n")
            self.li_open = False
        elif tag == "blockquote":
            self._bq = False
            self.emit("", block=True)
        elif tag == "pre":
            self.in_pre = max(0, self.in_pre - 1)
            if self.in_pre == 0:
                code = unescape_deep("".join(self.pre_buf))
                code = re.sub(r"<[^>]+>", "", code).strip("\n")
                self.emit("```\n" + code + "\n```", block=True)
        elif tag in ("script", "style"):
            self.skip_depth = max(0, self.skip_depth - 1)

    def handle_data(self, data):
        if self.skip_depth:
            return
        if self.in_pre:
            self.pre_buf.append(data)
            return
        text = data
        if getattr(self, "_bq", False):
            lines = text.split("\n")
            text = "\n".join(
                ("> " + ln.strip()) if ln.strip() else "" for ln in lines
            )
        if getattr(self, "_ina", False):
            self._atext.append(text)
            return
        self.out.append(text)

    def _img(self, a):
        src = a.get("src", "")
        alt = a.get("alt", "")
        if not src:
            return
        fn = src.split("/")[-1].split("?")[0]
        local = os.path.join(RAW_DIR, fn)
        if os.path.exists(local):
            # Use a site-relative path (no leading slash) so it resolves under
            # GitHub Pages subpath baseurl (/fromthesimulation/). A leading slash
            # would bypass baseurl and 404.
            url = "assets/img/raw/" + fn
        else:
            url = src  # keep remote as fallback
        self.emit("![%s](%s)" % (alt, url), block=True)

    def result(self):
        text = "".join(self.out)
        # collapse >2 blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        # strip trailing spaces on lines
        text = "\n".join(ln.rstrip() for ln in text.split("\n"))
        return text.strip() + "\n"


def convert_html(raw):
    # Normalize Substack-specific wrappers first.
    raw = HR_RE.sub("<hr>", raw)
    # <div><hr></div> variants and stray hr containers
    raw = re.sub(r"<\s*hr\s*/?\s*>", "<hr>", raw, flags=re.I)
    c = Converter()
    c.feed(raw)
    c.close()
    return c.result()


def yaml_str(s):
    if s is None:
        return '""'
    s = str(s).strip().replace('"', '\\"')
    if s == "":
        return '""'
    return '"%s"' % s


def main():
    rows = list(csv.DictReader(open(os.path.join(SRC, "posts.csv"), encoding="utf-8")))
    written = []
    skipped = []

    for row in rows:
        pid = row["post_id"]
        html_path = os.path.join(SRC, "posts", pid + ".html")
        if not os.path.exists(html_path):
            skipped.append((pid, "no html"))
            continue

        raw = open(html_path, encoding="utf-8").read()
        if len(raw.strip()) < 20:
            skipped.append((pid, "empty body (%d bytes)" % len(raw)))
            continue

        title = row.get("title", "").strip() or pid
        subtitle = row.get("subtitle", "").strip()
        published = row.get("is_published", "").strip().lower() == "true"
        date_raw = row.get("post_date", "").strip()
        if date_raw:
            d = date_raw.split("T")[0]
            t = date_raw.split("T")[1][:8] if "T" in date_raw else "00:00:00"
        else:
            d, t = "1970-01-01", "00:00:00"

        # slug: use the Substack slug (part after the id) when meaningful
        short = pid.split(".", 1)[1] if "." in pid else pid
        slug = slugify(short) or slugify(title)

        body = convert_html(raw)

        fm = [
            "---",
            "layout: post",
            "title: %s" % yaml_str(title),
        ]
        if subtitle:
            fm.append("subtitle: %s" % yaml_str(subtitle))
        fm.append("date: %s %s" % (d, t))
        fm.append("categories: [imported]")
        fm.append("tags: [substack]")
        fm.append("published: %s" % ("true" if published else "false"))
        fm.append("substack_id: %s" % pid)
        fm.append("---")

        out_path = os.path.join(POSTS_OUT, "%s-%s.md" % (d, slug))
        content = "\n".join(fm) + "\n\n" + body
        open(out_path, "w", encoding="utf-8", newline="\n").write(content)
        written.append((out_path, title, published, len(body)))

    print("WROTE %d posts" % len(written))
    for p, t, pub, n in written:
        print("  [%s] %-60s %6d chars  %s" % ("P" if pub else "D", t[:60], n, os.path.basename(p)))
    if skipped:
        print("SKIPPED %d" % len(skipped))
        for pid, why in skipped:
            print("  ", pid, "->", why)


if __name__ == "__main__":
    main()
