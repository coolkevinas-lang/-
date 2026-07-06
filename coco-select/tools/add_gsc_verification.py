#!/usr/bin/env python3
from pathlib import Path
import re

path = Path("coco-select/index.html")
text = path.read_text(encoding="utf-8")

verification_tag = '<meta name="google-site-verification" content="R6BfLWhL9jACGlbXIGRZT1YiJXjtMyYlrnjdcRo97GI">'

# Keep the patch idempotent: remove any previous Search Console verification meta tag.
text = re.sub(
    r'\n?<meta\s+name=["\']google-site-verification["\'][^>]*>',
    '',
    text,
    flags=re.IGNORECASE,
)

anchor = '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
if anchor not in text:
    raise SystemExit("SEO V3 robots anchor not found; refusing unsafe patch")

text = text.replace(anchor, anchor + "\n" + verification_tag, 1)
path.write_text(text, encoding="utf-8")
print("Google Search Console verification tag added.")
