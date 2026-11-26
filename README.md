# lcmadeira.github.io

Página pessoal de Luís Carlos Madeira, publicada pelo GitHub Pages em <https://lcmadeira.github.io/> (português) e <https://lcmadeira.github.io/en/> (inglês).

É um site estático em HTML, CSS e um pouco de JavaScript, sem build e sem Jekyll (o ficheiro `.nojekyll` faz o Pages servir os ficheiros tal como estão). O Pages publica a partir do ramo `master`.

## Documentação

| Documento | Conteúdo |
| --- | --- |
| `README.md` (este) | Como o site funciona e como se altera |
| [`docs/decisoes.md`](docs/decisoes.md) | Porque é que o site é como é: decisões, datas e motivos |
| [`docs/manutencao.md`](docs/manutencao.md) | Rotina mensal e o que mudar ao alterar a frase, um cartão, um recurso externo… |
| [`docs/ideias.md`](docs/ideias.md) | Ideias por fazer e limitações conhecidas |
| [`CLAUDE.md`](CLAUDE.md) | Regras do projeto para sessões com IA |

Ao mudar o funcionamento do site, atualizar este README; ao tomar uma decisão, registá-la em `docs/decisoes.md`.

## Estrutura

| Ficheiro | Para que serve |
| --- | --- |
| `index.html` | Página em português |
| `en/index.html` | Página em inglês, com a mesma estrutura e os mesmos cartões |
| `404.html` | Página de erro; usa caminhos absolutos (`/assets/...`) porque é servida em qualquer endereço |
| `robots.txt`, `sitemap.xml` | Indicações para os motores de pesquisa; o sitemap lista as duas línguas com `hreflang` e o Painel Pessoal (`/dash/`, publicado a partir do repositório `dash`, no mesmo domínio) |
| `assets/site.css` | Estilos partilhados pelas três páginas: tema escuro único, com o sistema visual do Painel Pessoal (cores e regras no comentário do topo) |
| `assets/activity.js` | Preenche a linha "atualizado há X" de cada cartão a partir de `data/activity.json` |
| `assets/404.js` | Mostra na página de erro o endereço pedido |
| `data/activity.json` | Data da última alteração de cada projeto, gerada pela automação diária |
| `assets/og.png`, `assets/og-en.png` | Imagens de pré-visualização para as redes sociais (1200×630), geradas a partir de `scripts/og-image.html` (instruções no próprio ficheiro); a frase tem de ser igual à do topo |
| `favicon.svg`, `favicon.ico`, `assets/*icon*.png` | Ícone do site (monograma LM). O original é o `favicon.svg`; os PNG e o ICO são gerados a partir dele (ver `docs/manutencao.md`) |
| `scripts/check-site.py` | Verificações antes de publicar (ver abaixo) |
| `scripts/update-activity.py` | Atualiza `data/activity.json` |
| `scripts/og-image.html` | Modelo das imagens de pré-visualização (não é uma página do site) |
| `.github/workflows/` | Automação: `check.yml` e `activity.yml` |
| `lighthouserc.json` | Páginas e limites da auditoria Lighthouse na CI (ver "Automação") |
| `.github/dependabot.yml` | Atualizações semanais das GitHub Actions |
| `LICENSE` | Licença MIT do código |
| `docs/`, `CLAUDE.md` | Documentação (ver acima) |

## Alterar o conteúdo

- **Qualquer texto muda nas duas línguas**, em `index.html` e em `en/index.html`. A verificação falha se as duas páginas tiverem cartões ou links externos diferentes.
- **Links externos** abrem em novo separador: `target="_blank" rel="noopener"`. A verificação também confirma isto.
- **Cartão novo**: copiar um `<article class="card">` existente nas duas páginas e dar-lhe um identificador próprio na linha da atividade, por exemplo `<p class="activity" data-activity="novo-projeto" hidden></p>`. Para a data aparecer:
  1. acrescentar a linha `novo-projeto <dono>/<repositório>` ao segredo `ACTIVITY_MAP`;
  2. se o repositório for privado, dar-lhe acesso no token `REPOS_READ_TOKEN` (definições do token no GitHub).

  Sem isto o cartão funciona na mesma; só não mostra a data.
- **Números do topo** (`<dl class="stats">`): são escritos à mão, nas duas páginas. Ao acrescentar ou retirar um cartão, atualizar o número de projetos (e o "um deles público", se mudar); a verificação falha se esse número não bater com os cartões. O número de serviços self-hosted tem de bater com a lista `ls -F apps/` da secção "O que uso" (também verificado); a lista mostra só os serviços, não as peças de infraestrutura ou administração do servidor. Os outros dois (backups diários, atualização do painel do servidor) não são verificados: atualizar quando mudarem no servidor.

- **Frase do topo, imagens de pré-visualização, contactos**: estão repetidos em vários sítios; seguir as listas de `docs/manutencao.md`.
- **Política de segurança (CSP)**: cada página tem uma meta `Content-Security-Policy` que só deixa carregar recursos do próprio site, das Google Fonts e da Cloudflare (estatísticas). Não há scripts nem estilos embutidos (`<script>` sem `src`, `style="…"`): ficam em `assets/`. Um recurso externo novo obriga a acrescentá-lo à CSP das três páginas, senão o browser bloqueia-o.

### O que pode ser público

Os cartões descrevem também projetos privados, alguns do trabalho. Nunca publicar nomes de clientes ou empresas, endereços IP, domínios, portas, emails (a única exceção é o email de contacto do topo, `PUBLIC_EMAIL` em `scripts/check-site.py`), métricas ou limiares reais, nem nomes de repositórios privados. Descrever o problema e a solução de forma genérica. Nos projetos do trabalho, não indicar o setor, a equipa, a plataforma, a origem dos dados nem horários.

