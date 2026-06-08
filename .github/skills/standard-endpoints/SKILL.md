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
- Todo `GET` com body (`200 OK`) deve retornar envelope com `data`, `meta` e `links`.
- `POST`, `PUT` e `PATCH` de sucesso retornam envelope com apenas `data`; `meta` e `links` não são retornados.
- Listagens paginadas devem retornar `data`, `meta` e `links`, com dados de paginação dentro de `meta` e links navegacionais quando aplicável.
- `meta` em `GET` deve seguir o padrão Open Finance: apenas campos de paginação.
- Paginação deve seguir contrato explícito com total, página, tamanho e total de páginas.
- Endpoints não devem conter regra de negócio; delegue para services.
- Use modelos de resposta Pydantic em `data`.
- Rotas `GET` devem usar o helper assíncrono compartilhado para montar `meta` e `links` dinamicamente a partir de `Request` e dados opcionais de paginação.
- Query params devem ser declarados dentro da assinatura do endpoint com `Query`, preferencialmente via `Annotated[..., Query(...)]`.
- Descrição, limites, exemplos e padrões de query params pertencem ao endpoint, porque dependem da intenção de negócio daquela rota; não coloque essa metadata em `Field` de modelo Pydantic.
- Retornos devem ser coerentes com OpenAPI por meio de `responses`.
- A definição de modelos, wrappers, `meta`, `links` e paginação pertence à skill `standard-data-models`; aqui apenas use esses contratos.
- Modelos de request e response usados em endpoints públicos devem trazer exemplos no próprio modelo Pydantic para completar a documentação do FastAPI.
- A definição de responses de erro pertence à skill `standard-errors`; aqui apenas declare os códigos esperados em `responses`.
- Endpoints públicos devem ter documentação completa com `summary`, `description`, `response_model`, `responses` e exemplos quando aplicável.
- Docstrings de rotas devem explicar a intenção de negócio do endpoint, o estado de negócio lido ou alterado e limites deliberados da operação.
- Endpoints operacionais isolados, como health check, não usam envelope Open Finance.

## Exemplo de Rotas

```python
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response, status

from src.models.users.requests.user_create_request import UserCreateRequest
from src.models.users.response.user_response import (
    UserCollectionResponse,
    UserCreatedResponse,
    UserEnvelopeResponse,
)
from src.models.utils.response_context import build_response_context
from src.services.users.user_service import UserService

router = APIRouter(tags=["users"])


@router.post(
    "/users",
    response_model=UserCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Usuário criado com sucesso."}},
)
async def create_user(
    payload: UserCreateRequest,
    service: UserService = Depends(),
) -> UserCreatedResponse:
    """Cria um usuário ativo a partir dos dados públicos recebidos.

    Este endpoint inicia o ciclo de vida de uma conta de usuário no domínio da
    aplicação. A regra de criação, validações de negócio e persistência ficam no
    service; a rota apenas recebe o contrato HTTP, delega a operação e devolve
    apenas o recurso criado em `data`.

    Parameters
    ----------
    payload : UserCreateRequest
        Dados validados para criação do usuário.
    service : UserService
        Serviço responsável pela regra de criação.

    Returns
    -------
    UserCreatedResponse
        Envelope contendo apenas o usuário criado.
    """

    user = await service.create_user(payload=payload)
    return UserCreatedResponse(data=user)


@router.get(
    "/users/{user_id}",
    response_model=UserEnvelopeResponse,
    response_model_exclude_none=True,
    responses={
        200: {"description": "Usuário encontrado."},
        204: {"description": "Usuário não encontrado."},
    },
)
async def get_user(
    request: Request,
    user_id: str,
    service: UserService = Depends(),
) -> UserEnvelopeResponse | Response:
    """Consulta a visão pública de um usuário pelo identificador.

    Este endpoint atende telas e integrações que precisam verificar o estado de
    uma conta já criada. Ele não altera dados de negócio e retorna `204` quando
    o identificador não representa um usuário disponível para exposição pública.

    Parameters
    ----------
    request : Request
        Requisição HTTP usada para montar links da resposta.
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

    response_context = await build_response_context(request=request)
    return UserEnvelopeResponse(
        data=user,
        meta=response_context.meta,
        links=response_context.links,
    )


@router.get(
    "/users",
    response_model=UserCollectionResponse,
    response_model_exclude_none=True,
    responses={200: {"description": "Lista paginada de usuários."}},
)
async def list_users(
    request: Request,
    page: Annotated[int, Query(ge=1, le=100_000, description="Página solicitada.")] = 1,
    page_size: Annotated[
        int,
        Query(ge=1, le=200, description="Quantidade de itens por página."),
    ] = 25,
    service: UserService = Depends(),
) -> UserCollectionResponse:
    """Lista usuários disponíveis para consulta operacional.

    Este endpoint entrega uma coleção paginada para telas de gestão e integrações
    de leitura. Ele preserva a ordenação e os filtros definidos pelo service,
    limita o tamanho da página na própria rota e monta links navegacionais a
    partir da URL recebida.

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

    users_page = await service.list_users(
        page=page,
        page_size=page_size,
    )
    response_context = await build_response_context(
        request=request,
        total_records=users_page.total_records,
        page=page,
        page_size=page_size,
    )
    return UserCollectionResponse(
        data=users_page.items,
        meta=response_context.meta,
        links=response_context.links,
    )
```

## Checklist

- [ ] `POST` retorna `201` com envelope contendo apenas `data`.
- [ ] `GET` de item retorna `200` ou `204`.
- [ ] Todo `GET` com body retorna `data`, `meta` e `links`.
- [ ] `meta` de `GET` contém apenas campos de paginação Open Finance.
- [ ] `meta` e `links` dos `GETs` são montados por helper assíncrono compartilhado.
- [ ] Endpoint é assíncrono, tipado e sem regra de negócio.
- [ ] Query params estão na assinatura do endpoint com `Query` e limites próprios da rota.
- [ ] `responses` documenta os códigos esperados.
- [ ] Documentação do endpoint inclui exemplos de sucesso e erro quando aplicável.
- [ ] Docstrings de rotas explicam a intenção de negócio, não apenas HTTP/path.
- [ ] Modelos Pydantic de request/response possuem exemplos para OpenAPI.
- [ ] Endpoints isolados, como health, não usam envelope Open Finance.
