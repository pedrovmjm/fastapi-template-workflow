---
agent: 'agent'
description: 'Avaliar se uma solucao deve usar cache em memoria'
---

Use #file:../skills/in-memory-cache/SKILL.md e suas referencias para avaliar a proposta abaixo.

Contexto: ${input:contexto:Descreva o fluxo, dado ou gargalo que voce quer otimizar}

Responda em pt-BR com:

- veredito: usar cache em memoria, nao usar, ou usar outro tipo de cache;
- fonte de verdade;
- TTL ou invalidacao recomendada;
- tamanho maximo e cardinalidade esperada;
- riscos de multi-worker, seguranca e memoria;
- testes obrigatorios antes de merge.
