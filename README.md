# exceptiongames.github.io

Public site of exception games, served by GitHub Pages at https://exceptiongames.github.io/.

It holds the public pages the App Store requires for Living Factory:
- privacy policy: https://exceptiongames.github.io/living-factory/privacy-policy/
- support: https://exceptiongames.github.io/living-factory/support/

Plain static HTML with one stylesheet (`assets/style.css`); no build step, no scripts, no trackers.

## Rules
- The privacy policy text is the public copy of `docs/PRIVACY_POLICY.md` in the private game repo. Change both together, and update the effective date when the meaning changes.
- These URLs are compiled into the game (`Config/Signing.local.xcconfig`) and set in App Store Connect. Never rename or move these pages.
- The logo files come from `AppStore/Brand/` in the game repo (`Scripts/generate_brand_logo.py`).
- Contact address: exceptiongames@icloud.com. Do not add other contacts.

## Preview locally
```bash
python3 -m http.server 8765
```
Then open http://localhost:8765/.
