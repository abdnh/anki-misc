from aqt import gui_hooks
from aqt.editor import EditorWebView
from aqt.qt import QMenu
from aqt.utils import openLink


def add_open_link(webview: EditorWebView, menu: QMenu):
    data = webview.page().contextMenuData()
    url = data.linkUrl()
    if url.isValid():
        a = menu.addAction("Open Link")
        a.triggered.connect(lambda _: openLink(url))


gui_hooks.editor_will_show_context_menu.append(add_open_link)
