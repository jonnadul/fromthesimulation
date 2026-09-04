"""Download all Substack-hosted post images into assets/img/raw (native Windows paths)."""
import os
import subprocess
import sys

DEST = r"C:\Users\jonna\blog\assets\img\raw"
os.makedirs(DEST, exist_ok=True)

URLS = [
    "https://substack-post-media.s3.amazonaws.com/public/images/7f084eef-fdc8-4ed7-a04b-54732e53641f_577x452.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/67d5771e-e315-49c5-a8b3-e18c3bebb77c_568x450.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/468ecb6b-6a45-480a-a37b-334e287ecf67_1732x974.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/1551dbc9-7d4c-48d6-9432-2c3dc1ecf0d6_1732x974.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/ba0b7544-b2df-4db0-8379-9167d8dde140_1280x720.jpeg",
    "https://substack-post-media.s3.amazonaws.com/public/images/614f2892-a63e-4a89-8620-42721eb24088_1528x492.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/c20addce-a23a-4ab1-abe9-766ed9967ce8_1215x661.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/e9a2eb1d-b454-4910-87ce-0e95f9bb7e66_1236x795.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/4ae50107-8d07-4154-8a96-e7608d16bae5_1116x445.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/db277e58-aa3d-4c0d-99e0-81401c425d95_1330x1004.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/710cc6f2-2206-46fc-80c9-9779fed98db5_899x548.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/b43917a4-1b9a-4f1c-bb25-861123d17694_1938x576.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/0f5936eb-76c4-4dc0-ae19-be6dad732102_1206x1913.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/12a47975-76cd-489d-b620-c44ef65039d5_1206x2622.png",
    "https://substack-post-media.s3.amazonaws.com/public/images/b76c55a3-a1ec-4c07-b686-5e3f8568ac18_2279x1001.png",
]

ok = 0
failed = []
for url in URLS:
    fn = url.split("/")[-1]
    out = os.path.join(DEST, fn)
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print("SKIP", fn, os.path.getsize(out), flush=True)
        ok += 1
        continue
    subprocess.run(["curl", "-sSL", "--max-time", "120", "-o", out, url])
    size = os.path.getsize(out) if os.path.exists(out) else 0
    if size > 1000:
        print("OK  ", fn, size, flush=True)
        ok += 1
    else:
        print("FAIL", fn, size, flush=True)
        failed.append(url)

print("downloaded %d / %d" % (ok, len(URLS)))
if failed:
    print("FAILED URLS:")
    for f in failed:
        print("  ", f)
    sys.exit(1)
