# Talita Lunar Lander

A retro lunar lander starring Talita. It's one HTML file drawn in SVG, with no libraries, and it installs as a PWA.

## Controls

| Input | Steer | Engine | Pause / Restart |
|---|---|---|---|
| Keyboard | ← → | ↑ or Space | P / R (M = mute) |
| Mouse | nose turns toward the pointer while the button is held | hold left button | ❚❚ / ↻ buttons |
| USB gamepad (PS3-style) | left stick or D-pad | any face/shoulder button, or stick up | START / SELECT |
| Phone / tablet | tilt the phone (or ◀ ▶) | hold the screen or 🔥 | ❚❚ / ↻ (tap ↻ twice) |

Tilt is measured relative to how the phone is held when each round starts, so any comfortable grip works.
You can turn it on or off with the **TILT** button.

## Running it

Opening `index.html` directly (file://) works for keyboard, mouse and gamepad play.
**Install, offline mode and phone tilt need http(s)**, because browsers only allow a service worker and motion sensors on a secure origin.

**On this PC (localhost counts as secure):**

```bash
cd "/lab/Talita Moon Lander"
python3 -m http.server 8000
# open http://localhost:8000
```

**On phones:** host the folder over HTTPS. The easiest way is GitHub Pages:

```bash
git init && git add index.html manifest.webmanifest sw.js icons README.md
git commit -m "Talita Lunar Lander"
git branch -M main
git remote add origin git@github.com:<you>/talita-lander.git
git push -u origin main
# GitHub → Settings → Pages → Deploy from branch: main / root
# Play at https://<you>.github.io/talita-lander/
```

Then install it:
- **Android (Chrome):** use the **⬇ Install** button, or the menu → *Install app*.
- **iPhone (Safari):** Share → *Add to Home Screen*. Allow Motion & Orientation access when you tap to launch.

A plain LAN address like `http://192.168.x.x:8000` will run the game on a phone, but without tilt or install.

## Gamepad notes

- It uses the browser Gamepad API. Press any button once after plugging the pad in, so the browser exposes it.
- It handles the standard mapping plus two layouts common on generic PS3-style clones: a Windows-style hat on axis 9, and a Linux-style hat on the last two axes.
- The pad rumbles on a crash if it supports rumble.
- Browsers don't count a gamepad press as a user gesture, so sound may start only after the first key press or click.

## Files

```
index.html              the whole game (faces embedded as data URLs)
manifest.webmanifest    PWA metadata (name, icons, landscape, fullscreen)
sw.js                   offline cache (bump CACHE when you change files)
icons/                  192, 512, maskable 512, Apple touch icon
tools/                  talita_faces.py (sprites), index_template.html + build.py, make_icons.py
assets/, docs/          sprite PNGs, sprite sheet, previews
```

To edit the game, change `tools/index_template.html` and run `python3 tools/build.py` (it embeds the sprites).
Or edit `index.html` directly. After changing files, bump `CACHE` in `sw.js` so installed copies update.

Tuning constants are at the top of the script: `G`, `THR`, `BURN`, `SAFE_VY`, `SAFE_VX`, `SAFE_ANG`, `LIVES`, `TILT_SENS`, `MOUSE_AIM`.
