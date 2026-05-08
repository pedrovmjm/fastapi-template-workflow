# Mapa de Ownership das Skills

Use este mapa para evitar sobreposição entre skills.

## Ownership

| Assunto | Skill dona | Observação |
| --- | --- | --- |
| Modelos Pydantic, `Field`, wrappers, envelopes | `standard-data-models` | Não repetir em endpoints ou docstrings. |
| Rotas, status HTTP, `APIRouter`, query params | `standard-endpoints` | Usa modelos já definidos por `standard-data-models`. |
| Contrato público de erro | `standard-errors` | Envelope `errors` com `code`, `title` e `message`. |
| Fronteiras entre camadas | `domain` | Decide ownership quando há dúvida. |
| Services e lógica de negócio | `standard-services` | Manipula dados, orquestra repositories e não conhece HTTP. |
| Interfaces por tipo de processamento | `processing-interfaces` | Define contracts, registries e factories para múltiplas estratégias ou formatos. |
| Repositories e execução técnica | `standard-repositories` | Executa query, blob e chamadas técnicas já configuradas, sem regra de negócio. |
| Integrações externas | `standard-integrations` | Define clients externos, HTTP async, timeout, retry, circuit breaker, webhooks e mapeamento de erro externo. |
| Persistência SQL/NoSQL | `standard-database` | Define lifecycle de banco, sessão, transação, migrations e índices. |
| Settings, providers e singletons | `standard-configs` | Centraliza `.env`, env vars e clients técnicos. |
| Testes unitários, integração e E2E | `standard-tests` | Define estratégia, fixtures, doubles e validação de contratos em teste. |
| Segurança transversal | `standard-security` | Define autenticação, autorização, OWASP, secrets, CORS, rate limiting e segurança LLM/GenAI. |
| Docstrings NumPy em pt-BR | `standard-docstrings` | Documenta intenção, não define contrato de dados. |
| Middlewares HTTP | `standard-middleware` | Uma preocupação por middleware. |
| Logging estruturado | `standard-logs` | Eventos, níveis, contexto seguro. |
| Tracing e spans | `standard-traces` | Observabilidade distribuída. |
| App factory, lifespan, DI, handlers | `fastapi-best-practices` | Composição da aplicação, não regras específicas das outras skills. |
| Feedback recorrente da conversa | `conversation-conventions` | Decide onde registrar novas convenções. |
| SDD, specs, tasks, execução | `spc-driven` | Workflow de planejamento e implementação. |

## Regra de Decisão

Quando uma regra parecer pertencer a duas skills, aplique esta ordem:

1. A skill mais específica fica dona da regra.
2. A skill mais geral apenas referencia a específica.
3. Exemplos completos devem morar na skill dona.
4. Outras skills podem importar ou mencionar o modelo, mas não redefinir sua estrutura.
