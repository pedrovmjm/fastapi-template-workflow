---
name: standard-integrations
description: Padroniza integrações externas em FastAPI, incluindo clients HTTP assíncronos, timeout, retry, circuit breaker, webhooks, mapeamento de erro, logs e traces.
---
# Standard Integrations - Clients Externos e Webhooks

Use esta skill ao criar ou revisar integrações com APIs externas, webhooks, SDKs, serviços de pagamento, mensageria HTTP, providers de IA ou qualquer dependência fora do processo da aplicação.

## Responsabilidade Desta Skill

Esta skill é dona de:

- clients HTTP assíncronos;
- timeouts, retries, backoff e circuit breaker;
- contratos de request/response externos;
- mapeamento de erros externos para exceções técnicas internas;
- webhooks, assinatura, idempotência e reprocessamento;
- observabilidade segura de integrações;
- limites de consumo, concorrência e custo.

Esta skill não é dona de:

- regra de negócio após resposta externa: use `standard-services`;
- execução técnica dentro de repository existente: use `standard-repositories`;
- criação de settings e singleton de client: use `standard-configs`;
- segurança transversal e OWASP: use `standard-security`;
- logs/traces detalhados: use `standard-logs` e `standard-traces`;
- testes de contrato e integração: use `standard-tests`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar clients http assíncronos. | [Clients HTTP assíncronos](references/http-clients.md) |
| Quando precisar aprofundar timeout, retry e circuit breaker. | [Timeout, retry e circuit breaker](references/resilience.md) |
| Quando precisar aprofundar mapeamento de erros externos. | [Mapeamento de erros externos](references/external-error-mapping.md) |
| Quando precisar aprofundar webhooks e idempotência. | [Webhooks e idempotência](references/webhooks.md) |
| Quando precisar aprofundar observabilidade de integrações. | [Observabilidade de integrações](references/integration-observability.md) |

## Regras Obrigatórias

- Toda chamada externa deve ter timeout explícito.
- Client HTTP assíncrono deve usar `httpx.AsyncClient`.
- Timeout do `httpx.AsyncClient` deve ser configurado explicitamente a partir de `settings`.
- Configurações globais de HTTP devem ter value domain próprio, como `src/configs/values_domains/httpx_client.py`.
- Retry deve existir apenas para operações idempotentes ou com idempotency key.
- Client externo deve ser injetado, não criado dentro do método de negócio.
- Erro externo deve ser traduzido para exceção interna conhecida.
- Dados sensíveis de request/response externo não devem ir para logs ou traces.
- Webhook deve validar assinatura quando o provider suportar.
- Operações caras devem ter limite de concorrência, custo ou rate limit.

## Checklist

- [ ] Client é assíncrono e configurado por provider.
- [ ] Client HTTP assíncrono usa `httpx.AsyncClient`.
- [ ] Timeout, retry e backoff foram definidos.
- [ ] Timeout explícito do `httpx.AsyncClient` vem de `settings` e do value domain de `httpx_client`.
- [ ] Idempotência foi considerada para escrita externa.
- [ ] Erros externos são mapeados.
- [ ] Webhooks validam assinatura e duplicidade.
- [ ] Logs/traces registram metadados seguros.
