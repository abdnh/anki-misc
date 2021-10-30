from anki.template import TemplateRenderOutput, TemplateRenderContext
from anki.hooks import card_did_render

js = """
<script>
    /* Some snippets are taken from https://stackoverflow.com/a/35970186 */

    function randColor() {
        var x = Math.floor(Math.random() * 256);
        var y = Math.floor(Math.random() * 256);
        var z = Math.floor(Math.random() * 256);
        return [x, y, z];
    }

    function fgFromBg(color) {
        let r = color[0];
        let g = color[1];
        let b = color[2];
        return (r * 0.299 + g * 0.587 + b * 0.114) > 186
            ? [0,0,0]
            : [255,255,255];
    }

    function formatColor(color) {
        let r = color[0].toString(16);
        let g = color[1].toString(16);
        let b = color[2].toString(16);
        return '#' + padZero(r) + padZero(g) + padZero(b);
    }

    function padZero(str, len) {
        len = len || 2;
        var zeros = new Array(len).join('0');
        return (zeros + str).slice(-len);
    }

    var container = document.getElementById("tag-list");
    var tags = "{{Tags}}".split(" ");
    for(let tag of tags) {
        if(!tag) {
            continue;
        }
        let span = document.createElement("span");
        span.className = "tag";
        span.textContent = tag;
        let color = randColor();
        span.style.backgroundColor = formatColor(color);
        span.style.color = formatColor(fgFromBg(color));
        container.appendChild(span);
        // add a non-breaking space for easy copying
        container.appendChild(new Text('\xA0'));
    }
    if(container.lastChild) {
        container.removeChild(container.lastChild);
    }
</script>
"""

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

html = """<div id="tag-list"></div>"""


def on_card_did_render(output: TemplateRenderOutput, ctx: TemplateRenderContext) -> None:
    tags = " ".join(ctx.note().tags)
    text = html + css + js.replace("{{Tags}}", tags)
    output.question_text = text + output.question_text
    output.answer_text = text + output.answer_text


card_did_render.append(on_card_did_render)
