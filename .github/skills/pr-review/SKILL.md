---
name: pr-review
description: Revisa pull requests do GitHub com personas especialistas do template FastAPI e publica o resultado como review ou comentario na propria PR via gh CLI. Use quando o usuario passar URL de PR ou pedir revisao de pull request no GitHub.
---

# PR Review - Revisao Multi-Persona no GitHub

Use esta skill para revisar Pull Requests do GitHub de forma abrangente, com personas especializadas e feedback publicado na propria PR. A revisao deve ser objetiva, acionavel e alinhada ao template FastAPI deste repositorio.

**Idioma:** review e comunicacao com o usuario em **pt-BR**. Preserve paths, comandos, nomes de arquivos e identificadores tecnicos em ingles quando necessario.

## Entrada

URL do PR no GitHub:

- Formato: `https://github.com/{owner}/{repo}/pull/{number}`
- Exemplo: `https://github.com/org/minha-api/pull/42`

## Saida

Publicacao no GitHub:

- `gh pr review --comment` para revisao consolidada sem bloquear.
- `gh pr review --request-changes` quando houver bloqueadores reais.
- `gh pr comment` quando o usuario pedir apenas um comentario informativo, sem evento formal de review.

Nao gere relatorio `.md` por padrao. Use arquivo temporario somente como suporte para `--body-file`, removendo-o ao final quando possivel.

## Workflow

### Passo 1: Obter detalhes do PR

1. Extraia o numero do PR da URL.
2. `gh pr view {numero} --json title,author,body,baseRefName,headRefName,labels,commits,additions,deletions,changedFiles,url` — metadados.
3. `gh pr diff {numero}` — alteracoes.
4. `gh pr diff {numero} --name-only` — classificar tipos de arquivo.
5. `gh pr checks {numero}` — status de CI, quando disponivel.

### Passo 2: Escolher personas relevantes

| Arquivos alterados | Personas |
|--------------------|----------|
| `src/routes/**`, `src/endpoints/**` | Merge Specialist, Backend |
| `src/services/**`, `src/domain/**` | Merge Specialist, Backend |
| `src/repository/**`, `src/models/**`, `src/db/**`, `src/database/**` | Merge Specialist, Backend |
| `src/configs/**`, `src/settings/**`, `.env.example` | Merge Specialist, Backend, **DevOps** |
| `src/security/**`, `src/routes/dependencies/**`, middleware de auth | Merge Specialist, Backend, **Security** |
| `src/agents/**`, `src/mcp/**`, tools LangGraph/OpenAI | Merge Specialist, Backend, **Security** |
| `src/middlewares/**`, `src/observability/**`, logs/traces/metrics | Merge Specialist, Backend, **DevOps** |
| `tests/**` | Merge Specialist, Backend |
| `.github/workflows/**`, `Dockerfile`, `docker-compose*`, `bootstrap.py` | Merge Specialist, **DevOps**, Security quando houver supply chain/secrets |
| `.specs/**`, `docs/**`, `README.md` | Merge Specialist |
| `pyproject.toml`, `requirements*.txt`, `poetry.lock`, `uv.lock` | Merge Specialist, DevOps, Security |

**Sempre participa:** Merge Specialist (Gatekeeper).

Consulte as definicoes existentes em `personas/`. Nao cite personas sem arquivo nessa pasta.

### Passo 2.5: Novas variaveis de configuracao (CRITICO)

Se o PR tocar configuracao, verifique propagacao antes das revisoes detalhadas. Ausencia de atualizacao coerente e **bloqueador**.

**Arquivos gatilho:**

```bash
gh pr diff {numero} --name-only | grep -E \
  -e '^\.env\.example$' \
  -e '^src/configs/' \
  -e '^src/.*/config' \
  -e '^src/.*/settings' \
  -e 'docker-compose' \
  -e '^\.github/workflows/'
```

**Verificar:**

- [ ] `.env.example` documenta novas variaveis (descricao, default, exemplo).
- [ ] Settings tipadas em `src/configs/settings.py` e `src/configs/values_domains/` refletem as novas chaves.
- [ ] Nenhum secret em plaintext no diff.
- [ ] `.specs/codebase/` ou documentacao de deploy atualizada quando o time usar brownfield docs.
- [ ] Skill `standard-configs` respeitada (providers, values domains).

Se faltar sincronizacao, veredito do Merge Specialist: **REQUEST CHANGES** com bloqueador "Configuracao nao propagada".

### Passo 3: Testes e qualidade (antes da revisao textual)

```bash
gh pr checkout {numero}

# Ajuste conforme README, pyproject.toml gerado ou scripts do app alvo
python -m pytest tests/ -q --tb=short
python -m ruff check .
python -m ruff format --check .

git checkout -
```

Registre comandos, exit codes e resumo no corpo da review. Se o projeto ainda for apenas o template/bootstrap e nao tiver `tests/` ou `pyproject.toml` no checkout atual, documente como `N/A` e valide o que existir, como `python -m compileall bootstrap.py` quando fizer sentido.

Falha de teste ou lint critico = bloqueador.

### Passo 4: Revisao por persona

