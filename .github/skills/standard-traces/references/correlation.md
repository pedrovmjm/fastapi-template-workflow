# Correlação em Traces

Use traces para conectar a execução distribuída com logs, erros e respostas HTTP.

## Regras

- O `correlation_id` deve vir de `request.state.correlation_id`, preenchido pelo middleware de correlação.
- Não gere `correlation_id` dentro de spans, services ou repositories.
- Inclua `app.correlation_id` no span de entrada e nos spans manuais relevantes quando disponível.
- Use `trace_id` e `span_id` do provedor de tracing para investigar a árvore de spans; não substitua esses IDs por `correlation_id`.
- Logs de erro e eventos relevantes devem carregar o mesmo `correlation_id` para permitir busca cruzada.
- Respostas HTTP devem propagar `X-Correlation-Id` conforme `standard-middleware`.
- O contrato do body de erro pertence a `standard-errors`; não adicione campos de tracing no body sem revisar essa skill.

## Exemplo

```python
from opentelemetry import trace


async def get_user(request: Request, user_id: str) -> UserResponse:
    """Busca usuário propagando o identificador de correlação no span."""

    correlation_id = getattr(request.state, "correlation_id", None)
    tracer = trace.get_tracer("app.users")

    with tracer.start_as_current_span("users.endpoint.get_user") as span:
        span.set_attribute("app.layer", "endpoint")
        span.set_attribute("http.route", "/users/{user_id}")
        span.set_attribute("http.method", request.method)
        span.set_attribute("app.user_id", user_id)
        if correlation_id is not None:
            span.set_attribute("app.correlation_id", correlation_id)

        return await service.get_user_response(
            user_id=user_id,
            correlation_id=correlation_id,
        )
```
