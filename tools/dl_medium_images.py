#!/usr/bin/env python3
"""Download Medium CDN images from an export into assets/img/raw.

Medium export images live on cdn-images-1.medium.com with URLs like:
  https://cdn-images-1.medium.com/max/2560/desat/multiply/grey/60/overlay/grey/1*XXXX.png
The path prefix (max/2560/...) is just a resize/transform directive; we can
request the largest variant by using max/2000 or stripping the transform.
"""
import os, re, sys, time, urllib.request, hashlib

SRC = r"C:/Users/jonna/Downloads/medium-export-1fd04de1e27644ea14035a260fd0779a6d66e5772f0fe6fbe0298a34109430d8/posts"
DEST = r"C:/Users/jonna/fromthesimulation/assets/img/raw"
os.makedirs(DEST, exist_ok=True)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def candidates(url):
    """Return list of URLs to try, largest first."""
    # https://cdn-images-1.medium.com/max/800/1*ABC.png
    m = re.match(r'(https://cdn-images-\d+\.medium\.com)/(.+?)/(\d+\*[^/]+)$', url)
    if m:
        host, mid, fid = m.groups()
        return [f"{host}/max/2400/{fid}", f"{host}/max/1600/{fid}", url]
    return [url]


def fetch(url, dest):
    for u in candidates(url):
        for attempt in range(3):
            try:
                req = urllib.request.Request(u, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
                if len(data) < 1000:
                    raise ValueError(f"suspiciously small ({len(data)}B)")
                with open(dest, "wb") as f:
                    f.write(data)
                return len(data), u
            except Exception as e:
                if attempt == 2:
                    print(f"    fail {u}: {e}")
                time.sleep(1.5)
    return None, None


def main():
    total, ok, skipped, failed = 0, 0, 0, 0
    mapping = {}
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".html"):
            continue
        h = open(os.path.join(SRC, fn), encoding="utf-8").read()
        urls = re.findall(r'src="(https://cdn-images-\d+\.medium\.com/[^"]+)"', h)
        for u in set(urls):
            total += 1
            fid = u.rsplit("/", 1)[-1]          # e.g. 1*u9gEfWbI8N4uUBeuImKzxg.png
            safe = fid.replace("*", "_")
            dest = os.path.join(DEST, safe)
            mapping[u] = safe
            if os.path.exists(dest) and os.path.getsize(dest) > 1000:
                skipped += 1
                print(f"  exists  {safe}")
                continue
            n, used = fetch(u, dest)
            if n:
                ok += 1
                print(f"  ok      {safe} ({n//1024}KB)")
            else:
                failed += 1
                print(f"  FAILED  {u}")
    print(f"\nunique={total} downloaded={ok} cached={skipped} failed={failed}")
    import json
    with open(r"C:/Users/jonna/fromthesimulation/tools/medium_img_map.json", "w") as f:
        json.dump(mapping, f, indent=1)


if __name__ == "__main__":
    main()
