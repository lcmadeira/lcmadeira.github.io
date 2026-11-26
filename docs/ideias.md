# Ideias e limitações conhecidas

O que ficou por fazer e o que se sabe que não é perfeito. Ao fazer uma ideia, retirá-la daqui e registar a decisão em `docs/decisoes.md` se for relevante.

## Ideias, por ordem de valor

1. **Capturas dos projetos privados**, anonimizadas (sem nomes, valores ou endereços reais): Homelab Control, Indicador de serviço e Painel de operação. É o que mais valorizaria o portfólio. Imagens otimizadas em `assets/`, com clique para ampliar; `img-src 'self'` na CSP já as permite. Uma primeira tentativa (faixa de largura total por baixo dos cartões, #44) foi retirada: o formato não agradou; falar com o autor antes de tentar outro.
2. **Rever o site com dados reais** de visitas e pesquisas (ver `docs/manutencao.md`) e afinar o que se vê primeiro conforme o dispositivo e a origem mais comuns.
3. **Frase de introdução em "O que uso"**, como a que existe em "Projetos". Ficou de fora por decisão do autor (23-11-2026); reconsiderar se a secção crescer.
4. **Segundo comando no terminal** (por exemplo os horários dos backups), para equilibrar a altura do painel da direita. Ficou de fora por decisão do autor (23-11-2026).

## Limitações conhecidas

- **Números do topo parcialmente manuais**: "backups diários" e "atualização do painel do servidor" não são verificados automaticamente.
- **Estatísticas por defeito**: o Brave e os bloqueadores de anúncios não deixam carregar o script da Cloudflare; os números ficam abaixo da realidade.
- **Sem cabeçalhos HTTP próprios** no GitHub Pages: a CSP vai por meta tag e não cobre `frame-ancestors`.
- **Histórico do Git público** com versões antigas mais detalhadas dos cartões do trabalho (ver `docs/decisoes.md`).
- **Fontes da Google**: o site depende de `fonts.googleapis.com` para a Inter; sem acesso, usa as fontes do sistema (definidas como alternativa no CSS).
- **Só tema escuro**: quem prefere tema claro vê o site escuro (decisão em `docs/decisoes.md`).
