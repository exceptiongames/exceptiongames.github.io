# exceptiongames.github.io

Public site of exception games, served by GitHub Pages at https://exceptiongames.github.io/.

It holds the public pages the App Store requires for Ant Foragers («Фуражиры»):
- privacy policy: https://exceptiongames.github.io/ant-foragers/privacy-policy/
- support: https://exceptiongames.github.io/ant-foragers/support/

The game was called Living Factory until October 16, 2026 (game repo, board card #66). Every old address under `living-factory/` is a page that sends the visitor to the new one.

Languages: English is the main one (the App Store links point to it), Ukrainian second (`…/uk/`), Russian third (`…/ru/`), then German (`…/de/`), Japanese (`…/ja/`), Korean (`…/ko/`), Simplified Chinese (`…/zh-hans/`) and Traditional Chinese (`…/zh-hant/`) (owner decision of October 12, 2026). Every page has a language switch with the 8 names. Every non-English page ends with a note that the English version applies if a translation differs (owner decision A of October 14, 2026). All seven translations are AI translations. There is no native-speaker review (owner decision of October 15, 2026): an independent AI reviewer per language checked them on October 15, 2026, and the English version applies if a translation differs. Other languages are not planned: Apple does not require them, and every policy change has to be translated again.

Plain static HTML with one stylesheet (`assets/style.css`); no scripts, no cookies, no trackers. All texts live in `build.py`; run `python3 build.py` after any change and commit the generated HTML with it.

## Rules
- `build.py` is the only source of the policy text. `docs/PRIVACY_POLICY.md` in the private game repo lists what the policy must cover; when the app's data handling changes, update both, change all eight languages the same way and set a new effective date (`UPDATED`).
- Owner decisions of October 11, 2026: support mail is deleted within 12 months after the question is resolved; the responsible party is the developer shown as the seller on the App Store page.
- UI names quoted on the pages (Restart, Settings → Players…) must match the app's strings in each language.
- These URLs are compiled into the game (`Config/Signing.local.xcconfig`) and set in App Store Connect. Never rename or move these pages. The redirect pages under `living-factory/` stay too: early builds and old links point there.
- The logo files come from `AppStore/Brand/` in the game repo (`Scripts/generate_brand_logo.py`): logo, dark logo, mark, touch icon, favicon. Pixel art is shown only at whole multiples of its grid (logo 10 px → 234 px wide).
- Design was checked by an independent design review on October 11, 2026: WCAG AA contrast in both themes, 44 px tap targets, visible focus.
- Contact address: exceptiongames@icloud.com. Do not add other contacts. Support answers in English, Ukrainian or Russian; the pages in the other languages say that we answer in English.

## Preview locally
```bash
python3 -m http.server 8765
```
Then open http://localhost:8765/.
