from typing import List

from aqt.utils import getText
from aqt.qt import *
from aqt import gui_hooks
from aqt.editor import Editor

addon_dir = os.path.dirname(__file__)

# TODO: Add the ability to add attributes
def add_tag(editor: Editor):
    tag = getText("The name of the tag: ")
    if tag[0] != "":
        editor.web.eval("wrap('<{0}>', '</{0}>');".format(tag[0]))


def add_editor_button(buttons: List[str], editor: Editor):
    button = editor.addButton(
        os.path.join(addon_dir, "icon.png"),
        "html_wrap",
        add_tag,
        tip="Wrap in HTML tag",
        keys="Ctrl+Shift+H",
    )

    buttons.append(button)


gui_hooks.editor_did_init_buttons.append(add_editor_button)
