from typing import Tuple, Any

import aqt
from aqt.reviewer import Reviewer
from aqt.clayout import CardLayout
from aqt.browser.previewer import Previewer
from aqt import gui_hooks


def handle_msg(handled: Tuple[bool, Any], message: str, context: Any):
    if not isinstance(
        context, (Reviewer, CardLayout, Previewer)
    ) or not message.startswith("search:"):
        return handled

    aqt.dialogs.open("Browser", aqt.mw, search=(message[len("search:") :],))
    return (True, None)


gui_hooks.webview_did_receive_js_message.append(handle_msg)
