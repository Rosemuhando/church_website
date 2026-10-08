const menu = document.querySelector('[data-site-menu]');
const menuToggle = document.querySelector('[data-menu-toggle]');
let menuOverlay;

if (menu && menuToggle) {
    menuOverlay = document.createElement('button');
    menuOverlay.type = 'button';
    menuOverlay.className = 'site-menu-overlay';
    menuOverlay.setAttribute('aria-label', 'Close site menu');
    menuOverlay.hidden = true;
    document.body.append(menuOverlay);

    const setMenuOpen = (isOpen, returnFocus = false) => {
        document.body.classList.toggle('site-menu-open', isOpen);
        menuToggle.setAttribute('aria-expanded', String(isOpen));
        menuToggle.setAttribute('aria-label', isOpen ? 'Close site menu' : 'Open site menu');
        const menuLabel = menuToggle.querySelector('[data-menu-label]');
        if (menuLabel) {
            menuLabel.textContent = isOpen ? 'Close' : 'Menu';
        }
        menu.setAttribute('aria-hidden', String(!isOpen));
        menuOverlay.hidden = !isOpen;

        if (isOpen) {
            menu.querySelector('a')?.focus();
        } else if (returnFocus) {
            menuToggle.focus();
        }
    };

    menuToggle.addEventListener('click', () => {
        setMenuOpen(menuToggle.getAttribute('aria-expanded') !== 'true');
    });
    menuOverlay.addEventListener('click', () => setMenuOpen(false, true));
    menu.addEventListener('click', (event) => {
        if (event.target.closest('a')) {
            setMenuOpen(false);
        }
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
            setMenuOpen(false, true);
        }
    });

}

const sitePages = [
    { label: 'Home', url: '/', keywords: ['welcome', 'church home'] },
    { label: 'About', url: '/about/', keywords: ['about us', 'our church'] },
    { label: 'Events', url: '/events/', keywords: ['event', 'kigocco sunday', 'kigocco', 'thanksgiving'] },
    { label: 'Gallery', url: '/gallery/', keywords: ['photos', 'pictures', 'church gallery'] },
    { label: 'Contact', url: '/contact/', keywords: ['contact us', 'prayer', 'prayer request'] },
    { label: 'Sermons', url: '/sermons/', keywords: ['sermon', 'preaching', 'bible messages'] },
    { label: 'Teachings', url: '/teachings/', keywords: ['teaching', 'latest teachings', 'bible study'] },
    { label: 'Announcements', url: '/announcements/', keywords: ['announcement', 'updates', 'church news'] },
    { label: 'Tithes & Offerings', url: '/giving/', keywords: ['tithe', 'tithes', 'offering', 'offerings', 'giving', 'give', 'paybill'] },
];

const normalizeSearch = (value) => value
    .toLocaleLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();

document.querySelectorAll('[data-page-search]').forEach((form) => {
    const input = form.querySelector('input[type="search"]');
    const status = form.querySelector('.site-search-status');
    const results = document.createElement('div');
    results.className = 'site-search-results';
    results.id = 'site-search-results';
    results.setAttribute('role', 'listbox');
    results.hidden = true;
    form.append(results);
    input.setAttribute('aria-controls', results.id);
    input.setAttribute('aria-autocomplete', 'list');

    const findPages = (query) => sitePages
        .map((sitePage) => {
            const names = [sitePage.label, ...sitePage.keywords].map(normalizeSearch);
            const scores = names.map((name) => {
                if (name === query) return 0;
                if (name.startsWith(query)) return 1;
                if (name.includes(query)) return 2;
                return Infinity;
            });
            return { ...sitePage, score: Math.min(...scores) };
        })
        .filter((sitePage) => Number.isFinite(sitePage.score))
        .sort((first, second) => first.score - second.score || first.label.length - second.label.length);

    const closeResults = () => {
        results.hidden = true;
        results.replaceChildren();
    };

    const showResults = () => {
        const query = normalizeSearch(input.value);
        results.replaceChildren();

        if (!query) {
            closeResults();
            status.textContent = '';
            return;
        }

        const matches = findPages(query);
        matches.forEach((sitePage) => {
            const link = document.createElement('a');
            link.href = sitePage.url;
            link.setAttribute('role', 'option');
            link.textContent = sitePage.label;
            results.append(link);
        });

        results.hidden = matches.length === 0;
        status.textContent = matches.length
            ? `${matches.length} matching ${matches.length === 1 ? 'page' : 'pages'}. Select a result or press Enter.`
            : 'No matching pages found.';
    };

    input.addEventListener('input', showResults);
    input.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            closeResults();
            status.textContent = '';
        }
    });

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const query = normalizeSearch(input.value);
        if (!query) {
            status.textContent = 'Enter a page name to search.';
            closeResults();
            return;
        }

        const matches = findPages(query);
        if (matches.length) {
            window.location.assign(matches[0].url);
            return;
        }
        showResults();
    });

    document.addEventListener('click', (event) => {
        if (!form.contains(event.target)) {
            closeResults();
        }
    });
});
