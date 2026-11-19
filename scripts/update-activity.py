#!/usr/bin/env python3
"""Atualiza data/activity.json com a data do último push de cada projeto.

A correspondência entre cartão e repositório vem da variável ACTIVITY_MAP
(segredo do repositório), uma linha por cartão: "<id-do-cartão> <dono>/<repo>".
Vários repositórios para o mesmo cartão: usa-se o mais recente.
Assim os nomes dos repositórios privados não ficam públicos.

Precisa de GH_TOKEN com leitura dos repositórios (metadados).
Repositórios a que o token não chega são ignorados e mantêm a data anterior.
"""
import json, os, sys, urllib.request, urllib.error
from datetime import datetime, timezone

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'activity.json')

def pushed_at(repo, token):
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}',
        headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json',
                 'User-Agent': 'activity-updater'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r).get('pushed_at')
    except urllib.error.HTTPError as e:
        print(f'aviso: um repositório devolveu HTTP {e.code}; mantém-se a data anterior', file=sys.stderr)
        return None

def main():
    mapping, token = os.environ.get('ACTIVITY_MAP', ''), os.environ.get('GH_TOKEN', '')
    if not mapping.strip() or not token:
        print('ACTIVITY_MAP ou GH_TOKEN em falta: nada a fazer.'); return 0
    try:
        old = json.load(open(OUT)).get('projects', {})
    except (OSError, ValueError):
        old = {}
    fresh = {}
    for line in mapping.splitlines():
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        card, repo = line.split()
        when = pushed_at(repo, token)
        if when:
            fresh[card] = max(when, fresh.get(card, ''))
    new = {**old, **fresh}
    if new == old:
        print('Sem alterações.'); return 0
    with open(OUT, 'w') as f:
        json.dump({'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                   'projects': dict(sorted(new.items()))}, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'Atualizado: {len(new)} cartões.'); return 0

if __name__ == '__main__':
    sys.exit(main())
