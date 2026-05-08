---
name: standard-tests
description: Padroniza testes FastAPI com pytest, cobrindo testes unitários, integração e E2E de fluxos completos, sem depender apenas de mocks.
---
# Standard Tests - Unidade, Integração e E2E

Use esta skill ao criar ou revisar testes automatizados para endpoints, services, repositories, integrações externas, contratos de erro, envelopes e fluxos completos.

## Responsabilidade Desta Skill

Esta skill é dona de:

- estratégia de testes unitários, integração e E2E;
- uso de `pytest`, fixtures, `pytest-asyncio` ou equivalente;
- testes de endpoints FastAPI com client assíncrono;
- testes de services com doubles bem delimitados;
- testes de repositories com banco/container/test database quando necessário;
- validação de envelopes `data`, `meta`, `links` e `errors`;
- testes de fluxos ponta a ponta por comportamento de usuário/API.

Esta skill não é dona de:

- definição de status HTTP esperado: use `standard-endpoints`;
- definição de contratos Pydantic: use `standard-data-models` e `standard-errors`;
- regra de negócio: use `standard-services`;
- queries e persistência: use `standard-repositories` e `standard-database`;
- política de segurança: use `standard-security`;
- processo SPC de cobertura por tarefa: use `spc-driven`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar estratégia de testes. | [Estratégia de testes](references/test-strategy.md) |
| Quando precisar aprofundar testes unitários. | [Testes unitários](references/unit-tests.md) |
| Quando precisar aprofundar testes de integração. | [Testes de integração](references/integration-tests.md) |
| Quando precisar aprofundar testes e2e de fluxos. | [Testes E2E de fluxos](references/e2e-flow-tests.md) |
| Quando precisar aprofundar fixtures, dados e doubles. | [Fixtures, dados e doubles](references/fixtures-and-doubles.md) |

## Regras Obrigatórias

- Todo comportamento novo deve ter pelo menos um teste no nível adequado.
- Teste unitário valida regra isolada; teste de integração valida fronteiras reais; teste E2E valida fluxo completo.
- Testes devem espelhar a estrutura do arquivo testado para deixar a relação óbvia.
- Para testar `src/services/auth/auth.py`, crie o teste unitário em `tests/unit/services/auth/test_auth.py`.
- Para outros níveis, preserve o mesmo caminho de domínio dentro do diretório do nível: `tests/integration/services/auth/test_auth.py` ou `tests/e2e/services/auth/test_auth.py`, quando fizer sentido.
- A meta mínima para unitários é cerca de 80% de cobertura no escopo testado.
- Cada ponto de comportamento testável deve ter pelo menos 3 testes, combinando cenários felizes e infelizes.
- Não substitua integração ou E2E por mocks quando o risco está na fiação, contrato, banco ou provider.
- Mocks devem representar dependências externas ou cenários difíceis, não esconder bugs de integração interna.
- Testes async devem usar client e fixtures compatíveis com async.
- Erros devem validar envelope `errors[].code/title/message`.
- Listagens devem validar `data`, `meta` e `links`.
- Testes de segurança devem incluir casos negativos de autorização.
- Ao concluir os testes, gere um pequeno relatório em `.spec/tests/<dominio>/<arquivo_testado>.md` descrevendo os cenários exercitados, comandos usados e resultado de cobertura.

## Estrutura de Arquivos de Teste

Clone a estrutura do repositório a partir de `src` dentro do nível de teste escolhido.

```text
src/services/auth/auth.py
tests/unit/services/auth/test_auth.py
.spec/tests/services/auth/auth.md
```

Use o mesmo padrão para endpoints, repositories, clients e módulos auxiliares:

```text
src/routes/health/health.py
tests/integration/routes/health/test_health.py
.spec/tests/routes/health/health.md
```

## Relatório de Testes

Cada arquivo ou componente testado deve ter um relatório curto em `.spec/tests/<dominio>/<arquivo_testado>.md`.

Inclua:

- arquivo testado;
- arquivo(s) de teste criados ou alterados;
- cenários felizes cobertos;
- cenários infelizes cobertos;
- doubles, fixtures ou dependências reais usadas;
- comando executado;
- resultado de cobertura, mirando cerca de 80% de unitários no escopo testado.

Exemplo:

```markdown
# src/services/auth/auth.py

## Testes

- tests/unit/services/auth/test_auth.py

## Cenários

- Login válido retorna usuário autenticado.
- Credenciais inválidas retornam erro de autenticação.
- Usuário inativo é bloqueado.

## Execução

- Comando: `pytest tests/unit/services/auth/test_auth.py --cov=src/services/auth --cov-report=term-missing`
- Cobertura unitária: 82%
```

## Checklist

- [ ] O caminho do teste espelha o caminho do arquivo em `src`.
- [ ] Há teste unitário para regra de negócio relevante.
- [ ] Há pelo menos 3 testes por ponto de comportamento testável.
- [ ] Unitários miram cerca de 80% de cobertura no escopo testado.
- [ ] Há teste de integração para repository, banco, client externo ou endpoint quando a fiação importa.
- [ ] Há teste E2E para fluxo crítico de negócio/API.
- [ ] Mocks são usados apenas onde reduzem custo sem ocultar risco real.
- [ ] Contratos de sucesso e erro são validados.
- [ ] Casos negativos cobrem validação, autorização e recurso inexistente.
- [ ] Relatório curto foi gerado em `.spec/tests/<dominio>/<arquivo_testado>.md`.