## Ver e verificar antes de publicar

```bash
python3 -m http.server 8000          # abrir http://localhost:8000 e http://localhost:8000/en/
python3 scripts/check-site.py        # verificações locais
python3 scripts/check-site.py --external   # e também os links externos
```

A atividade dos cartões só aparece com o site servido por HTTP, não ao abrir o ficheiro diretamente.

`check-site.py` falha se:

- uma página tiver etiquetas por fechar ou ids repetidos;
- um link externo não abrir em novo separador;
- um link ou recurso interno apontar para um ficheiro que não existe;
- as páginas PT e EN tiverem cartões ou links externos diferentes;
- um bloco JSON-LD (dados estruturados no `<head>`) ou o `sitemap.xml` forem inválidos;
- `data/activity.json` for inválido ou tiver cartões que a página não tem;
- o número de projetos ou de serviços no topo não bater com os cartões ou com a lista `apps/`;
- aparecer um endereço IPv4, um email (exceto o de contacto, `PUBLIC_EMAIL`) ou um termo privado em qualquer ficheiro publicado;
- (com `--external`) um link externo devolver 404 ou 410. X e Threads bloqueiam pedidos automáticos e não são verificados.

Localmente, os termos privados só são verificados com a variável `PRIVATE_TERMS` definida; sem ela aparece um aviso. Na CI são sempre verificados.

## Serviços externos

| Serviço | Para que serve | Onde está no site |
| --- | --- | --- |
| GitHub Pages | Alojamento, HTTPS | Ramo `master` |
| Cloudflare Web Analytics | Estatísticas de visitas sem cookies (páginas, país, origem, dispositivo); painel em Análise → Web Analytics. Browsers com bloqueio (Brave, uBlock) não são contados | Script no fim das três páginas; uma página nova também o deve ter |
| Google Search Console | Pesquisas, cliques e indexação; sitemap submetido | Meta `google-site-verification` em `index.html` (não remover) |
| Google Fonts | Inter (o terminal usa a letra monoespaçada do sistema) | `<link>` no `<head>`; autorizado na CSP |

A pesquisa usa ainda `robots.txt`, `sitemap.xml` e um bloco JSON-LD `Person` no `<head>` de cada página. Se mudar a frase do topo, os links ou o email, atualizar também o JSON-LD.

## Proteções do repositório

- **Regra "Proteger master"** (*Settings → Rules*): o `master` não pode ser apagado nem reescrito à força. Não exige pull request, porque o workflow diário faz push de `data/activity.json`.
- **GitHub Actions fixadas por SHA**, com o Dependabot a propor atualizações; `check.yml` não guarda credenciais no checkout.
- **Email dos commits**: o `noreply` do GitHub; o GitHub recusa pushes que exponham o email pessoal.

## Automação

| Workflow | Quando corre | O que faz |
| --- | --- | --- |
| `check.yml` (Verificar site) | Em cada pull request e em cada push para `master` | Corre `scripts/check-site.py --external` e, num segundo job, o Lighthouse nas três páginas (`lighthouserc.json`): falha se a acessibilidade ficar abaixo de 100, as boas práticas abaixo de 90 ou o SEO abaixo de 90 (a 404 fica de fora do SEO, porque não é para indexar); o desempenho abaixo de 90 só dá aviso. Os relatórios ficam 14 dias nos artefactos da execução |
| `activity.yml` (Atualizar atividade dos projetos) | Todos os dias às 06:30 UTC, ou à mão em *Actions* | Lê a data do último push de cada projeto, verifica o site e, se alguma data mudou, faz commit de `data/activity.json` no `master` |

## Segredos do repositório

Definidos em *Settings → Secrets and variables → Actions*. Os valores nunca vão para o código: o repositório é público e uma lista de termos proibidos revelaria precisamente o que deve ficar privado.

| Segredo | Função |
| --- | --- |
| `PRIVATE_TERMS` | Termos que não podem aparecer no site, um por linha |
| `ACTIVITY_MAP` | Correspondência entre cartão e repositório, uma linha por cartão: `<id-do-cartão> <dono>/<repositório>`; vários repositórios para o mesmo cartão usam a data mais recente |
| `REPOS_READ_TOKEN` | Token *fine-grained* só com `Metadata: read`, limitado aos repositórios dos cartões; sem ele só os repositórios públicos são lidos e os restantes mantêm a data anterior |

Para os definir ou alterar com a linha de comandos: `gh secret set <NOME> -R lcmadeira/lcmadeira.github.io` (pede o valor sem o mostrar).

## Fluxo de trabalho

1. Criar um ramo a partir do `master` atualizado.
2. Fazer as alterações nas duas línguas e correr `python3 scripts/check-site.py`.
3. Abrir um pull request; a CI verifica-o.
4. Fazer o merge. O Pages publica em um ou dois minutos e o ramo remoto é apagado automaticamente.
5. Atualizar a documentação na mesma alteração, se for caso disso (ver "Documentação").

As descrições dos pull requests e as mensagens de commit são públicas: descrever a alteração sem citar dados privados ou o texto sensível que se retira.

## Licença

O código (HTML, CSS, JavaScript e scripts) está sob a licença MIT, ver `LICENSE`. Os textos, o nome, a marca "LM" e as imagens em `assets/` não estão abrangidos: todos os direitos reservados.
