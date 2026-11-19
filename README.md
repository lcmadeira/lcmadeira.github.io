# lcmadeira.github.io

Página pessoal de Luís Carlos Madeira, publicada pelo GitHub Pages em <https://lcmadeira.github.io/> (português) e <https://lcmadeira.github.io/en/> (inglês).

É um site estático em HTML, CSS e um pouco de JavaScript, sem build e sem Jekyll (o ficheiro `.nojekyll` faz o Pages servir os ficheiros tal como estão). O Pages publica a partir do ramo `master`.

## Estrutura

| Ficheiro | Para que serve |
| --- | --- |
| `index.html` | Página em português |
| `en/index.html` | Página em inglês, com a mesma estrutura e os mesmos cartões |
| `404.html` | Página de erro; usa caminhos absolutos (`/assets/...`) porque é servida em qualquer endereço |
| `assets/site.css` | Estilos partilhados pelas três páginas, com tema claro e escuro (Catppuccin Latte e Mocha) |
| `assets/activity.js` | Preenche a linha "atualizado há X" de cada cartão a partir de `data/activity.json` |
| `data/activity.json` | Data da última alteração de cada projeto, gerada pela automação diária |
| `assets/og.png`, `assets/og-en.png` | Imagens de pré-visualização para as redes sociais (1200×630) |
| `favicon.ico`, `assets/*icon*.png` | Ícone do site (monograma LM) |
| `scripts/check-site.py` | Verificações antes de publicar (ver abaixo) |
| `scripts/update-activity.py` | Atualiza `data/activity.json` |
| `.github/workflows/` | Automação: `check.yml` e `activity.yml` |

## Alterar o conteúdo

- **Qualquer texto muda nas duas línguas**, em `index.html` e em `en/index.html`. A verificação falha se as duas páginas tiverem cartões ou links externos diferentes.
- **Links externos** abrem em novo separador: `target="_blank" rel="noopener"`. A verificação também confirma isto.
- **Cartão novo**: copiar um `<article class="card">` existente nas duas páginas e dar-lhe um identificador próprio na linha da atividade, por exemplo `<p class="activity" data-activity="novo-projeto" hidden></p>`. Para a data aparecer:
  1. acrescentar a linha `novo-projeto <dono>/<repositório>` ao segredo `ACTIVITY_MAP`;
  2. se o repositório for privado, dar-lhe acesso no token `REPOS_READ_TOKEN` (definições do token no GitHub).

  Sem isto o cartão funciona na mesma; só não mostra a data.

### O que pode ser público

Os cartões descrevem também projetos privados, alguns do trabalho. Nunca publicar nomes de clientes ou empresas, endereços IP, domínios, portas, emails, métricas ou limiares reais, nem nomes de repositórios privados. Descrever o problema e a solução de forma genérica.

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
- `data/activity.json` for inválido ou tiver cartões que a página não tem;
- aparecer um endereço IPv4, um email ou um termo privado em qualquer ficheiro publicado;
- (com `--external`) um link externo devolver 404 ou 410. X e Threads bloqueiam pedidos automáticos e não são verificados.

Localmente, os termos privados só são verificados com a variável `PRIVATE_TERMS` definida; sem ela aparece um aviso. Na CI são sempre verificados.

## Automação

| Workflow | Quando corre | O que faz |
| --- | --- | --- |
| `check.yml` (Verificar site) | Em cada pull request e em cada push para `master` | Corre `scripts/check-site.py --external` |
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
4. Fazer o merge. O Pages publica em um ou dois minutos e o ramo é apagado automaticamente.
