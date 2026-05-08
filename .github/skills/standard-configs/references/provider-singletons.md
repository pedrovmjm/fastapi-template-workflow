# Provider Singletons

Use providers para criar e reutilizar clients técnicos.

## Regras

- Provider fica em `src/configs/{provider}.py`.
- Use lock assíncrono para evitar criação concorrente.
- Exponha função `get_*_client`.
- Exponha função `close_*_client` quando o client tiver fechamento.
- Não coloque regra de negócio no provider.

## Exemplo Genérico

```python
import asyncio


_client: ExternalClient | None = None
_client_lock = asyncio.Lock()


async def get_external_client(settings: Settings) -> ExternalClient:
    """Retorna singleton assíncrono do client externo.

    Parameters
    ----------
    settings : Settings
        Configurações finais da aplicação.

    Returns
    -------
    ExternalClient
        Client externo configurado.
    """

    global _client
    if _client is None:
        async with _client_lock:
            if _client is None:
                _client = ExternalClient(timeout=settings.external.timeout_seconds)

    return _client


async def close_external_client() -> None:
    """Fecha o singleton do client externo quando existir."""

    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
```
