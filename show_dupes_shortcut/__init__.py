from typing import List, Tuple

import aqt


def show_dupes_hook(shortcuts: List[Tuple], editor: aqt.editor.Editor):
    def show_dupes():
        if editor.note.dupeOrEmpty() == 2:
            editor.saveNow(editor.showDupes)

    shortcuts.append(("Ctrl+Shift+D", show_dupes, True))


aqt.gui_hooks.editor_did_init_shortcuts.append(show_dupes_hook)
