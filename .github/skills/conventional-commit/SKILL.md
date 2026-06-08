---
name: conventional-commit
description: Prepara e executa commits Git incrementais seguindo Conventional Commits 1.0.0, sanitiza autoria de IA na mensagem, com rastreabilidade a specs/tarefas e aprovacao explicita do usuario antes de qualquer commit. Use quando o usuario pedir para commitar, registrar entrega, fechar tarefa ou finalizar implementacao com git.
---

# Conventional Commit - Commit com Convencao e Aprovacao

Use esta skill para preparar e executar commits incrementais no padrao [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/), **somente depois** que o usuario validar o resumo da entrega e autorizar o commit ou o plano de commits.

Espelha o fluxo de `.github/skills/create-pull-request/SKILL.md`: primeiro validacao, depois permissao, por ultimo execucao.

## Pre-requisitos

- Implementacao concluida (ou escopo fechado) para a tarefa/spec em questao.
- Testes e lint executados ou impossibilidade documentada.
- Revisao de seguranca feita quando o escopo exigir (`security-reviewer` ou equivalente).
- Nenhum arquivo sensivel (`.env`, credenciais, cache) deve entrar no commit.
- A mensagem nao deve atribuir autoria a ferramentas de IA.

## Regra Critica: Nunca Commitar Sem Aprovacao

1. Apresente o **resumo da entrega** e o **rascunho do commit** ou **plano de commits incrementais** (mensagem completa + arquivos por commit).
2. Pergunte: *"Posso fazer o commit/plano de commits com estas mensagens e estes arquivos?"*
3. So execute `git add` e `git commit` apos aprovacao explicita do usuario para o commit unico ou para o plano completo.
4. **PARE e aguarde resposta.** Nao execute `git add`, `git commit` nem `git push` enquanto o usuario nao aprovar.
5. Se o usuario pedir ajustes (mensagem, arquivos, escopo), atualize o rascunho e volte ao passo 2.

Respostas que **nao** contam como aprovacao: silencio, "depois", perguntas sem confirmacao, ou pedidos de revisao adicional.

Respostas que contam como aprovacao: `sim`, `pode commitar`, `aprovado`, `ok para commit`, `autorizado`.

**Nunca** use `git commit --amend`, `--no-verify` ou force push, salvo pedido explicito do usuario.

## Regra Critica: Sem Coautoria de Ferramentas de IA

Nao inclua rodapes, trailers ou textos de autoria para ferramentas de IA em commits.

Proibido:

- `Co-authored-by: Cursor ...`
- `Co-authored-by: Claude Code ...`
- `Co-authored-by: Codex ...`
- `Generated-by: ...`
- `Created with ...`
- Qualquer variacao que atribua autoria, coautoria ou geracao a assistentes/ferramentas de IA.

O commit deve registrar a mudanca tecnica e sua rastreabilidade, nao a ferramenta usada para auxiliar.

## Scripts da Skill

| Momento | Script obrigatorio |
| --- | --- |
| Setup inicial do clone | `scripts/setup-git-hooks.sh` |
| Imediatamente antes de `git commit` | `scripts/sanitize-ai-attribution.sh` |
| Imediatamente apos `git commit` | verificar e `git commit --amend` se o Cursor injetar trailer |

O Cursor pode injetar `Co-authored-by: Cursor <cursoragent@cursor.com>` mesmo com mensagem sanitizada. Por isso:

1. Configure o hook com `scripts/setup-git-hooks.sh` (`.githooks/commit-msg` chama o sanitizer com `--write`).
2. Sanitize a mensagem aprovada antes do commit.
3. Apos o commit, valide com `git log -1 --format=%B`. Se ainda houver autoria de IA, **amende** com a mensagem sanitizada:

```bash
git log -1 --format=%B > /tmp/last-commit-msg.txt
.github/skills/conventional-commit/scripts/sanitize-ai-attribution.sh --write /tmp/last-commit-msg.txt
git commit --amend -F /tmp/last-commit-msg.txt
```

**Execute** o sanitizer antes do commit. So prossiga quando retornar `APTO_PARA_PUBLICAR=sim` e o hook/amend deixarem o commit limpo.

## Fluxo

### 1. Estado do repositorio

Execute em paralelo:

```bash
git status
git diff
git diff --staged
git log -5 --oneline
```

Confirme:

- Branch atual.
- Arquivos modificados, nao rastreados e ja em stage.
- O que **nao** deve entrar no commit (`.env`, credenciais, `.pytest_cache`, artefatos gerados).
- Spec ou tarefa: `.specs/features/<slug>/spec.md`, `tasks.md` ou `.specs/quick/<id>/TASK.md`.
- IDs de requisito (`[FEAT]-01`, etc.) quando existirem.

