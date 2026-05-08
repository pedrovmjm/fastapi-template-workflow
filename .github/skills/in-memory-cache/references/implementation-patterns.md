# Padroes de Implementacao

Use implementacao simples, local e explicita. O cache deve ficar perto do owner do custo que ele otimiza.

## Onde Colocar

- Em service quando o valor e derivado de regra de negocio e usado por multiplos endpoints.
- Em repository/client quando o custo e tecnico, como chamada externa idempotente ou descoberta de schema.
- Em config/provider quando o valor e configuracao estavel carregada uma vez ou com TTL.
- Evite cache diretamente em route handler; endpoint deve continuar fino.

## Opcoes Python

- Use `functools.lru_cache` apenas para funcao pura, argumentos hashable, sem necessidade de TTL e cardinalidade pequena.
- Use `functools.cached_property` para valor imutavel no ciclo de vida de um objeto.
- Use helper local com `time.monotonic()` para TTL simples de poucos itens.
- Considere biblioteca externa apenas se o projeto ja usar ou se houver requisito claro de LRU + TTL + concorrencia.
- Para async, nao use `lru_cache` diretamente em coroutine; cacheie resultado materializado em camada controlada.

## Concorrencia

- Proteja estado mutavel compartilhado com `asyncio.Lock` em codigo async ou lock equivalente em codigo sync.
- Evite segurar lock durante I/O externo quando isso puder bloquear todas as chamadas; quando necessario, use estrategia de single-flight ou aceite refresh duplicado.
- Defina comportamento em erro de refresh: falhar, servir stale ou tentar refetch sincronamente.

## Chaves

- Normalize chaves: lowercase quando aplicavel, remova espacos irrelevantes, ordene parametros e use tipos estaveis.
- Nunca use payload bruto ou body completo como chave.
- Inclua versao, tenant ou escopo quando o valor depender disso.
- Evite dados sensiveis na chave porque chaves costumam aparecer em logs, metrics ou dumps.

## Valores

- Trate valores como imutaveis.
- Retorne copia quando o chamador puder mutar listas, dicts ou modelos.
- Cacheie DTOs simples ou estruturas pequenas.
- Nao cacheie objetos acoplados ao request, sessao, transacao ou event loop.

## FastAPI

- Module-level cache e por processo; com `uvicorn --workers N`, existem N caches separados.
- Prefira dependencia/service configuravel quando TTL, tamanho, metricas ou reset de teste forem necessarios.
- Nao permita que readiness check use somente sucesso cacheado se o objetivo e provar acesso vivo a dependencia.
- Em lifespan, inicialize apenas cache que realmente precisa de warmup; lazy miss costuma ser mais simples.

## Comentarios e Config

- Coloque comentario curto apenas para tradeoff nao obvio de consistencia ou invalidacao.
- Torne TTL e tamanho maximo configuraveis quando impactarem producao.
- Use nomes explicitos: `_feature_flags_cache`, `_schema_cache`, `_metadata_cache`.
