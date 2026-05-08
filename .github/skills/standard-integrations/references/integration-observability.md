# Observabilidade de Integrações

Integrações precisam ser observáveis sem expor dados privados. Registre o suficiente para diagnosticar latência, erro e custo.

## Logs

- Siga `standard-logs` para formato, níveis e dados sensíveis.
- Use logs estruturados com `event` e `layer`.
- Use `layer` igual a `integration`.
- Nomeie `event` com padrão estável, como `external.timeout` ou `{dominio}.{acao}`.
- Inclua `provider`, `operation`, `external_status`, `duration_ms`, `attempt`, `result` e `correlation_id` quando disponíveis.

Não registre headers de autenticação, header `Authorization`, cookies, payload completo, tokens, API keys, senhas, documentos, cartões, prompts sensíveis ou responses completas.

## Exemplo de Log

```python
logger.warning(
    "Dependência externa respondeu com atraso.",
    extra={
        "event": "external.timeout",
        "layer": "integration",
        "provider": "payments",
        "operation": "authorize",
        "external_status": 504,
        "duration_ms": 3000,
        "attempt": 1,
        "result": "timeout",
        "correlation_id": correlation_id,
    },
)
```

## Traces

- Siga `standard-traces` para nomes de spans, atributos seguros e erros.
- Nomeie span como `{dominio}.integration.{operacao}`.
- Use atributos seguros com prefixo `app.*`.
- Inclua `app.layer`, `app.operation`, `app.result` e `app.correlation_id` quando disponíveis.
- Inclua provider, status externo e duração apenas quando forem dados seguros.
- Marque erro com `span.record_exception(error)`, status `ERROR` e categoria interna.
- Relance a exceção depois de registrar o erro no span.
- Propague `correlation_id` quando possível.

## Exemplo de Trace

```python
with tracer.start_as_current_span("payments.integration.authorize") as span:
    span.set_attribute("app.layer", "integration")
    span.set_attribute("app.operation", "authorize")
    span.set_attribute("app.provider", "payments")
    if correlation_id is not None:
        span.set_attribute("app.correlation_id", correlation_id)

    try:
        response = await client.authorize(payload=payload)
        span.set_attribute("app.result", "success")
        span.set_attribute("app.external_status", response.status_code)
    except Exception as error:
        span.record_exception(error)
        span.set_status(Status(StatusCode.ERROR, type(error).__name__))
        span.set_attribute("app.result", "failed")
        raise
```

## Métricas

- Latência por provider/operação.
- Taxa de erro por categoria.
- Rate limit externo.
- Retry count.
- Circuit breaker aberto.
- Custo aproximado quando houver cobrança por uso.

## Checklist

- [ ] Logs têm `event`, `layer`, `provider`, `operation`, status e duração.
- [ ] Logs usam `layer` igual a `integration`.
- [ ] Logs incluem `correlation_id` quando disponível.
- [ ] Traces usam atributos seguros com prefixo `app.*`.
- [ ] Traces registram erro e relançam exceção.
- [ ] Métricas indicam latência e erro.
- [ ] Dados sensíveis foram omitidos.
- [ ] `correlation_id` acompanha a chamada.
