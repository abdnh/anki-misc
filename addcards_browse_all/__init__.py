import aqt
from aqt.qt import QAction, qconnect


def add_browse_all(addcards, menu):
    def browse_history():
        browser = aqt.dialogs.open("Browser", addcards.mw)
        nids = []
        for nid in addcards.history:
            nids.append(str(nid))
        browser.form.searchEdit.lineEdit().setText("nid:%s" % ",".join(nids))
        browser.onSearchActivated()

    actions = menu.actions()
    a = QAction("Browse All", menu)
    qconnect(a.triggered, browse_history)
    menu.insertAction(actions[0], a)


aqt.gui_hooks.add_cards_will_show_history_menu.append(add_browse_all)
