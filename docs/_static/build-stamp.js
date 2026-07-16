// Standard thin-shell site-build stamp.
//
// GitHub Pages sets Last-Modified on each published HTML file when the site
// artifact is deployed. Display that value as a book-level build time. This is
// deliberately not described as the last edit time for the current page.
(function () {
    'use strict';

    const formatter = new Intl.DateTimeFormat('en-US', {
        timeZone: 'America/Chicago',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        timeZoneName: 'short'
    });

    function renderStamp(modified) {
        if (!(modified instanceof Date) || Number.isNaN(modified.getTime())) {
            return;
        }

        const footer = document.querySelector('.bd-footer-content__inner');
        if (!footer || footer.querySelector('.webbook-build-stamp')) {
            return;
        }

        const item = document.createElement('div');
        item.className = 'footer-item webbook-build-stamp';
        item.dataset.buildUtc = modified.toISOString();
        item.title = 'Published site build time, not the last substantive edit to this page.';

        const text = document.createElement('p');
        text.textContent = `Site build: ${formatter.format(modified)}`;
        text.style.cssText = [
            'color: var(--pst-color-text-muted, #666)',
            'font-size: 0.8rem',
            'margin-bottom: 5px'
        ].join('; ');

        item.appendChild(text);
        footer.appendChild(item);
    }

    async function addBuildStamp() {
        try {
            const response = await fetch(window.location.href, {
                method: 'HEAD',
                cache: 'no-store'
            });
            const header = response.headers.get('Last-Modified');
            if (header) {
                renderStamp(new Date(header));
                return;
            }
        } catch (_) {
            // Local file previews may not support HEAD. Use the browser's
            // document timestamp as a best-effort fallback.
        }
        renderStamp(new Date(document.lastModified));
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addBuildStamp);
    } else {
        addBuildStamp();
    }
}());