Para cada persona relevante, adote a perspectiva e revise o diff. Use o formato de saida de cada arquivo em `personas/`.

Skills do projeto a cruzar quando aplicavel:

- `standard-security`, `standard-tests`, `standard-logs`, `standard-traces`
- `fastapi-best-practices`, `domain`, `standard-endpoints`, `standard-data-models`
- `standard-configs`, `standard-middleware`, `standard-errors`, `standard-services`, `standard-repositories`
- `standard-database`, `standard-integrations`, `standard-docstrings`, `in-memory-cache`

### Passo 5: Montar corpo da review

Estrutura:

```markdown
## Revisao do PR #{numero}: {titulo}

**Veredito geral:** APROVAR | COMENTAR | SOLICITAR ALTERACOES
**Base:** `{base}` <- `{head}`
**Autor:** @{autor}

### Resumo
- ...

### Validacoes executadas
| Check | Status | Detalhes |
|-------|--------|----------|
| CI GitHub | PASS/FAIL/N/A | ... |
| Testes locais | PASS/FAIL/N/A | `...` |
| Lint/format | PASS/FAIL/N/A | `...` |

### Achados que precisam de acao
1. **{Severidade} - {titulo curto}**
   - Local: `{arquivo:linha}`
   - Impacto: ...
   - Recomendacao: ...

### Checklist do template FastAPI
| Area | Status | Notas |
|------|--------|-------|
| Configuracao (`src/configs`, `.env.example`) | PASS/FAIL/N/A | ... |
| Contratos `data/meta/links` | PASS/FAIL/N/A | ... |
| Erros publicos `errors[]` | PASS/FAIL/N/A | ... |
| Logs/traces sem dados sensiveis | PASS/FAIL/N/A | ... |
| Testes proporcionais ao risco | PASS/FAIL/N/A | ... |

### Painel de revisores
| Papel | Revisor | Veredito |
|-------|---------|----------|
| Merge | Gatekeeper | ... |
| Backend | Byte | ... |
| Seguranca | Cipher | ... |
| DevOps | Circuit | ... |

{secoes por persona}

### Acoes obrigatorias antes do merge
- [ ] ...
```

### Passo 6: Publicar no GitHub

Escolha o comando conforme o veredito:

```bash
# Sem bloqueadores, feedback informativo
gh pr review {numero} --comment --body-file /tmp/pr-{numero}-review-body.txt

# Com bloqueadores reais
gh pr review {numero} --request-changes --body-file /tmp/pr-{numero}-review-body.txt

# Apenas comentario, quando o usuario pedir explicitamente comentario em vez de review formal
gh pr comment {numero} --body-file /tmp/pr-{numero}-review-body.txt
```

Nunca use `--approve` automaticamente. Aprove somente se o usuario pedir explicitamente aprovacao formal e a revisao nao encontrar bloqueadores.

Se o usuario pediu apenas para "revisar" e nao especificou publicacao, publique como `gh pr review --comment` por padrao. Se a PR estiver em repositorio de terceiros ou a publicacao puder notificar muita gente, mostre o corpo e peca confirmacao antes de postar.

### Passo 7: Apresentar resumo ao usuario

1. Veredito geral.
2. Lista de bloqueadores.
3. Comando usado (`gh pr review` ou `gh pr comment`).
4. URL da PR.

**Nao faca merge nem push** salvo pedido explicito do usuario.

## Principios de revisao

Alinhados ao template e `.github/skills/spc-driven/references/coding-principles.md`:

- **Simplicidade** — codigo legivel, sem over-engineering.
- **Seguranca primeiro** — OWASP, validacao em fronteiras, sem secrets no diff.
- **Testes** — cobertura proporcional ao risco; nenhum teste enfraquecido sem justificativa.
- **Rastreabilidade** — commits/PR referenciam spec quando existir.

### Severidade

| Nivel | Significado |
|-------|-------------|
| Bloqueador | Deve corrigir antes do merge |
| Major | Deve corrigir; pode negociar prazo |
| Minor | Melhoria desejavel |

### Criterios de veredito

| Veredito | Quando |
|----------|--------|
| **APROVAR** | Testes/lint ok, sem vulnerabilidades, padroes atendidos |
| **COMENTAR** | Apenas issues menores ou feedback informativo |
| **SOLICITAR ALTERACOES** | Testes falhando, seguranca, breaking change injustificado, config incompleta |

## Exemplo

Usuario: "Revisa https://github.com/org/api/pull/10"

1. PR #10, diff em `src/services/auth_service.py`, `tests/unit/test_auth.py`
2. Personas: Gatekeeper, Byte, Cipher
3. Testes: pass
4. Review publicado com `gh pr review 10 --comment --body-file /tmp/pr-10-review-body.txt`
5. Resumo com veredito ao usuario

## Integracao com o fluxo do repositorio

1. Implementacao + testes + lint (agents do workflow).
2. Usuario valida entrega (`conventional-commit`).
3. Commit aprovado.
4. Usuario valida PR (`create-pull-request`).
5. Revisao opcional com esta skill (auto-review ou terceiros).
