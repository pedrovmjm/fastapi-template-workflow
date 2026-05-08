# Documentação Completa de Endpoint

Use este guia para endpoints com OpenAPI rico: request, response, erro e exemplos.

## Regras

- Todo endpoint deve declarar `response_model`.
- Todo endpoint deve declarar `status_code` quando não for o padrão.
- `responses` deve documentar respostas de sucesso adicionais, `204` e erros esperados.
- Exemplos de request pertencem ao modelo de request em `standard-data-models`, usando `Field(examples=...)` e `model_config.json_schema_extra`.
- Exemplos de response de sucesso pertencem ao modelo de response em `standard-data-models`, usando `Field(examples=...)` e `model_config.json_schema_extra`.
- Evite duplicar exemplos de sucesso em `Body(...)` ou em `responses.content` quando o modelo Pydantic já documenta o schema.
- Exemplos de erro devem seguir `standard-errors`.
- A docstring explica intenção e contrato do endpoint, não regra de negócio.

## Exemplo

```python
from fastapi import APIRouter, Depends, status

from src.models.common.data.error_response import ErrorResponse
from src.models.users.data.user_create_request import UserCreateRequest
from src.models.users.data.user_response import UserEnvelopeResponse
from src.services.users.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserEnvelopeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um usuário.",
    description="Cria um usuário e retorna seus dados públicos.",
    responses={
        201: {
            "description": "Usuário criado com sucesso.",
            "model": UserEnvelopeResponse,
        },
        409: {
            "description": "Usuário já existe.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [
                            {
                                "code": 409,
                                "title": "CONFLICT",
                                "message": "A operação conflita com o estado atual do recurso.",
                            }
                        ]
                    }
                }
            },
        },
    },
)
async def create_user(
    payload: UserCreateRequest,
    service: UserService = Depends(),
) -> UserEnvelopeResponse:
    """Cria um usuário e retorna o contrato público.

    Parameters
    ----------
    payload : UserCreateRequest
        Dados validados para criação do usuário.
    service : UserService
        Serviço responsável pela regra de criação.

    Returns
    -------
    UserEnvelopeResponse
        Envelope contendo o usuário criado.
    """

    user = await service.create_user(payload=payload)
    return UserEnvelopeResponse(data=user)
```
