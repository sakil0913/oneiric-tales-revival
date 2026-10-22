# -*- coding: utf-8 -*-
"""Fandom wiki dumper (stdlib only) — for Termux / Pydroid / any Python 3.

Usage:
    python wiki_dump.py                       # 默认抓 oneirictales/zh
    python wiki_dump.py --out ./dump
    python wiki_dump.py --proxy http://127.0.0.1:7890
    python wiki_dump.py --api https://oneirictales.fandom.com/api.php
    python wiki_dump.py --max 20              # 先抓 20 页试水

Outputs: siteinfo.json, titles.txt, pages.jsonl, images.json, categories.json
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request

UA = "OneiricTalesArchiver/1.0 (preservation research)"


class Api:
    def __init__(self, base, proxy=None, delay=0.2, timeout=60):
        self.base = base
        self.delay = delay
        self.timeout = timeout
        handlers = []
        if proxy:
            handlers.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
        self.opener = urllib.request.build_opener(*handlers)

    def get(self, **params):
        params.setdefault("format", "json")
        params.setdefault("formatversion", "2")
        qs = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        url = self.base + "?" + qs
        last = None
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with self.opener.open(req, timeout=self.timeout) as r:
                    return json.loads(r.read().decode("utf-8"))
            except Exception as e:  # noqa: BLE001
                last = e
                time.sleep(1.0 * (attempt + 1))
        raise RuntimeError("API failed: %s\n%s" % (url, last))

    def cont_of(self, resp):
        c = resp.get("continue")
        if not c:
            return {}
        return {k: v for k, v in c.items() if k != "continue"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="https://oneirictales.fandom.com/zh/api.php")
    ap.add_argument("--out", default="./dump")
    ap.add_argument("--proxy", default=os.environ.get("HTTPS_PROXY", ""))
    ap.add_argument("--max", type=int, default=0, help="limit pages (0 = all)")
    ap.add_argument("--delay", type=float, default=0.2)
    ap.add_argument("--skip-images", action="store_true")
    ap.add_argument("--ns", default="0,10", help="namespaces to scrape, e.g. 0,10")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    api = Api(args.api, args.proxy or None, args.delay)

    def w(name, text):
        with open(os.path.join(args.out, name), "w", encoding="utf-8") as f:
            f.write(text)
        print("   wrote", name, len(text), "chars")

    print("== API:", args.api)
    site = api.get(action="query", meta="siteinfo", siprop="general|statistics")
    w("siteinfo.json", json.dumps(site, ensure_ascii=False, indent=2))
    st = site.get("query", {}).get("statistics", {})
    print("== pages=%s images=%s" % (st.get("pages"), st.get("images")))

    # 1) titles
    print("== listing pages …")
    titles = []
    seen = set()
    nss = [n.strip() for n in str(args.ns).split(",") if n.strip() != ""]
    for ns in nss:
        cont = {}
        while True:
            r = api.get(action="query", list="allpages", aplimit="500", apnamespace=ns, **cont)
            for p in r.get("query", {}).get("allpages", []):
                if p["title"] not in seen:
                    seen.add(p["title"])
                    titles.append(p["title"])
            print("   ns=%s: %d" % (ns, len(titles)))
            if args.max and len(titles) >= args.max:
                titles = titles[: args.max]
                break
            cont = api.cont_of(r)
            if not cont:
                break
            time.sleep(args.delay)
        if args.max and len(titles) >= args.max:
            break
    w("titles.txt", "\n".join(titles))
    print("== total titles:", len(titles))

    # 2) wikitext
    print("== fetching content …")
    pages_path = os.path.join(args.out, "pages.jsonl")
    if os.path.exists(pages_path):
        os.remove(pages_path)
    batch = 50
    with open(pages_path, "a", encoding="utf-8") as fh:
        for i in range(0, len(titles), batch):
            group = titles[i:i + batch]
            r = api.get(action="query", prop="revisions", rvprop="content", rvslots="main",
                        titles="|".join(group))
            for p in r.get("query", {}).get("pages", []):
                if p.get("missing"):
                    continue
                text = ""
                rev = p.get("revisions")
                if rev and rev[0].get("slots", {}).get("main"):
                    text = rev[0]["slots"]["main"].get("content", "")
                fh.write(json.dumps({"title": p["title"], "ns": p.get("ns", 0), "text": text},
                                    ensure_ascii=False) + "\n")
            print("   %d/%d" % (min(i + batch, len(titles)), len(titles)))
            time.sleep(args.delay)

    # 3) images
    if not args.skip_images:
        print("== listing images …")
        imgs = []
        cont = {}
        while True:
            r = api.get(action="query", list="allimages", ailimit="500",
                        aiprop="url|size|mime", **cont)
            imgs.extend(r.get("query", {}).get("allimages", []))
            cont = api.cont_of(r)
            if not cont:
                break
            time.sleep(args.delay)
        w("images.json", json.dumps(imgs, ensure_ascii=False, indent=1))
        print("== images:", len(imgs))

    # 4) categories
    try:
        cats = []
        cont = {}
        while True:
            r = api.get(action="query", list="allcategories", aclimit="500", **cont)
            cats.extend(c.get("category") for c in r.get("query", {}).get("allcategories", []))
            cont = api.cont_of(r)
            if not cont:
                break
            time.sleep(args.delay)
        w("categories.json", json.dumps(cats, ensure_ascii=False, indent=1))
    except Exception as e:  # noqa: BLE001
        print("!! categories failed (ignored):", e)

    print("\nDone. Output:", os.path.abspath(args.out))
    print("把整个目录给我即可（pages.jsonl 是关键；图片我从 CDN 自己下）。")


if __name__ == "__main__":
    sys.exit(main())
