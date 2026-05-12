# Envelopes, Meta, Links e Paginação

Use este guia para respostas inspiradas no padrão Open Finance: previsíveis, navegáveis e explícitas.

Envelopes, listas e paginação não criam domínio ou arquivo próprio. Quando
pertencem a um contrato de response, ficam no arquivo `*_response.py` do recurso,
por exemplo `user_response.py`. O nome público do contrato deve continuar
expressando response, sem codificar `DataWrapper` ou `List`.

Modelos reutilizáveis de `meta`, `links` e paginação compartilhada ficam em
`src/models/utils/`. Use essa pasta para contratos comuns entre domínios.
Rotas `GET` devem montar esses objetos com helper assíncrono compartilhado, por
exemplo `build_response_context`, para manter URL, versão de API, timezone e
paginação consistentes.

## Recurso Único

Use um envelope no arquivo de response do recurso para respostas com um único
recurso. Não crie arquivos ou classes como `data_wrapper_user_response.py` ou
`DataWrapperUserResponse`.

```python
from pydantic import BaseModel, ConfigDict, Field

from src.models.utils.links import ResponseLinks
from src.models.utils.meta import ResponseMeta


class UserEnvelopeResponse(BaseModel):
    """Envelope de dados para resposta de usuário.

    Notes
    -----
    Esta classe pertence ao contrato de response e deve ficar em
    `user_response.py`, junto do modelo `UserResponse`.
    """

    model_config = ConfigDict(extra="forbid")

    data: UserResponse = Field(
        ...,
        description="Dados públicos do usuário retornado pela operação.",
    )
    meta: ResponseMeta = Field(
        ...,
        description="Metadados públicos da resposta.",
    )
    links: ResponseLinks = Field(
        ...,
        description="Links públicos relacionados à resposta.",
    )
```

## Links

```python
from pydantic import BaseModel, ConfigDict, Field


class Links(BaseModel):
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

## Meta de Paginação

```python
from pydantic import BaseModel, ConfigDict, Field


class PaginationMeta(BaseModel):
    """Descreve a paginação da coleção retornada."""

    model_config = ConfigDict(extra="forbid")

    total_records: int = Field(
        ...,
        description="Quantidade total de registros disponíveis.",
        ge=0,
        le=1_000_000,
    )
    total_pages: int = Field(
        ...,
        description="Quantidade total de páginas disponíveis.",
        ge=0,
        le=100_000,
    )
    page: int = Field(
        ...,
        description="Página atual solicitada.",
        ge=1,
        le=100_000,
    )
    page_size: int = Field(
        ...,
        description="Quantidade máxima de itens por página.",
        ge=1,
        le=200,
    )
```

## Coleção Paginada

```python
from pydantic import BaseModel, ConfigDict, Field

from src.models.utils.links import Links
from src.models.utils.pagination_meta import PaginationMeta


class UserCollectionResponse(BaseModel):
    """Envelope de dados para resposta de listagem de usuários.

    Notes
    -----
    Esta classe pertence ao contrato de response e deve ficar em
    `user_response.py`, junto do modelo `UserResponse`.
    """

    model_config = ConfigDict(extra="forbid")

    data: list[UserResponse] = Field(
        ...,
        description="Lista de usuários da página atual.",
        min_length=0,
        max_length=200,
    )
    meta: PaginationMeta = Field(
        ...,
        description="Metadados de paginação da coleção.",
    )
    links: Links = Field(
        ...,
        description="Links navegacionais da coleção.",
    )
```



## Regras de Status HTTP Relacionadas

- `GET` com `200 OK` retorna `data`, `meta` e `links`, mesmo quando a resposta não é paginada.
- `GET` de item sem dados retorna `204` sem body.
- `GET` de coleção retorna `200` com `data=[]` quando a coleção está vazia e retornando links e meta válidos.
- `POST` de criação retorna `201` com envelope de response no arquivo `*_response.py` do recurso.
- A definição dos códigos HTTP pertence à skill `standard-endpoints`.
