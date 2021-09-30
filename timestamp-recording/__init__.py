import datetime
import json

import aqt
from aqt.editor import Editor


def on_rec_sound(self) -> None:
    def on_done(file):
        now = datetime.datetime.now().isoformat(timespec="seconds")
        txt = now + ":&nbsp;"
        self.web.evalWithCallback(
            f"setFormat('inserthtml', {json.dumps(txt)});",
            lambda _: self.addMedia(file),
        )

    aqt.sound.record_audio(
        self.parentWindow,
        self.mw,
        True,
        on_done,
    )


# It seems we have to monkey-patch onRecSound via _links because this is how Anki calls it
Editor._links["record"] = on_rec_sound
