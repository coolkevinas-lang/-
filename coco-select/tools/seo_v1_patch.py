from pathlib import Path

INDEX = Path("coco-select/index.html")
START = "<!-- SEO-V1-START -->"
END = "<!-- SEO-V1-END -->"

text = INDEX.read_text(encoding="utf-8")

if START in text:
    print("SEO V1 block already present; no changes needed.")
    raise SystemExit(0)

anchor = '<meta content="#f5efe1" name="theme-color"/>'
if anchor not in text:
    raise RuntimeError("Expected theme-color anchor not found; refusing unsafe patch.")

seo_block = r'''<!-- SEO-V1-START -->
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<link rel="canonical" href="https://coolkevinas-lang.github.io/-/coco-select/"/>
<link rel="alternate" hreflang="zh-TW" href="https://coolkevinas-lang.github.io/-/coco-select/"/>
<link rel="alternate" hreflang="en" href="https://coolkevinas-lang.github.io/-/coco-select/en/"/>
<link rel="alternate" hreflang="x-default" href="https://coolkevinas-lang.github.io/-/coco-select/en/"/>
<link rel="manifest" href="./manifest.webmanifest"/>
<meta property="og:site_name" content="CO CO SELECT"/>
<meta property="og:url" content="https://coolkevinas-lang.github.io/-/coco-select/"/>
<meta property="og:locale:alternate" content="en_US"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="CO CO SELECT｜少買錯，買得更聰明"/>
<meta name="twitter:description" content="從膚況、穿著感、生活情境到送禮需求，幫妳更快找到真正適合自己的選擇。"/>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://coolkevinas-lang.github.io/-/coco-select/#website",
      "url": "https://coolkevinas-lang.github.io/-/coco-select/",
      "name": "CO CO SELECT",
      "description": "精選美妝保養、內衣與飾品，以清楚分類、推薦理由與快速決策，幫助使用者找到更適合自己的選擇。",
      "inLanguage": ["zh-TW", "en"]
    },
    {
      "@type": "CollectionPage",
      "@id": "https://coolkevinas-lang.github.io/-/coco-select/#webpage",
      "url": "https://coolkevinas-lang.github.io/-/coco-select/",
      "name": "CO CO SELECT｜少買錯，買得更聰明",
      "description": "從膚況、穿著感、生活情境到送禮需求，幫妳更快找到真正適合自己的選擇。",
      "isPartOf": {"@id": "https://coolkevinas-lang.github.io/-/coco-select/#website"},
      "inLanguage": "zh-TW"
    }
  ]
}
</script>
<!-- SEO-V1-END -->'''

patched = text.replace(anchor, anchor + "\n" + seo_block, 1)
INDEX.write_text(patched, encoding="utf-8")
print("Injected SEO V1 metadata into coco-select/index.html")
