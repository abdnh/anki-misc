// ==UserScript==
// @name katex-copy
// @namespace Violentmonkey Scripts
// @match *://*/*
// @grant GM_addStyle
// @description Modifies browser's copy behavior to copy the LaTeX source of KaTeX expressions surrounded by specified delimiters
// ==/UserScript==

GM_addStyle(`
    .katex,
    .katex-display {
        user-select: all !important;
    }
`);

// Set these to how you want inline and display math to be delimited.
const defaultCopyDelimiters = {
    inline: ['\\(', '\\)'],    // alternative:  ['$', '$']
    display: ['\\[', '\\]'], // alternative: ['$$', '$$']
};

// Replace .katex elements with their TeX source (<annotation> element).
// Modifies fragment in-place.  Useful for writing your own 'copy' handler,
// as in copy-tex.js.
const katexReplaceWithTex = function (fragment,
    copyDelimiters = defaultCopyDelimiters) {
    // Remove .katex-html blocks that are preceded by .katex-mathml blocks
    // (which will get replaced below).
    const katexHtml = fragment.querySelectorAll('.katex-mathml + .katex-html');
    for (let i = 0; i < katexHtml.length; i++) {
        const element = katexHtml[i];
        if (element.remove) {
            element.remove(null);
        } else {
            element.parentNode.removeChild(element);
        }
    }
    // Replace .katex-mathml elements with their annotation (TeX source)
    // descendant, with inline delimiters.
    const katexMathml = fragment.querySelectorAll('.katex-mathml');
    for (let i = 0; i < katexMathml.length; i++) {
        const element = katexMathml[i];
        const texSource = element.querySelector('annotation');
        if (texSource) {
            if (element.replaceWith) {
                element.replaceWith(texSource);
            } else {
                element.parentNode.replaceChild(texSource, element);
            }
            texSource.innerHTML = copyDelimiters.inline[0] +
                texSource.innerHTML + copyDelimiters.inline[1];
        }
    }
    // Switch display math to display delimiters.
    const displays = fragment.querySelectorAll('.katex-display annotation');
    for (let i = 0; i < displays.length; i++) {
        const element = displays[i];
        element.innerHTML = copyDelimiters.display[0] +
            element.innerHTML.substr(copyDelimiters.inline[0].length,
                element.innerHTML.length - copyDelimiters.inline[0].length
                - copyDelimiters.inline[1].length)
            + copyDelimiters.display[1];
    }
    return fragment;
};


// Global copy handler to modify behavior on .katex elements.
document.addEventListener('copy', function (event) {
    const selection = window.getSelection();
    if (selection.isCollapsed) {
        return;  // default action OK if selection is empty
    }
    const fragment = selection.getRangeAt(0).cloneContents();
    if (!fragment.querySelector('.katex-mathml')) {
        return;  // default action OK if no .katex-mathml elements
    }

    const processedFragment = katexReplaceWithTex(fragment);
    const div = document.createElement('div');
    div.appendChild(processedFragment.cloneNode(true));
    event.clipboardData.setData('text/html', div.innerHTML);

    // Rewrite plain-text version.
    event.clipboardData.setData('text/plain',
        processedFragment.textContent);
    // Prevent normal copy handling.
    event.preventDefault();
});
