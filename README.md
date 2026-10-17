# Spec Gap website

A static site (HTML/CSS/vanilla JS). No build step is needed to host it.

## Placeholders to replace
1. **Domain, YouTube channel URL and email**: these are at the top of `build.py` (`SITE_URL`, `CHANNEL_URL`, `EMAIL`). Edit them, then run `python3 build.py` to rewrite every page, plus sitemap.xml and robots.txt.
2. **Videos**: the entries in `videos.js` are marked `[PLACEHOLDER]`. Replace them with your real videos.
3. **About page copy** (`build.py`, about section) and the **contact form** (it uses mailto for now. See the comment in the form about Netlify Forms or Formspree).

## Adding a video
Open `videos.js` and copy one block:
```
{ "id": "dQw4w9WgXcQ", "title": "...", "description": "...", "date": "2026-11-01", "category": "Tank Test", "featured": false },
```
- `id` is the part after `watch?v=` in the YouTube link. The thumbnail is loaded automatically.
- `category` can be Review, Tank Test, Head to Head or Challenge. Filter buttons appear automatically.
- `featured: true` shows the video under "Featured tests" on the home page.
The site updates as soon as you save. Run `python3 build.py` afterwards to refresh the SEO VideoObject data and the no-JS fallback on videos.html.

## Run locally
`python3 -m http.server 8000`, then open http://localhost:8000

## Deploy
- **Netlify**: drag the folder onto app.netlify.com/drop, or connect the repo (no build command; publish directory `/`).
- **Cloudflare Pages**: create a project, connect the repo or upload directly. Leave the build command empty and set the output directory to `/`.
- **GitHub Pages**: push to a repo, then go to Settings → Pages → Deploy from branch `main` / root. For a custom domain, add a `CNAME` file containing `www.yourdomain.com`.
After going live, submit `https://yourdomain/sitemap.xml` in Google Search Console.

## Base path / custom domain
The site is currently set up for GitHub Pages at `https://luxrepair2025-rgb.github.io/specgap/`. All page links and assets use relative paths, so the site works under a subpath or at a root domain without changes. Only `SITE_URL` at the top of `build.py` needs to change. That setting controls canonical tags, Open Graph, JSON-LD, sitemap.xml and robots.txt, and it also sets the `<base>` tag on 404.html.
To move to a custom domain: set `SITE_URL = "https://www.specgap.com"`, run `python3 build.py`, add a `CNAME` file containing `www.specgap.com`, set the custom domain in the repo's Settings → Pages, and point your DNS at GitHub Pages.
Note: search engines only read robots.txt at a domain root, so while the site is on a subpath, submit the sitemap URL directly in Search Console.
