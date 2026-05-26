# Logging e Tracing de Agentes

Use com `standard-logs` e `standard-traces`.

## Eventos minimos

- `agent.run_started`
- `agent.run_completed`
- `agent.run_failed`
- `agent.tool_requested`
- `agent.tool_authorized`
- `agent.tool_denied`
- `agent.tool_completed`
- `agent.guardrail_triggered`

## Campos seguros

Inclua quando existir:

- `event`
- `layer`
- `operation`
- `decision`
- `reason_code`
- `correlation_id`
- `tenant_id`
- `actor_id_hash` ou identificador publico nao sensivel
- `agent_name`
- `sdk`
- `tool_name`
- `resource_type`
- `resource_id` publico, se nao revelar dado sensivel
- `required_scopes`
- `required_roles`
- `required_groups`

## Campos proibidos

- token, refresh token, API key, cookie, segredo;
- prompt completo, mensagem completa, documento bruto ou payload de tool;
- claims completas do JWT;
- email, nome, documento, telefone ou dado pessoal sem necessidade explicita;
- resposta de LLM com dado sensivel.

## Spans

- Crie spans por responsabilidade: agent run, tool execution, service authorization, repository query e integracao externa.
- Marque `app.agent.name`, `app.agent.sdk`, `app.tool.name`, `app.auth.decision`, `app.auth.reason_code`, `app.layer`, `app.correlation_id`, `app.tenant_id`.
- Negacao esperada de autorizacao pode ser resultado de negocio com `decision=denied`; falha tecnica deve marcar status de erro.
- Relance excecoes para handlers globais depois de registrar contexto seguro.
- Logs de agente vao para o console (`standard-logs`); respostas HTTP ao cliente seguem `standard-errors` — veja `standard-logs/references/log-levels-vs-http-errors.md`.

## Exemplo de log

```python
logger.info(
    "Tool negada para o ator autenticado.",
    extra={
        "event": "agent.tool_denied",
        "layer": "service",
        "sdk": "openai-agents-sdk",
        "agent_name": "document_assistant",
        "tool_name": "delete_document",
        "decision": "denied",
        "reason_code": "missing_scope",
        "tenant_id": actor.tenant_id,
        "correlation_id": actor.correlation_id,
        "resource_type": "document",
        "resource_id": document_id,
    },
)
```
