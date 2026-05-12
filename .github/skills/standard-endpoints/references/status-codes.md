# Status Codes e Respostas Vazias

Use status codes de forma previsível para reduzir ambiguidade no contrato da API.

## Regras

- `POST` de criação retorna `201 Created`.
- `GET` de item retorna `200 OK` quando o recurso existe.
- `GET` de item retorna `204 No Content` quando o recurso não existe e essa ausência é um resultado esperado.
- `GET` de coleção retorna `200 OK`, mesmo quando `data=[]`.
- `204` não deve ter body.
- Erros de validação de payload ficam em `422`, respeitando o padrão do FastAPI, salvo decisão explícita do projeto.

## Exemplo de `GET` com `204`

```python
from fastapi import APIRouter, Depends, Response, status

from src.models.users.user_response import UserEnvelopeResponse
from src.services.users.user_service import UserService

router = APIRouter(tags=["users"])


@router.get(
    "/users/{user_id}",
    response_model=UserEnvelopeResponse,
    responses={
        200: {"description": "Usuário encontrado."},
        204: {"description": "Usuário não encontrado."},
    },
)
async def get_user(
    user_id: str,
    service: UserService = Depends(),
) -> UserEnvelopeResponse | Response:
    """Consulta a visão pública de um usuário pelo identificador.

    Este endpoint atende leituras de estado de uma conta já criada e retorna
    `204` quando o identificador não representa um usuário disponível para
    exposição pública.
    """

    user = await service.get_user_response(user_id=user_id)
    if user is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return UserEnvelopeResponse(data=user)
```
