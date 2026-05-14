# Copilot Instructions

Responda ao usuario em pt-BR por padrao.

Este repositorio usa custom agents do GitHub Copilot em `.github/agents/` e skills em `.github/skills/`.

Para tarefas FastAPI que envolvam planejamento, implementacao, seguranca, testes ou lint e que devam percorrer o workflow do repositorio, selecione explicitamente o agente `workflow-orchestrator` como ponto de entrada. Ele coordena:

- `sdd-planner` para especificacao, design e plano SDD/SPC.
- `sdd-refiner` para revisar ambiguidade, criterios de aceite, riscos e tarefas.
- `coder-engineer` para implementacao com as skills standard aplicaveis.
- `cache-reviewer` para decidir ou revisar cache em memoria, TTL, invalidacao, limites e risco multi-worker.
- `security-reviewer` para auditoria de seguranca, privacidade, logs, traces e abuso.
- `test-engineer` para criar, ajustar e executar testes depois da revisao de seguranca.
- `lint-engineer` para lint, format e type checks depois dos testes.

Quando o pedido do usuario for executar uma feature, bugfix ou mudanca usando o workflow deste repositorio, a acao correta e selecionar explicitamente `workflow-orchestrator`; nao pule direto para `sdd-planner` apenas porque existe etapa de planejamento.

Use `sdd-planner` diretamente somente quando o usuario pedir apenas especificacao, design, quebra de tarefas, revisao de plano ou handoff, sem solicitar implementacao/validacao completa.

O orquestrador so pode coordenar com `read`, `search`, `todo` e `agent`. O alias `agent` representa a capacidade de chamar subagents, isto e, `runSubagents`. Ele nao deve escrever arquivos, rodar comandos, implementar codigo ou executar skills diretamente.

O orquestrador deve executar o workflow de forma estritamente sequencial. Nao dispare swarm, fan-out ou multiplos subagents em paralelo: chame um agent por vez, aguarde o resultado, atualize o contexto/todo e so entao decida a proxima chamada. Revisores, testes e lint so devem ser acionados depois do output da etapa anterior.

Skills em `.github/skills/` sao referencias de padrao e ownership. O orquestrador deve encaminhar as skills relevantes no prompt dos subagents responsaveis; quem executa planejamento, codigo, revisao ou validacao e sempre um agent especializado.

Antes de alterar codigo, o agent executor deve consultar as skills relevantes em `.github/skills/` e preservar os padroes locais do projeto.

Use `.github/skills/spc-driven/SKILL.md` para dimensionar o fluxo: rapido, medio, grande ou complexo. Para mudancas pequenas, condense o processo, mas mantenha a ordem codigo -> seguranca -> testes -> lint quando houver impacto real.

Use `.github/skills/in-memory-cache/SKILL.md` quando a tarefa mencionar cache em memoria, cache local, memoizacao, TTL, LRU ou reducao de chamadas repetidas. Para avaliacoes pontuais, use tambem os prompts em `.github/prompts/avaliar-cache-memoria.prompt.md` e `.github/prompts/revisar-cache-memoria.prompt.md`.

Use `.github/skills/fastapi-best-practices/references/authentication-authorization.md` quando a tarefa envolver endpoint autenticado, Azure AD/Microsoft Entra ID, autorizacao por owner/tenant/grupo/role ou repositories filtrados por usuario.

Use `.github/skills/start-agents/SKILL.md` quando a tarefa envolver OpenAI Agents SDK, LangGraph, tools, guardrails, logging, tracing ou agentes que executam acoes em nome do usuario.

Ao concluir uma tarefa, reporte arquivos alterados, skills usadas, validacoes executadas e riscos remanescentes.
