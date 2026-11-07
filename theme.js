// Apply a saved appearance before CSS paints. No network requests or identifiers.
(() => {
  try {
    const preference = localStorage.getItem('falcon-site-theme');
    if (preference === 'light' || preference === 'dark') document.documentElement.dataset.theme = preference;
  } catch { /* Storage can be unavailable; fall back to the system appearance. */ }

  // Browser chrome must follow the selected page theme, including a saved override.
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  const syncThemeColor = () => {
    const theme = document.documentElement.dataset.theme;
    const dark = theme ? theme === 'dark' : systemTheme.matches;
    document.querySelectorAll('meta[name="theme-color"]').forEach(meta => {
      meta.content = dark ? '#0c101b' : '#f7f8fc';
    });
  };
  syncThemeColor();
  systemTheme.addEventListener('change', syncThemeColor);
  new MutationObserver(syncThemeColor).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme'],
  });
})();
