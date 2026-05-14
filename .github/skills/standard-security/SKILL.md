---
name: standard-security
description: Padroniza segurança transversal em FastAPI, cobrindo autenticação, autorização, OWASP Web/API, OWASP LLM/GenAI, secrets, CORS, rate limiting e proteção de dados.
---
# Standard Security - Segurança Transversal

Use esta skill ao criar ou revisar autenticação, autorização, controles contra riscos OWASP, segurança de APIs, segurança de fluxos com LLM/GenAI, proteção de dados, secrets, CORS ou rate limiting.

## Responsabilidade Desta Skill

Esta skill é dona de:

- política de autenticação e autorização;
- controles contra OWASP Top 10 Web e OWASP API Security Top 10;
- controles contra OWASP Top 10 para LLM/GenAI;
- proteção contra prompt injection, vazamento de dados e uso excessivo de ferramentas;
- gestão segura de secrets e tokens;
- política de CORS, rate limiting e abuse prevention;
- requisitos de segurança para endpoints, services, repositories, logs e traces.

Esta skill não é dona de:

- implementação detalhada de middleware: use `standard-middleware`;
- formato de logs seguros: use `standard-logs`;
- atributos seguros de traces: use `standard-traces`;
- contrato público de erro: use `standard-errors`;
- modelagem Pydantic comum: use `standard-data-models`;
- queries, sessions e banco: use `standard-database` e `standard-repositories`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando revisar riscos Web/API em FastAPI. | [OWASP Web e API em FastAPI](references/owasp-web-api.md) |
| Quando houver LLM, agentes, prompts ou tools. | [OWASP LLM e GenAI](references/owasp-llm-genai.md) |
| Quando precisar aprofundar autenticação, autorização e escopos. | [Autenticação, autorização e escopos](references/authentication-authorization.md) |
| Quando auth envolver Azure AD, dependency injection, posse de recurso, services ou repositories. | `../fastapi-best-practices/references/authentication-authorization.md` |
| Quando houver agentes OpenAI Agents SDK, LangGraph, tools, guardrails, logs ou traces de agente. | `../start-agents/SKILL.md` |
| Quando precisar aprofundar proteção de dados, secrets e abuso. | [Proteção de dados, secrets e abuso](references/data-protection-and-abuse.md) |

## Regras Obrigatórias

- Toda decisão sensível deve validar identidade, autorização e posse do recurso.
- Authorization não pode depender apenas de esconder rota, campo ou botão no cliente.
- Inputs externos devem ser validados antes de chegar à regra de negócio.
- Outputs externos, inclusive respostas de LLM, devem ser tratados como não confiáveis.
- Tokens, secrets, cookies e dados pessoais não devem aparecer em logs, traces ou responses de erro.
- CORS deve liberar origens explícitas por ambiente.
- Rate limiting deve proteger autenticação, endpoints caros e fluxos com LLM.
- Fluxos agentic/LLM com ferramentas devem ter allowlist, escopo mínimo e confirmação para ações destrutivas.

## Checklist

- [ ] Autenticação e autorização foram revisadas separadamente.
- [ ] BOLA/BFLA foram considerados em endpoints com ids ou ações por recurso.
- [ ] Rate limiting e limites de payload foram definidos para rotas críticas.
- [ ] Dados sensíveis são mascarados ou omitidos em logs, traces e erros.
- [ ] Secrets vêm de provider seguro e nunca do código.
- [ ] LLM output não é executado, renderizado ou persistido sem validação.
- [ ] Ferramentas chamadas por LLM usam allowlist e permissões mínimas.
