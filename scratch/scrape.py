#!/usr/bin/env python3
"""One-time content/image scraper for cloning sajesanctuary.com.
Stdlib only. Fetches raw HTML + a plain-text render of visible text for each
page, and downloads referenced images into ../images/.
"""
import json
import os
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://www.sajesanctuary.com"
HERE = Path(__file__).resolve().parent
RAW_DIR = HERE / "raw"
IMG_DIR = HERE.parent / "images"
CONTENT_DIR = HERE / "content"
for d in (RAW_DIR, IMG_DIR, CONTENT_DIR):
    d.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

PAGES = {
    "home": "/",
    "practitioners": "/practitioners",
    "resources": "/resources",
    "book": "/book",
    "offerings/akashic-record-readings": "/offerings/akashic-record-readings",
    "offerings/apothecary": "/offerings/apothecary",
    "offerings/astrology-readings": "/offerings/astrology-readings",
    "offerings/aura-photography": "/offerings/aura-photography",
    "offerings/breathwork": "/offerings/breathwork",
    "offerings/chakra-balancing": "/offerings/chakra-balancing",
    "offerings/dream-interpretation": "/offerings/dream-interpretation",
    "offerings/energetic-signature": "/offerings/energetic-signature",
    "offerings/magdalene-reiki": "/magdalene-reiki",
    "offerings/reiki-energy-healing": "/offerings/reiki-energy-healing",
    "offerings/sound-alchemy": "/offerings/sound-alchemy",
    "offerings/spirit-guide": "/offerings/spirit-guide",
    "offerings/tarot-oracle-readings": "/offerings/tarot-oracle-readings",
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


class TextExtractor(HTMLParser):
    SKIP_TAGS = {"script", "style", "noscript", "template", "svg", "header", "footer", "nav"}

    def __init__(self):
        super().__init__()
        self.skip_depth = 0
        self.chunks = []
        self.in_main = 0
        self.main_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "main" or (tag == "article"):
            self.in_main += 1
        if self.in_main:
            self.main_depth += 1
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        if tag == "br":
            self.chunks.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1
        if self.in_main:
            self.main_depth -= 1
            if tag in ("main", "article") and self.main_depth <= 0:
                self.in_main -= 1

    def handle_data(self, data):
        if self.skip_depth:
            return
        if not self.in_main:
            return
        text = data.strip()
        if text:
            self.chunks.append(text)


def extract_text(html):
    p = TextExtractor()
    p.feed(html)
    lines = []
    for c in p.chunks:
        if c == "\n":
            continue
        lines.append(c)
    # de-dup consecutive repeats (Squarespace often doubles nav/link text)
    deduped = []
    for l in lines:
        if not deduped or deduped[-1] != l:
            deduped.append(l)
    return "\n".join(deduped)


IMG_RE = re.compile(r'<img[^>]+src="([^"]+)"[^>]*>')
ALT_RE = re.compile(r'alt="([^"]*)"')


def extract_images(html):
    found = []
    for m in re.finditer(r'<img[^>]+>', html):
        tag = m.group(0)
        src_m = re.search(r'src="([^"]+)"', tag)
        if not src_m:
            continue
        src = src_m.group(1)
        if src.startswith("//"):
            src = "https:" + src
        if "squarespace-cdn.com" not in src:
            continue
        alt_m = ALT_RE.search(tag)
        found.append({"src": src, "alt": alt_m.group(1) if alt_m else ""})
    return found


def slugify(url):
    name = url.split("/")[-1].split("?")[0]
    return name


def download_image(url, dest_dir=IMG_DIR):
    name = slugify(url)
    if not name:
        return None
    dest = dest_dir / name
    if dest.exists():
        return dest.name
    # request a reasonably large but not huge size
    base_url = url.split("?")[0]
    fetch_url = base_url + "?format=1500w"
    try:
        req = urllib.request.Request(fetch_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        dest.write_bytes(data)
        return dest.name
    except Exception as e:
        print(f"  ! failed {fetch_url}: {e}")
        return None


def main():
    manifest = {}
    all_images = {}
    for key, path in PAGES.items():
        url = BASE + path
        print(f"Fetching {url}")
        try:
            html = fetch(url)
        except Exception as e:
            print(f"  ! failed to fetch {url}: {e}")
            continue
        safe_key = key.replace("/", "__")
        (RAW_DIR / f"{safe_key}.html").write_text(html, encoding="utf-8")
        text = extract_text(html)
        images = extract_images(html)
        for img in images:
            all_images[img["src"]] = img["alt"]
        (CONTENT_DIR / f"{safe_key}.txt").write_text(text, encoding="utf-8")
        (CONTENT_DIR / f"{safe_key}.images.json").write_text(json.dumps(images, indent=2), encoding="utf-8")
        manifest[key] = {"url": url, "images": len(images), "text_len": len(text)}

    print(f"\nDownloading {len(all_images)} unique images...")
    downloaded = {}
    for i, (src, alt) in enumerate(all_images.items(), 1):
        fname = download_image(src)
        if fname:
            downloaded[src] = fname
        if i % 10 == 0:
            print(f"  {i}/{len(all_images)}")

    (CONTENT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (CONTENT_DIR / "image_map.json").write_text(json.dumps(downloaded, indent=2), encoding="utf-8")
    print(f"\nDone. {len(downloaded)}/{len(all_images)} images downloaded to {IMG_DIR}")


if __name__ == "__main__":
    main()
