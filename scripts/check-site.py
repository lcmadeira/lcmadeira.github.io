#!/usr/bin/env python3
"""Verificações do site antes de publicar.

  python3 scripts/check-site.py             # verificações locais
  python3 scripts/check-site.py --external  # e também os links externos

Falha (código 1) se:
  - um ficheiro HTML tiver etiquetas por fechar ou ids repetidos;
  - um link externo não abrir em novo separador (target="_blank" rel="noopener");
  - um link ou recurso interno apontar para um ficheiro que não existe;
  - as versões PT e EN não tiverem os mesmos cartões e links externos;
  - data/activity.json for inválido ou tiver cartões que a página não tem;
  - o número de projetos no topo (data-count="cards") não bater com os cartões;
  - aparecer um endereço IPv4, um email (exceto o de contacto, PUBLIC_EMAIL) ou um
    termo privado em qualquer ficheiro publicado. Os termos privados vêm da variável PRIVATE_TERMS (um por linha,
    segredo do repositório), para a lista não ficar ela própria pública.
"""
import html.parser, json, os, re, sys, urllib.request, urllib.error

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
PAGES = ['index.html', 'en/index.html', '404.html']
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
SVG_LEAF = {'path', 'use', 'circle', 'rect', 'line', 'polyline', 'polygon', 'ellipse'}
# Bloqueiam pedidos automáticos: não se verificam (só o formato).
# Único email que pode ser publicado: o botão de contacto no topo.
PUBLIC_EMAIL = 'lcmadeira@outlook.pt'
SKIP_EXTERNAL = ('https://x.com/', 'https://www.threads.com/')
errors, warnings = [], []

class Page(html.parser.HTMLParser):
    def __init__(self, name):
        super().__init__(convert_charrefs=True)
        self.name, self.stack, self.ids, self.links, self.refs, self.activity = name, [], set(), [], [], set()
        self.cards, self.count, self.in_count = 0, None, False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: errors.append(f'{self.name}: id repetido "{a["id"]}"')
            self.ids.add(a['id'])
        if 'data-activity' in a: self.activity.add(a['data-activity'])
        if tag == 'article' and 'card' in a.get('class', '').split(): self.cards += 1
        if a.get('data-count') == 'cards': self.count, self.in_count = '', True
        if tag == 'a' and a.get('href', '').startswith(('http://', 'https://')):
            self.links.append(a)
        for attr in ('href', 'src'):
            v = a.get(attr)
            if v and not v.startswith(('http://', 'https://', '#', 'mailto:', 'data:')) and not (tag == 'use'):
                self.refs.append(v)
        if tag not in VOID and tag not in SVG_LEAF:
            self.stack.append((tag, self.getpos()[0]))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and tag not in SVG_LEAF and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
    def handle_data(self, data):
        if self.in_count: self.count += data
    def handle_endtag(self, tag):
        self.in_count = False
        if tag in SVG_LEAF: return
        if self.stack and self.stack[-1][0] == tag: self.stack.pop()
        else: errors.append(f'{self.name}:{self.getpos()[0]}: </{tag}> sem abertura correspondente')

def check_pages():
    pages = {}
    for name in PAGES:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            errors.append(f'falta {name}'); continue
        p = Page(name); p.feed(open(path, encoding='utf-8').read()); p.close()
        for tag, line in p.stack: errors.append(f'{name}:{line}: <{tag}> não fechado')
        for a in p.links:
            if a.get('target') != '_blank' or 'noopener' not in a.get('rel', ''):
                errors.append(f'{name}: link externo sem novo separador: {a["href"]}')
        base = os.path.dirname(path)
        for ref in p.refs:
            clean = ref.split('#')[0].split('?')[0]
            if not clean: continue
            target = os.path.join(ROOT, clean.lstrip('/')) if clean.startswith('/') else os.path.join(base, clean)
            if clean.endswith('/'): target = os.path.join(target, 'index.html')
            if not os.path.exists(target):
                errors.append(f'{name}: aponta para {ref}, que não existe')
        if p.count is not None and p.count.strip() != str(p.cards):
            errors.append(f'{name}: o topo diz {p.count.strip()!r} projetos, mas há {p.cards} cartões')
        pages[name] = p
    pt, en = pages.get('index.html'), pages.get('en/index.html')
    if pt and en:
        if pt.activity != en.activity:
            errors.append(f'PT e EN com cartões diferentes: {sorted(pt.activity ^ en.activity)}')
        ext = lambda p: {a['href'] for a in p.links if 'og' not in a.get('rel', '')}
        if ext(pt) != ext(en):
            errors.append(f'PT e EN com links externos diferentes: {sorted(ext(pt) ^ ext(en))}')
    return pages

