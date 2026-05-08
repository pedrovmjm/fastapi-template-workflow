# Limites, Observabilidade e Testes

## Defaults Conservadores

- TTL para dados de banco ou API externa: 30 segundos a 5 minutos.
- TTL para referencia raramente alterada: ate 1 hora, se stale for aceitavel.
- Max items inicial: 128 a 1024, salvo cardinalidade provadamente menor.
- Evite valores multi-MB; prefira cache distribuido, storage ou outra estrategia.
- Use refresh lazy no primeiro miss. Background refresh so vale quando latencia justificar e erro estiver bem definido.

## Invalidacao

- Se houver escrita que muda leitura cacheada, exponha invalidacao explicita.
- Se invalidacao explicita for dificil, use TTL curto e documente o risco.
- Em multi-worker, invalidacao local nao invalida outros processos.
- Nunca dependa de restart para corrigir dado stale em fluxo critico.

## Observabilidade

Para cache nao trivial, exponha pelo menos:

- hits e misses;
- expiracoes e evictions;
- tamanho atual;
- erros de refresh;
- latencia de refresh;
- idade do valor servido quando stale for permitido.

Evite logar chaves completas quando puderem conter dados de usuario. Prefira hash, tipo de chave ou dimensoes de baixa cardinalidade.

## Testes Obrigatorios Quando o Cache Altera Comportamento

- Miss inicial chama a fonte de verdade.
- Hit reutiliza valor sem chamada extra.
- Expiracao apos TTL refaz a chamada.
- Invalidacao remove ou atualiza valor.
- Erro de refresh segue o comportamento definido.
- Valores mutaveis nao vazam alteracao entre chamadas.
- Limite de tamanho evita crescimento indefinido.

## Testes em FastAPI

- Injete TTL curto ou clock controlado quando possivel.
- Exponha metodo de clear/reset para fixtures.
- Evite sleeps longos; prefira clock fake ou TTL muito baixo.
- Em health/readiness, teste que o cache nao mascara dependencia indisponivel quando o endpoint promete checagem viva.

## Checklist de Review

- O codigo funciona corretamente se todo lookup for miss?
- O staleness documentado e aceitavel para o contrato publico?
- O keyspace e limitado?
- O cache nao armazena dado sensivel ou objeto vivo?
- Existe limite de memoria por processo?
- A invalidacao cobre writes relevantes?
- O comportamento multi-worker foi considerado?
- A complexidade e justificada pelo custo evitado?
