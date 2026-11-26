# 10 — What even is normal? (English version)

Rewrite, not translation. Same scene and timeline as the Turkish version (line starts follow audio.py / zamanlama.json).
Cultural swap: the "our food that tourists find gross" beat uses **hot dogs** instead of kokoreç (American viewer = YOU;
stand sign, grill and sandwich are drawn as hot dogs in EN; breakfast tea glass becomes a coffee mug). The turning point stays:
YOU laugh at the tourist's face over your hot dog, then realize you made that same face at the grasshoppers.
Honey fact kept simple: bees bring nectar back to the hive and spit it up.

Voice: Speko / Cartesia "Kyle" c961b81c-a935-4c17-bfb3-ba2239de8c2f, sonic-3.5, speed 1.0, language en. All lines verified with transcribe.

| # | Start | Tempo | TR window | English line |
|---|---|---|---|---|
| l01 | 0.3 | 1.06 | 0.3–5.2 | You eat honey, that's normal. But eating bugs is gross? Quick, don't think. |
| l02 | 5.5 | 1.04 | 5.5–10.4 | Morning. Breakfast table. You dip your bread in honey. You love it. Normal. |
| l03 | 10.7 | 1.0 | 10.7–13.2 | So where does honey come from? Any idea? |
| l04 | 13.4 | 1.06 | 13.4–18.9 | Bees collect nectar from flowers. Back at the hive, they spit it up. That's honey. |
| l05 | 19.1 | 1.0 | 19.1–22.95 | So the stuff on your toast came out of a bee's mouth. Still normal. |
| l06 | 23.2 | 1.04 | 23.2–28.7 | Now, another country. Street stall: fried grasshoppers. We all yell: Gross! |
| l07 | 28.9 | 1.08 | 28.9–33.3 | But the local kid eats them like chips. Crunch, crunch. Normal. |
| l08 | 33.65 | 1.0 | 33.6–39.6 | Snails in France. Mold in cheese. One makes a face, the other digs in. |
| l09 | 39.75 | 1.08 | 39.8–43.1 | Hot dogs? Classic. To a tourist? Gross. |
| l10 | 43.5 | 1.06 | 43.3–48.3 | Last night, eating a hot dog... the tourist next to you made a face. You laughed. |
| l11 | 48.65 | 1.06 | 48.5–53.9 | Then you froze. You made that same face at the grasshoppers. Normal is just how you grew up. |
| l12 | 54.1 | 1.0 | 54.1–57.9 | Next time you're about to say "gross"... ask yourself: says who? |

EN-only timing shifts (scene.html via L()/T(), audio_en.py SFX matched):
- sBee: hive / spit / HONEY events 0.6 s later (`t - 0.6*sm(14.6,15.4,t)`), "they spit it up" lands on the drop.
- sMirror: whole scene 0.3 s later (froze / same face / "Normal is just" four tables).
- Tourist "Gross!" at 42.85 instead of 42.55; captions retimed to English word times (zamanlama_en.json).
- Rejected takes: "Ask a tourist... gross." (transcribed as "grossed" twice), longer l04/l06/l07/l08 drafts (did not fit).
