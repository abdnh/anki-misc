import random
from typing import List

from anki.template import TemplateRenderOutput, TemplateRenderContext
from anki.hooks import card_did_render


css = """
<style>
.tag {
    display: inline-block;
    margin: 5px;
    padding: 5px;
    border: 1px dashed black;
}
</style>
"""

html = """<div id="tag-list">{}</div>"""

# Some snippets are adapted from https://stackoverflow.com/a/35970186


def rand_color() -> List[int]:
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return [r, g, b]


def fb_from_bg(color):
    r = color[0]
    g = color[1]
    b = color[2]
    return [0, 0, 0] if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else [255, 255, 255]


def pad_zero(s):
    return s.zfill(2)


def format_color(color):
    r = hex(color[0])[2:]
    g = hex(color[1])[2:]
    b = hex(color[2])[2:]
    return "#" + pad_zero(r) + pad_zero(g) + pad_zero(b)


def taglist_str(tags: List[str]) -> str:
    elements = []
    for tag in tags:
        color = rand_color()
        bg_color = format_color(color)
        fg_color = format_color(fb_from_bg(color))
        span = f'<span class="tag" style="color: {fg_color}; background-color: {bg_color};">{tag}</span>'
        elements.append(span)
        # add a non-breaking space for easy copying
        elements.append("\xA0")
    if len(elements) > 0:
        elements.pop()

    return "\n".join(elements)


def on_card_did_render(
    output: TemplateRenderOutput, ctx: TemplateRenderContext
) -> None:
    tags = ctx.note().tags
    text = html.format(taglist_str(tags)) + css
    output.question_text = text + output.question_text
    output.answer_text = text + output.answer_text


card_did_render.append(on_card_did_render)
