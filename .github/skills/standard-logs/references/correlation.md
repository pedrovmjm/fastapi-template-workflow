# Correlação Entre Logs, Traces e Erros

Use `correlation_id` para conectar requisição, logs e traces.

## Regras

- O middleware de correlação deve preencher `request.state.correlation_id`.
- Logs devem incluir `correlation_id` quando disponível.
- Traces devem incluir `app.correlation_id` quando disponível.
- Responses de erro seguem `standard-errors`; não adicione `correlation_id` no body sem mudar essa skill.
- Handlers globais registram `correlation_id` no log do console; o body `errors[]` permanece sem detalhe interno.
- Headers de resposta devem propagar `X-Correlation-Id`.

## Exemplo

```python
correlation_id = getattr(request.state, "correlation_id", None)
logger.exception(
    "Falha inesperada ao processar requisição.",
    extra={
        "event": "request.unexpected_error",
        "layer": "handler",
        "correlation_id": correlation_id,
    },
)
```
