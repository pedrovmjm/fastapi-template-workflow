---
agent: 'agent'
description: 'Revisar implementacao de cache em memoria'
---

Revise a implementacao de cache em memoria informada abaixo usando #file:../skills/in-memory-cache/SKILL.md, #file:../skills/in-memory-cache/references/decision-gate.md, #file:../skills/in-memory-cache/references/implementation-patterns.md e #file:../skills/in-memory-cache/references/limits-observability-tests.md.

Alvo da revisao: ${input:alvo:Informe arquivos, diff, PR ou descricao da implementacao}

Entregue findings priorizados com arquivo/linha quando possivel, cobrindo:

- corretude se todo lookup for miss;
- staleness e invalidacao;
- limite de memoria e cardinalidade de chaves;
- risco multi-worker;
- dados sensiveis ou objetos vivos cacheados;
- observabilidade;
- testes ausentes.
