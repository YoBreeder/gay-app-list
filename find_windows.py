from pywinauto.findwindows import find_windows
from pywinauto import Application

all_wins = find_windows(visible_only=True)
for hw in all_wins:
    try:
        a = Application(backend='uia').connect(handle=hw)
        win = a.window(handle=hw)
        t = win.window_text()
        if t and len(t) > 3:
            print(f'hwnd={hw} title={t!r}')
    except:
        pass
