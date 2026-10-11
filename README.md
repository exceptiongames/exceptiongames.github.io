# exceptiongames.github.io

Public site of exception games, served by GitHub Pages at https://exceptiongames.github.io/.

It holds the public pages the App Store requires for Living Factory:
- privacy policy: https://exceptiongames.github.io/living-factory/privacy-policy/
- support: https://exceptiongames.github.io/living-factory/support/

Languages: English is the main one (the App Store links point to it), Ukrainian second (`…/uk/`), Russian third (`…/ru/`). Every page has a language switch. Other languages are not needed: Apple does not require them, and every policy change would have to be translated again.

Plain static HTML with one stylesheet (`assets/style.css`); no scripts, no cookies, no trackers. All texts live in `build.py`; run `python3 build.py` after any change and commit the generated HTML with it.

## Rules
- `build.py` is the only source of the policy text. `docs/PRIVACY_POLICY.md` in the private game repo lists what the policy must cover; when the app's data handling changes, update both, change all three languages the same way and set a new effective date (`UPDATED`).
- Owner decisions of October 11, 2026: support mail is deleted within 12 months after the question is resolved; the responsible party is the developer shown as the seller on the App Store page.
- UI names quoted on the pages (Restart, Settings → Players…) must match the app's strings in each language.
- These URLs are compiled into the game (`Config/Signing.local.xcconfig`) and set in App Store Connect. Never rename or move these pages.
- The logo files come from `AppStore/Brand/` in the game repo (`Scripts/generate_brand_logo.py`): logo, dark logo, mark, touch icon, favicon. Pixel art is shown only at whole multiples of its grid (logo 10 px → 234 px wide).
- Design was checked by an independent design review on October 11, 2026: WCAG AA contrast in both themes, 44 px tap targets, visible focus.
- Contact address: exceptiongames@icloud.com. Do not add other contacts.

## Preview locally
```bash
python3 -m http.server 8765
```
Then open http://localhost:8765/.
