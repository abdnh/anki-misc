// ==UserScript==
// @name mathjax-copy
// @namespace Violentmonkey Scripts
// @match *://*/*
// @grant GM_addStyle
// @description Modifies browser's copy behavior to copy the LaTeX source of MathJax expressions enclosed in `\\(` for easy pasting in Anki
// ==/UserScript==

/*
*** TODO ***
- Sometimes extra line breaks are inserted before text nodes when pasting in Anki because Anki apparently wraps them in divs.
- Only works with MathJax 2
*/


GM_addStyle(`
  span[id*="MathJax-Element-"] {
    user-select: all;
  }
`);


document.addEventListener('copy', function (event) {
    const selection = window.getSelection();
    if (selection.isCollapsed) {
        return;
    }
    const fragment = new DocumentFragment();
    for (let i = 0; i < selection.rangeCount; i++) {
        fragment.append(selection.getRangeAt(i).cloneContents());
    }

    const mathjaxElements = fragment.querySelectorAll('span[id*="MathJax-Element-"]');
    if (mathjaxElements.length <= 0) {
        return;
    }

    // Remove empty MathJax_Preview elements
    for (const el of fragment.querySelectorAll('.MathJax_Preview')) {
        el.remove();
    }

    for (const el of mathjaxElements) {
        const id = el.id;
        const n = id.slice(0, id.search('Frame') - 1).split('-')[2];
        const scr = document.querySelector('#MathJax-Element-' + n);
        const expr = '\\(' + scr.textContent + '\\)';
        const span = document.createElement('span');
        span.innerText = expr;
        el.parentNode.replaceChild(span, el);
    }

    const div = document.createElement('div');
    div.appendChild(fragment.cloneNode(true));
    event.clipboardData.setData('text/html', div.innerHTML);
    event.clipboardData.setData('text/plain', div.innerText);

    event.preventDefault();
}, true);
