# Orquestração Assíncrona no Domínio

Use `asyncio` para coordenar I/O independente sem transformar o código em uma fila invisível de tarefas soltas.

## Quando Usar `asyncio.gather`

Use quando as operações:

- são independentes;
- podem falhar como parte da mesma operação maior;
- precisam terminar antes de montar a resposta final.

```python
import asyncio


async def load_user_context(user_id: str) -> UserContext:
    """Carrega contexto de usuário com consultas independentes.

    Parameters
    ----------
    user_id : str
        Identificador público do usuário.

    Returns
    -------
    UserContext
        Contexto consolidado para execução do caso de uso.
    """

    profile_task = asyncio.create_task(get_profile(user_id=user_id))
    permissions_task = asyncio.create_task(get_permissions(user_id=user_id))
    sessions_task = asyncio.create_task(count_sessions(user_id=user_id))

    profile, permissions, sessions = await asyncio.gather(
        profile_task,
        permissions_task,
        sessions_task,
    )
    return UserContext(
        profile=profile,
        permissions=permissions,
        sessions=sessions,
    )
```

## Quando Evitar Paralelismo

Evite paralelizar quando:

- a segunda operação depende do resultado da primeira;
- a ordem representa uma regra de negócio;
- a concorrência aumenta chance de conflito transacional;
- o custo de abrir tarefas é maior que o ganho;
- a operação usa biblioteca bloqueante.

## Regras de Segurança

- Toda task criada deve ser aguardada ou cancelada.
- Não esconda exceções com `return_exceptions=True` sem mapear o resultado.
- Não use `create_task` para trabalho em background crítico sem fila, retry e observabilidade.
- Para processamento longo, prefira fila externa ou worker dedicado.
