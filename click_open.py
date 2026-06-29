"""
Complete the file dialog: set the path and click Open.
Run this immediately after the file dialog is open.
"""
import time, sys
from pywinauto import Application, Desktop
from pywinauto.findwindows import find_windows
from pywinauto.keyboard import send_keys

AAB_PATH = r'C:\Users\DH\gay-app-list\android\app\build\outputs\bundle\release\app-release.aab'


def main():
    print("Looking for Open file dialog...")
    file_dialog = None
    for attempt in range(5):
        all_wins = find_windows(class_name='#32770', visible_only=True)
        for hw in all_wins:
            try:
                a = Application(backend='uia').connect(handle=hw)
                dlg = a.window(handle=hw)
                title = dlg.window_text()
                print(f"  Found: '{title}' hwnd={hw}")
                if title == 'Open':
                    file_dialog = dlg
                    break
            except:
                pass
        if file_dialog:
            break
        time.sleep(1)

    if not file_dialog:
        print("No 'Open' dialog found")
        sys.exit(1)

    print(f"File dialog: '{file_dialog.window_text()}'")

    # Print all edit controls
    edits = file_dialog.descendants(control_type='Edit')
    print(f"Edit controls ({len(edits)}):")
    for i, e in enumerate(edits):
        print(f"  [{i}] '{e.window_text()}'")

    # Set filename in the filename edit (usually the one labeled 'File name:' or similar)
    # The filename bar is usually the last visible Edit, or the one with empty/path text
    filename_edit = None
    for e in edits:
        try:
            t = e.window_text()
            # Look for the filename input (usually shorter text or empty)
            if t == '' or 'aab' in t.lower() or 'All Files' not in t:
                filename_edit = e
        except:
            pass

    # Use the last edit control as fallback (typical for Windows file dialogs)
    if not filename_edit:
        filename_edit = edits[-1]

    print(f"\nSetting filename in edit: '{filename_edit.window_text()}'")
    filename_edit.set_focus()
    time.sleep(0.2)
    # Use type_keys with special handling to clear and type the path
    filename_edit.set_text('')
    time.sleep(0.1)
    send_keys(AAB_PATH.replace('\\', '\\\\'), with_spaces=True, pause=0.01)
    time.sleep(0.5)

    print("Pressing Enter to submit...")
    send_keys('{ENTER}')
    time.sleep(1)

    print("Checking if dialog is still open...")
    time.sleep(2)
    remaining = find_windows(class_name='#32770', visible_only=True)
    if remaining:
        print(f"Dialog still open - trying to click Open button...")
        for hw in remaining:
            try:
                a = Application(backend='uia').connect(handle=hw)
                dlg = a.window(handle=hw)
                # Get all buttons
                btns = dlg.descendants(control_type='Button')
                print(f"Buttons in dialog:")
                for b in btns:
                    t = b.window_text()
                    rect = b.rectangle()
                    print(f"  '{t}' at {rect}")

                # Click the main 'Open' button (usually bottom right)
                open_buttons = [b for b in btns if b.window_text() in ('Open', '&Open')]
                if open_buttons:
                    # Sort by position, click the last one (bottom right = main action)
                    open_buttons_sorted = sorted(open_buttons, key=lambda b: (b.rectangle().top, b.rectangle().left))
                    btn = open_buttons_sorted[-1]
                    print(f"Clicking '{btn.window_text()}' at {btn.rectangle()}")
                    btn.click_input()
                    print("CLICKED Open!")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("=== Dialog closed — file submitted successfully! ===")


if __name__ == '__main__':
    main()
