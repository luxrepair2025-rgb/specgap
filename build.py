#!/usr/bin/env python3
"""Regenerates the HTML pages, sitemap.xml, robots.txt and site.webmanifest.
Optional: the generated files are already included. Re-run after changing SITE_URL,
CHANNEL_URL, or videos.js (to refresh the SEO VideoObject data): python3 build.py"""
# ===================== EDIT THESE PLACEHOLDERS =====================
SITE_URL    = "https://luxrepair2025-rgb.github.io/specgap"  # Live URL, no trailing slash. For a custom domain at root use e.g. "https://www.specgap.com"
CHANNEL_URL = "https://www.youtube.com/@specgap"             # YouTube channel URL
EMAIL       = "hello@specgap.com"                            # PLACEHOLDER contact email
# ===================================================================
import json, re, html, datetime, pathlib
from urllib.parse import urlparse
ROOT = pathlib.Path(__file__).parent
BASE_PATH = urlparse(SITE_URL).path.rstrip("/") + "/"   # "/specgap/" on GitHub Pages, "/" on a root domain
src = (ROOT/"videos.js").read_text()
_m = re.search(r"window\.SPECGAP_VIDEOS\s*=\s*(\[.*?\])\s*;", src, re.S)
_arr = re.sub(r"/\*.*?\*/", "", _m.group(1), flags=re.S)
_arr = re.sub(r"(?m)^\s*//.*$", "", _arr)
_arr = re.sub(r",\s*([\]}])", r"\1", _arr)
VIDEOS = json.loads(_arr)
VIDEOS.sort(key=lambda v: v["date"], reverse=True)
TODAY = datetime.date.today().isoformat()
e = html.escape
NAV = [("index.html","Home"),("videos.html","Videos"),("tests.html","Tests"),("about.html","About"),("contact.html","Contact")]
ORG = {"@context":"https://schema.org","@type":"Organization","@id":SITE_URL+"/#org","name":"Spec Gap","url":SITE_URL+"/",
       "logo":SITE_URL+"/assets/img/logo.png","slogan":"Know the difference","sameAs":[CHANNEL_URL]}
WEB = {"@context":"https://schema.org","@type":"WebSite","@id":SITE_URL+"/#website","name":"Spec Gap","url":SITE_URL+"/","publisher":{"@id":SITE_URL+"/#org"},"inLanguage":"en"}

def url(f): return SITE_URL+"/" + ("" if f=="index.html" else f)
def video_ld(v):
    return {"@context":"https://schema.org","@type":"VideoObject","name":v["title"],"description":v["description"],
            "thumbnailUrl":[f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"],"uploadDate":v["date"],
            "contentUrl":f"https://www.youtube.com/watch?v={v['id']}","embedUrl":f"https://www.youtube.com/embed/{v['id']}",
            "genre":v["category"],"publisher":{"@id":SITE_URL+"/#org"}}
def ld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False).replace("</","<\\/")+'</script>'

def page(f, title, desc, body, name, extra_ld=()):
    crumbs = [("index.html","Home")] + ([] if f=="index.html" else [(f,name)])
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":url(p)} for i,(p,n) in enumerate(crumbs)]}
    lds = [ORG, WEB, bc] if f=="index.html" else [ORG, bc]
    lds += list(extra_ld)
    nav = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p==f else ""}>{n}</a></li>' for p,n in NAV)
    out = f'''<!doctype html>
<html lang="en" data-channel="{e(CHANNEL_URL)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url(f)}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#0a0a0b">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Spec Gap">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url(f)}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Spec Gap logo: Know the difference">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE_URL}/assets/img/og-image.jpg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/img/favicon-16.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://i.ytimg.com">
<link rel="stylesheet" href="css/style.css">
{chr(10).join(ld(o) for o in lds)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<a class="brand" href="index.html" aria-label="Spec Gap home"><img src="assets/img/logo-600.png" alt="Spec Gap" width="600" height="249"></a>
<nav aria-label="Main"><button class="menu-btn" aria-expanded="false" aria-controls="menu" aria-label="Toggle menu">&#9776;</button><ul id="menu">{nav}</ul></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site"><div class="wrap">
<div><img src="assets/img/logo-600.png" alt="Spec Gap" width="600" height="249" loading="lazy"><p>&copy; <span id="year">{TODAY[:4]}</span> Spec Gap. Know the difference.</p></div>
<ul>{nav}<li><a href="{e(CHANNEL_URL)}" target="_blank" rel="noopener">YouTube</a></li></ul>
</div></footer>
<script src="videos.js" defer></script>
<script src="js/main.js" defer></script>
</body>
</html>
'''
    (ROOT/f).write_text(out)

