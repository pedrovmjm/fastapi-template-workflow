---
name: standard-agents
description: Boas praticas para criar agentes seguros no repositorio com OpenAI Agents SDK ou LangGraph, incluindo autenticacao, autorizacao, tools, guardrails, logging, tracing e testes.
---
# Standard Agents - Boas Praticas para Agentes

Use esta skill ao criar, revisar ou planejar agentes com OpenAI Agents SDK, LangGraph, tools, handoffs, graph nodes, chamadas OpenAI, logs ou traces.

## Responsabilidade Desta Skill

Esta skill e dona de:

- escolha do padrao de agente por SDK;
- contrato de autenticacao/autorizacao para tools e nodes;
- separacao entre prompt, policy, service e repository;
- logging e tracing de runs, tools e decisoes;
- guardrails e limites de side effect;
- testes negativos para agentes e tools.

Esta skill complementa:

- `fastapi-best-practices` para auth de endpoints e dependency injection;
- `standard-security` para OWASP API e OWASP LLM/GenAI;
- `standard-repositories` para chamadas OpenAI via clients configurados;
- `standard-logs` e `standard-traces` para observabilidade;
- `standard-tests` para estrategia de testes.

## Tabela de Decisao - Referencias

| Quando precisar detalhar | Leia |
| --- | --- |
| Criar agente com OpenAI Agents SDK. | [OpenAI Agents SDK](references/openai-agents-sdk.md) |
| Criar agente, grafo, node ou thread com LangGraph. | [LangGraph](references/langgraph.md) |
| Definir logs, traces e metadata de agentes. | [Logging e tracing](references/logging-tracing.md) |
| Revisar seguranca, tools e testes negativos. | [Agentes seguros](references/secure-agents.md) |

## Regras Obrigatorias

- Agente nao autentica usuario por prompt. A aplicacao autentica antes e passa contexto confiavel.
- Tools/nodes que acessam dados ou executam acoes devem validar permissao server-side.
- Prompt, guardrail ou system message nao substituem RBAC, ABAC, posse de recurso, tenant ou grupo.
- Tools devem ser pequenas, nomeadas por capacidade, com input tipado e escopo minimo.
- Nao exponha tool generica de banco, HTTP, shell ou filesystem para o modelo sem sandbox e aprovacao explicita.
- Logs e traces de agente nao devem conter token, prompt completo, payload sensivel, documento bruto ou resposta sensivel.
- Runs agenticos devem propagar `correlation_id`, `tenant_id`, identificador publico/hash do ator e identificadores de recurso seguros.
- Side effects destrutivos exigem confirmacao explicita, idempotencia quando possivel e autorizacao no handler da tool/node.

## Checklist

- [ ] O SDK escolhido esta declarado no design.
- [ ] O contexto autenticado entra no run/graph sem depender do modelo.
- [ ] Tools/nodes chamam services/repositories com contexto autenticado.
- [ ] Guardrails cobrem abuso, prompt injection e output sensivel quando aplicavel.
- [ ] Logging e tracing seguem referencias desta skill, `standard-logs` e `standard-traces`.
- [ ] Testes cobrem negacao de acesso, recurso de outro usuario, tenant errado, prompt injection e ausencia de contexto.
