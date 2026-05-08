# Atributos Seguros em Traces

Use atributos para diagnóstico sem expor dados sensíveis.

## Permitido

- `app.layer`
- `app.operation`
- `app.result`
- `app.correlation_id`
- identificadores públicos não sensíveis;
- contagens;
- duração;
- nome de provider externo;
- status HTTP.

## Proibido

- token;
- senha;
- API key;
- documento;
- cartão;
- payload completo;
- header `Authorization`;
- SQL com valores sensíveis.

## Exemplo

```python
span.set_attribute("app.layer", "service")
span.set_attribute("app.operation", "create_user")
span.set_attribute("app.result", "created")
span.set_attribute("app.correlation_id", correlation_id)
```
