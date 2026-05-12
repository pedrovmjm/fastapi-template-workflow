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
import logging

from fastapi import APIRouter, Depends, Request, status
from opentelemetry import trace

from src.models.users.user_create_request import UserCreateRequest
from src.models.users.user_response import UserEnvelopeResponse
from src.services.users.user_service import UserService

router = APIRouter(tags=["users"])
logger = logging.getLogger("app.routes.users")
tracer = trace.get_tracer("app.routes.users")


@router.post(
    "/users",
    response_model=UserEnvelopeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: Request,
    payload: UserCreateRequest,
    service: UserService = Depends(),
) -> UserEnvelopeResponse:
    """Cria um usuário ativo a partir dos dados públicos recebidos.

    Este endpoint inicia o ciclo de vida de uma conta de usuário. A rota recebe
    o contrato HTTP, delega regras de negócio para o service e devolve o
    envelope público criado.
    """

    correlation_id = getattr(request.state, "correlation_id", None)
    with tracer.start_as_current_span("users.endpoint.create_user") as span:
        span.set_attribute("app.layer", "endpoint")
        span.set_attribute("app.operation", "create_user")
        if correlation_id is not None:
            span.set_attribute("app.correlation_id", correlation_id)

        logger.info(
            "Criação de usuário recebida.",
            extra={
                "event": "user_create.request_received",
                "layer": "endpoint",
                "correlation_id": correlation_id,
            },
        )
        user = await service.create_user(
            payload=payload,
            correlation_id=correlation_id,
        )
        span.set_attribute("app.result", "created")
        logger.info(
            "Criação de usuário respondida.",
            extra={
                "event": "user_create.request_succeeded",
                "layer": "endpoint",
                "user_id": user.id,
                "correlation_id": correlation_id,
            },
        )
        return UserEnvelopeResponse(data=user)
```
