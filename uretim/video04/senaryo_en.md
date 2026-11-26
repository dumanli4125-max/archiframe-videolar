# 04 (EN) — Mom's calls

Voice: Cartesia "Kyle" (sonic-3.5, speed 1.0, Speko). Same scene and timeline as the Turkish version (split screen: top = YOU, bottom = mom's place).
Tempo: l02 ×1.03, l03 ×1.04, l07 ×1.02 (to fit the TR windows). Everything else 1.0.

| # | Start | TR window | Line (EN) | Length (speech) |
|---|------|-----------|-----------|--------|
| l01 | 0.3 | 0.3–3.6 | When did your mom last call? Did you pick up? | 2.75 |
| l02 | 3.6 | 3.6–8.6 | Tuesday, you're in a meeting. Phone buzzes. The screen says: Mom. | 5.05 (×1.03 → 4.9) |
| l03 | 8.6 | 8.6–12.1 | You hit decline. Then a quick text: I'll call you later. | 3.60 (×1.04 → 3.46) |
| l04 | 12.1 | 12.1–18.0 | Next evening, she calls again. You're out with friends, having fun. Again: Later. | 5.62 |
| l05 | 18.0 | 18.0–24.4 | Meanwhile, your mom has set two cups of tea on the table. Phone in hand, she waits. | 5.79 |
| l06 | 24.4 | 24.4–29.4 | Missed calls... one. Two. Five... Twelve. | 3.94 |
| l07 | 29.4 | 29.4–33.4 | Then a text comes in: I cooked. Thought you might come by. | 4.02 (×1.02 → 3.94) |
| l08 | 33.4 | 33.4–37.5 | You said: Later. That later... never came. | 3.46 |
| l09 | 37.5 | 37.5–44.6 | One night, you can't take it. This time, you call her. It rings... and rings... No answer. | 6.65 |
| l10 | 44.6 | 44.6–51.0 | Just as you're about to hang up, a voice. ... Sweetheart... I heard your voice. That's enough. | 5.96 |
| l11 | 51.0 | 51.0–57.5 | Close this video. Call your mom. | 2.07 |

Hook: "When did your mom last call? Did you pick up?" — second person, a reminder rather than a guilt trip.
Final action: "Close this video. Call your mom." No gender specified for YOU ("Sweetheart" / "SWEETIE").

On-screen (L()): call card ANNEM/arıyor.../reddedildi → MOM / calling... / declined (avatar M); TOPLANTI→MEETING, DIŞARIDA→OUT,
İŞ→WORK, EV→HOME (TAG_EN), SEN→YOU (TAG_EN), ANNENİN EVİ→MOM'S PLACE, ÇARŞAMBA/CUMA/PAZAR/2 HAFTA → WEDNESDAY/FRIDAY/SUNDAY/2 WEEKS,
CEVAPSIZ ARAMA→MISSED CALLS. Mom's phone contact name YAVRUM→SWEETIE (avatar S).
Bubbles/messages: "I'll call you later." · "Later." · "I cooked. Thought you might come by." · "Sweetheart..." · "I heard your voice. That's enough."
Final: "Close this video." / "Call your mom."

EN timing shifts in scene.html (via L()):
- Missed-call counter hits (HITS) 25.7/26.6/27.4/28.3 → 25.6/26.4/27.2/27.85 (one/two/five/twelve); weekday tags and counter follow. audio_en.py buzzes too.
- "I'll call you later." bubble 10.8→11.3, mom's SWEETIE message 10.9→11.35 (ping 11.3).
- "Later." bubble 16.7→17.15, SWEETIE message 16.8→17.2 (ping 17.15).
- Final "Call your mom." 52.6→52.4.
- Captions: own capsEn() / hookCaps EN branch with splits at EN word times (2.3, 14.4, 19.8, 22.0, 31.1, 35.0, 41.4, 43.3, 47.0).
