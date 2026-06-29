from pywinauto import Application
from pywinauto.keyboard import send_keys
import time, ctypes

HWND = 5768674

SHORT_DESC = "The ultimate LGBTQ+ app directory. Discover 70+ apps worldwide."

FULL_DESC = "Gay App List is the world's most comprehensive directory of LGBTQ+ dating, social, and community apps.\n\nWhether you're gay, lesbian, bisexual, transgender, queer, or an ally, Gay App List helps you discover the best apps built for the LGBTQ+ community - from global giants to regional gems.\n\nWHAT YOU'LL FIND:\n- 70+ LGBTQ+ apps organized by region and audience\n- Global apps: Grindr, Scruff, HER, Hornet, Taimi, Feeld, Lex, and more\n- Regional apps for Asia, Europe, Latin America, Africa, and the Middle East\n- Apps for gay men, queer women, trans people, bears, and all identities\n- Historical archive of defunct apps\n- App Store and Google Play links for each listing\n\nREGIONS COVERED:\nGlobal | Asia & Pacific | Europe | Latin America | Africa | Middle East\n\nGay App List is built for the community, by the community. Whether you're looking for love, friendship, or just want to explore - we've got you covered.\n\nNew apps added regularly. Free forever."

a = Application(backend='uia').connect(handle=HWND)
win = a.window(handle=HWND)
win.set_focus()
time.sleep(0.5)

edits = win.descendants(control_type='Edit')
print(f'Found {len(edits)} edit fields')

# Try scrolling the window into view first, then clicking via Win32 mouse
# Get the rectangle of edit[2]
short_edit = edits[2]
rect = short_edit.rectangle()
print(f'Short edit rect: {rect}')

# Use pywinauto's scroll wrapper on the win to bring the edit into view
# First try clicking by coordinates - UIA sometimes works even if "not visible"
import win32api, win32con, win32gui

def win32_click(x, y, hwnd):
    # Move mouse to position relative to screen
    lParam = win32api.MAKELONG(x, y)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    time.sleep(0.05)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

# Use scroll to bring the field into view
# Tab from app name field to short desc
short_name_edit = edits[1]  # app name
try:
    short_name_edit.click_input()
    time.sleep(0.3)
except:
    pass

# Tab twice to get to short description
send_keys('{TAB}')
time.sleep(0.2)
print('Tabbed once')

# Now we should be in short description - type it
send_keys('^a')
time.sleep(0.1)

# Type the short desc
for char in SHORT_DESC:
    if char == "'":
        send_keys("'", with_spaces=True)
    elif char == '"':
        send_keys('"', with_spaces=True)
    else:
        send_keys(char, with_spaces=True)

print('Short desc typed')
time.sleep(0.5)

# Tab to full description
send_keys('{TAB}')
time.sleep(0.3)
print('Tabbed to full desc')
send_keys('^a')
time.sleep(0.1)

# Type full desc
for char in FULL_DESC:
    if char == '\n':
        send_keys('{ENTER}')
    elif char == "'":
        send_keys("'", with_spaces=True)
    else:
        send_keys(char, with_spaces=True)

print('Full desc typed')
time.sleep(1)

# Now find and click Save
btns = win.descendants(control_type='Button')
for b in btns:
    try:
        t = b.window_text()
        if t:
            print(f'  BTN: {t!r}')
    except:
        pass
