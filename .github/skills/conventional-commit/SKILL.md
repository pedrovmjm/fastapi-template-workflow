---
name: conventional-commit
description: Prepara e executa commits Git seguindo Conventional Commits 1.0.0, com rastreabilidade a specs/tarefas e aprovacao explicita do usuario antes de qualquer commit. Use quando o usuario pedir para commitar, registrar entrega, fechar tarefa ou finalizar implementacao com git.
---

# Conventional Commit - Commit com Convencao e Aprovacao

Use esta skill para preparar e executar commits no padrao [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/), **somente depois** que o usuario validar o resumo da entrega e autorizar o commit.

Espelha o fluxo de `.github/skills/create-pull-request/SKILL.md`: primeiro validacao, depois permissao, por ultimo execucao.

## Pre-requisitos

- Implementacao concluida (ou escopo fechado) para a tarefa/spec em questao.
- Testes e lint executados ou impossibilidade documentada.
- Revisao de seguranca feita quando o escopo exigir (`security-reviewer` ou equivalente).
- Nenhum arquivo sensivel (`.env`, credenciais, cache) deve entrar no commit.

## Regra Critica: Nunca Commitar Sem Aprovacao

1. Apresente o **resumo da entrega** e o **rascunho do commit** (mensagem completa + arquivos).
2. Pergunte: *"Posso fazer o commit com esta mensagem e estes arquivos?"*
3. So execute `git add` e `git commit` apos aprovacao explicita do usuario.
4. **PARE e aguarde resposta.** Nao execute `git add`, `git commit` nem `git push` enquanto o usuario nao aprovar.
5. Se o usuario pedir ajustes (mensagem, arquivos, escopo), atualize o rascunho e volte ao passo 2.

Respostas que **nao** contam como aprovacao: silencio, "depois", perguntas sem confirmacao, ou pedidos de revisao adicional.

Respostas que contam como aprovacao: `sim`, `pode commitar`, `aprovado`, `ok para commit`, `autorizado`.

**Nunca** use `git commit --amend`, `--no-verify` ou force push, salvo pedido explicito do usuario.

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

### 2. Resumo para validacao do usuario

Apresente em pt-BR (mesmo padrao visual do PR):

```markdown
## Validacao antes do Commit

**Branch:** [nome]
**Spec/tarefa:** [caminho ou N/A]
**Requisitos/tarefas cobertos:** [lista ou N/A]

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

### Commit proposto

**Mensagem:**
```
<type>(<scope>): <description>

[corpo opcional]

Refs: [FEAT]-01, [FEAT]-02
```

**Aguardando sua aprovacao para fazer o commit.**
```

Apos enviar o resumo, **pare**. Nao prossiga ate o usuario responder.

### 3. Fazer commit (apos aprovacao)

Somente quando o usuario aprovar explicitamente:

```bash
git add <arquivos explicitamente aprovados>
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

Refs: [FEAT]-01

EOF
)"
git status
```

- Inclua apenas arquivos listados e aprovados no passo 2.
- Nao commite `.env`, chaves ou artefatos fora do escopo.
- Informe o hash do commit (`git log -1 --oneline`).

### 4. Proximo passo (opcional)

Apos commit bem-sucedido:

1. Informe hash e mensagem final.
2. Pergunte: *"Deseja abrir um Pull Request?"*
3. Se sim, use `.github/skills/create-pull-request/SKILL.md` (novo ciclo de validacao + permissao, igual ao commit).

## Formato da mensagem (Conventional Commits)

Referencia para montar o rascunho no passo 2. Detalhes em `.github/skills/spc-driven/references/implement.md`.

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

**Escopo:** area em minusculas (`auth`, `clients`, `config`, nome da feature).

**Descricao:** imperativo, primeira letra minuscula, sem ponto final. Teste: "Se aplicado, este commit vai _[descricao]_."

**Breaking change:** `tipo(escopo)!: descricao` + rodape `BREAKING CHANGE: ...`

**Rastreabilidade:** `Refs:` no corpo com IDs de requisito ou numero da tarefa.

**Uma tarefa = um commit.** Nao agrupe tarefas distintas.

## Integracao com o Workflow

| Etapa | Quem prepara | Quem pede permissao | Quem executa |
|-------|--------------|---------------------|--------------|
| Implementacao | `coder-engineer`, `test-engineer`, `lint-engineer` | — | agents |
| Commit | qualquer agent com shell | **usuario** (esta skill) | apos `sim` |
| PR | esta skill encadeia | **usuario** (`create-pull-request`) | apos `sim` |

- O `workflow-orchestrator` **nao** commita nem abre PR; encerra com resumo e indica as skills de commit/PR.
- Commit e PR sao **dois gates independentes**: aprovacao do commit nao autoriza o PR automaticamente.
