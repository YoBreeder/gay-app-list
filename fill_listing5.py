from pywinauto import Application
from pywinauto.keyboard import send_keys
import time, win32clipboard, win32con

HWND = 5768674

SHORT_DESC = "The ultimate LGBTQ+ app directory. Discover 70+ apps worldwide."

FULL_DESC = "Gay App List is the world's most comprehensive directory of LGBTQ+ dating, social, and community apps.\n\nWhether you're gay, lesbian, bisexual, transgender, queer, or an ally, Gay App List helps you discover the best apps built for the LGBTQ+ community - from global giants to regional gems.\n\nWHAT YOU'LL FIND:\n- 70+ LGBTQ+ apps organized by region and audience\n- Global apps: Grindr, Scruff, HER, Hornet, Taimi, Feeld, Lex, and more\n- Regional apps for Asia, Europe, Latin America, Africa, and the Middle East\n- Apps for gay men, queer women, trans people, bears, and all identities\n- Historical archive of defunct apps\n- App Store and Google Play links for each listing\n\nREGIONS COVERED:\nGlobal | Asia and Pacific | Europe | Latin America | Africa | Middle East\n\nGay App List is built for the community, by the community. Whether you're looking for love, friendship, or just want to explore - we've got you covered.\n\nNew apps added regularly. Free forever."

def set_clipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()

a = Application(backend='uia').connect(handle=HWND)
win = a.window(handle=HWND)
win.set_focus()
time.sleep(0.5)

edits = win.descendants(control_type='Edit')
print(f'Found {len(edits)} edit fields')

# Click the app name field (which is visible)
name_edit = edits[1]  # 'GAY APP LIST'
name_edit.click_input()
time.sleep(0.3)

# Tab once to get to short description
send_keys('{TAB}')
time.sleep(0.5)

# Paste short description
set_clipboard(SHORT_DESC)
send_keys('^a')
time.sleep(0.1)
send_keys('^v')
time.sleep(0.5)
print('Short desc pasted')

# Tab to full description
send_keys('{TAB}')
time.sleep(0.5)

# Paste full description
set_clipboard(FULL_DESC)
send_keys('^a')
time.sleep(0.1)
send_keys('^v')
time.sleep(1)
print('Full desc pasted')

# Find and click Save
time.sleep(0.5)
btns = win.descendants(control_type='Button')
save_btn = None
for b in btns:
    try:
        t = b.window_text()
        if t:
            print(f'  BTN: {t!r}')
        if t in ('Save', 'Save draft', 'Save changes'):
            save_btn = b
    except:
        pass

if save_btn:
    print(f'Clicking: {save_btn.window_text()!r}')
    save_btn.click_input()
    time.sleep(4)
    print('Done! Title:', win.window_text())
else:
    print('No save button found by name - trying to find by scrolling...')
    # Try pressing Tab more to find save or use keyboard shortcut
