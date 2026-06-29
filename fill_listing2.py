from pywinauto import Application
from pywinauto.keyboard import send_keys
import time

HWND = 5768674

SHORT_DESC = "The ultimate LGBTQ+ app directory. Discover 70+ apps worldwide."

FULL_DESC = """Gay App List is the world's most comprehensive directory of LGBTQ+ dating, social, and community apps.

Whether you're gay, lesbian, bisexual, transgender, queer, or an ally, Gay App List helps you discover the best apps built for the LGBTQ+ community - from global giants to regional gems.

WHAT YOU'LL FIND:
- 70+ LGBTQ+ apps organized by region and audience
- Global apps: Grindr, Scruff, HER, Hornet, Taimi, Feeld, Lex, and more
- Regional apps for Asia, Europe, Latin America, Africa, and the Middle East
- Apps for gay men, queer women, trans people, bears, and all identities
- Historical archive of defunct apps
- App Store and Google Play links for each listing
- App details: founding year, country of origin, and audience info

REGIONS COVERED:
Global | Asia & Pacific | Europe | Latin America | Africa | Middle East

Gay App List is built for the community, by the community. Whether you're looking for love, friendship, or just want to explore what's out there - we've got you covered.

New apps added regularly. Free forever."""

a = Application(backend='uia').connect(handle=HWND)
win = a.window(handle=HWND)
win.set_focus()
time.sleep(1)

edits = win.descendants(control_type='Edit')
print(f'Found {len(edits)} edit fields')
for i, e in enumerate(edits):
    try:
        name = e.element_info.name
        val = e.window_text()
        print(f'  [{i}] name={name!r} val={val[:60]!r}')
    except Exception as ex:
        print(f'  [{i}] error: {ex}')
