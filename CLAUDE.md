# Regras do projeto (para sessões com IA)

Site pessoal estático, público. Antes de alterar, ler `README.md` (como funciona), `docs/decisoes.md` (porque é assim) e `docs/manutencao.md` (o que mais é preciso mudar).

## Sempre

- Escrever em português europeu; o inglês da página `/en/` em grafia britânica.
- Mudar **as duas línguas** (`index.html` e `en/index.html`) na mesma alteração.
- Correr `python3 scripts/check-site.py` antes de cada commit; em alterações visuais, ver o resultado em ecrã largo e estreito (`docs/manutencao.md`, "Como testar").
- Trabalhar num ramo e abrir um pull request; nunca fazer push direto para o `master` nem merge sem autorização explícita do autor.
- Atualizar a documentação na mesma alteração: `README.md` se mudar o funcionamento, `docs/decisoes.md` se for uma decisão, `docs/ideias.md` se uma ideia for feita ou abandonada.
- Commits com o email `noreply` do GitHub (já configurado); o GitHub recusa pushes que exponham o email pessoal.

## Nunca

- Publicar dados privados: o repositório e as descrições dos pull requests são públicos. Ver "O que pode ser público" no `README.md`, incluindo a regra dos projetos do trabalho. Isto vale também para mensagens de commit e descrições de pull requests: descrever a alteração sem citar o texto sensível que se retira.
- Acrescentar `<script>` sem `src` ou `style="…"` (a CSP bloqueia-os) ou recursos externos sem os acrescentar à CSP das três páginas.
- Reescrever o histórico ou forçar push (a regra do `master` impede-o e não é para contornar).
- Remover as meta tags `google-site-verification` e `msvalidate.01` (Bing) de `index.html`.
