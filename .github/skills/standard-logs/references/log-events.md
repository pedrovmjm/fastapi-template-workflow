# Eventos de Log

Use eventos estáveis para que logs sejam filtráveis e úteis em incidentes.

## Regras

- Todo log estruturado deve conter `event`.
- Todo log estruturado deve conter `layer`.
- O nome do evento deve seguir `dominio.acao` ou `camada.resultado`.
- Eventos devem ser estáveis; não renomeie sem motivo.
- Mensagens podem mudar, mas `event` deve permanecer compatível.
- A mensagem deve complementar o `event` com contexto de negócio legível; veja [Mensagens orientadas ao negócio](log-messages.md).

## Exemplos

```python
logger.info(
    "Usuário criado com sucesso.",
    extra={
        "event": "user.created",
        "layer": "service",
        "user_id": user_id,
        "correlation_id": correlation_id,
    },
)
```

```python
logger.warning(
    "Dependência externa respondeu com atraso.",
    extra={
        "event": "external.timeout",
        "layer": "integration",
        "provider": "payments",
        "timeout_ms": 3000,
        "correlation_id": correlation_id,
    },
)
```