def check_activity(pages):
    path = os.path.join(ROOT, 'data', 'activity.json')
    try:
        data = json.load(open(path, encoding='utf-8'))
    except (OSError, ValueError) as e:
        errors.append(f'data/activity.json inválido: {e}'); return
    cards = pages['index.html'].activity if 'index.html' in pages else set()
    for k, v in data.get('projects', {}).items():
        if k not in cards: errors.append(f'data/activity.json: cartão "{k}" não existe na página')
        if not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', str(v)): errors.append(f'data/activity.json: data inválida em "{k}"')

def published_files():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x != '.git']
        for f in files:
            if f.endswith(('.html', '.css', '.js', '.json', '.py', '.yml', '.yaml', '.md', '.txt', '.svg', '.webmanifest')):
                yield os.path.join(d, f)

def check_privacy():
    terms = [t.strip() for t in os.environ.get('PRIVATE_TERMS', '').splitlines() if t.strip()]
    if not terms:
        warnings.append('PRIVATE_TERMS não definida: termos privados não verificados')
    ipv4 = re.compile(r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])')
    email = re.compile(r'[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z]{2,})+')
    svg_data = re.compile(r'\s(?:d|viewBox|points)="[^"]*"')  # coordenadas SVG não são IPs
    term_re = [re.compile(r'(?<![\w])' + re.escape(t) + r'(?![\w])', re.I) for t in terms]
    for path in published_files():
        rel = os.path.relpath(path, ROOT)
        text = svg_data.sub(' ', open(path, encoding='utf-8', errors='replace').read())
        for n, line in enumerate(text.splitlines(), 1):
            for m in ipv4.finditer(line):
                if all(int(x) <= 255 for x in m.group().split('.')):
                    errors.append(f'{rel}:{n}: endereço IPv4 ({m.group()})')
            for m in email.finditer(line):
                if not m.group().startswith('noreply@') and m.group() != PUBLIC_EMAIL:
                    errors.append(f'{rel}:{n}: endereço de email')
            for i, r in enumerate(term_re):
                if r.search(line):
                    errors.append(f'{rel}:{n}: termo privado n.º {i + 1} da lista')

def check_external(pages):
    urls = sorted({a['href'] for p in pages.values() for a in p.links})
    for url in urls:
        if url.startswith(SKIP_EXTERNAL):
            continue
        status = None
        for attempt in range(2):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (link check)'})
                with urllib.request.urlopen(req, timeout=20) as r:
                    status = r.status
                break
            except urllib.error.HTTPError as e:
                status = e.code
                break
            except Exception as e:
                status = f'erro de rede ({type(e).__name__})'
        if status in (404, 410):
            errors.append(f'link partido ({status}): {url}')
        elif not isinstance(status, int) or status >= 400:
            warnings.append(f'link não confirmado ({status}): {url}')
    print(f'{len(urls)} links externos verificados.')

def main():
    pages = check_pages()
    check_activity(pages)
    check_privacy()
    if '--external' in sys.argv:
        check_external(pages)
    for w in warnings: print(f'aviso: {w}')
    for e in errors: print(f'ERRO: {e}')
    print('OK' if not errors else f'{len(errors)} erro(s).')
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
