# Query Params e Paginação

Use query params tipados, limitados e documentados.

## Regras

- Todo query param numérico deve ter `ge` e `le`.
- Query params devem ficar na assinatura do endpoint com `Query`, preferencialmente via `Annotated[..., Query(...)]`.
- Descrição, limites, exemplos e `pattern` de query params dependem da intenção de negócio da rota; não mova essa metadata para `Field` de modelo Pydantic.
- `page` começa em `1`.
- `page_size` deve ter limite superior para proteger a API.
- Filtros string devem ter `min_length` e `max_length` quando possível.
- Ordenação deve ter vocabulário fechado.
- Listagens devem retornar contrato definido em `standard-data-models`.

## Exemplo

```python
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from src.models.users.user_response import UserCollectionResponse
from src.services.users.user_service import UserService

router = APIRouter(tags=["users"])


@router.get("/users", response_model=UserCollectionResponse)
async def list_users(
    request: Request,
    page: Annotated[int, Query(ge=1, le=100_000, description="Página solicitada.")] = 1,
    page_size: Annotated[
        int,
        Query(ge=1, le=200, description="Quantidade de itens por página."),
    ] = 25,
    status: Annotated[
        str | None,
        Query(
            min_length=6,
            max_length=8,
            pattern="^(active|inactive|blocked)$",
            description="Filtro opcional por estado operacional do usuário.",
        ),
    ] = None,
    service: UserService = Depends(),
) -> UserCollectionResponse:
    """Lista usuários disponíveis para consulta operacional.

    Este endpoint atende telas e integrações de leitura paginada, preservando
    filtros e limites definidos para a consulta pública de usuários.
    """

    return await service.list_users(
        base_url=str(request.url),
        page=page,
        page_size=page_size,
        status=status,
    )
```
