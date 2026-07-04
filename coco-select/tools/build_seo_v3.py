#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import struct
import zlib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SITE_DIR = ROOT / "coco-select"
INDEX = SITE_DIR / "index.html"
BASE = "https://coolkevinas-lang.github.io/-/coco-select/"
OG_URL = BASE + "assets/og/coco-select-og.png"
TODAY = "2026-07-04"

SLUGS = {
    "P001": "korena",
    "P002": "kissme",
    "P003": "bffect",
    "P004": "jiama-plus-size-bra",
    "P005": "s3-beauty",
    "P006": "6ixty-8ight",
    "P007": "dian-jing-pin",
    "P008": "esosomi-exosome",
    "P009": "puravida",
    "P010": "natural-miracle",
    "P011": "eva-hair-removal",
    "P012": "speio",
    "P013": "serlando",
    "P014": "isr-skin-health",
    "P015": "care-plus",
    "P016": "mcctill",
    "P017": "herbal-rabbit",
    "P018": "fu-jie",
}

EN_NAMES = {
    "P001": "KORENA",
    "P002": "KISSME",
    "P003": "BFFECT Skincare Lab",
    "P004": "Jiama Fuller-Bust Bra",
    "P005": "S3 Beauty",
    "P006": "6ixty 8ight",
    "P007": "Dian Jing Pin Jewelry",
    "P008": "ESOSOMI",
    "P009": "PuraVida",
    "P010": "Natural Miracle",
    "P011": "Eva Professional Salon",
    "P012": "Speio",
    "P013": "Serlando",
    "P014": "ISR SKIN Health",
    "P015": "CARE+",
    "P016": "McCTILL",
    "P017": "Herbal Rabbit",
    "P018": "Fu Jie",
}

EN_CATEGORY = {
    "美妝保養": "Beauty & Skincare",
    "內衣飾品": "Lingerie, Jewelry & Accessories",
}

EN_NEED = {
    "進階保養": "Advanced Skincare",
    "開架彩妝": "Drugstore Makeup",
    "精華保養": "Serum Skincare",
    "機能內著": "Functional Lingerie",
    "美妝補貨": "Beauty Replenishment",
    "日常內著": "Everyday Lingerie",
    "送禮飾品": "Gift Jewelry",
    "進階修護": "Advanced Repair",
    "保養補貨": "Skincare Replenishment",
    "自然保養": "Natural Skincare",
    "除毛護理": "Professional Grooming Service",
    "肌膚保養": "Skin Care",
    "美容保養": "Beauty Care",
    "肌膚健康": "Skin Health",
    "日常修護": "Daily Repair",
    "質感保養": "Premium-Feel Skincare",
    "草本護理": "Herbal Care",
    "私密護理": "Personal Care",
}

EN_DESC = {
    "P001": "A clearly positioned skincare choice for comparing daily hydration, repair-focused routines and skin-condition stability.",
    "P002": "A recognizable eye-makeup option suited to everyday looks, practical replenishment and budget-conscious decisions.",
    "P003": "A serum-focused choice suited to comparisons based on ingredients, current skin condition and daily routine steps.",
    "P004": "A functional lingerie choice focused on fuller-bust support, sizing and long-wear comfort.",
    "P005": "A beauty replenishment destination for shoppers comparing multiple skincare and makeup options in one trip.",
    "P006": "An everyday lingerie option centered on comfort, flexible styling and low-friction daily wear.",
    "P007": "A jewelry choice with clear use cases for anniversaries, birthdays and self-reward.",
    "P008": "An advanced-repair selection where formulation, evidence and individual skin compatibility should be checked before deciding.",
    "P009": "A skincare replenishment choice for shoppers who value sensory experience and routine consistency.",
    "P010": "A natural-skincare-oriented choice for shoppers prioritizing gentleness, daily use and ingredient understanding.",
    "P011": "A professional grooming service choice for summer, pre-travel preparation and routine appearance management.",
    "P012": "A skincare-focused choice suited to decisions based on current skin condition, routine steps and consistency.",
    "P013": "A beauty-care choice for shoppers who value appearance details and a more deliberate routine experience.",
    "P014": "A skin-health-oriented choice centered on clear needs, current skin condition and sustainable use.",
    "P015": "A daily-repair choice for dryness, seasonal transitions and gentleness-conscious routines.",
    "P016": "A premium-feel skincare choice for shoppers who value daily experience, design and ritual.",
    "P017": "A herbal-care-oriented choice with approachable positioning for everyday routines and natural-style content.",
    "P018": "A personal-care choice for shoppers considering cleansing habits, gentleness and everyday use context.",
}

