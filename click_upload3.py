"""
Click the upload button in the Play Console Prepare release window and upload the AAB.
"""
import time, sys
from pywinauto import Application, Desktop
from pywinauto.findwindows import find_windows

AAB_PATH = r'C:\Users\DH\gay-app-list\android\app\build\outputs\bundle\release\app-release.aab'

# Target the specific window we found
HWND = 5768674  # 'Prepare release | GAY APP LIST - Google Chrome'


def main():
    print(f"Connecting to hwnd={HWND} (Prepare release window)...")
    app = Application(backend='uia').connect(handle=HWND)
    win = app.window(handle=HWND)
    win.set_focus()
    time.sleep(2)
    print(f"Title: '{win.window_text()}'")

    # Wait for Angular to render the upload section
    print("Waiting for page to fully load...")
    time.sleep(3)

    # Scan all UIA elements
    descs = win.descendants()
    print(f"Total UIA elements: {len(descs)}")

    # Print all elements with text
    print("\nAll page elements:")
    upload_btn = None
    for d in descs:
        try:
            t = d.window_text()
            ct = d.element_info.control_type
            if t and len(t) < 120:
                print(f"  [{ct}] '{t}'")
                if ct == 'Button' and any(x in t.lower() for x in ['choose', 'upload', 'browse', 'select file', 'file']):
                    print(f"  *** UPLOAD BUTTON CANDIDATE ***")
                    upload_btn = d
        except:
            pass

    if not upload_btn:
        print("\nNo upload button found directly. Trying invoke on any matching element...")
        # Try all elements including non-buttons
        for d in descs:
            try:
                t = d.window_text()
                ct = d.element_info.control_type
                if t and any(x in t.lower() for x in ['choose files', 'upload app bundle', 'drag & drop']):
                    print(f"Found: [{ct}] '{t}'")
                    upload_btn = d
            except:
                pass

    if upload_btn:
        print(f"\nInvoking: '{upload_btn.window_text()}'")
        try:
            upload_btn.invoke()
        except:
            upload_btn.click_input()
        print("Clicked! Waiting for file dialog...")
        time.sleep(3)
    else:
        print("\nERROR: No upload button found")
        sys.exit(1)

    # Handle the native Windows file dialog
    print("Looking for file dialog...")
    desktop = Desktop(backend='uia')
    file_dialog = None

    for attempt in range(20):
        # Standard Windows file dialog has class #32770
        all_wins = find_windows(class_name='#32770', visible_only=True)
        for hw in all_wins:
            try:
                a = Application(backend='uia').connect(handle=hw)
                dlg_win = a.window(handle=hw)
                title = dlg_win.window_text()
                print(f"  #32770 dialog: '{title}'")
                file_dialog = dlg_win
                break
            except:
                pass

        if file_dialog:
            break

        print(f"  Attempt {attempt+1}: waiting...")
        time.sleep(1)

    if not file_dialog:
        print("No file dialog appeared")
        sys.exit(1)

    print(f"\nFile dialog: '{file_dialog.window_text()}'")
    edits = file_dialog.descendants(control_type='Edit')
    print(f"Edit controls: {len(edits)}")

    if edits:
        target_edit = edits[-1]
        print(f"Setting path: {AAB_PATH}")
        target_edit.set_focus()
        target_edit.set_text(AAB_PATH)
        time.sleep(0.5)

        # Click Open
        for bt in ['Open', '&Open', 'OK']:
            try:
                ob = file_dialog.child_window(title=bt, control_type='Button')
                if ob.exists(timeout=2):
                    ob.click_input()
                    print(f"\n=== SUCCESS: Clicked '{bt}' — FILE IS UPLOADING ===")
                    time.sleep(3)
                    return
            except Exception as e:
                print(f"  '{bt}': {e}")

        print("Could not click Open button")
    else:
        print("No edit control in dialog")


if __name__ == '__main__':
    main()
