#!/usr/bin/env python3
"""Fetch Public Domain / CC real photos via Wikimedia Commons & NASA Images API (v2.1).

Usage:
    python3 tools/fetch_real_assets.py --out assets_raw/real \
      --query "apollo:nasa:Apollo 11 Moon landing" \
      --query "saturn5:wiki:Saturn V launch NASA"
    # Or pass --targets targets.json: [{"name":"apollo","kind":"nasa","queries":["Apollo 11"]}]
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.parse

UA = "VoxRemotionSkill/2.1 (research; community) curl"


def curl_json(url):
    r = subprocess.run(
        ["curl", "-sL", "--max-time", "20", "-A", UA, url],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed {r.returncode}: {url}\n{r.stderr[:300]}")
    return json.loads(r.stdout)


def curl_dl(url, dest):
    r = subprocess.run(
        ["curl", "-sL", "--max-time", "60", "-A", UA, "-o", dest, url],
        capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(dest) or os.path.getsize(dest) < 5000:
        raise RuntimeError(f"download failed {url}: rc={r.returncode} size="
                           f"{os.path.getsize(dest) if os.path.exists(dest) else 0}")
    return dest


def wiki_search(query, want_ext=("jpg", "jpeg")):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrnamespace": "6", "gsrlimit": "6",
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": "1200",
    })
    data = curl_json(f"https://commons.wikimedia.org/w/api.php?{q}")
    out = []
    for p in (data.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        if not any(mime.endswith(e) for e in want_ext):
            continue
        lic = ((ii.get("extmetadata") or {}).get("LicenseShortName") or {}).get("value", "?")
        out.append({"title": p.get("title"), "url": ii.get("thumburl") or ii.get("url"),
                    "orig": ii.get("url"), "width": ii.get("width"),
                    "height": ii.get("height"), "license": lic, "source": "wikimedia"})
    return out


def nasa_search(query):
    q = urllib.parse.urlencode({"q": query, "media_type": "image", "page_size": "6"})
    data = curl_json(f"https://images-api.nasa.gov/search?{q}")
    out = []
    for it in data.get("collection", {}).get("items", []):
        d = (it.get("data") or [{}])[0]
        href = it.get("href", "")
        # href is a collection.json listing asset files; fetch it
        try:
            files = curl_json(href)
        except Exception as e:
            print("  nasa collection fetch failed:", e)
            continue
        # prefer ~medium.jpg, else ~small.jpg, else first jpg
        pick = None
        for f in files:
            if "~medium.jpg" in f:
                pick = f
                break
        if not pick:
            for f in files:
                if "~small.jpg" in f:
                    pick = f
                    break
        if not pick:
            pick = next((f for f in files if f.lower().endswith(".jpg")), None)
        if pick:
            out.append({"title": d.get("title"), "nasa_id": d.get("nasa_id"),
                        "url": pick, "source": "nasa",
                        "license": "NASA public domain"})
    return out


def run_fetch(targets, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    manifest = {}
    for item in targets:
        name = item["name"]
        kind = item.get("kind", "wiki")
        queries = item.get("queries", [])
        dest = os.path.join(out_dir, f"{name}.jpg")
        got = None
        for query in queries:
            try:
                cands = nasa_search(query) if kind == "nasa" else wiki_search(query)
            except Exception as e:
                print(f"[{name}] query {query!r} failed: {e}")
                continue
            for c in cands:
                try:
                    curl_dl(c["url"], dest)
                    got = c
                    print(f"[{name}] OK {c['title']} via {query!r} -> {c['url']}")
                    break
                except Exception as e:
                    print(f"[{name}] download failed {c['url']}: {e}")
            if got:
                break
        if got:
            manifest.setdefault(name, got)
            manifest[name]["file"] = os.path.join(out_dir, f"{name}.jpg")
        else:
            print(f"[{name}] FAILED all queries")

    sources_path = os.path.join(out_dir, "SOURCES.json")
    with open(sources_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("manifest:", json.dumps({k: v.get("title") for k, v in manifest.items()}, ensure_ascii=False))
    print("done, files:", sorted(os.listdir(out_dir)))


def main():
    parser = argparse.ArgumentParser(description="Fetch real Wikimedia/NASA images for any VOX topic")
    parser.add_argument("--out", default="assets_raw/real", help="Output folder")
    parser.add_argument("--targets", help="JSON file of [{name, kind, queries}]")
    parser.add_argument("--query", action="append", default=[], help="Format: name:nasa|wiki:query")
    args = parser.parse_args()

    targets = []
    if args.targets:
        with open(args.targets, encoding="utf-8") as f:
            targets.extend(json.load(f))
    for q in args.query:
        parts = q.split(":", 2)
        if len(parts) != 3:
            raise ValueError(f"Invalid --query format (expected name:nasa|wiki:query): {q}")
        targets.append({"name": parts[0], "kind": parts[1], "queries": [parts[2]]})
    if not targets:
        parser.print_help()
        return 0
    run_fetch(targets, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
