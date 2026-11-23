// Mostra o caminho pedido na linha do "cd" (só texto, sem HTML).
(function () {
  try {
    var p = decodeURIComponent(location.pathname).replace(/^\/+/, '');
    var el = document.getElementById('nf-path');
    if (p && el) el.textContent = p.length > 60 ? p.slice(0, 57) + '…' : p;
  } catch (e) {}
})();
