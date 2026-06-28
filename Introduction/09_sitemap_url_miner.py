"""Mine URLs and timestamps from an XML sitemap."""

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd
import requests


DEFAULT_SITEMAP = "https://www.python.org/sitemap.xml"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "sitemap_urls"
HEADERS = {"User-Agent": "api-web-mining-ds-learning/1.0"}


def fetch_sitemap_xml(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.text


def namespace(root: ET.Element) -> dict[str, str]:
    if root.tag.startswith("{"):
        uri = root.tag.split("}", 1)[0].strip("{")
        return {"sm": uri}
    return {"sm": ""}


def child_text(element: ET.Element, tag: str, ns: dict[str, str]) -> str:
    if ns["sm"]:
        child = element.find(f"sm:{tag}", ns)
    else:
        child = element.find(tag)
    return child.text.strip() if child is not None and child.text else ""


def parse_sitemap(xml_text: str) -> pd.DataFrame:
    root = ET.fromstring(xml_text)
    ns = namespace(root)
    url_nodes = root.findall("sm:url", ns) if ns["sm"] else root.findall("url")

    rows = [
        {
            "loc": child_text(node, "loc", ns),
            "lastmod": child_text(node, "lastmod", ns),
            "changefreq": child_text(node, "changefreq", ns),
            "priority": child_text(node, "priority", ns),
        }
        for node in url_nodes
    ]
    return pd.DataFrame(rows)


def mine_sitemap(url: str = DEFAULT_SITEMAP) -> pd.DataFrame:
    urls = parse_sitemap(fetch_sitemap_xml(url))
    urls["source_sitemap"] = url
    urls["path_depth"] = urls["loc"].str.strip("/").str.count("/")
    return urls


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    urls = mine_sitemap()

    csv_path = OUTPUT_DIR / "sitemap_urls.csv"
    urls.to_csv(csv_path, index=False)

    print(f"Mined {len(urls)} sitemap URLs")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