CSS = r''':root{--bg:#f5efe1;--paper:#fffaf3;--ink:#1c1913;--muted:#645c4f;--gold:#b8893c;--wine:#92384b;--line:#dfd1b5;--shadow:0 22px 60px rgba(60,43,15,.09)}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 12% 0,rgba(255,255,255,.95),transparent 32%),linear-gradient(135deg,#fffdf8,var(--bg));color:var(--ink);font-family:Arial,"Microsoft JhengHei",sans-serif;line-height:1.72}.w{width:min(1040px,calc(100% - 36px));margin:auto}.top{display:flex;justify-content:space-between;gap:16px;align-items:center;padding:22px 0;border-bottom:1px solid var(--line)}.brand{font-weight:800;letter-spacing:.14em;text-decoration:none;color:var(--ink)}.topnav{display:flex;gap:14px;align-items:center}.lang,.back{color:var(--wine);font-weight:700;text-decoration:none}.crumb{padding:18px 0 0;color:var(--muted);font-size:.9rem}.crumb a{color:inherit}.hero{padding:64px 0 30px}.eyebrow{color:#7b5c29;font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase}.hero h1{font-family:Georgia,"DFKai-SB","標楷體",serif;font-size:clamp(2.35rem,7vw,5rem);line-height:1.04;margin:.16em 0 .28em}.lead{font-size:1.12rem;color:var(--muted);max-width:760px}.meta{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0}.pill{padding:7px 12px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.68)}.score{font-weight:800;color:var(--wine)}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:20px 0}.panel{padding:28px;border:1px solid var(--line);border-radius:24px;background:var(--paper);box-shadow:var(--shadow)}.panel h2{font-family:Georgia,"DFKai-SB","標楷體",serif;margin-top:0}.panel ul{margin-bottom:0}.cta{display:inline-block;margin-top:18px;padding:13px 20px;border-radius:999px;background:var(--wine);color:#fff;text-decoration:none;font-weight:800}.note{font-size:.9rem;color:var(--muted)}.related{padding:26px;margin:28px 0;border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.55)}.foot{padding:38px 0 52px;color:var(--muted);border-top:1px solid var(--line);margin-top:50px}.index-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding:20px 0 76px}.index-card{padding:22px;border:1px solid var(--line);border-radius:18px;background:var(--paper);text-decoration:none;color:var(--ink);box-shadow:0 12px 30px rgba(60,43,15,.05)}.index-card strong{display:block;font-family:Georgia,"DFKai-SB","標楷體",serif;font-size:1.18rem}.index-card span{color:var(--muted);font-size:.92rem}@media(max-width:760px){.grid,.index-grid{grid-template-columns:1fr}.hero{padding-top:48px}.panel{padding:22px}.top{align-items:flex-start}.topnav{flex-wrap:wrap;justify-content:flex-end}}'''


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def parse_items() -> list[dict[str, Any]]:
    text = INDEX.read_text(encoding="utf-8")
    marker = "const items ="
    pos = text.index(marker) + len(marker)
    arr_pos = text.index("[", pos)
    items, _ = json.JSONDecoder().raw_decode(text[arr_pos:])
    if len(items) != 18:
        raise RuntimeError(f"Expected 18 items, found {len(items)}")
    missing = [x["id"] for x in items if x["id"] not in SLUGS]
    if missing:
        raise RuntimeError(f"Missing slug mapping: {missing}")
    return items


def json_script(data: Any) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"


