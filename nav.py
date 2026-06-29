import sys
from pywinauto import Application
from pywinauto.keyboard import send_keys
import time

HWND = 5768674
url = sys.argv[1] if len(sys.argv) > 1 else ''

a = Application(backend='uia').connect(handle=HWND)
win = a.window(handle=HWND)
win.set_focus()
time.sleep(0.5)

edits = win.descendants(control_type='Edit')
addr = edits[0]
addr.click_input()
time.sleep(0.3)
send_keys('^a')
time.sleep(0.1)
send_keys(url, with_spaces=True)
send_keys('{ENTER}')
time.sleep(7)
print('Title:', win.window_text())
edits2 = win.descendants(control_type='Edit')
print('URL:', edits2[0].window_text() if edits2 else 'N/A')
