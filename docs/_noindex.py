"""Staging noindex: keep the deployed book out of search results until share-time.

WHY THIS EXISTS
    The book deploys to a public URL before it is shared with anyone (M021: the
    deploy is a staging surface, not a send). Search indexing would quietly
    falsify "no one has the URL", so every built page carries
    `<meta name="robots" content="noindex, nofollow">` until the material is
    ready to be found.

HOW TO TURN IT OFF AT SHARE-TIME  <-- the one thing to do
    Comment out (or delete) the single line `_noindex: .` under
    `sphinx.local_extensions` in docs/_config.yml, then rebuild. Nothing else
    changes; this file can stay where it is. Confirm with:

        grep -c 'name="robots"' docs/_build/html/index.html      # 1 -> 0

WHY NOT robots.txt
    The book is served from a GitHub *project* Pages site,
    https://markhendricks.github.io/quant-ai/. Crawlers read robots.txt only at
    the host root (markhendricks.github.io/robots.txt), which this repository
    does not publish, so a robots.txt shipped inside the book would sit at
    /quant-ai/robots.txt and be ignored. A per-page meta tag is read wherever
    the page is served, which also means it keeps working if the site ever
    moves to its own domain.

    The tag is emitted through Sphinx's `html-page-context` event, so it reaches
    every generated page — content pages, the search page, the index — not only
    the pages written in MyST.
"""

TAG = '<meta name="robots" content="noindex, nofollow" />'


def _add_noindex(app, pagename, templatename, context, doctree):
    # `metatags` is rendered inside <head> by sphinx's basic/layout.html, which
    # pydata_sphinx_theme inherits. Append rather than assign: MyST front-matter
    # and other extensions write here too.
    context["metatags"] = context.get("metatags", "") + "\n    " + TAG


def setup(app):
    app.connect("html-page-context", _add_noindex)
    return {"version": "1.0", "parallel_read_safe": True,
            "parallel_write_safe": True}
