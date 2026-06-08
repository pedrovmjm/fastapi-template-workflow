# Envelopes, Meta, Links e Paginação

Use este guia para respostas inspiradas no padrão Open Finance: previsíveis, navegáveis e explícitas.

Envelopes, listas e paginação não criam domínio ou arquivo próprio. Quando
pertencem a um contrato de response, ficam em `src/models/<dominio>/response/*_response.py`.
O nome público do contrato deve continuar expressando response, sem codificar
`DataWrapper` ou `List`.

Modelos reutilizáveis de `meta`, `links` e helpers de montagem ficam em
`src/models/utils/`. Rotas `GET` devem montar esses objetos com helper assíncrono
compartilhado, por exemplo `build_response_context`, para manter URL e paginação
consistentes.

## Regra por Verbo HTTP

| Verbo | Envelope | `meta` | `links` |
| --- | --- | --- | --- |
| `GET` | `data`, `meta`, `links` | Sim, padrão Open Finance | Sim |
| `POST`, `PUT`, `PATCH` | apenas `data` | Não | Não |

Endpoints operacionais isolados, como health check, não seguem este envelope.

## Recurso Único em `GET`

Use um envelope no arquivo de response do recurso para respostas com um único
recurso. Não crie arquivos ou classes como `data_wrapper_user_response.py` ou
`DataWrapperUserResponse`.

```python
from pydantic import BaseModel, ConfigDict, Field

from src.models.utils.links import ResponseLinks
from src.models.utils.meta import ResponseMeta


class UserEnvelopeResponse(BaseModel):
    """Envelope de leitura para resposta de usuário.

    Notes
    -----
    Esta classe pertence ao contrato de response e deve ficar em
    `src/models/users/response/user_response.py`, junto do modelo `UserResponse`.
    """

    model_config = ConfigDict(extra="forbid")

    data: UserResponse = Field(
        ...,
        description="Dados públicos do usuário retornado pela operação.",
    )
    meta: ResponseMeta = Field(
        ...,
        description="Metadados de paginação no padrão Open Finance.",
    )
    links: ResponseLinks = Field(
        ...,
        description="Links públicos relacionados à resposta.",
    )
```

## Mutação em `POST`

Rotas de criação ou alteração retornam apenas o recurso em `data`:

```python
from pydantic import BaseModel, ConfigDict, Field


class UserCreatedResponse(BaseModel):
    """Envelope de criação sem meta nem links."""

    model_config = ConfigDict(extra="forbid")

    data: UserResponse = Field(
        ...,
        description="Usuário criado pela operação.",
    )
```

## Meta Open Finance

`meta` contém apenas campos de paginação. Não inclua nome da aplicação, versão,
timezone ou outros metadados operacionais.

```python
from pydantic import BaseModel, ConfigDict, Field


class ResponseMeta(BaseModel):
    """Descreve metadados de paginação no padrão Open Finance."""

    model_config = ConfigDict(extra="forbid")

    total_records: int | None = Field(
        None,
        description="Quantidade total de registros disponíveis; ausente quando a resposta não é paginada.",
        ge=0,
        le=1_000_000,
    )
    total_pages: int | None = Field(
        None,
        description="Quantidade total de páginas disponíveis; ausente quando a resposta não é paginada.",
        ge=0,
        le=100_000,
    )
    page: int | None = Field(
        None,
        description="Página atual solicitada; ausente quando a resposta não é paginada.",
        ge=1,
        le=100_000,
    )
    page_size: int | None = Field(
        None,
        description="Quantidade máxima de itens por página; ausente quando a resposta não é paginada.",
        ge=1,
        le=200,
    )
```

Em listagens paginadas, os quatro campos devem estar presentes. Em leituras de
item único, `meta` permanece no envelope, mas os campos de paginação ficam
ausentes ou `None` e podem ser omitidos com `response_model_exclude_none=True`.

## Links

```python
from pydantic import BaseModel, ConfigDict, Field


class ResponseLinks(BaseModel):
    """Representa links navegacionais da resposta."""

    model_config = ConfigDict(extra="forbid")

    self: str = Field(
        ...,
        description="URL canônica do recurso atual.",
        min_length=1,
        max_length=2048,
    )
    first: str | None = Field(
        None,
        description="URL da primeira página; ausente quando a resposta não é paginada.",
        max_length=2048,
    )
    prev: str | None = Field(
        None,
        description="URL da página anterior; ausente quando não existe página anterior.",
        max_length=2048,
    )
    next: str | None = Field(
        None,
        description="URL da próxima página; ausente quando não existe próxima página.",
        max_length=2048,
    )
    last: str | None = Field(
        None,
        description="URL da última página; ausente quando a resposta não é paginada.",
        max_length=2048,
    )
```

## Coleção Paginada

```python
from pydantic import BaseModel, ConfigDict, Field

from src.models.utils.links import ResponseLinks
from src.models.utils.meta import ResponseMeta


class UserCollectionResponse(BaseModel):
    """Envelope de dados para resposta de listagem de usuários.

    Notes
    -----
    Esta classe pertence ao contrato de response e deve ficar em
    `src/models/users/response/user_response.py`, junto do modelo `UserResponse`.
    """

    model_config = ConfigDict(extra="forbid")

    data: list[UserResponse] = Field(
        ...,
        description="Lista de usuários da página atual.",
        min_length=0,
        max_length=200,
    )
    meta: ResponseMeta = Field(
        ...,
        description="Metadados de paginação da coleção no padrão Open Finance.",
    )
    links: ResponseLinks = Field(
        ...,
        description="Links navegacionais da coleção.",
    )
```

## Regras de Status HTTP Relacionadas

- `GET` com `200 OK` retorna `data`, `meta` e `links`.
- `GET` de item sem dados retorna `204` sem body.
- `GET` de coleção retorna `200` com `data=[]` quando a coleção está vazia, mantendo `meta` e `links` válidos.
- `POST` de criação retorna `201` com envelope contendo apenas `data`.
- A definição dos códigos HTTP pertence à skill `standard-endpoints`.
