from pywinauto import Application
from pywinauto.keyboard import send_keys
import time

HWND = 5768674

SHORT_DESC = "The ultimate LGBTQ+ app directory. Discover 70+ apps worldwide."

FULL_DESC = "Gay App List is the world's most comprehensive directory of LGBTQ+ dating, social, and community apps.\n\nWhether you're gay, lesbian, bisexual, transgender, queer, or an ally, Gay App List helps you discover the best apps built for the LGBTQ+ community - from global giants to regional gems.\n\nWHAT YOU'LL FIND:\n- 70+ LGBTQ+ apps organized by region and audience\n- Global apps: Grindr, Scruff, HER, Hornet, Taimi, Feeld, Lex, and more\n- Regional apps for Asia, Europe, Latin America, Africa, and the Middle East\n- Apps for gay men, queer women, trans people, bears, and all identities\n- Historical archive of defunct apps\n- App Store and Google Play links for each listing\n\nREGIONS COVERED:\nGlobal | Asia & Pacific | Europe | Latin America | Africa | Middle East\n\nGay App List is built for the community, by the community. Whether you're looking for love, friendship, or just want to explore what's out there - we've got you covered.\n\nNew apps added regularly. Free forever."

a = Application(backend='uia').connect(handle=HWND)
win = a.window(handle=HWND)
win.set_focus()
time.sleep(1)

edits = win.descendants(control_type='Edit')
print(f'Found {len(edits)} edit fields')

# [2] = Short description
short_edit = edits[2]
print('Filling short description...')
short_edit.click_input()
time.sleep(0.3)
send_keys('^a')
time.sleep(0.1)
try:
    short_edit.set_text(SHORT_DESC)
except Exception as e:
    print(f'set_text error: {e}')
    # fallback: type it
    short_edit.type_keys(SHORT_DESC, with_spaces=True)
time.sleep(0.5)
print(f'Short desc result: {short_edit.window_text()[:60]!r}')

# [3] = Full description
full_edit = edits[3]
print('Filling full description...')
full_edit.click_input()
time.sleep(0.3)
send_keys('^a')
time.sleep(0.1)
try:
    full_edit.set_text(FULL_DESC)
except Exception as e:
    print(f'set_text error: {e}')
    full_edit.type_keys(FULL_DESC, with_spaces=True)
time.sleep(0.5)
print(f'Full desc result: {full_edit.window_text()[:80]!r}')

# Look for Save button
time.sleep(1)
btns = win.descendants(control_type='Button')
save_btn = None
for b in btns:
    try:
        t = b.window_text()
        if t in ('Save', 'Save draft', 'Save changes'):
            print(f'Found save button: {t!r}')
            save_btn = b
            break
    except:
        pass

if save_btn:
    save_btn.click_input()
    time.sleep(4)
    print('Saved! Title:', win.window_text())
else:
    print('No save button found, listing all buttons:')
    for b in btns:
        try:
            t = b.window_text()
            if t:
                print(f'  {t!r}')
        except:
            pass
