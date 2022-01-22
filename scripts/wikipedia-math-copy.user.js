// ==UserScript==
// @name wikipedia-math-copy
// @namespace Violentmonkey Scripts
// @match *://*.wikipedia.org/*
// @grant GM_addStyle
// @description Modifies browser's copy behavior to copy the LaTeX source of math expressions in Wikipedia
// ==/UserScript==

GM_addStyle(`
.mwe-math-element {
  user-select: all;
}
`);

document.addEventListener('copy', function (event) {
    const selection = window.getSelection();
    if (selection.isCollapsed) {
        return;
    }
    const fragment = selection.getRangeAt(0).cloneContents();
    const mathElements = fragment.querySelectorAll('.mwe-math-element');
    for (let j = 0; j < mathElements.length; j++) {
        const img = mathElements[j].querySelector('img');
        const latex = img.alt;
        mathElements[j].innerHTML = '\\(' + latex + '\\)';
    }
    const div = document.createElement('div');
    div.appendChild(fragment.cloneNode(true));
    event.clipboardData.setData('text/html', div.innerHTML);
    event.clipboardData.setData('text/plain',
        fragment.textContent);
    event.preventDefault();
}, true);
