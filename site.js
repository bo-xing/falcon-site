/* Progressive enhancements only: links, legal text and FAQs work without JS. */
(() => {
  const languageLink = document.querySelector('.language-link');
  const syncLanguageAnchor = () => {
    if (languageLink) languageLink.hash = location.hash;
  };
  syncLanguageAnchor();
  window.addEventListener('hashchange', syncLanguageAnchor);
  window.addEventListener('pageshow', syncLanguageAnchor);

  const themeButton = document.querySelector('.theme-toggle');
  if (themeButton) {
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
    const isDark = () => document.documentElement.dataset.theme ? document.documentElement.dataset.theme === 'dark' : systemTheme.matches;
    const updateLabel = () => themeButton.setAttribute('aria-label', isDark() ? themeButton.dataset.lightLabel : themeButton.dataset.darkLabel);
    themeButton.hidden = false;
    updateLabel();
    themeButton.addEventListener('click', () => {
      const theme = isDark() ? 'light' : 'dark';
      document.documentElement.dataset.theme = theme;
      try { localStorage.setItem('falcon-site-theme', theme); } catch { /* Optional preference. */ }
      updateLabel();
    });
    systemTheme.addEventListener('change', updateLabel);
  }
  const nav = document.querySelector('.site-nav');
  const menu = document.querySelector('.menu-toggle');
  if (nav && menu) {
    document.documentElement.classList.add('nav-ready');
    menu.hidden = false;
    const closeMenu = () => { nav.classList.remove('is-open'); menu.setAttribute('aria-expanded', 'false'); };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      nav.classList.toggle('is-open', open);
      menu.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); }
    });
    window.matchMedia('(min-width: 900px)').addEventListener('change', closeMenu);
  }

  const tablist = document.querySelector('.screen-tabs');
  if (tablist) {
    const tabs = [...tablist.querySelectorAll('[role="tab"]')];
    const galleryHint = document.querySelector('.gallery-hint');
    const select = tab => {
      tabs.forEach(item => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
        const panel = document.getElementById(item.getAttribute('aria-controls'));
        panel.hidden = !selected;
        panel.setAttribute('role', 'tabpanel');
        panel.tabIndex = 0;
        if (selected && galleryHint) {
          galleryHint.hidden = panel.querySelectorAll('.screenshot-card').length < 2;
        }
      });
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); select(tabs[next]); tabs[next].focus(); }
      });
    });
    select(tabs[0]);
    document.documentElement.classList.add('tabs-ready');
    tablist.hidden = false;
  }

  const dialog = document.querySelector('.lightbox');
  if (dialog && typeof dialog.showModal === 'function') {
    const preview = dialog.querySelector('img');
    const caption = dialog.querySelector('figcaption');
    let trigger;
    document.querySelectorAll('[data-lightbox]').forEach(link => {
      link.addEventListener('click', event => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        trigger = link;
        preview.src = link.href;
        preview.alt = link.querySelector('img').alt;
        caption.textContent = preview.alt;
        dialog.showModal();
      });
    });
    dialog.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => { preview.removeAttribute('src'); trigger?.focus(); });
  }

  const copyButton = document.querySelector('.copy-email');
  if (copyButton && navigator.clipboard?.writeText) {
    copyButton.hidden = false;
    copyButton.addEventListener('click', async () => {
      const status = document.querySelector('.copy-status');
      try {
        await navigator.clipboard.writeText(copyButton.dataset.copy);
        status.textContent = copyButton.dataset.success;
      } catch { status.textContent = copyButton.dataset.failure; }
    });
  }

  const toc = document.querySelector('.toc details');
  if (toc && window.matchMedia('(max-width: 620px)').matches) toc.open = false;

  // Direct FAQ URLs should reveal their answer, including restored browser pages.
  const revealAnswer = () => {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target?.matches('details.faq-item')) {
      target.open = true;
      requestAnimationFrame(() => target.scrollIntoView({ behavior: 'instant', block: 'start' }));
    }
  };
  window.addEventListener('pageshow', revealAnswer);
  window.addEventListener('hashchange', revealAnswer);
})();