def review_schema(item: dict[str, Any], lang: str) -> dict[str, Any]:
    en = lang == "en"
    return {
        "@type": "Review",
        "name": "CO CO SELECT Editorial Review" if en else "CO CO SELECT 編輯評測",
        "reviewBody": EN_DESC[item["id"]] if en else item.get("whyWorthChoosing", item.get("description", "")),
        "reviewRating": {"@type": "Rating", "ratingValue": item["score"], "bestRating": 100, "worstRating": 0},
        "author": {"@type": "Organization", "name": "CO CO SELECT"},
    }


def product_schema(item: dict[str, Any], lang: str, url: str) -> dict[str, Any]:
    en = lang == "en"
    name = EN_NAMES[item["id"]] if en else item["name"]
    description = EN_DESC[item["id"]] if en else item["description"]
    category = (EN_CATEGORY.get(item["category"], item["category"]) + " / " + EN_NEED.get(item["need"], item["need"])) if en else item["category"] + " / " + item["need"]
    schema_type = "Service" if item["id"] == "P011" else "Product"
    return {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": name,
        "description": description,
        "category": category,
        "url": url,
        "review": review_schema(item, lang),
    }


def breadcrumb_schema(item: dict[str, Any], lang: str, url: str) -> dict[str, Any]:
    en = lang == "en"
    name = EN_NAMES[item["id"]] if en else item["name"]
    index_url = BASE + ("en/products/" if en else "products/")
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CO CO SELECT", "item": BASE + ("en/" if en else "")},
            {"@type": "ListItem", "position": 2, "name": "All Guides" if en else "全部選品", "item": index_url},
            {"@type": "ListItem", "position": 3, "name": name, "item": url},
        ],
    }


