---
name: standard-endpoints
description: Padroniza endpoints FastAPI assíncronos, tipados, com códigos HTTP previsíveis e envelope inspirado em Open Finance para data, meta, links e paginação.
---
# Standard Endpoints - FastAPI e Open Finance

Use esta skill ao criar ou revisar rotas FastAPI.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar status codes e respostas vazias. | [Status codes e respostas vazias](references/status-codes.md) |
| Quando precisar aprofundar padrões de router. | [Padrões de router](references/router-patterns.md) |
| Quando precisar aprofundar query params e paginação. | [Query params e paginação](references/query-params.md) |
| Quando precisar aprofundar documentação completa de endpoint. | [Documentação completa de endpoint](references/endpoint-documentation.md) |
| Quando precisar definir request/response models com exemplos para OpenAPI. | Use `standard-data-models`, especialmente `references/request-response-contracts.md` |

## Regras Obrigatórias

- Endpoints devem ser `async def` e totalmente tipados.
- `POST` de criação deve retornar `201 Created`.
- `GET` de item deve retornar `200 OK` quando houver dados e `204 No Content` quando não houver dados.
- Listagens devem retornar envelope com `data`, `meta` e `links`.
- Paginação deve seguir contrato explícito com total, página, tamanho e total de páginas.
- Endpoints não devem conter regra de negócio; delegue para services.
- Use modelos de resposta Pydantic em `data`.
- Retornos devem ser coerentes com OpenAPI por meio de `responses`.
- A definição de modelos, wrappers, `meta`, `links` e paginação pertence à skill `standard-data-models`; aqui apenas use esses contratos.
- Modelos de request e response usados em endpoints públicos devem trazer exemplos no próprio modelo Pydantic para completar a documentação do FastAPI.
- A definição de responses de erro pertence à skill `standard-errors`; aqui apenas declare os códigos esperados em `responses`.
- Endpoints públicos devem ter documentação completa com `summary`, `description`, `response_model`, `responses` e exemplos quando aplicável.

## Exemplo de Rotas

```python
from fastapi import APIRouter, Depends, Query, Request, Response, status

from src.models.users.data.user_create_request import UserCreateRequest
from src.models.users.data.user_response import UserCollectionResponse, UserEnvelopeResponse
from src.services.users.user_service import UserService

router = APIRouter(tags=["users"])


@router.post(
    "/users",
    response_model=UserEnvelopeResponse,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Usuário criado com sucesso."}},
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
    """Retorna um usuário pelo identificador público.

    Parameters
    ----------
    user_id : str
        Identificador público do usuário.
    service : UserService
        Serviço responsável pela consulta.

    Returns
    -------
    UserEnvelopeResponse | Response
        `200` com dados quando encontrado ou `204` sem corpo.
    """

    user = await service.get_user_response(user_id=user_id)
    if user is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return UserEnvelopeResponse(data=user)


@router.get(
    "/users",
    response_model=UserCollectionResponse,
    responses={200: {"description": "Lista paginada de usuários."}},
)
async def list_users(
    request: Request,
    page: int = Query(1, ge=1, le=100_000, description="Página solicitada."),
    page_size: int = Query(25, ge=1, le=200, description="Quantidade de itens por página."),
    service: UserService = Depends(),
) -> UserCollectionResponse:
    """Lista usuários com paginação e links navegacionais.

    Parameters
    ----------
    request : Request
        Requisição HTTP usada para montar links absolutos.
    page : int
        Página solicitada.
    page_size : int
        Quantidade máxima de itens por página.
    service : UserService
        Serviço responsável pela listagem.

    Returns
    -------
    UserCollectionResponse
        Envelope paginado com `data`, `meta` e `links`.
    """

    return await service.list_users(
        base_url=str(request.url.include_query_params()),
        page=page,
        page_size=page_size,
    )
```

## Checklist

- [ ] `POST` retorna `201`.
- [ ] `GET` de item retorna `200` ou `204`.
- [ ] Listas retornam `data`, `meta` e `links`.
- [ ] Endpoint é assíncrono, tipado e sem regra de negócio.
- [ ] Query params possuem limites mínimos e máximos.
- [ ] `responses` documenta os códigos esperados.
- [ ] Documentação do endpoint inclui exemplos de sucesso e erro quando aplicável.
- [ ] Modelos Pydantic de request/response possuem exemplos para OpenAPI.
