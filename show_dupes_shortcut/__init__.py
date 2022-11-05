from typing import List, Tuple

import aqt

config = aqt.mw.addonManager.getConfig(__name__)


def show_dupes_hook(shortcuts: List[Tuple], editor: aqt.editor.Editor):
    def show_dupes():
        if editor.note.dupeOrEmpty() == 2:
            editor.saveNow(editor.showDupes)

    shortcuts.append((config["shortcut"], show_dupes, True))


aqt.gui_hooks.editor_did_init_shortcuts.append(show_dupes_hook)
