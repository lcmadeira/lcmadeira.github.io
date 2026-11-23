# Manutenção

Listas de verificação para manter o site correto. As regras gerais (duas línguas, verificação, fluxo de pull request) estão no `README.md`.

## Rotina

**Mensal (10 minutos)**

- [ ] Cloudflare → Análise → Web Analytics → `lcmadeira.github.io`: visitas, países, origem (X, Threads, pesquisa), telemóvel vs computador. Se a maioria vier do telemóvel ou de uma rede, rever o que se vê primeiro nesse caso.
- [ ] Google Search Console → Desempenho: por que pesquisas o site aparece e quantos cliques tem. Indexação → Páginas: as duas línguas indexadas, sem erros. Sitemaps: estado "Êxito".
- [ ] Pull requests do Dependabot: rever e fazer merge. Se atualizar o `actions/checkout`, correr à mão o workflow "Atualizar atividade dos projetos" e confirmar que o push de `data/activity.json` continua a funcionar.
- [ ] Separador *Actions*: o workflow diário de atividade sem falhas.
- [ ] `python3 scripts/check-site.py --external`: nenhum link partido.

**Quando muda alguma coisa no servidor ou nos projetos**

- [ ] Números do topo ainda verdadeiros (backups diários, atualização do painel do servidor). Os outros dois são verificados automaticamente.
- [ ] Horários do cartão "Automação do servidor" e lista `ls -F apps/` ainda corretos.
- [ ] Cartões continuam a descrever o que o projeto faz hoje.

## Ao alterar…

### A frase do topo

Está repetida em vários sítios; mudar todos, nas duas línguas:

1. `<p class="lede">` em `index.html` e `en/index.html` (manter `<span class="nw">self-hosted</span>`);
2. `og:description` e `og:image:alt`;
3. `meta name="description"` (começa por "Portfólio de…" / "Portfolio of…");
4. `description` do bloco JSON-LD;
5. imagens `assets/og.png` e `og-en.png` (ver abaixo) e subir o `?v=N` do `og:image`;
6. bio do perfil do GitHub (fora do repositório).

### As imagens de pré-visualização

1. Editar a frase em `scripts/og-image.html` (português no HTML, inglês no `<script>`).
2. Fotografar com o Firefox a 1200×630, como indicado no topo desse ficheiro (o Firefox instalado por snap só escreve dentro de `~/snap/firefox/common/`).
3. Rever as duas imagens antes de as copiar para `assets/`.
4. Subir o `?v=N` do `og:image` nas duas páginas.

### O ícone

1. Editar `favicon.svg` (o original).
2. Fotografá-lo com o Firefox a 512×512 (uma página com `<img src="favicon.svg" width="512">`) e reduzir com o Pillow para `assets/favicon-32.png`, `assets/icon-192.png` e `favicon.ico` (16, 32 e 48). O `assets/apple-touch-icon.png` (180×180) vai sem cantos arredondados: o iOS arredonda-os.
3. Confirmar que se lê a 16 px.

### As cores

As cores estão em variáveis no topo de `assets/site.css` (as mesmas do Painel Pessoal). Ao mudar uma, medir o contraste WCAG contra os três fundos (`--bg`, `--surface`, `--card`): mínimo 4,5:1 para texto. Atualizar também `scripts/og-image.html` e `favicon.svg` se a cor lá aparecer.

### Um cartão (projeto novo ou retirado)

1. Cartão nas duas páginas, com ícone (`<symbol id="c-…">` no topo de cada página) e `data-activity` próprio.
2. Número de projetos no topo (e "um deles público", se mudar): verificado.
3. `ACTIVITY_MAP` e, se for privado, acesso no `REPOS_READ_TOKEN` (ver `README.md`).
4. Se for um projeto do trabalho: seguir a regra de "O que pode ser público" do `README.md`.

### Um recurso externo (script, fonte, imagem de outro site)

1. Acrescentá-lo à `Content-Security-Policy` das três páginas (`index.html`, `en/index.html`, `404.html`).
2. Nada de `<script>` sem `src` nem `style="…"`: o código vai para `assets/`.
3. Testar no browser com as ferramentas de programador abertas: um bloqueio da CSP aparece na consola.

### Contactos, links ou email

1. Botões do topo nas duas páginas.
2. `sameAs` e `email` do JSON-LD.
3. Se o email mudar: `PUBLIC_EMAIL` em `scripts/check-site.py`.

## Como testar alterações visuais

Servir o repositório (`python3 -m http.server 8000`) e abrir `/` e `/en/` no browser, em ecrã largo e estreito (o site só tem tema escuro). Sem browser à mão, o Firefox tira capturas sem janela:

```bash
firefox --headless --window-size=1280,3000 --screenshot ~/snap/firefox/common/pagina.png http://localhost:8000/
firefox --headless --window-size=390,5000  --screenshot ~/snap/firefox/common/telemovel.png http://localhost:8000/en/
```