def head(name, h1, p):
    return f'''<div class="page-head"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="index.html">Home</a></li><li aria-current="page">{name}</li></ol></nav>
<h1>{h1}</h1><p>{p}</p></div></div>'''

SUB = f'''<section><div class="wrap"><div class="cta-band"><div><h2>Never miss a test</h2><p>New reviews and real-world challenges on YouTube. Subscribe so you know the difference before you buy.</p></div>
<a class="btn btn-red" href="{e(CHANNEL_URL)}?sub_confirmation=1" target="_blank" rel="noopener">&#9654; Subscribe on YouTube</a></div></div></section>'''

EMPTY = f'''<div class="soon"><span class="eyebrow">Coming soon</span><h2>First tests coming soon</h2><p>The channel is just getting started. Subscribe now to catch the first reviews and challenges the moment they go live.</p>
<a class="btn btn-red btn-lg" href="{e(CHANNEL_URL)}?sub_confirmation=1" target="_blank" rel="noopener">&#9654; Subscribe on YouTube</a>
<div class="grid teasers">
<div class="card teaser"><div class="tz" aria-hidden="true">&#9981;</div><span class="tag">Tank Test</span><h3>How far on one tank?</h3><p>Fill it up and drive until it's empty.</p></div>
<div class="card teaser"><div class="tz" aria-hidden="true">&#9878;</div><span class="tag">Head to Head</span><h3>Is the price gap worth it?</h3><p>Two rivals on the same roads.</p></div>
<div class="card teaser"><div class="tz" aria-hidden="true">&#128269;</div><span class="tag">Review</span><h3>Honest full reviews</h3><p>The cars people actually buy.</p></div>
<div class="card teaser"><div class="tz" aria-hidden="true">&#127937;</div><span class="tag">Challenge</span><h3>Top Gear-style challenges</h3><p>Simple rules, a stopwatch and plenty of opinions.</p></div>
</div></div>'''
page("index.html","Spec Gap | Real-World Car Reviews & Top Gear-Style Tests",
 "Spec Gap reviews cars and runs real-world, Top Gear-style tests like how far you can go on one tank of gas. Know the difference before you buy.",
 f'''<section class="hero"><div class="wrap">
<img class="logo" src="assets/img/logo.png" alt="Spec Gap logo: brake disc with red caliper, tagline Know the Difference" width="983" height="408" fetchpriority="high">
<h1>Real-world car reviews and tests</h1>
<p>Brochures give you numbers. We go out and check them. Spec Gap runs honest, Top Gear-style tests, like how far a car really goes on one tank, so you can see the gap between the spec sheet and the road.</p>
<div class="cta"><a class="btn btn-red" href="videos.html">Watch the videos</a><a class="btn btn-ghost" href="{e(CHANNEL_URL)}" target="_blank" rel="noopener">YouTube channel</a></div>
</div></section>
{'' if not any(v.get('featured') for v in VIDEOS) else '''<section aria-labelledby="ft"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Featured tests</span><h2 id="ft">Put to the test</h2></div><a class="btn btn-ghost" href="tests.html">How we test</a></div>
<div class="grid" id="featured-videos"></div></div></section>'''}
<section aria-labelledby="fmt"><div class="wrap"><span class="eyebrow">What we do</span><h2 id="fmt">Our test formats</h2>
<div class="grid" style="margin-top:1.5rem">
<a class="card feature" href="videos.html?category=Tank%20Test" style="text-decoration:none"><div class="icon" aria-hidden="true">&#9981;</div><h3>Tank Tests</h3><p>One full tank, one fixed route, driven until it's empty. Real range compared with the claimed figure.</p></a>
<a class="card feature" href="videos.html?category=Head%20to%20Head" style="text-decoration:none"><div class="icon" aria-hidden="true">&#9878;</div><h3>Head to Head</h3><p>Two rivals, the same roads and the same tests. Find out if the spec gap is worth the price gap.</p></a>
<a class="card feature" href="videos.html?category=Review" style="text-decoration:none"><div class="icon" aria-hidden="true">&#128269;</div><h3>Reviews</h3><p>Honest, in-depth reviews of the cars people actually buy, looking at comfort, tech, space and running costs.</p></a>
<a class="card feature" href="videos.html?category=Challenge" style="text-decoration:none"><div class="icon" aria-hidden="true">&#127937;</div><h3>Challenges</h3><p>Top Gear-style challenges with simple rules, a stopwatch and plenty of opinions.</p></a>
</div></div></section>
<section aria-labelledby="lv"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Latest</span><h2 id="lv">Latest videos</h2></div><a class="btn btn-ghost" href="videos.html">All videos &rarr;</a></div>
{'<div class="grid" id="latest-videos"></div>' if VIDEOS else '<div id="latest-videos">'+EMPTY+'</div>'}</div></section>
{SUB}''',"Home")

