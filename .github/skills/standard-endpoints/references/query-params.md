# Query Params e Paginação

Use query params tipados, limitados e documentados.

## Regras

- Todo query param numérico deve ter `ge` e `le`.
- `page` começa em `1`.
- `page_size` deve ter limite superior para proteger a API.
- Filtros string devem ter `min_length` e `max_length` quando possível.
- Ordenação deve ter vocabulário fechado.
- Listagens devem retornar contrato definido em `standard-data-models`.

## Exemplo

```python
from fastapi import APIRouter, Depends, Query, Request

from src.models.users.data.user_response import UserCollectionResponse
from src.services.users.user_service import UserService

router = APIRouter( tags=["users"]) 


@router.get("/users", response_model=UserCollectionResponse)
async def list_users(
    request: Request,
    page: int = Query(1, ge=1, le=100_000, description="Página solicitada."),
    page_size: int = Query(25, ge=1, le=200, description="Quantidade de itens por página."),
    status: str | None = Query(
        None,
        min_length=6,
        max_length=8,
        pattern="^(active|inactive|blocked)$",
        description="Filtro opcional por estado operacional do usuário.",
    ),
    service: UserService = Depends(),
) -> UserCollectionResponse:
    """Lista usuários com paginação e filtros opcionais."""

    return await service.list_users(
        base_url=str(request.url),
        page=page,
        page_size=page_size,
        status=status,
    )
```
