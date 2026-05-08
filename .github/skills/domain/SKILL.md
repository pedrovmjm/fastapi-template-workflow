---
name: domain
description: Padroniza fronteiras de domínio, separação entre regra de negócio e execução técnica, casos de uso e dependências entre camadas FastAPI.
---
# Domain - Fronteiras de Domínio

Use esta skill para revisar fronteiras entre camadas e impedir mistura de regra de negócio, transporte HTTP, persistência e configuração.

Ela funciona como uma skill de decisão arquitetural: identifica qual camada deve possuir cada responsabilidade e aponta a skill, o agente ou a referência mais adequada antes de implementar.

## Tabela de Decisão - Skills

| Quando a tarefa envolver | Use a skill | Decisão de ownership |
| --- | --- | --- |
| Composição da aplicação, app factory, lifespan, DI global e arquitetura FastAPI | `fastapi-best-practices` | Define a estrutura da aplicação sem assumir contratos, erros, logs ou traces. |
| Fronteiras entre domínio, transporte HTTP, persistência e configuração | `domain` | Decide onde a responsabilidade pertence e evita mistura entre camadas. |
| Planejamento SDD/SPC, especificação, design, tarefas, execução, validação e handoff | `tlc-spec-driven` | Organiza escopo, rastreabilidade, tarefas atômicas e validação. |
| Endpoints, routers, status codes, query params e documentação HTTP | `standard-endpoints` | Mantém rotas finas e delega regra de negócio para services. |
| Modelos Pydantic, contratos `data`, wrappers, envelopes, paginação e validação de campos | `standard-data-models` | Define contratos públicos de entrada e saída, sem regra de negócio. |
| Services, casos de uso, manipulação de dados e orquestração assíncrona | `standard-services` | Centraliza regra de negócio e coordena repositories, providers e integrações. |
| Interfaces por tipo de processamento, estratégias, registry e factory | `processing-interfaces` | Define contratos plugáveis para múltiplas implementações sem acoplar endpoints ou services a detalhes técnicos. |
| Repositories, queries, blobs, clients configurados e chamadas OpenAI | `standard-repositories` | Executa acesso técnico sem decidir regra de negócio. |
| Persistência SQL/NoSQL, sessões, transações, migrations e índices | `standard-database` | Define infraestrutura de dados consumida por repositories. |
| Settings, `values_domains`, providers, singletons e leitura de ambiente | `standard-configs` | Fornece configuração e clients sem regra de negócio. |
| Integrações externas, clients HTTP, retry, circuit breaker, webhooks e mapeamento de erro externo | `standard-integrations` | Isola comunicação externa e resiliência fora do domínio puro. |
| Contratos de erro, exceções, validação e respostas `errors` | `standard-errors` | Padroniza a superfície pública de falhas da API. |
| Segurança transversal, auth, autorização, OWASP, secrets, CORS, rate limiting e proteção de dados | `standard-security` | Revisa riscos que atravessam endpoints, services, logs, traces e integrações. |
| Middlewares FastAPI/Starlette, correlation id, headers e ordem de execução | `standard-middleware` | Implementa comportamento transversal de request/response. |
| Logs estruturados, eventos, correlação e dados sensíveis | `standard-logs` | Define eventos observáveis sem vazar dados sensíveis. |
| Traces, spans, atributos seguros e propagação de `correlation_id` | `standard-traces` | Instrumenta fluxos por responsabilidade sem expor payloads sensíveis. |
| Testes unitários, integração, E2E, fixtures e doubles | `standard-tests` | Define estratégia de validação proporcional ao risco da mudança. |
| Docstrings NumPy em pt-BR para módulos, classes, funções, endpoints, services e repositories | `standard-docstrings` | Documenta comportamento sem definir contratos de dados. |
| Transformar feedback recorrente da conversa em padrão reutilizável | `conversation-conventions` | Decide onde registrar novas convenções em skills ou referências. |

## Tabela de Decisão - Agentes

| Quando acionar | Use o agente | Papel no fluxo |
| --- | --- | --- |
| A tarefa exigir coordenação entre especificação, implementação, segurança, testes, lint ou handoff | `fastapi-workflow-orchestrator` | Orquestra o SDLC e seleciona agentes e skills aplicáveis. |
| For necessário especificar feature, mapear escopo, propor design ou quebrar tarefas antes de codificar | `sdd-planner` | Planeja o trabalho com critérios de aceite, riscos e validações. |
| Uma especificação, design ou lista de tarefas precisar de revisão antes da implementação | `sdd-refiner` | Refina clareza, dependências, rastreabilidade e ambiguidade. |
| A tarefa estiver pronta para implementar um slice vertical FastAPI | `fastapi-coder` | Codifica seguindo as skills standard e as fronteiras de domínio. |
| A mudança tocar auth, autorização, dados sensíveis, secrets, logs, traces, LLM, webhooks, CORS ou rate limiting | `security-reviewer` | Audita riscos de segurança, privacidade e defaults inseguros. |
| For necessário criar, ajustar ou executar testes, lint, format ou type checks | `test-lint-engineer` | Valida a mudança com testes e checks do projeto. |

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Fronteira entre regra de negócio e execução técnica | [Fronteiras entre service e repository](references/service-repository-boundaries.md) |
| Orquestração assíncrona em services e casos de uso | [Orquestração assíncrona no domínio](references/async-orchestration.md) |

## Regras Obrigatórias

- Cada camada deve ter uma responsabilidade principal.
- Services não devem importar `Request`, `Response`, `APIRouter` ou outros detalhes HTTP.
- Repositories não devem conhecer modelos de resposta HTTP.
- Configs/providers não devem conter regra de negócio.
- Entidades internas podem ser dataclasses, modelos de ORM ou tipos próprios.
- Contratos Pydantic públicos pertencem a `standard-data-models`.
- Evite misturar regra de negócio, persistência e transporte HTTP no mesmo arquivo.

## Estrutura Recomendada

```text
src/
├── models/
│   └── users/
│       └── responses/
│           ├── user_response.py
│           └── data_wrapper_user_response.py
│       └── requests/
│           └── user_request.py
├── repository/
│   └── users/
│       └── user_repository.py
├── services/
│   └── users/
│       └── user_service.py
└── routes/
   └── users/
       └── users.py
```

## Checklist

- [ ] Cada camada possui uma responsabilidade clara.
- [ ] Código de domínio não depende de `Request`, `Response` ou detalhes de rota.
- [ ] Services seguem `standard-services`.
- [ ] Repositories seguem `standard-repositories`.
- [ ] Configurações e providers seguem `standard-configs`.
