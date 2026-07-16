# @hauntghosttours Instagram launch kit

This kit turns the existing Haunt launch strategy into a usable first profile. It uses the production app icon, real app screens, the 12-city launch inventory, and claims already supported by the live App Store copy.

## Set up the profile

- Handle: `@hauntghosttours`
- Display name: `Haunt | GPS Ghost Tours`
- Account type: public professional/business account
- Category: `Travel Service` (showing the category is optional)
- Profile photo: `exports/profile-photo-primary.png` (recommended) or `exports/profile-photo-inverted.png`
- Bio: `Cinematic self-guided haunted-history walks. 12 cities. Every tour starts free on iPhone. ↓`
- Link: `https://apps.apple.com/us/app/haunt-ghost-tours/id6760312968`
- Contact: `support@gethauntapp.com`
- Security: turn on two-factor authentication and store recovery codes in the password manager

Replace the direct App Store URL with an App Store Connect campaign link when available. Use one campaign token per platform × month × content family, such as `ig_jul_product`.

## Publish the first row

The desired visible row is:

`01 launch/how it works` | `02 twelve cities` | `03 trust/privacy`

Because Instagram places the newest post at the left, publish in this order:

1. `exports/posts/03-trust-privacy.png`
2. `exports/posts/02-twelve-cities.png`
3. `exports/posts/01-launch-how-it-works.png`
4. Pin all three.

### Post 1 — Trust/privacy (publish first)

Caption:

> A ghost tour should know where the next story begins—not build an ad profile around everywhere you go. Haunt has no ads and no tracking, and your location stays on your device. When you walk, keep headphones low, respect posted hours and private property, and stay aware of traffic and your surroundings. Safety and privacy are part of the experience, not fine print. #HauntGhostTours #GhostTour #TravelApp

Alt text:

> Black and amber Haunt graphic reading “Built for the walk,” with the statements “No ads,” “No tracking,” and “Your location stays on your device,” plus a responsible-exploration reminder.

### Post 2 — Cities (publish second)

Caption:

> Twelve cities. Stories hiding in plain sight. Explore Boston, Salem, Savannah, Charleston, St. Augustine, Key West, Tampa, Baltimore, Los Angeles, San Francisco, Chicago, and Gettysburg. Every tour's introduction and first stop are free on iPhone. Which city should we walk first? #HauntGhostTours #HauntedHistory #GhostTours

Alt text:

> Amber Haunt graphic listing the twelve launch cities: Boston, Salem, Savannah, Charleston, St. Augustine, Key West, Tampa, Baltimore, Los Angeles, San Francisco, Chicago, and Gettysburg.

### Post 3 — Launch/how it works (publish last)

Caption:

> Some cities never bury their past. Haunt turns your iPhone into a cinematic self-guided ghost tour: choose a route, walk to the marker, and listen where the story happened. Every tour's introduction and first stop are free. Haunt is available now on iPhone—link in bio. #HauntGhostTours #GhostTourApp #HauntedHistory

Alt text:

> Black and amber Haunt launch graphic reading “Haunt is live” and “Walk. Arrive. Listen.” beside a real in-app tour screen showing Haunted Hollywood, a route map, and narration controls.

## Stories and highlights

- Post `exports/stories/launch-story.png` on launch day with the App Store link sticker.
- Add four story groups, then use the matching covers in `exports/highlights/`: `Start Here`, `Cities`, `How It Works`, and `Safety`.
- Add `Reviews` only after genuine customer reviews exist.

## The next 30 days

Use `content-calendar.csv` as the source of truth. Create three original concepts per week for four weeks, then keep only winning pillars. Each concept should become one clean 9:16 master, uploaded natively to Reels, TikTok, and YouTube Shorts without cross-platform watermarks.

Each post gets exactly one CTA. After posting, do one 15-minute comment pass and one follow-up pass the next day. Do not use gore, recent-victim imagery, unsupported allegations, sensational thumbnails, or private-venue marks that imply affiliation.

After 30 days, scale only if Instagram produces at least five attributed first-time downloads and at least two posts beat the account median on saves + shares or link taps. Otherwise keep the handle and mirror only proven winners.

## Update and re-render

Edit `content.json`, then run:

```bash
python3 render_social.py
```

The renderer writes two circle-safe profile images, three square posts, four highlight covers, a launch story, and `grid-preview.png` under `exports/`. It extracts the exact production ghost mark from `marketing/source/AppIcon-1024.png`; it never redraws or generatively reinterprets the logo. Its palette mirrors the canonical brand tokens in `public/index.html`. Pillow is the only Python dependency.

Typography intentionally mirrors the app's serif-display/sans-body hierarchy: Georgia Bold/Regular for durable raster headlines and Avenir Next Demi Bold/Regular for supporting copy. The Avenir TTC face indexes are explicit so regular copy cannot silently render as bold.
