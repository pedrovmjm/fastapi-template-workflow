---
name: in-memory-cache
description: Orienta decisao, desenho, implementacao e revisao de cache em memoria dentro de um processo da aplicacao. Use quando a tarefa mencionar cache em memoria, cache local, memoizacao, LRU, TTL, reduzir chamadas externas, acelerar leituras caras, cachear dados derivados, configuracoes, health/status helpers, API clients, services, repositories ou comportamento FastAPI com risco de consistencia, limite de memoria, invalidacao ou multi-worker.
---
# Cache em Memoria - Cache Local por Processo

Use esta skill para tratar cache em memoria como otimizacao, nunca como fonte de verdade.

## Responsabilidade Desta Skill

Esta skill e dona de:

- decisao de usar ou rejeitar cache em memoria;
- TTL, tamanho maximo, politica de expulsao e invalidacao;
- riscos de consistencia em apps com multiplos workers, pods ou processos;
- ownership de cache em services, repositories, clients e helpers;
- observabilidade, testes e revisao de comportamento stale.

Esta skill nao e dona de:

- cache distribuido com Redis/Memcached: use esta skill apenas para decidir quando migrar para cache compartilhado;
- banco, sessoes e transacoes: use `standard-database`;
- clients externos, retry e circuit breaker: use `standard-integrations`;
- logs e traces: use `standard-logs` e `standard-traces`;
- estrategia geral de testes: use `standard-tests`.

## Tabela de Decisao - Referencias

| Quando precisar detalhar | Leia a referencia |
| --- | --- |
| Decidir se cache em memoria e apropriado ou deve ser evitado. | [Portao de decisao](references/decision-gate.md) |
| Implementar cache local em Python/FastAPI sem esconder acoplamento. | [Padroes de implementacao](references/implementation-patterns.md) |
| Definir TTL, limites, observabilidade, invalidacao e testes. | [Limites, observabilidade e testes](references/limits-observability-tests.md) |

## Regras Obrigatorias

- Defina a fonte de verdade antes de cachear qualquer valor.
- Documente o staleness maximo aceitavel em TTL ou regra de invalidacao.
- Defina limite maximo de itens; nao aceite keyspace aberto sem bound.
- Trate cache em memoria como estado por processo. Em multi-worker, cada worker tem seu proprio cache.
- Nao cacheie secrets, tokens, sessoes, conexoes, locks, generators, requests, responses mutaveis ou objetos de ORM vivos.
- Nao use cache para decisoes de autorizacao, permissao, billing, estoque, compliance ou escrita critica sem invalidacao forte.
- Nao adicione dependencia nova de cache se `functools` ou um helper local simples resolverem o caso com menor risco.
- Exponha forma de limpar cache em testes.
- Inclua testes de miss, hit, expiracao e invalidacao quando o cache alterar comportamento observavel.

## Padrao de Decisao Rapida

Use cache em memoria quando:

- o dado e pequeno, recomputavel e tolera staleness;
- o custo evitado e claro: latencia, CPU, serializacao, I/O ou chamadas idempotentes;
- a cardinalidade das chaves e naturalmente baixa ou limitada;
- a inconsistencia entre workers nao quebra contrato publico.

Evite cache em memoria quando:

- a aplicacao precisa de consistencia global entre workers, pods ou maquinas;
- a entrada vem de usuario e pode gerar chaves infinitas;
- o valor e grande ou sensivel;
- stale data pode causar escrita incorreta, acesso indevido ou resposta enganosa;
- o cache seria usado para mascarar indisponibilidade em readiness/health check.

## Checklist

- [ ] Fonte de verdade identificada.
- [ ] TTL ou invalidacao explicita definida.
- [ ] Tamanho maximo configurado.
- [ ] Implicacao multi-worker documentada.
- [ ] Valores mutaveis protegidos contra alteracao por chamada.
- [ ] Metricas/logs/traces definidos quando o cache nao for trivial.
- [ ] Testes cobrem hit, miss, expiracao, invalidacao e falha de refresh quando aplicavel.
