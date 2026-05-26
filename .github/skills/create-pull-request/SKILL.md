---
name: create-pull-request
description: Cria pull request no GitHub com gh CLI apos validar responsabilidade unica, titulo fiel ao diff, rascunho baseado em template e aprovacao explicita do usuario. Use quando o usuario pedir para abrir PR, criar pull request ou publicar branch apos commits aprovados.
---

# Create Pull Request - Abrir PR com Aprovacao

Use esta skill para criar um Pull Request no GitHub com `gh`, **somente depois** que o usuario validar o resumo da entrega, revisar o rascunho do PR e autorizar a abertura.

## Pre-requisitos

- Commits ja feitos na branch (use `.github/skills/conventional-commit/SKILL.md` antes, se ainda nao houver commit).
- `gh` autenticado e branch com alteracoes prontas para revisao.
- Testes e lint executados ou impossibilidade documentada.
- Base branch identificada (`main` ou `master`, salvo contexto diferente do repositorio).

## Regra Critica: Nunca Abrir PR Sem Aprovacao

1. Apresente o **resumo da entrega** e o **rascunho do PR** (titulo + corpo).
2. Pergunte: *"Posso criar o PR com este titulo e descricao?"*
3. So execute `git push` e `gh pr create` apos aprovacao explicita do usuario.
4. **PARE e aguarde resposta.** Nao execute `git push` nem `gh pr create` enquanto o usuario nao aprovar.
5. Se o usuario pedir ajustes (titulo, corpo, escopo), atualize o rascunho e volte ao passo 2.

Respostas que **nao** contam como aprovacao: silencio, "depois", perguntas sem confirmacao, ou pedidos de revisao adicional.

Respostas que contam como aprovacao: `sim`, `pode criar o PR`, `aprovado`, `ok para abrir o PR`, `autorizado`.

## Regra Critica: Sem Autoria de Ferramentas de IA

Nao inclua coautoria, autoria, assinatura ou nota de geracao por ferramenta de IA no titulo, corpo, comentarios ou metadata do PR.

Proibido:

- `Co-authored-by: Cursor ...`
- `Co-authored-by: Claude Code ...`
- `Co-authored-by: Codex ...`
- `Generated-by: ...`
- `Created with ...`
- Qualquer mencao equivalente que atribua autoria ou coautoria a assistentes/ferramentas de IA.

O PR deve descrever escopo, validacoes, riscos e rastreabilidade da mudanca, nao a ferramenta usada para auxiliar.

## Fluxo

### 1. Estado da branch

Execute em paralelo:

```bash
git status
git branch -vv
git log main..HEAD --oneline
git diff main...HEAD --stat
```

Confirme:

- Branch atual e base (`main` ou `master`).
- Se precisa push: `git push -u origin HEAD` (apos aprovacao).
- Se existem arquivos nao commitados. Se houver, explique que nao entrarao no PR ate serem commitados.
- Se a branch esta atrasada em relacao a base. Nao faca rebase/merge sem pedido explicito.

### 2. Gate de responsabilidade unica

Antes de montar titulo e corpo, avalie se a branch tem uma unica responsabilidade revisavel.

Use os commits, arquivos e diff para preencher uma leitura honesta do escopo:

- Areas alteradas: exemplo `cors`, `logging`, `agents`, `auth`, `configs`, `docs`, `tests`.
- Relacao entre areas: mesma feature/bug ou mudancas independentes.
- Risco de review: baixo quando tudo pertence a uma entrega; alto quando mistura temas sem dependencia.

Se o PR mistura responsabilidades independentes, recomende dividir em PRs menores antes de abrir. Se o usuario quiser seguir com um PR unico, o titulo e o resumo devem declarar o escopo completo.

Exemplos:

- Correto para CORS apenas: `fix(cors): ajustar origens permitidas`
- Incorreto se tambem altera logging e agents: `fix(cors): ajustar origens permitidas`
- Melhor para escopo misto inevitavel: `chore(template): alinhar cors logging e agents`
- Melhor ainda quando separavel: abrir PRs distintos para CORS, logging e agents.

O titulo do PR nunca deve usar um scope menor do que o diff. Se a branch altera CORS, logging e agents, nao chame a PR apenas de CORS.

