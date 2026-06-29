from pywinauto import Application
from pywinauto.keyboard import send_keys
import time

HWND = 5768674

SHORT_DESC = "The ultimate LGBTQ+ app directory. Discover 70+ apps from around the world."

FULL_DESC = """Gay App List is the world's most comprehensive directory of LGBTQ+ dating, social, and community apps.

Whether you're gay, lesbian, bisexual, transgender, queer, or an ally, Gay App List helps you discover the best apps built for the LGBTQ+ community — from global giants to regional gems you may never have heard of.

WHAT YOU'LL FIND:
- 70+ LGBTQ+ apps organized by region and audience
- Global apps: Grindr, Scruff, HER, Hornet, Taimi, Feeld, Lex, and more
- Regional apps for Asia, Europe, Latin America, Africa, and the Middle East
- Apps for gay men, queer women, trans people, bears, and all identities
- Historical archive of defunct apps
- App Store and Google Play links for each listing
- App details: founding year, country of origin, and audience info

REGIONS COVERED:
🌍 Global | 🌏 Asia & Pacific | 🇪🇺 Europe | 🌎 Latin America | 🌍 Africa | 🇮🇱 Middle East

Gay App List is built for the community, by the community. Whether you're looking for love, friendship, or just want to explore what's out there — we've got you covered.

New apps added regularly. Free forever."""

a = Application(backend='uia').connect(handle=HWND)
win = a.window(handle=HWND)
win.set_focus()
time.sleep(1)

edits = win.descendants(control_type='Edit')
print(f'Found {len(edits)} edit fields')

# [2] = Short description, [3] = Full description
short_edit = edits[2]
full_edit = edits[3]

# Fill short description
print('Setting short description...')
short_edit.click_input()
time.sleep(0.3)
send_keys('^a')
short_edit.set_text(SHORT_DESC)
time.sleep(0.3)
print(f'Short desc set: {short_edit.window_text()[:50]}')

# Fill full description
print('Setting full description...')
full_edit.click_input()
time.sleep(0.3)
send_keys('^a')
full_edit.set_text(FULL_DESC)
time.sleep(0.3)
print(f'Full desc set: {full_edit.window_text()[:80]}')

# Save as draft
time.sleep(1)
btns = win.descendants(control_type='Button')
for b in btns:
    try:
        if 'Save' in b.window_text() and 'draft' not in b.window_text().lower() and 'Discard' not in b.window_text():
            print(f'Clicking Save: {b.window_text()!r}')
            b.click_input()
            time.sleep(4)
            print('Saved. Title:', win.window_text())
            break
    except: pass
