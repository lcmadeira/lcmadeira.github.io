// Mostra "atualizado há X" em cada cartão, a partir de data/activity.json.
// O ficheiro é gerado uma vez por dia por .github/workflows/activity.yml.
// Sem o ficheiro, ou sem data para um cartão, a linha fica escondida.
(function () {
  var lang = (document.documentElement.lang || 'pt-PT').toLowerCase().startsWith('en') ? 'en' : 'pt-PT';
  var label = lang === 'en' ? 'updated ' : 'atualizado ';
  var src = document.currentScript && document.currentScript.src
    ? new URL('../data/activity.json', document.currentScript.src).href
    : 'data/activity.json';
  var rtf = typeof Intl !== 'undefined' && Intl.RelativeTimeFormat
    ? new Intl.RelativeTimeFormat(lang, { numeric: 'auto' }) : null;

  function relative(date) {
    var days = Math.round((date - Date.now()) / 86400000);
    if (!rtf) return date.toLocaleDateString(lang);
    if (Math.abs(days) < 1) return rtf.format(0, 'day');
    if (Math.abs(days) < 31) return rtf.format(days, 'day');
    if (Math.abs(days) < 365) return rtf.format(Math.round(days / 30), 'month');
    return rtf.format(Math.round(days / 365), 'year');
  }

  fetch(src, { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (data) {
      if (!data || !data.projects) return;
      document.querySelectorAll('[data-activity]').forEach(function (el) {
        var iso = data.projects[el.getAttribute('data-activity')];
        var date = iso ? new Date(iso) : null;
        if (!date || isNaN(date)) return;
        el.textContent = label + relative(date);
        el.title = date.toLocaleDateString(lang, { day: 'numeric', month: 'long', year: 'numeric' });
        if (Date.now() - date < 14 * 86400000) el.classList.add('recent');
        el.hidden = false;
      });
    })
    .catch(function () {});
})();
