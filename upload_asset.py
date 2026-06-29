"""Upload an asset to Play Console by clicking the Nth 'Add assets' button."""
import sys, time, ctypes
from pywinauto import Application, Desktop
from pywinauto.findwindows import find_windows
from pywinauto.keyboard import send_keys
import win32gui, win32con, win32api

HWND = 5768674
# Usage: python upload_asset.py <button_index> <file_path>
# button_index: 0-based index among 'Add assets' buttons

btn_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
file_path = sys.argv[2] if len(sys.argv) > 2 else ''

if not file_path:
    print("Usage: python upload_asset.py <btn_index> <file_path>")
    sys.exit(1)

print(f'Uploading: {file_path}')
print(f'Button index: {btn_idx}')

a = Application(backend='uia').connect(handle=HWND)
win = a.window(handle=HWND)
win.set_focus()
time.sleep(0.5)

# Find all 'Add assets' buttons
btns = win.descendants(control_type='Button')
add_assets_btns = []
for b in btns:
    try:
        if 'Add assets' in b.window_text() or 'add assets' in b.window_text().lower():
            add_assets_btns.append(b)
    except:
        pass

print(f'Found {len(add_assets_btns)} "Add assets" buttons')

if btn_idx >= len(add_assets_btns):
    print(f'ERROR: button index {btn_idx} out of range')
    sys.exit(1)

target_btn = add_assets_btns[btn_idx]
print(f'Clicking button {btn_idx}: {target_btn.window_text()!r}')

try:
    target_btn.invoke()
except:
    target_btn.click_input()

print('Waiting for file dialog...')
time.sleep(2)

# Handle the Windows file dialog
file_dialog = None
for attempt in range(15):
    all_wins = find_windows(class_name='#32770', visible_only=True)
    for hw in all_wins:
        try:
            a2 = Application(backend='uia').connect(handle=hw)
            dlg = a2.window(handle=hw)
            t = dlg.window_text()
            print(f'  Found dialog: {t!r} hwnd={hw}')
            if t in ('Open', 'Choose File', 'Upload', 'Select File', 'Open Files'):
                file_dialog = dlg
                break
            elif t == '':
                # Might be file dialog without title
                edits = dlg.descendants(control_type='Edit')
                if edits:
                    file_dialog = dlg
                    break
        except:
            pass
    if file_dialog:
        break
    print(f'  Attempt {attempt+1}: no dialog yet')
    time.sleep(1)

if not file_dialog:
    print('ERROR: No file dialog appeared')
    sys.exit(1)

print(f'Dialog: {file_dialog.window_text()!r}')
edits = file_dialog.descendants(control_type='Edit')
print(f'Edit controls: {len(edits)}')

if edits:
    target_edit = edits[-1]
    target_edit.set_focus()
    target_edit.set_text(file_path)
    time.sleep(0.5)
    print(f'Set path to: {file_path}')

    # Win32 method to submit
    import ctypes
    IDOK = 1
    hwnd_dlg = file_dialog.handle
    ctypes.windll.user32.SendDlgItemMessageW(hwnd_dlg, 0x047c, win32con.WM_SETTEXT, 0, file_path)
    time.sleep(0.2)
    ctypes.windll.user32.PostMessageW(hwnd_dlg, win32con.WM_COMMAND, IDOK, 0)
    time.sleep(2)

    # Check if dialog closed
    remaining = find_windows(class_name='#32770', visible_only=True)
    if not any(hw == file_dialog.handle for hw in remaining):
        print(f'=== SUCCESS: File uploaded: {file_path} ===')
    else:
        print('Dialog still open - trying Enter key')
        send_keys('{ENTER}')
        time.sleep(2)
else:
    print('No edit controls in dialog')
    sys.exit(1)
