# @hauntghosttours Instagram launch kit

This kit turns the existing Haunt launch strategy into a usable first profile. It uses the production app icon, real app screens, the 12-city launch inventory, and claims already supported by the live App Store copy.

## Set up the profile

- Handle: `@hauntghosttours`
- Display name: `Haunt | GPS Ghost Tours`
- Account type: public professional/business account
- Category: `Travel Service` (showing the category is optional)
- Profile photo: `exports/profile-photo-inverted.png` (recommended for small-size clarity) or `exports/profile-photo-primary.png`
- Bio: `Cinematic self-guided haunted-history walks. 12 launch cities—and growing. First stop free on iPhone. ↓`
- Link: `https://apps.apple.com/us/app/haunt-ghost-tours/id6760312968`
- Contact: `support@gethauntapp.com`
- Security: turn on two-factor authentication and store recovery codes in the password manager

Replace the direct App Store URL with an App Store Connect campaign link when available. Use one campaign token per platform × month × content family, such as `ig_jul_product`.

## Publish the starter set

Start with two feed posts:

`01 launch/how it works` | `02 cities at launch`

Because Instagram places the newest post at the left, publish the cities post first:

1. `exports/posts/02-twelve-cities.png`
2. `exports/posts/01-launch-how-it-works.png`
3. Pin both.

Before sharing, use Instagram's preview controls to verify that the square artwork fits the profile-grid thumbnail without cropping either edge.

### Post 1 — Cities at launch (publish first)

Caption:

> Haunt launches in 12 cities: Boston, Salem, Savannah, Charleston, St. Augustine, Key West, Tampa, Baltimore, Los Angeles, San Francisco, Chicago, and Gettysburg. This is the starting map—not the final one. New Orleans, New York City, and San Antonio are already coming soon, with more cities added as new tours are ready. Where should Haunt go next? #HauntGhostTours #HauntedHistory #GhostTours

Alt text:

> Amber Haunt graphic reading “At launch” and “12 cities,” listing Boston, Salem, Savannah, Charleston, St. Augustine, Key West, Tampa, Baltimore, Los Angeles, San Francisco, Chicago, and Gettysburg, and stating that more cities are already on the way.

### Post 2 — Launch/how it works (publish second)

Caption:

> Some cities never bury their past. Haunt turns your iPhone into a cinematic self-guided ghost tour: choose a route, walk to the marker, and listen where the story happened. Every tour's introduction and first stop are free. Haunt is available now on iPhone—link in bio. #HauntGhostTours #GhostTourApp #HauntedHistory

Alt text:

> Black and amber Haunt launch graphic reading “Haunt is live” and “Walk. Arrive. Listen.” beside a real in-app tour screen showing Haunted Hollywood, a route map, and narration controls.

### Hold for later — Trust/privacy

`exports/posts/03-trust-privacy.png` is useful supporting content, but its safety and privacy detail is dense for a brand-new profile. Publish it later as part of a focused privacy or responsible-exploration sequence rather than using it as launch-day filler.

Caption:

> A ghost tour should know where the next story begins—not build an ad profile around everywhere you go. Haunt has no ads and no tracking, and your location stays on your device. When you walk, keep headphones low, respect posted hours and private property, and stay aware of traffic and your surroundings. Safety and privacy are part of the experience, not fine print. #HauntGhostTours #GhostTour #TravelApp

Alt text:

> Black and amber Haunt graphic reading “Built for the walk,” with the statements “No ads,” “No tracking,” and “Your location stays on your device,” plus a responsible-exploration reminder.

## Stories and highlights

- The two feed posts and profile photo are enough to establish the account. Add `exports/stories/launch-story.png` when you are ready to place and verify the App Store link sticker in Instagram.
- Start with one `Start Here` Highlight. Add `Cities`, `How It Works`, and `Safety` only after each has enough useful Story frames to justify the section.
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