### 3. Montar rascunho com template

Use `references/pr-body-template.md` como referencia de corpo. Inclua as secoes relevantes e remova secoes vazias ou marcadas como N/A quando nao agregarem valor.

Pontos que devem ser considerados no rascunho:

- Escopo real do diff, sem prometer alteracoes que nao existem.
- Responsabilidade unica: informar se o PR e coeso ou se deveria ser dividido.
- Sem coautoria, assinatura ou nota de geracao por ferramentas de IA.
- Rastreabilidade com `.specs/features/<slug>/` quando existir.
- Impacto em API, contratos `data/meta/links`, errors `errors[]`, settings, env vars, banco, observabilidade e seguranca.
- Validacoes executadas com comandos concretos.
- Riscos residuais e follow-ups, quando houver.
- Como o reviewer deve validar manualmente, se aplicavel.

### 4. Resumo para validacao do usuario

```markdown
## Validacao antes do Pull Request

**Branch:** [nome]
**Base:** [main/master]
**Commits incluidos:** [N]
**Spec:** [.specs/... ou N/A]
**Responsabilidade unica:** SIM/NAO
**Recomendacao de escopo:** [abrir PR unico / dividir em PRs menores]

### Resumo da entrega
- [bullet]

### Commits nesta branch
| Hash | Mensagem |
|------|----------|
| ... | ... |

### Arquivos alterados (visao geral)
[stat ou lista curta]

### Analise de responsabilidade
| Area | Arquivos | Relação com o objetivo |
|------|----------|------------------------|
| ... | ... | ... |

### Validacoes
| Check | Status |
|-------|--------|
| Testes | ... |
| Lint/type | ... |
| Revisao de seguranca | ... |

### PR proposto

**Titulo:** [titulo]

**Corpo:**
[corpo baseado em references/pr-body-template.md]

**Aguardando sua aprovacao para criar o PR.**
```

Apos enviar o resumo, **pare**. Nao prossiga ate o usuario responder.

### 5. Criar PR (apos aprovacao)

Somente quando o usuario aprovar explicitamente:

```bash
git push -u origin HEAD

gh pr create --base main --head "{branch}" --title "titulo" --body-file /tmp/pr-body.txt
```

Retorne a **URL do PR** ao usuario.

Antes de executar, grave o corpo aprovado em `/tmp/pr-body.txt` ou outro arquivo temporario equivalente. Se a base correta for `master` ou outra branch, ajuste `--base`.

### 6. Revisao pos-criacao (opcional)

Se o usuario quiser revisao multi-persona do PR criado, use `.github/skills/pr-review/SKILL.md` com a URL do PR.

## Titulo do PR

- Preferir um titulo coerente com o conjunto de commits ou com o resumo real da feature.
- Exemplo: `feat(auth): bootstrap Azure AD com validacao de token`
- Evite titulo generico como `update files`, `fix stuff` ou `ajustes`.
- O scope do titulo deve cobrir o diff real. Nao use `fix(cors)` para uma PR que tambem altera logging e agents.
- Se houver multiplas areas relacionadas, use um scope agregador honesto, como `template`, `observability`, `auth` ou o nome da feature.
- Se as areas nao forem relacionadas, pare e recomende dividir a branch em PRs menores.

## Template de Referencia

Leia `references/pr-body-template.md` quando precisar montar ou revisar o corpo do PR.

Adapte o template ao tamanho da entrega:

- PR pequeno: manter `Resumo`, `Validacoes`, `Rastreabilidade` e `Riscos`.
- PR com API/config/banco/seguranca: manter tambem as secoes de impacto especificas.
- PR de documentacao/skills: manter foco em contexto, arquivos afetados e validacao textual.

## Integracao com o Workflow

| Etapa | Quem prepara | Quem pede permissao | Quem executa |
|-------|--------------|---------------------|--------------|
| Commit | `conventional-commit` | **usuario** | apos `sim` |
| PR | esta skill | **usuario** | apos `sim` |

- Orquestrador apresenta consolidado final e **nao** commita nem abre PR.
- Aprovacao do commit (`conventional-commit`) **nao** autoriza o PR automaticamente; cada etapa exige `sim` explicito.
- Nao substitui code review humano; complementa com `pr-review` quando solicitado.
