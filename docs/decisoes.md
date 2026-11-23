# Registo de decisões

Porque é que o site é como é. Antes de mudar alguma destas coisas, ler a razão; se a decisão mudar, acrescentar uma entrada nova (não apagar a antiga) com a data e o motivo.

Formato: **decisão**: razão. *(data, pull request quando existe)*

## Arquitetura

- **Site estático sem build e sem Jekyll** (`.nojekyll`): três páginas HTML, um CSS e dois scripts pequenos. Nada para compilar nem dependências para atualizar; o GitHub Pages serve os ficheiros tal como estão. *(19-11-2026)*
- **Duas línguas em páginas separadas** (`/` e `/en/`) com a mesma estrutura: mais simples do que traduzir no browser e indexável pelo Google em cada língua (`hreflang`, sitemap). A verificação obriga a terem os mesmos cartões e links. *(19-11-2026)*
- **Sem domínio próprio**: fica em `lcmadeira.github.io` por decisão do autor. *(23-11-2026)*
- ~~**Tema Catppuccin** (Latte no claro, Mocha no escuro), seguindo a preferência do sistema; o bloco de terminal é sempre Mocha, de propósito.~~ *(19-11-2026; substituída a 23-11-2026, ver "Design")*

## Conteúdo

- **Tom técnico e nominal nos cartões** ("Extração automática de…", não "Descarrega… sozinho"); cada "Objetivo" começa por verbo, nas duas línguas. *(23-11-2026, #14 e #28)*
- **Frase do topo**: "Automação de processos, monitorização de operações e infraestrutura self-hosted." Escolhida entre três opções por ser nominal como os cartões. Está repetida em vários sítios (ver `docs/manutencao.md`). *(23-11-2026, #20)*
- **Projetos do trabalho descritos de forma genérica**: sem setor, equipa, plataforma, origem dos dados nem horários, para não expor ferramentas internas. O grupo chama-se "Automação operacional". *(23-11-2026, #26)*
- **Lista de serviços (`ls -F apps/`) sem peças de infraestrutura ou administração do servidor**: um site público não ganha nada com o detalhe da arquitetura de segurança. O número do topo conta só os serviços. *(23-11-2026, #27)*
- **Termos técnicos exatos**: "sem suporte CORS" (confirmado no README do repositório `dash`) e "SMART" (confirmado pelo autor). *(23-11-2026, #29)*
- **Chaves do fastfetch em inglês nas duas páginas**: é uma imitação do comando real, que as mostra em inglês. *(23-11-2026, #19)*
- **Bandeira de Portugal em SVG**, não em emoji: o emoji de bandeira não aparece no Windows (mostra "PT"). *(23-11-2026, #19)*
- **"self-hosted" com `<span class="nw">`**: evita que a palavra parta no hífen. *(23-11-2026, #20 e #30)*
- **Email público de contacto**: só o do botão do topo, declarado em `PUBLIC_EMAIL` no `check-site.py`; qualquer outro email publicado faz falhar a verificação. *(23-11-2026, #18)*

## Design

- **Sistema visual do Painel Pessoal** (`lcmadeira.github.io/dash`): fundo quase preto em três níveis (fundo, superfície, cartão), texto em três níveis, azul `#6EA8FE` para interação e destaque, verde, âmbar e vermelho só com significado (recente, aviso, erro); letra Inter; pílulas arredondadas para selos, tecnologias e estado; etiquetas em maiúsculas espaçadas. O autor preferia este estilo ao Catppuccin: o portfólio e o projeto em destaque ficam com a mesma identidade. *(23-11-2026)*
- **`~ $ whoami` no topo, em destaque** (letra monoespaçada, `~` a azul): dá o tom técnico e liga ao terminal de "O que uso". Foi trocado por uma etiqueta "Portfólio · Évora, Portugal" ao adotar o estilo do painel e reposto a pedido do autor; Évora fica no rodapé. *(23-11-2026)*
- **Só tema escuro**, como o painel: um segundo tema duplicava o trabalho de cada alteração visual sem ganho claro para um portfólio técnico. `color-scheme: dark` e uma única `theme-color`. *(23-11-2026)*
- **Ícone LM desenhado com traços** (`favicon.svg`), sem depender de letra instalada: L claro e M azul sobre o cartão escuro; legível a 16 px. Os PNG e o ICO são gerados a partir do SVG. O logótipo do fastfetch em "O que uso" é o mesmo ficheiro, para haver uma só marca. *(23-11-2026)*
- **Paleta do fastfetch** com as cores do sistema visual, em vez das 14 do Catppuccin. *(23-11-2026)*
- **Sem selo "Privado" nos cartões**: a introdução da secção já o diz, e o selo repetido criava ruído e partia títulos. *(23-11-2026, #15)*
- **Verde só para estado** (atividade recente); o rodapé de cada cartão (horário/contexto) é texto neutro. *(23-11-2026, #15)*
- **Ícone de traço por cartão**, desenhado à mão em SVG (sem bibliotecas), para distinguir os grupos de relance. *(23-11-2026, #16)*
- **Números no topo** à direita em ecrã largo, por baixo no telemóvel; os que podem ser verificados são-no (`data-count`). *(23-11-2026, #16, #17, #19)*
- **Contraste medido pela fórmula WCAG** em todas as combinações de cores; o texto mais fraco (`--t3`) tem pelo menos 5,6:1 sobre o cartão. As bordas dos cartões ficam abaixo de 3:1 de propósito: são decorativas. *(23-11-2026, #17; refeito com o sistema visual novo)*

## Privacidade, segurança e confiança

- **Estatísticas: Cloudflare Web Analytics**: sem cookies, dados agregados, conta Cloudflare já existente. Self-hosting no servidor de casa foi rejeitado (o servidor desliga-se à noite e não está exposto à Internet). *(23-11-2026, #21)*
- **CSP por meta tag e sem scripts ou estilos embutidos**: o GitHub Pages não permite cabeçalhos HTTP próprios; a meta tag é a alternativa. `frame-ancestors` não funciona em meta tag, fica de fora. *(23-11-2026, #24)*
- **GitHub Actions fixadas por SHA** e atualizadas pelo Dependabot: uma tag pode ser movida, um SHA não. *(23-11-2026, #24)*
- **Regra do `master`: proíbe apagar e reescrever à força, mas não obriga a pull request**: a automação diária faz push direto de `data/activity.json`, e uma regra de pull request obrigatório bloqueava-a. *(23-11-2026)*
- **Email dos commits: o `noreply` do GitHub**, com bloqueio de pushes que exponham o email pessoal. Os commits antigos ficam como estão: reescrever o histórico é destrutivo e o endereço já tinha sido recolhido. *(23-11-2026)*
- **Histórico do Git não reescrito**: versões antigas do HTML contêm descrições mais detalhadas dos projetos do trabalho. Aceite: tirá-las obrigava a push forçado, que a regra do `master` agora impede. *(23-11-2026)*
- **Licença MIT só para o código**; textos, nome, marca "LM" e imagens reservados. *(23-11-2026, #24)*

## Pesquisa

- **`robots.txt`, `sitemap.xml` e JSON-LD `Person`**; site verificado no Google Search Console por meta tag em `index.html` (não remover: o Google volta a confirmá-la). *(23-11-2026, #22 e #23)*
- **`og:image` com `?v=N`**: ao refazer as imagens de pré-visualização, subir o número para as redes não usarem a imagem em cache. *(23-11-2026, #20)*
