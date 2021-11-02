# -*- coding: utf-8 -*-

"""
Anki Add-on: Quick Field Navigation

Implements shortcuts that allow you to navigate 
through your fields in the card editor.

Copyright: Glutanimate 2015-2020 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
Modified by Abdo <github.com/abdnh/>
"""

from anki.hooks import addHook
from anki import version as anki_version

point_release = int(anki_version.split(".")[-1])

def changeFocusTo(self, fldnr):
    fldnr = fldnr - 1
    fldstot = len(self.note.fields) -1
    if fldnr >= fldstot or fldnr < 0:
        # ignore onid field (Note Organizer add-on)
        if self.note.model()['flds'][-1]['name'] == "onid":
            fldnr = fldstot - 1
        else:
            fldnr = fldstot
    elif self.note.model()['flds'][0]['name'] == "ID (hidden)":
        # ignore hidden ID field (Image Occlusion Enhanced)
        fldnr += 1
    self.web.setFocus()
    self.web.eval("focusField(%d);" % int(fldnr))


if point_release < 41:
    focus_next_js = "if(!currentField) -1; else currentFieldOrdinal();"
else:
    focus_next_js = "if(!getCurrentField()) -1; else getCurrentField().ord;"

def focusNext(self):
    def cb(n):
        changeFocusTo(self, (int(n)+2) % len(self.note.fields))

    self.web.evalWithCallback(focus_next_js, cb)

if point_release < 41:
    focus_prev_js = lambda n: f"if(!currentField) {n}; else currentFieldOrdinal();"
else:
    focus_prev_js = lambda n: f"if(!getCurrentField()) {n}; else getCurrentField().ord;"

def focusPrev(self):
    def cb(n):
        changeFocusTo(self, int(n))
    self.web.evalWithCallback(focus_prev_js(len(self.note.fields)), cb)

def onSetupShortcuts(cuts, editor):
    cuts.extend(
        [(f"Ctrl+Shift+{i}", lambda f=i: changeFocusTo(editor, f), True) for i in range(10)]
    )
    cuts.append(("Ctrl+Shift+Down", lambda: focusNext(editor), True))
    cuts.append(("Ctrl+Shift+Up", lambda: focusPrev(editor), True))
    return cuts

addHook("setupEditorShortcuts", onSetupShortcuts)