def page_html(item: dict[str, Any], lang: str) -> str:
    en = lang == "en"
    slug = SLUGS[item["id"]]
    url = BASE + ("en/products/" if en else "products/") + slug + "/"
    alt_url = BASE + ("products/" if en else "en/products/") + slug + "/"
    name = EN_NAMES[item["id"]] if en else item["name"]
    category = EN_CATEGORY.get(item["category"], item["category"]) if en else item["category"]
    need = EN_NEED.get(item["need"], item["need"]) if en else item["need"]
    desc = EN_DESC[item["id"]] if en else item["description"]
    title = f"{name} Review & Buying Guide | CO CO SELECT" if en else f"{name} 評價與選購指南｜CO CO SELECT"
    pros = item.get("pros", [])
    cons = item.get("cons", [])
    if en:
        pros_html = "".join(f"<li>{esc(x)}</li>" for x in [f"Clear positioning around {need}", "Easy to compare in a decision-first context", "Suitable for a curated shortlist"])
        cons_html = "".join(f"<li>{esc(x)}</li>" for x in ["Check individual fit and current product details", "Popularity does not guarantee personal suitability"])
        best_for = f"Shoppers whose actual needs match {need.lower()} and who value a clear, sustainable routine."
        not_for = "Shoppers choosing only by hype, the lowest price, or expecting an immediate one-time transformation."
        why = EN_DESC[item["id"]]
        alternative = "Compare nearby options in the full CO CO SELECT guide before deciding."
        heading_fit = "Who is it for?"
        heading_not = "Who may want to skip it?"
        heading_pros = "Reasons to consider"
        heading_cons = "What to check first"
        heading_why = "Why it made the shortlist"
        heading_alt = "A smarter way to decide"
        cta = "View current product information"
        note = "This is editorial decision support. Verify current product or service details before purchasing or booking."
        back = "All guides"
        lang_label = "繁體中文"
    else:
        pros_html = "".join(f"<li>{esc(x)}</li>" for x in pros)
        cons_html = "".join(f"<li>{esc(x)}</li>" for x in cons)
        best_for = item.get("bestFor", "依實際需求與使用情境評估的人")
        not_for = item.get("notFor", "只看熱門度、不考慮自身需求的人")
        why = item.get("whyWorthChoosing", item["description"])
        alternative = item.get("alternative", "可回到完整比較頁查看其他相近選擇。")
        heading_fit = "適合誰"
        heading_not = "不適合誰"
        heading_pros = "優點"
        heading_cons = "購買前留意"
        heading_why = "為什麼值得推薦"
        heading_alt = "怎麼選更聰明"
        cta = "查看目前商品資訊"
        note = "本頁為編輯選物與決策輔助；購買或預約前請再確認當前商品、服務、價格與適用資訊。"
        back = "全部選品"
        lang_label = "English"
    promo = item.get("promoUrl") or (BASE + "#featured")
    rel = ' rel="sponsored nofollow noopener noreferrer" target="_blank"' if item.get("promoUrl") else ""
    product_json = json_script(product_schema(item, lang, url))
    crumb_json = json_script(breadcrumb_schema(item, lang, url))
    locale = "en_US" if en else "zh_TW"
    alt_locale = "zh_TW" if en else "en_US"
    root_href = "../../../" if en else "../../"
    index_href = "../"
    lang_href = alt_url
    return f'''<!doctype html>
<html lang="{"en" if en else "zh-Hant"}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-TW" href="{BASE}products/{slug}/">
<link rel="alternate" hreflang="en" href="{BASE}en/products/{slug}/">
<link rel="alternate" hreflang="x-default" href="{BASE}en/products/{slug}/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="CO CO SELECT">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{locale}">
<meta property="og:locale:alternate" content="{alt_locale}">
<meta property="og:image" content="{OG_URL}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="CO CO SELECT">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{OG_URL}">
<link rel="stylesheet" href="{root_href}assets/product-v3.css">
{product_json}
{crumb_json}
</head>
<body>
<div class="w">
<header class="top"><a class="brand" href="{root_href}">CO CO SELECT</a><nav class="topnav"><a class="back" href="{index_href}">{back}</a><a class="lang" href="{lang_href}">{lang_label}</a></nav></header>
<nav class="crumb" aria-label="Breadcrumb"><a href="{root_href}">CO CO SELECT</a> › <a href="{index_href}">{back}</a> › <span>{esc(name)}</span></nav>
<main>
<section class="hero"><div class="eyebrow">{esc(need)}</div><h1>{esc(name)}</h1><p class="lead">{esc(desc)}</p><div class="meta"><span class="pill">{esc(category)}</span><span class="pill">{esc(need)}</span><span class="pill score">{"Editor score" if en else "推薦"} {item["score"]}{"" if en else " 分"}</span></div></section>
<section class="grid"><article class="panel"><h2>{heading_fit}</h2><p>{esc(best_for)}</p></article><article class="panel"><h2>{heading_not}</h2><p>{esc(not_for)}</p></article><article class="panel"><h2>{heading_pros}</h2><ul>{pros_html}</ul></article><article class="panel"><h2>{heading_cons}</h2><ul>{cons_html}</ul></article></section>
<section class="panel"><h2>{heading_why}</h2><p>{esc(why)}</p></section>
<section class="related"><h2>{heading_alt}</h2><p>{esc(alternative)}</p><a class="cta" href="{esc(promo)}"{rel}>{cta}</a><p class="note">{note}</p></section>
</main>
<footer class="foot">© 2026 CO CO SELECT · {"Curated choices for more confident decisions." if en else "少買錯，買得更聰明。"}</footer>
</div>
</body>
</html>'''


def item_list_schema(items: list[dict[str, Any]], lang: str) -> dict[str, Any]:
    en = lang == "en"
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "CO CO SELECT Curated Guides" if en else "CO CO SELECT 全部選品",
        "numberOfItems": len(items),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx,
                "name": EN_NAMES[x["id"]] if en else x["name"],
                "url": BASE + ("en/products/" if en else "products/") + SLUGS[x["id"]] + "/",
            }
            for idx, x in enumerate(items, 1)
        ],
    }


