const currentPageTitle = document.querySelector('[data-current-page-title]');
if (currentPageTitle) {
    const title = document.title.split('|')[0].trim();
    currentPageTitle.textContent = window.location.pathname === '/' && title === 'Full Gospel Churches of Kenya - Njiru'
        ? 'Home'
        : title;
}

const pageChrome = document.querySelector('.page-chrome');
const siteNavbar = document.querySelector('.navbar');
if (pageChrome && siteNavbar) {
    const siteLogo = siteNavbar.querySelector('.logo');
    if (siteLogo) {
        siteLogo.after(pageChrome);
    } else {
        siteNavbar.prepend(pageChrome);
    }
}

document.querySelector('[data-page-back]')?.addEventListener('click', () => window.history.back());
document.querySelector('[data-page-forward]')?.addEventListener('click', () => window.history.forward());
document.querySelector('[data-page-refresh]')?.addEventListener('click', () => window.location.reload());

const menu = document.querySelector('[data-site-menu]');
const menuToggle = document.querySelector('[data-menu-toggle]');

if (menu && menuToggle) {
    const primaryLabels = ['home', 'about', 'sermons', 'contact'];
    const links = Array.from(menu.querySelectorAll('a'));
    const primaryLinks = links
        .filter((link) => primaryLabels.includes(link.textContent.trim().toLocaleLowerCase()))
        .sort((first, second) => primaryLabels.indexOf(first.textContent.trim().toLocaleLowerCase())
            - primaryLabels.indexOf(second.textContent.trim().toLocaleLowerCase()));
    const primaryIcons = {
        home: 'fa-house',
        about: 'fa-church',
        sermons: 'fa-book-bible',
        contact: 'fa-phone',
    };
    const moreLinks = links.filter((link) => !primaryLinks.includes(link));
    const primaryNavigation = document.createElement('div');
    const morePages = document.createElement('div');
    const morePanel = document.createElement('div');

    primaryNavigation.className = 'site-primary-links';
    primaryNavigation.setAttribute('aria-label', 'Main pages');
    morePages.className = 'site-more-pages';
    morePanel.className = 'site-more-panel';
    morePanel.id = 'site-more-pages-menu';
    morePanel.hidden = true;

    primaryLinks.forEach((link) => {
        const labelText = link.textContent.trim();
        const label = labelText.toLocaleLowerCase();
        let icon = link.querySelector('i');

        if (!icon) {
            icon = document.createElement('i');
        }

        icon.className = `fa-solid ${primaryIcons[label]}`;
        icon.setAttribute('aria-hidden', 'true');
        const labelElement = document.createElement('span');
        labelElement.className = 'site-primary-label';
        labelElement.textContent = labelText;
        link.replaceChildren(icon, labelElement);
        link.setAttribute('aria-label', labelText);
        link.title = labelText;
        primaryNavigation.append(link);
    });
    moreLinks.forEach((link) => morePanel.append(link));

    menuToggle.replaceChildren(document.createTextNode('More '));
    const moreIcon = document.createElement('i');
    moreIcon.className = 'fa-solid fa-chevron-down';
    moreIcon.setAttribute('aria-hidden', 'true');
    menuToggle.append(moreIcon);
    menuToggle.setAttribute('aria-controls', morePanel.id);
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'More pages');

    morePages.append(menuToggle, morePanel);
    menu.replaceChildren(primaryNavigation, morePages);

    const headerTools = document.createElement('div');
    const pageTitle = siteNavbar.querySelector('.page-chrome-title');
    const pageControls = siteNavbar.querySelector('.page-chrome-controls');
    const searchForm = siteNavbar.querySelector('[data-page-search]');

    headerTools.className = 'site-header-tools';
    if (pageTitle && pageControls && searchForm) {
        headerTools.append(pageControls, pageTitle, searchForm);
        pageChrome?.remove();
        siteNavbar.append(headerTools);
    }

    const setMoreExpanded = (isExpanded, returnFocus = false) => {
        menuToggle.setAttribute('aria-expanded', String(isExpanded));
        morePanel.hidden = !isExpanded;
        morePages.classList.toggle('is-open', isExpanded);

        if (returnFocus) {
            menuToggle.focus();
        }
    };

    setMoreExpanded(false);
    menuToggle.addEventListener('click', () => {
        setMoreExpanded(menuToggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
            setMoreExpanded(false, true);
        }
    });
    document.addEventListener('click', (event) => {
        if (!morePages.contains(event.target)) {
            setMoreExpanded(false);
        }
    });
    morePanel.addEventListener('click', (event) => {
        if (event.target.closest('a')) {
            setMoreExpanded(false);
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
    { label: 'Sign in', url: '/login/', keywords: ['login', 'member account', 'user access'] },
    { label: 'Create account', url: '/register/', keywords: ['register', 'sign up', 'new member'] },
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
