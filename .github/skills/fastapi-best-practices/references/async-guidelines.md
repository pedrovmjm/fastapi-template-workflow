# Regras Assíncronas

Use async para I/O e orquestração. Evite async decorativo que só embrulha código bloqueante.

## Regras

- Endpoints, services, repositories e middlewares devem ser assíncronos.
- Use clientes assíncronos para banco, HTTP, cache e filas.
- Use `asyncio.gather` para operações independentes.
- Use `asyncio.create_task` quando precisar iniciar tarefas antes de aguardar.
- Cancele ou aguarde tarefas criadas manualmente.
- Não chame bibliotecas bloqueantes em fluxo async sem adaptação.
- Para CPU pesado, use worker externo, fila ou executor controlado.

## Exemplo

```python
import asyncio


async def load_user_summary(user_id: str) -> UserSummaryResponse:
    """Carrega dados independentes do resumo do usuário em paralelo.

    Parameters
    ----------
    user_id : str
        Identificador público do usuário.

    Returns
    -------
    UserSummaryResponse
        Resumo consolidado do usuário.
    """

    profile_task = asyncio.create_task(get_profile(user_id=user_id))
    permissions_task = asyncio.create_task(get_permissions(user_id=user_id))
    metrics_task = asyncio.create_task(get_metrics(user_id=user_id))

    profile, permissions, metrics = await asyncio.gather(
        profile_task,
        permissions_task,
        metrics_task,
    )
    return UserSummaryResponse(
        profile=profile,
        permissions=permissions,
        metrics=metrics,
    )
```
