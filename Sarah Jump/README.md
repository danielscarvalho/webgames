# Sarah Jump — Phase 1

A Doodle-Jump-style parkour game starring **Sarah**, the parkour champion.
HTML + CSS + JavaScript + Bootstrap 5, avatar drawn in SVG, sound made from MIDI notes, installable as a PWA.

## Run it
A PWA (install + offline) needs to be served over http(s), not opened as a file:

```bash
cd "/lab/Sarah Jump"
python3 -m http.server 8080      # then open http://localhost:8080
# or: npx serve .
```
For phones on the same Wi-Fi, open `http://<your-PC-IP>:8080`. Tilt steering on iPhone and
"Add to Home Screen" install need **HTTPS** (e.g. GitHub Pages, Netlify, or `npx localtunnel`).
Opening `index.html` directly still plays, just without install/offline.

## Files
| File | Purpose |
|---|---|
| `index.html` | The whole game: avatar, physics, input, audio, UI |
| `manifest.webmanifest` | PWA name, colours, icons, portrait fullscreen |
| `sw.js` | Service worker, cache-first offline play |
| `icons/` | `icon.svg`, 192/512 PNG and maskable icon (Sarah's "proud" face) |

## Controls
| | Move | Air flip | Kong dash | Pause |
|---|---|---|---|---|
| Keyboard | ← → / A D | ↑ / W | Space / ↓ | P / Esc (M = mute) |
| PS3-style USB pad | Left stick / D-pad | ✕ or △ | □ or ○ | START (rumble on impacts) |
| Mobile | Tilt the device | Tap screen / FLIP | DASH | ⏸ |

## Sarah
- SVG avatar built from the reference photos: middle-parted dark hair with a braided ponytail and pink tie, gold stud earrings, gap-tooth smile, pink tee, navy leggings, gold "26" medal on a magenta ribbon.
- **7 emotions** (`EMOTIONS` in code): Happy, Excited, Focused, Surprised, Scared, Sad, Proud, each triggered by game events.
- **4 body poses**: stand, tuck (flips), star (apex/twist/fall), dash.

## Parkour moves (7 types)
Front Flip · Back Flip · Kong Dash · Super Spring (double flip) · Twist 360 (trampoline) · Precision Landing (combo bonus) · Pigeon Stomp

## World
Platforms: solid (teal), moving (blue), cracked (brown, breaks), one-time (dashed white), trampoline (pink), springs.
Gold medals = +100. Pigeons appear above ~350 m; stomp them, don't bump into them.
Sky goes from morning → sunset → night as you climb. **Phase 1 goal: 2026 m** (+500 bonus, keep climbing endlessly).

## Sound / MIDI
All music and effects are written as MIDI note numbers and played by a Web Audio chiptune synth
(square lead, triangle bass, noise drums); tempo rises with altitude.
Settings → **Send to MIDI device** streams the same notes through the Web MIDI API (Chrome/Edge):
ch 1 lead, ch 2 bass, ch 3 effects, ch 10 drums (GM programs set automatically).

## Tuning knobs (top of section 4 in `index.html`)
`GRAV`, `JUMP`, `GOAL`, `M_PER_PX`; platform mix in `generate()`; colours in `C` (avatar) and `SKY`.

## Ideas for Phase 2
Wall-runs on building edges, power-ups (jetpack-style "zipline"), boss pigeon, level select, online leaderboard.
