# OpenAI Agents SDK

Use esta referencia para agentes criados com OpenAI Agents SDK.

## Fontes oficiais

- Tracing: https://openai.github.io/openai-agents-python/tracing/
- Configuration: https://openai.github.io/openai-agents-python/config/
- Tools: https://openai.github.io/openai-agents-python/tools/
- Guardrails: https://openai.github.io/openai-agents-python/guardrails/
- Context management: https://openai.github.io/openai-agents-python/context/

## Estrutura recomendada

- Crie o agente na camada de service ou em modulo de composicao de agentes; repositories ficam para I/O tecnico e clients configurados.
- Injete clients e settings pela infraestrutura existente do projeto.
- Use contexto local do run para carregar `ActorContext`, `correlation_id` e dependencias que tools precisam.
- Se usar agent-as-tool ou handoff, preserve o mesmo contexto autenticado e nao amplie permissao por padrao.

## Auth e tools

- O endpoint/job autentica antes de chamar `Runner.run`.
- A tool valida scope, role, grupo, tenant e posse antes de executar I/O.
- O modelo nao pode fabricar `ActorContext`; injete via closure, contexto local ou dependencia controlada pela aplicacao.
- Tools destrutivas precisam de confirmacao e autorizacao dentro do handler.

## Guardrails

- Use input guardrails para bloquear abuso antes do custo alto quando o risco for conhecido.
- Use tool guardrails quando precisar validar cada chamada de tool.
- Use output guardrails para impedir resposta que exponha dado sensivel ou formato proibido.
- Guardrail e defesa complementar; autorizacao real fica em service/repository/tool handler.

## Tracing e logging

- O SDK possui tracing ligado por padrao.
- Em producao com dados sensiveis, use `RunConfig(trace_include_sensitive_data=False)` ou `OPENAI_AGENTS_TRACE_INCLUDE_SENSITIVE_DATA=0`.
- Mantenha `OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1` e `OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1` como default seguro.
- Use `workflow_name`, `group_id` e metadata segura para correlacionar run com request, tenant e recurso.
- O SDK define loggers `openai.agents` e `openai.agents.tracing`; eles devem seguir a configuracao de logging da aplicacao.

## Checklist

- [ ] `Runner.run` recebe contexto confiavel.
- [ ] Tool sensivel valida permissao antes do side effect.
- [ ] Guardrails foram escolhidos pelo risco real.
- [ ] Tracing nao captura dados sensiveis em producao.
- [ ] Logs do SDK nao registram dados de modelo/tool sensiveis.
