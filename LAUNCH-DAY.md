# Launch-day runbook (this branch: `post-launch`)

This branch is the fully-built post-launch site. Two placeholder tokens remain:

- `APP_STORE_URL_TBD` — the full App Store link (in `public/index.html` × 3 hrefs + JSON-LD, and `public/llms.txt`)
- `HAUNT_APP_ID_TBD` — the numeric app ID for the Apple smart-app-banner meta tag (the digits after `id` in the App Store URL)

## When the app is live

Given a link like `https://apps.apple.com/us/app/haunt/id6741234567`:

```bash
git checkout post-launch
git pull
URL="https://apps.apple.com/us/app/haunt/id6741234567"   # real link here
ID="6741234567"                                           # digits after "id"
TODAY=$(date +%F)
sed -i '' "s|APP_STORE_URL_TBD|$URL|g" public/index.html public/llms.txt
sed -i '' "s|HAUNT_APP_ID_TBD|$ID|g" public/index.html
sed -i '' "s|<lastmod>.*</lastmod>|<lastmod>$TODAY</lastmod>|" public/sitemap.xml
git rm LAUNCH-DAY.md
git commit -am "Launch: swap in App Store link"
git checkout main && git merge post-launch && git push origin main
```

Cloudflare auto-deploys on push to main. Verify at https://gethauntapp.com after ~1 min:
- Hero + final CTA "Download on the App Store" buttons open the store link
- Nav "Get the app" pill opens the store link
- No `TBD` left: `curl -s https://gethauntapp.com | grep -c TBD` → 0

## What changed vs. the pre-launch site
- Both Kit waitlist forms → App Store download buttons (amber, Apple glyph)
- Nav CTA "Join the waitlist" → "Get the app"
- Hero eyebrow "Coming Soon" → "Now on the App Store"
- Final CTA: "Be first through the door." → "The door is open."
- Meta description / llms.txt: "Coming soon" → "Out now on iOS"
- JSON-LD MobileApplication: + installUrl, + free Offer
- Added `apple-itunes-app` smart-banner meta (Safari shows a native install banner)
- CSP: removed app.kit.com from connect-src / form-action
- Removed the waitlist submit JS

## Optional follow-ups (post-launch, not blocking)
- Email the Kit waitlist announcing launch
- Add og:image 1200×630 (still pending from pre-launch)
- Add App Store rating to JSON-LD once reviews exist
