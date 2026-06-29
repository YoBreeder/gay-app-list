"""
Use UIA to:
1. Navigate Chrome to the Play Console prepare release page
2. Find and click the "Choose files" upload button
3. Handle the file dialog
"""
import time, sys
from pywinauto import Application, Desktop
from pywinauto.findwindows import find_windows
from pywinauto.keyboard import send_keys

AAB_PATH = r'C:\Users\DH\gay-app-list\android\app\build\outputs\bundle\release\app-release.aab'
CHROME_HWND = 526114
RELEASE_URL = 'https://play.google.com/console/u/0/developers/8841904810182759765/app/4974539322578443286/tracks/4697670620529789193/releases/1/prepare'


def navigate_to_release_page(win):
    """Type URL into address bar and navigate."""
    print("Navigating to release page via address bar...")
    try:
        addr_bar = win.child_window(title='Address and search bar', control_type='Edit')
        if addr_bar.exists(timeout=3):
            addr_bar.click_input()
            time.sleep(0.3)
            addr_bar.set_text(RELEASE_URL)
            time.sleep(0.3)
            send_keys('{ENTER}')
            print("URL entered, waiting for page load...")
            time.sleep(5)
            return True
    except Exception as e:
        print(f"Address bar navigation failed: {e}")
    return False


def find_and_click_upload(win):
    """Find the upload button and click it."""
    print(f"Window title: '{win.window_text()}'")
    print("Scanning for upload/file input button...")

    # Wait for page to fully load
    for attempt in range(5):
        try:
            descs = win.descendants()
            texts = []
            for d in descs:
                try:
                    t = d.window_text()
                    ct = d.element_info.control_type
                    if t:
                        texts.append((ct, t))
                except:
                    pass

            # Look for upload-related elements
            upload_elements = [(ct, t) for ct, t in texts if any(
                x in t.lower() for x in ['choose files', 'upload', 'browse', '.aab', 'app bundle']
            )]
            if upload_elements:
                print(f"Found upload elements: {upload_elements[:5]}")
                break
            else:
                print(f"Attempt {attempt+1}: No upload button yet, waiting...")
                time.sleep(2)
        except Exception as e:
            print(f"Scan error: {e}")
            time.sleep(2)

    # Try clicking upload button
    for text in ['Choose files', 'Upload', 'Browse', 'Select files']:
        try:
            btn = win.child_window(title=text, control_type='Button')
            if btn.exists(timeout=2):
                print(f"Found button '{text}', clicking via UIA InvokePattern...")
                btn.invoke()  # UIA invoke - treated as trusted
                print("Invoked!")
                time.sleep(3)
                return True
        except Exception as e:
            print(f"  Button '{text}': {e}")

    # Try by partial text match
    try:
        all_btns = win.descendants(control_type='Button')
        for btn in all_btns:
            try:
                t = btn.window_text()
                if 'choose' in t.lower() or 'upload' in t.lower() or 'browse' in t.lower():
                    print(f"Clicking button by scan: '{t}'")
                    btn.invoke()
                    time.sleep(3)
                    return True
            except:
                pass
    except Exception as e:
        print(f"Btn scan: {e}")

    return False


def handle_file_dialog():
    """Handle the native Windows file dialog."""
    print("Waiting for file open dialog...")
    time.sleep(2)
    desktop = Desktop(backend='uia')

    for _ in range(10):
        for pat in ['Open', 'Choose File', 'Upload', '']:
            try:
                if pat:
                    dlgs = desktop.windows(title_re=f'.*{pat}.*')
                else:
                    dlgs = desktop.windows(class_name='#32770')  # Standard file dialog class
                for dlg in dlgs:
                    title = dlg.window_text()
                    if title not in ('', 'New Tab - Google Chrome', 'Claude', 'ChatGPT'):
                        print(f"Potential file dialog: '{title}'")
                        edits = dlg.descendants(control_type='Edit')
                        if edits:
                            target_edit = edits[-1]
                            print(f"Setting filename to: {AAB_PATH}")
                            target_edit.set_text(AAB_PATH)
                            time.sleep(0.5)
                            # Click Open button
                            for bt in ['Open', '&Open', 'OK']:
                                try:
                                    ob = dlg.child_window(title=bt, control_type='Button')
                                    if ob.exists(timeout=1):
                                        ob.click_input()
                                        print(f"SUCCESS: Clicked '{bt}' in file dialog!")
                                        return True
                                except:
                                    pass
            except:
                pass
        print("  No file dialog found yet, retrying...")
        time.sleep(1)

    print("File dialog not found after retries")
    return False


def main():
    print(f"Connecting to Chrome hwnd={CHROME_HWND}...")
    app = Application(backend='uia').connect(handle=CHROME_HWND)
    win = app.window(handle=CHROME_HWND)
    win.set_focus()
    time.sleep(0.5)

    # Navigate to the release page
    if not navigate_to_release_page(win):
        print("WARNING: Could not navigate via address bar, trying anyway...")

    print(f"Window title after navigation: '{win.window_text()}'")

    # Find and click upload
    if find_and_click_upload(win):
        # Handle the file dialog
        if handle_file_dialog():
            print("\n=== UPLOAD INITIATED SUCCESSFULLY ===")
        else:
            print("\nWARNING: File dialog not handled")
    else:
        print("\nCould not find upload button")
        # Dump all text elements for debugging
        try:
            descs = win.descendants()
            print(f"\nAll text elements ({len(descs)} total):")
            for d in descs[:200]:
                try:
                    t = d.window_text()
                    ct = d.element_info.control_type
                    if t and len(t) < 100:
                        print(f"  [{ct}] '{t}'")
                except:
                    pass
        except:
            pass


if __name__ == '__main__':
    main()
