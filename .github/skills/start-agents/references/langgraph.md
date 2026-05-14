# LangGraph

Use esta referencia para agentes, grafos, nodes e threads com LangGraph/LangSmith.

## Fontes oficiais

- LangGraph Platform auth: https://docs.langchain.com/langgraph-platform/auth
- LangSmith observability para LangGraph: https://docs.langchain.com/oss/python/langgraph/observability
- Trace LangGraph applications: https://docs.langchain.com/langsmith/trace-with-langgraph

## LangGraph Platform

- Autenticacao fica em `@auth.authenticate`: validar credencial e retornar identidade.
- Autorizacao fica em `@auth.on`: filtrar, negar ou marcar metadata de threads, runs, crons e assistants.
- Para recursos single-owner, grave `owner` em metadata na criacao e retorne filtro por `owner` em leitura/listagem.
- Para RBAC/ABAC, derive `permissions`, `roles`, `groups` e `tenant_id` no auth handler e valide nos handlers especificos.
- Self-hosted sem auth default precisa de decisao explicita antes de producao.

## LangGraph embutido em FastAPI

- Reutilize o `ActorContext` autenticado pelo endpoint.
- Passe contexto via `configurable`, contexto do grafo ou dependencia controlada pela aplicacao.
- Nodes/tools que acessam dados chamam services/repositories com `ActorContext`.
- O grafo nao deve carregar dados de outro tenant/owner apenas porque o historico cita um id.

## Observabilidade

- LangSmith tracing pode ser ativado por variaveis como `LANGSMITH_TRACING=true` e `LANGSMITH_PROJECT`.
- Adicione metadata segura: ambiente, versao, `correlation_id`, `tenant_id`, ator publico/hash e recurso publico quando seguro.
- Use anonymizers/callbacks quando mensagens, prompts ou outputs puderem conter dado sensivel.
- Nao envie token, documento completo, segredo ou payload sensivel para traces.

## Checklist

- [ ] AuthN roda em toda request protegida.
- [ ] AuthZ filtra recursos por owner/tenant/grupo.
- [ ] Metadata de thread/run inclui owner/tenant seguro quando necessario.
- [ ] Nodes/tools repetem autorizacao antes de I/O ou mutacao.
- [ ] Tracing LangSmith tem metadata segura e redacao/anonymizer quando aplicavel.
