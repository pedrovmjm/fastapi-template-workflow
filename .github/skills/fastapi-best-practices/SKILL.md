---
name: fastapi-best-practices
description: Padroniza boas práticas de composição de aplicações FastAPI: app factory, lifespan, dependency injection, registro de exception handlers, async boundaries e revisão arquitetural sem sobrepor endpoints, modelos, erros, middlewares, logs ou traces.
---
# FastAPI Best Practices - Composição da Aplicação

Use esta skill ao criar ou revisar a estrutura principal de uma aplicação FastAPI.

## Responsabilidade Desta Skill

Esta skill é dona de:

- criação da aplicação (`create_app`);
- organização de routers;
- `lifespan`;
- dependency injection;
- autenticacao/autorizacao como dependencia da aplicacao e propagacao segura de contexto autenticado;
- estrutura transversal de auth em `src/security/` quando o projeto escolher tratar seguranca como capacidade similar a `observability`;
- registro de exception handlers;
- fronteiras assíncronas;
- revisão de acoplamento entre camadas.

Esta skill não é dona de:

- modelos Pydantic e contratos `data`: use `standard-data-models`;
- regras de endpoint e status HTTP: use `standard-endpoints`;
- contrato público de erro: use `standard-errors`;
- middlewares específicos: use `standard-middleware`;
- logs estruturados: use `standard-logs`;
- traces: use `standard-traces`;
- regra de negócio: use `domain`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar composição da aplicação. | [Composição da aplicação](references/application-composition.md) |
| Quando precisar aprofundar dependency injection. | [Dependency injection](references/dependency-injection.md) |
| Quando precisar aprofundar autenticacao, autorizacao, Azure AD, posse de recurso e contexto autenticado. | [Autenticacao e autorizacao](references/authentication-authorization.md) |
| Quando precisar aprofundar tratamento de erros. | [Tratamento de erros](references/error-handling.md) |
| Quando precisar aprofundar regras assíncronas. | [Regras assíncronas](references/async-guidelines.md) |
| Quando precisar aprofundar mapa de ownership das skills. | [Mapa de ownership das skills](references/skill-ownership.md) |

## Regras Obrigatórias

- A aplicação deve ser criada por uma função `async def create_app() -> FastAPI` quando houver inicialização assíncrona.
- `create_app` deve delegar o registro de routers para `_register_routes(app)`.
- `create_app` deve delegar o registro de middlewares para `_register_middlewares(app, settings)`.
- A instância `FastAPI` deve receber metadados e paths públicos a partir de `settings`, como `title`, `description`, `version`, `docs_url`, `redoc_url` e `openapi_url`.
- Routers devem ser registrados em um ponto previsível da aplicação.
- `lifespan` deve concentrar abertura e fechamento de recursos globais.
- Dependências devem ser pequenas, tipadas e testáveis.
- Endpoints autenticados devem validar identidade por dependencia, propagar contexto autenticado para services/repositories e reforcar posse/permissao no servidor.
- Handlers de erro devem transformar exceções conhecidas no contrato definido por `standard-errors`.
- Código bloqueante não deve rodar diretamente dentro de endpoints assíncronos.
- Configurações devem ser lidas por uma camada própria, não espalhadas em rotas.
- Cada camada deve depender apenas da camada imediatamente necessária.

## Checklist de Revisão

- [ ] Existe ponto único de criação da aplicação.
- [ ] Routers são registrados sem lógica condicional espalhada.
- [ ] Recursos globais são abertos e fechados no `lifespan`.
- [ ] Dependências são tipadas e substituíveis em testes.
- [ ] Endpoints autenticados validam token e propagam contexto seguro entre camadas.
- [ ] Erros de domínio não vazam como exceções cruas para o cliente.
- [ ] Contratos públicos de erro seguem `standard-errors`.
- [ ] Não há I/O bloqueante em fluxo assíncrono.
- [ ] A skill correta foi usada para modelos, endpoints, middlewares, logs e traces.