def index_page(items: list[dict[str, Any]], lang: str) -> str:
    en = lang == "en"
    base_href = "../../" if en else "../"
    title = "CO CO SELECT | All Curated Buying Guides" if en else "CO CO SELECT 全部選品｜18 個獨立選購指南"
    desc = "Browse 18 independent editorial buying guides across beauty, skincare, lingerie, jewelry and personal care." if en else "瀏覽 CO CO SELECT 18 個獨立美妝保養、內著、飾品與日常照護選購指南。"
    url = BASE + ("en/products/" if en else "products/")
    cards = []
    for x in items:
        name = EN_NAMES[x["id"]] if en else x["name"]
        need = EN_NEED.get(x["need"], x["need"]) if en else x["need"]
        cards.append(f'<a class="index-card" href="{SLUGS[x["id"]]}/"><strong>{esc(name)}</strong><span>{esc(need)} · {x["score"]}</span></a>')
    return f'''<!doctype html><html lang="{"en" if en else "zh-Hant"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="zh-TW" href="{BASE}products/"><link rel="alternate" hreflang="en" href="{BASE}en/products/"><link rel="alternate" hreflang="x-default" href="{BASE}en/products/"><meta property="og:type" content="website"><meta property="og:site_name" content="CO CO SELECT"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{OG_URL}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{OG_URL}"><link rel="stylesheet" href="{base_href}assets/product-v3.css">{json_script(item_list_schema(items, lang))}</head><body><div class="w"><header class="top"><a class="brand" href="{base_href}">CO CO SELECT</a><a class="lang" href="{BASE + ('products/' if en else 'en/products/')}">{'繁體中文' if en else 'English'}</a></header><main><section class="hero"><div class="eyebrow">{'All curated guides' if en else '18 independent guides'}</div><h1>{'All Guides' if en else '全部選品'}</h1><p class="lead">{esc(desc)}</p></section><nav class="index-grid">{''.join(cards)}</nav></main><footer class="foot">© 2026 CO CO SELECT</footer></div></body></html>'''


def png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def make_og_png(path: Path) -> None:
    width, height = 1200, 630
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            # Linen background with restrained wine/gold editorial geometry.
            if 70 < x < 1130 and 70 < y < 560:
                r, g, b = 255, 250, 240
            else:
                r, g, b = 245, 239, 225
            if (x - 940) ** 2 + (y - 170) ** 2 < 115 ** 2:
                r, g, b = 146, 56, 75
            if 110 < x < 520 and 390 < y < 420:
                r, g, b = 184, 137, 60
            if 110 < x < 560 and 190 < y < 208:
                r, g, b = 28, 25, 19
            row.extend((r, g, b))
        rows.append(bytes(row))
    raw = b"".join(rows)
    png = b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) + png_chunk(b"IDAT", zlib.compress(raw, 9)) + png_chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


def patch_home(items: list[dict[str, Any]]) -> None:
    text = INDEX.read_text(encoding="utf-8")
    start, end = "<!-- SEO-V3-START -->", "<!-- SEO-V3-END -->"
    if start in text and end in text:
        text = re.sub(re.escape(start) + r"[\s\S]*?" + re.escape(end), "", text, count=1)
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "CO CO SELECT", "inLanguage": ["zh-TW", "en"]},
            {"@type": "CollectionPage", "@id": BASE + "#webpage", "url": BASE, "name": "CO CO SELECT｜少買錯，買得更聰明", "isPartOf": {"@id": BASE + "#website"}, "inLanguage": "zh-TW"},
            item_list_schema(items, "zh"),
        ],
    }
    block = f'''{start}
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="{BASE}">
<link rel="alternate" hreflang="zh-TW" href="{BASE}">
<link rel="alternate" hreflang="en" href="{BASE}en/">
<link rel="alternate" hreflang="x-default" href="{BASE}en/">
<link rel="manifest" href="./manifest.webmanifest">
<meta property="og:site_name" content="CO CO SELECT">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{OG_URL}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="CO CO SELECT">
<meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="CO CO SELECT｜少買錯，買得更聰明">
<meta name="twitter:description" content="從膚況、穿著感、生活情境到送禮需求，幫妳更快找到真正適合自己的選擇。">
<meta name="twitter:image" content="{OG_URL}">
{json_script(graph)}
{end}'''
    anchor = '<meta content="#f5efe1" name="theme-color"/>'
    if anchor not in text:
        raise RuntimeError("Homepage theme-color anchor not found; refusing unsafe patch")
    text = text.replace(anchor, anchor + "\n" + block, 1)
    INDEX.write_text(text, encoding="utf-8")


