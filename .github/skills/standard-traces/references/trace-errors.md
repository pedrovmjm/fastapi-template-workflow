# Erros em Traces

Use spans para registrar falhas sem engolir exceções.

## Regras

- Use `span.record_exception(error)` para exceções relevantes.
- Use status `ERROR` quando a operação falhar.
- Relance a exceção depois de registrar no span.
- Não coloque payload sensível como atributo.
- O contrato HTTP do erro pertence a `standard-errors`.

## Exemplo

```python
from opentelemetry.trace import Status, StatusCode


try:
    result = await repository.get_by_id(user_id=user_id)
except Exception as error:
    span.record_exception(error)
    span.set_status(Status(StatusCode.ERROR, type(error).__name__))
    raise
```