### 2. Classificar escopo e plano incremental

Antes de propor commits, classifique o diff por responsabilidade. Cada commit deve representar uma unidade logica revisavel, mas uma feature pode e deve ser dividida em varios commits incrementais quando isso melhora revisao, rollback ou rastreabilidade.

Nao force commit unico por feature. Prefira commits incrementais quando a entrega tiver etapas naturais, como:

- base de configuracao;
- contrato/modelos;
- implementacao de service/repository;
- endpoint/middleware;
- observabilidade/logging/tracing;
- documentacao;
- testes, quando estiverem no escopo do agente responsavel.

Use estes sinais para decidir se deve dividir:

- Mudancas em dominios independentes, como CORS, logging e agents no mesmo diff.
- Arquivos de configuracao sem relacao direta com o codigo alterado.
- Documentacao ou skills misturadas com mudanca funcional sem dependencia clara.
- Testes cobrindo comportamentos diferentes que poderiam ser revisados separadamente.

Se houver responsabilidades independentes ou etapas incrementais claras, proponha commits separados e peca aprovacao para cada grupo de arquivos ou para o plano completo. Nao esconda escopo amplo em um scope estreito.

Exemplos:

- Correto para CORS apenas: `fix(cors): ajustar origens permitidas`
- Correto para logging apenas: `refactor(logging): padronizar eventos de tracing`
- Correto para agents apenas: `feat(agents): configurar tracing seguro`
- Incorreto se altera CORS, logging e agents: `fix(cors): ajustar configuracoes`
- Melhor quando nao der para separar: `chore(template): alinhar cors logging e agents`
- Melhor quando der para separar: tres commits incrementais, um para `cors`, um para `logging` e um para `agents`

### 3. Resumo para validacao do usuario

Apresente em pt-BR (mesmo padrao visual do PR):

```markdown
## Validacao antes do Commit

**Branch:** [nome]
**Spec/tarefa:** [caminho ou N/A]
**Requisitos/tarefas cobertos:** [lista ou N/A]
**Responsabilidade unica:** SIM/NAO
**Plano de commits:** [commit unico ou lista incremental de commits]

### Resumo da entrega
- [bullet objetivo]

### Arquivos que entrarao no commit
| Arquivo | Motivo |
|---------|--------|
| ... | ... |

### Arquivos excluidos (se houver)
| Arquivo | Motivo da exclusao |
|---------|-------------------|
| ... | ... |

### Validacoes
| Check | Status | Evidencia |
|-------|--------|-----------|
| Testes | PASS/FAIL/PENDENTE | [comando + exit code] |
| Lint/format/type | PASS/FAIL/PENDENTE | [comando + exit code] |
| Revisao de seguranca | SIM/NAO/N/A | [agente ou nota] |
| Sem secrets no diff | SIM/NAO | [observacao] |

### Commit(s) proposto(s)

**Mensagem:**
```
<type>(<scope>): <description>

[corpo opcional]

Refs: [FEAT]-01, [FEAT]-02
```

**Quando houver multiplos commits:**
| Ordem | Mensagem | Arquivos | Motivo |
|-------|----------|----------|--------|
| 1 | `...` | `...` | ... |
| 2 | `...` | `...` | ... |

**Aguardando sua aprovacao para fazer o commit ou o plano de commits.**
```

Apos enviar o resumo, **pare**. Nao prossiga ate o usuario responder.

### 4. Executar script de sanitizacao (apos aprovacao, antes do commit)

Somente quando o usuario aprovar explicitamente:

1. Grave a mensagem aprovada em um arquivo temporario, por exemplo `/tmp/commit-msg.txt`.
2. **Execute** o script da skill:

```bash
.github/skills/conventional-commit/scripts/sanitize-ai-attribution.sh /tmp/commit-msg.txt \
  > /tmp/commit-msg.sanitized.txt
```

3. Confirme `APTO_PARA_PUBLICAR=sim` no stderr e exit code `0`.
4. Use somente o conteudo de `/tmp/commit-msg.sanitized.txt` no commit.

### 5. Fazer commit(s)

```bash
.github/skills/conventional-commit/scripts/setup-git-hooks.sh

git add <arquivos explicitamente aprovados>
git commit -F /tmp/commit-msg.sanitized.txt
git log -1 --format=%B > /tmp/last-commit-msg.txt
.github/skills/conventional-commit/scripts/sanitize-ai-attribution.sh --write /tmp/last-commit-msg.txt
git commit --amend -F /tmp/last-commit-msg.txt
git status
```