def write_sitemap(items: list[dict[str, Any]]) -> None:
    ns = 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml"'
    pairs = [(BASE, BASE + "en/"), (BASE + "products/", BASE + "en/products/")]
    pairs += [(BASE + "products/" + SLUGS[x["id"]] + "/", BASE + "en/products/" + SLUGS[x["id"]] + "/") for x in items]
    rows = ['<?xml version="1.0" encoding="UTF-8"?>', f"<urlset {ns}>"]
    for zh, en in pairs:
        for loc in (zh, en):
            rows.append("<url>")
            rows.append(f"<loc>{loc}</loc>")
            rows.append(f"<lastmod>{TODAY}</lastmod>")
            rows.append(f'<xhtml:link rel="alternate" hreflang="zh-TW" href="{zh}"/>')
            rows.append(f'<xhtml:link rel="alternate" hreflang="en" href="{en}"/>')
            rows.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{en}"/>')
            rows.append("</url>")
    rows.append("</urlset>")
    (SITE_DIR / "sitemap.xml").write_text("\n".join(rows) + "\n", encoding="utf-8")


def clean_v2() -> None:
    for rel in [
        "products/mcctill-guide",
        "en/products/p008-guide",
        "en/products/p011-guide",
        "en/products/p014-guide",
        "en/products/mcctill-guide",
    ]:
        p = SITE_DIR / rel
        if p.exists():
            shutil.rmtree(p)
    for rel in ["assets/product-renderer.js", "assets/product-data-a.js", "assets/product-data-b.js", "assets/product-extra.js"]:
        p = SITE_DIR / rel
        if p.exists():
            p.unlink()


def validate(items: list[dict[str, Any]]) -> None:
    expected = []
    for x in items:
        slug = SLUGS[x["id"]]
        expected += [SITE_DIR / "products" / slug / "index.html", SITE_DIR / "en" / "products" / slug / "index.html"]
    missing = [str(p.relative_to(ROOT)) for p in expected if not p.exists()]
    if missing:
        raise RuntimeError(f"Missing generated pages: {missing}")
    if "SEO-V3-START" not in INDEX.read_text(encoding="utf-8"):
        raise RuntimeError("Homepage SEO V3 block missing")
    sitemap = (SITE_DIR / "sitemap.xml").read_text(encoding="utf-8")
    if sitemap.count("<url>") != 40:
        raise RuntimeError(f"Expected 40 sitemap URLs, found {sitemap.count('<url>')}")


def main() -> None:
    items = parse_items()
    (SITE_DIR / "assets").mkdir(exist_ok=True)
    (SITE_DIR / "assets" / "product-v3.css").write_text(CSS + "\n", encoding="utf-8")
    make_og_png(SITE_DIR / "assets" / "og" / "coco-select-og.png")
    for item in items:
        slug = SLUGS[item["id"]]
        for lang in ("zh", "en"):
            out = SITE_DIR / ("en/products" if lang == "en" else "products") / slug / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page_html(item, lang), encoding="utf-8")
    (SITE_DIR / "products" / "index.html").write_text(index_page(items, "zh"), encoding="utf-8")
    (SITE_DIR / "en" / "products" / "index.html").write_text(index_page(items, "en"), encoding="utf-8")
    patch_home(items)
    write_sitemap(items)
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: " + BASE + "sitemap.xml\n", encoding="utf-8")
    (SITE_DIR / "SEARCH_CONSOLE_READY.md").write_text(
        "# CO CO SELECT Search Console Ready\n\n"
        f"- Property URL: `{BASE}`\n"
        f"- Sitemap URL: `{BASE}sitemap.xml`\n"
        "- Status: Technical files prepared. Ownership verification still requires a real Google-issued token or DNS verification.\n"
        "- Do not add a fake verification token.\n",
        encoding="utf-8",
    )
    clean_v2()
    validate(items)
    print("SEO V3 built successfully: 18 zh + 18 en static pages, 40 sitemap URLs.")


if __name__ == "__main__":
    main()