static_cards = EMPTY if not VIDEOS else "".join(f'''<article class="card video"><a href="https://www.youtube.com/watch?v={e(v['id'])}" target="_blank" rel="noopener"><div class="thumb"><img src="https://i.ytimg.com/vi/{e(v['id'])}/hqdefault.jpg" alt="Thumbnail for {e(v['title'])}" loading="lazy" width="480" height="360"></div><div class="body"><h3>{e(v['title'])}</h3><p>{e(v['description'])}</p></div></a></article>''' for v in VIDEOS)
page("videos.html","Videos | Car Reviews, Tank Tests & Challenges | Spec Gap",
 "Browse every Spec Gap video: car reviews, one-tank range tests, head-to-head comparisons and Top Gear-style challenges. Filter by category and watch on YouTube.",
 head("Videos","All videos","Every review, tank test and challenge in one place. Choose a category, then click a thumbnail to watch on YouTube.")+
 f'''<section><div class="wrap"><div class="filters" id="filters"{' hidden' if not VIDEOS else ''} role="group" aria-label="Filter videos by category"></div>
<p class="meta" id="count" aria-live="polite"></p>
<div class="{'grid' if VIDEOS else ''}" id="all-videos">{static_cards}</div></div></section>{SUB}''',"Videos",
 extra_ld=([] if not VIDEOS else [{"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"https://www.youtube.com/watch?v={v['id']}"} for i,v in enumerate(VIDEOS)]}]+[video_ld(v) for v in VIDEOS]))

page("tests.html","Our Test Formats | How Spec Gap Tests Cars",
 "How Spec Gap tests cars: one-tank range runs, head-to-head comparisons, in-depth reviews and Top Gear-style challenges, with consistent methods you can trust.",
 head("Tests","How we test","Same routes, same rules, honest results. Here's what goes into each Spec Gap format.")+
 '''<section><div class="wrap prose">
<article class="card test"><div class="num">01</div><div><h2 style="margin-top:0">Tank Test</h2><p>We fill the tank to the first click, reset the trip computer and drive a mixed route at legal, realistic speeds until the car runs dry or reaches a safe stopping point. Then we compare the real range and economy with the manufacturer's claim.</p></div></article>
<article class="card test"><div class="num">02</div><div><h2 style="margin-top:0">Head to Head</h2><p>Two rivals, same day, same roads. We compare performance, comfort, practicality, tech and value, then decide whether the spec gap is worth the price gap.</p></div></article>
<article class="card test"><div class="num">03</div><div><h2 style="margin-top:0">Full Review</h2><p>A detailed look at one car covering how it drives, what it's like to live with, what it costs to run and who it's for. We give honest verdicts with no hype.</p></div></article>
<article class="card test"><div class="num">04</div><div><h2 style="margin-top:0">Challenges</h2><p>Top Gear-style challenges with simple rules: cold starts, boot-space tests, budget builds and anything else worth arguing about. Entertaining, but still fair.</p></div></article>
<h2>Our principles</h2><ul><li>Consistent routes and conditions wherever possible</li><li>We always state how a test was run</li><li>Safety and the law come first</li><li>We tell you when a car isn't loaned or sponsored, and when it is</li></ul>
<p><a class="btn btn-red" href="videos.html">See the tests in action</a></p></div></section>''',"Tests")

page("about.html","About Spec Gap | Independent Car Review Channel",
 "Spec Gap is an independent YouTube channel that reviews cars and runs real-world tests to show the gap between the spec sheet and the road.",
 head("About","About Spec Gap","A small, independent channel with one simple question: does the car live up to its spec?")+
 f'''<section><div class="wrap prose">
<h2>Know the difference</h2><p>Every car comes with a list of numbers covering range, economy, power and space. Spec Gap exists to find out how those numbers hold up in the real world. We take cars out on real roads, run repeatable tests and report what we find.</p>
<h2>Why we started</h2><p>We grew up on shows that made car testing fun, and we wanted to bring that spirit to the cars normal people actually drive. We keep the tests simple and the results honest.</p>
<h2>Get involved</h2><p>Got a car you want tested, or a challenge idea? <a href="contact.html">Get in touch</a>, or join us on <a href="{e(CHANNEL_URL)}" target="_blank" rel="noopener">YouTube</a>.</p>
<p class="note">Placeholder copy. Replace with your own story, team names and photos.</p></div></section>{SUB}''',"About")

page("contact.html","Contact Spec Gap | Test Ideas, Collaborations & Press",
 "Contact Spec Gap with test ideas, car loans, brand collaborations or press enquiries.",
 head("Contact","Get in touch","Test ideas, car loans, collaborations or press: we'd love to hear from you.")+
 f'''<section><div class="wrap">
<p>Email us directly: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<form action="mailto:{EMAIL}" method="post" enctype="text/plain">
<!-- PLACEHOLDER FORM: on Netlify add the attribute data-netlify="true" and name="contact" and remove action; or point action at Formspree etc. -->
<div><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
<div><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
<div><label for="topic">Topic</label><select id="topic" name="topic"><option>Test idea</option><option>Car loan / collaboration</option><option>Press</option><option>Other</option></select></div>
<div><label for="msg">Message</label><textarea id="msg" name="message" rows="6" required></textarea></div>
<div><button class="btn btn-red" type="submit">Send message</button></div>
<p class="note">This form currently opens your email app. It can be connected to a form service when the site goes live.</p>
</form></div></section>''',"Contact")

(ROOT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+
  "".join(f"  <url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if p=='index.html' else '0.8'}</priority></url>\n" for p,_ in NAV)+"</urlset>\n")
(ROOT/"robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
(ROOT/"site.webmanifest").write_text(json.dumps({"name":"Spec Gap","short_name":"Spec Gap","description":"Real-world car reviews and tests. Know the difference.",
  "start_url":"./","scope":"./","display":"standalone","background_color":"#0a0a0b","theme_color":"#0a0a0b",
  "icons":[{"src":"assets/img/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"assets/img/icon-512.png","sizes":"512x512","type":"image/png"}]},indent=2))
(ROOT/"404.html").write_text((ROOT/"index.html").read_text().split("<main")[0].replace("<title>Spec Gap | Real-World Car Reviews &amp; Top Gear-Style Tests</title>","<title>Page not found | Spec Gap</title>").replace('content="index,follow"','content="noindex"').replace('<meta charset="utf-8">','<meta charset="utf-8">\n<base href="'+BASE_PATH+'">')+
  '<main id="main"><section class="hero"><div class="wrap"><h1>404: we ran out of road</h1><p>That page doesn\'t exist.</p><a class="btn btn-red" href="index.html">Back home</a></div></section></main></body></html>')
print("Built", len(VIDEOS), "videos")
