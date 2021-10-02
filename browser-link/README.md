# browser-link

Adds the `search` [pycmd](https://addon-docs.ankiweb.net/hooks-and-filters.html#webview) command to open a browser window with the provided search string from the review/preview/card layout screens.

As an example, you can use the following HTML code in your notes to open a browser window to search in the Default deck:
```html
<a href=# onclick="pycmd('search:deck:Default'); return false;">Search Default deck</a>
```
