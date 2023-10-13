import subprocess

from anki.utils import isMac, isWin, noBundledLibs
from aqt import mw
from aqt.gui_hooks import editor_will_show_context_menu, webview_will_show_context_menu
from aqt.qt import *
from aqt.webview import AnkiWebView


# Credit: https://stackoverflow.com/questions/3490336/how-to-reveal-in-finder-or-show-in-explorer-with-qt
def reveal_in_file_manager(path: str) -> None:
    if isWin:
        subprocess.run(f"explorer /select,file://{path}", check=False, shell=True)
    elif isMac:
        subprocess.run(
            [
                "osascript",
                "-e",
                'tell application "Finder"',
                "-e",
                "activate",
                "-e",
                f'select POSIX file "{path}"',
                "-e",
                "end tell",
            ],
            check=False,
        )
    else:
        # Just open the file in any other platform
        with noBundledLibs():
            QDesktopServices.openUrl(QUrl(f"file://{path}"))


def add_reveal_in_file_manager(webview: AnkiWebView, menu: QMenu) -> None:
    if qtmajor >= 6:
        context_data = webview.lastContextMenuRequest()
    else:
        context_data = webview.page().contextMenuData()
    url = context_data.mediaUrl()
    image_name = url.fileName()
    path = os.path.join(mw.col.media.dir(), image_name)
    if url.isValid():
        action = menu.addAction("Reveal in file manager")
        action.triggered.connect(lambda _, u=path: reveal_in_file_manager(u))


editor_will_show_context_menu.append(add_reveal_in_file_manager)
webview_will_show_context_menu.append(add_reveal_in_file_manager)