- Use `git commit -F` com o arquivo sanitizado pelo script da skill.
- O `git commit --amend` final remove trailers que o Cursor injeta apos o commit.
- Para multiplos commits, repita sanitizacao, `git add <arquivos do commit N>` e `git commit ...` na ordem aprovada.
- Inclua apenas arquivos listados e aprovados no resumo de validacao.
- Nao commite `.env`, chaves ou artefatos fora do escopo.
- Informe o hash de cada commit (`git log --oneline -n <N>`).

### 6. Proximo passo (opcional)

Apos commit bem-sucedido:

1. Informe hash e mensagem final.
2. Pergunte: *"Deseja abrir um Pull Request?"*
3. Se sim, use `.github/skills/create-pull-request/SKILL.md` (novo ciclo de validacao + permissao, igual ao commit).

## Formato da mensagem (Conventional Commits)

Referencia para classificar o diff e montar o rascunho nos passos 2 e 3. Detalhes em `.github/skills/spc-driven/references/implement.md`.

```
<type>(<scope>): <description>

[corpo opcional]

[rodape opcional]
```

| Tipo | Quando usar |
|------|-------------|
| `feat` | Nova funcionalidade |
| `fix` | Correcao de bug |
| `refactor` | Refatoracao sem mudar comportamento |
| `docs` | Apenas documentacao |
| `test` | Testes |
| `style` | Formatacao sem mudanca logica |
| `perf` | Performance |
| `build` | Build ou dependencias |
| `ci` | CI/CD |
| `chore` | Manutencao fora de src/test |

### Regras obrigatorias

- O header deve seguir exatamente: `<type>(<scope>): <description>` ou `<type>: <description>` quando nao houver scope claro.
- `type` deve ser um dos tipos da tabela.
- `scope` deve ser curto, em minusculas, sem espacos, e refletir o escopo real do diff.
- Se o diff cruza areas independentes ou etapas incrementais claras, divida em commits ou use scope mais amplo e descricao honesta quando a separacao nao for pratica.
- `description` deve ser em imperativo, primeira letra minuscula, sem ponto final.
- O header inteiro deve ficar preferencialmente ate 72 caracteres.
- Breaking change usa `!` no header e rodape `BREAKING CHANGE: ...`.

**Escopo:** area em minusculas (`auth`, `cors`, `logging`, `agents`, `configs`, `template`, nome da feature).

**Descricao:** teste mental: "Se aplicado, este commit vai _[descricao]_." Se a frase nao fizer sentido, reescreva.

**Breaking change:** `tipo(escopo)!: descricao` + rodape `BREAKING CHANGE: ...`

**Rastreabilidade:** `Refs:` no corpo com IDs de requisito ou numero da tarefa.

**Autoria:** nao use `Co-authored-by`, `Generated-by`, `Created with` ou notas equivalentes para ferramentas de IA como Cursor, Claude Code ou Codex.

**Uma unidade logica = um commit.** Uma feature pode ter varios commits incrementais. Nao agrupe tarefas distintas, mas tambem nao force tudo em um unico commit so porque pertence a mesma feature.

### Checklist de validacao da mensagem

- [ ] Header segue Conventional Commits.
- [ ] Tipo corresponde a natureza da mudanca.
- [ ] Scope nao reduz indevidamente o escopo real.
- [ ] Descricao e imperativa, minuscula e sem ponto final.
- [ ] Corpo explica motivacao quando o header nao basta.
- [ ] Rodape inclui `Refs:` quando houver spec/tarefa.
- [ ] O script `scripts/sanitize-ai-attribution.sh` foi executado e retornou `APTO_PARA_PUBLICAR=sim`.
- [ ] Nao ha `Co-authored-by`, `Generated-by`, `Created with` ou autoria atribuida a ferramenta de IA.
- [ ] O comando final de commit nao usa `--trailer` para autoria de IA.
- [ ] Cada commit contem uma unica responsabilidade logica.
- [ ] Entregas maiores foram divididas em commits incrementais quando isso melhora revisao ou rollback.

## Integracao com o Workflow

| Etapa | Quem prepara | Quem pede permissao | Quem executa |
|-------|--------------|---------------------|--------------|
| Implementacao | `coder-engineer`, `test-engineer`, `lint-engineer` | — | agents |
| Commit | qualquer agent com shell | **usuario** (esta skill) | apos `sim` |
| PR | esta skill encadeia | **usuario** (`create-pull-request`) | apos `sim` |

- O `workflow-orchestrator` **nao** commita nem abre PR; encerra com resumo e indica as skills de commit/PR.
- Commit e PR sao **dois gates independentes**: aprovacao do commit nao autoriza o PR automaticamente.
