# Padrões de Router

Use routers pequenos, coesos e orientados a recurso.

## Regras

- Um módulo de rota deve representar um recurso ou capacidade principal.
- O prefixo deve ser plural quando representa coleção: `/users`, `/accounts`.
- `tags` deve ser estável e curta.
- Endpoint não deve montar entidade manualmente quando isso pertence ao service.
- Endpoint pode montar wrapper final quando o service retorna o modelo de dados.
- Dependências devem entrar por `Depends`.
- Não coloque configuração global de aplicação dentro do arquivo de rota.

## Exemplo

```python
from fastapi import APIRouter, Depends, status

from src.models.users.data.user_create_request import UserCreateRequest
from src.models.users.data.user_response import UserEnvelopeResponse
from src.services.users.user_service import UserService

router = APIRouter( tags=["users"])


@router.post(
    "/users",
    response_model=UserEnvelopeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: UserCreateRequest,
    service: UserService = Depends(),
) -> UserEnvelopeResponse:
    """Cria um usuário e retorna o contrato público."""

    user = await service.create_user(payload=payload)
    return UserEnvelopeResponse(data=user)
```
