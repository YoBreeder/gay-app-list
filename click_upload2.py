"""
Find the NEW Chrome window with Play Console Prepare Release page and click upload.
"""
import time, sys
from pywinauto import Application, Desktop
from pywinauto.findwindows import find_windows
from pywinauto.keyboard import send_keys

AAB_PATH = r'C:\Users\DH\gay-app-list\android\app\build\outputs\bundle\release\app-release.aab'


def main():
    print("Scanning all Chrome_WidgetWin_1 windows...")
    wins = find_windows(class_name='Chrome_WidgetWin_1', visible_only=True)
    print(f"Found {len(wins)} windows")

    target_win = None
    target_app = None

    for hwnd in wins:
        try:
            app = Application(backend='uia').connect(handle=hwnd)
            win = app.window(handle=hwnd)
            title = win.window_text()
            print(f"  hwnd={hwnd}: '{title}'")
            if 'GAY APP LIST' in title.upper() and ('Prepare release' in title or 'GAY APP' in title):
                target_win = win
                target_app = app
                print(f"  => TARGET FOUND")
        except Exception as e:
            print(f"  hwnd={hwnd}: error={e}")

    if not target_win:
        print("\nTarget window not found. Printing all window titles:")
        for hwnd in wins:
            try:
                app = Application(backend='uia').connect(handle=hwnd)
                win = app.window(handle=hwnd)
                print(f"  {hwnd}: '{win.window_text()}'")
            except:
                pass
        sys.exit(1)

    target_win.set_focus()
    time.sleep(1)

    print(f"\nScanning for upload button in '{target_win.window_text()}'...")
    time.sleep(3)  # Let page fully load

    # Scan all descendants for upload button
    descs = target_win.descendants()
    print(f"Total UIA elements: {len(descs)}")

    upload_btn = None
    for d in descs:
        try:
            t = d.window_text()
            ct = d.element_info.control_type
            if t and len(t) < 200:
                if any(x in t.lower() for x in ['choose files', 'upload', 'browse', 'select files']):
                    print(f"UPLOAD: [{ct}] '{t}'")
                    if ct == 'Button':
                        upload_btn = d
        except:
            pass

    if not upload_btn:
        print("\nNo upload button found. Page elements:")
        for d in descs:
            try:
                t = d.window_text()
                ct = d.element_info.control_type
                if t and len(t) < 100:
                    print(f"  [{ct}] '{t}'")
            except:
                pass
        sys.exit(1)

    print(f"\nClicking upload button: '{upload_btn.window_text()}'")
    upload_btn.set_focus()
    time.sleep(0.3)
    upload_btn.invoke()  # Trusted UIA click
    print("Button invoked! Waiting for file dialog...")
    time.sleep(3)

    # Handle file dialog
    desktop = Desktop(backend='uia')
    file_dialog = None
    for _ in range(15):
        dlgs = desktop.windows(class_name='#32770')  # Standard Windows file dialog
        for dlg in dlgs:
            title = dlg.window_text()
            print(f"  Dialog found: '{title}'")
            file_dialog = dlg
            break
        if file_dialog:
            break
        # Also try by title patterns
        for pat in ['Open', 'Choose', 'Browse', 'Upload']:
            dlgs = desktop.windows(title_re=f'.*{pat}.*')
            for dlg in dlgs:
                title = dlg.window_text()
                if title not in ('New Tab - Google Chrome', 'Claude', 'ChatGPT', 'Prepare release | GAY APP LIST - Google Chrome'):
                    print(f"  Found dialog (pattern): '{title}'")
                    file_dialog = dlg
                    break
            if file_dialog:
                break
        if file_dialog:
            break
        print("  Waiting for file dialog...")
        time.sleep(1)

    if not file_dialog:
        print("No file dialog appeared")
        sys.exit(1)

    print(f"File dialog: '{file_dialog.window_text()}'")
    edits = file_dialog.descendants(control_type='Edit')
    print(f"Edit controls: {len(edits)}")
    for i, e in enumerate(edits):
        print(f"  Edit {i}: '{e.window_text()}'")

    if edits:
        target_edit = edits[-1]
        target_edit.set_focus()
        target_edit.set_text(AAB_PATH)
        time.sleep(0.5)
        print(f"Set filename to: {AAB_PATH}")

        # Click Open
        for bt in ['Open', '&Open', 'OK']:
            try:
                ob = file_dialog.child_window(title=bt, control_type='Button')
                if ob.exists(timeout=2):
                    ob.click_input()
                    print(f"Clicked '{bt}' — FILE UPLOAD INITIATED!")
                    break
            except Exception as e:
                print(f"  '{bt}': {e}")
    else:
        print("No edit control in file dialog")


if __name__ == '__main__':
    main()
