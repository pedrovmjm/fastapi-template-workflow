---
name: standard-data-models
description: Padroniza contratos Pydantic em models por domínio, modelos de request/response, envelopes de response, meta, links, paginação, Field obrigatório e validações explícitas.
---
# Standard Data Models - Pydantic e Contratos HTTP

Use esta skill ao criar ou revisar modelos Pydantic, contratos HTTP, envelopes de response, metadados e modelos de paginação.

## Responsabilidade Desta Skill

Esta skill é dona de:

- organização de modelos Pydantic em `src/models/<dominio>/{requests,response,persistence,commons}/`;
- contratos compartilhados de resposta em `src/models/utils/`, como `meta` e `links`;
- separação de modelos de entrada e saída;
- uso obrigatório de `Field`;
- limites mínimos e máximos por tipo;
- envelopes de response com `data`, `meta` e `links` em rotas `GET`;
- envelopes de mutação com apenas `data` em rotas `POST`, `PUT` e `PATCH`;
- modelos de paginação inspirados em Open Finance;
- exemplos de request e response;
- fronteira entre modelos públicos Pydantic e modelos internos de persistência.

Esta skill não é dona de:

- regras de endpoint, códigos HTTP e `APIRouter`: use `standard-endpoints`;
- contratos públicos de erro: use `standard-errors`;
- regra de negócio, services e repositories: use `domain`;
- formato de docstring: use `standard-docstrings`;
- logs, traces e middlewares: use as skills específicas.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando definir validação e documentação de campos Pydantic. | [Regras de campos Pydantic](references/field-rules.md) |
| Quando separar modelos de entrada e saída HTTP. | [Contratos request e response](references/request-response-contracts.md) |
| Quando montar envelopes públicos com data, meta, links ou paginação. | [Envelopes, meta, links e paginação](references/open-finance-envelope.md) |
| Quando definir modelos de dados usados pelo banco de dados. | [Modelos de dados e persistência](references/persistence-data-models.md) |

## Estrutura por Domínio

Cada domínio em `src/models/<dominio>/` deve usar subpastas por intenção:

| Subpasta | Conteúdo |
| --- | --- |
| `requests/` | Modelos `*_request.py` de entrada HTTP. |
| `response/` | Modelos `*_response.py`, envelopes de `GET` e envelopes de mutação com apenas `data`. |
| `persistence/` | Modelos internos de banco, documentos e registros persistidos. |
| `commons/` | Tipos compartilhados do domínio que não são request, response nem persistência. |

Contratos reutilizáveis entre domínios, como `meta`, `links` e helpers de montagem, ficam em `src/models/utils/`.

Endpoints operacionais isolados, como health check, podem ter contrato próprio em `src/models/<capacidade>/response/` sem envelope Open Finance.

## Regras Obrigatórias

- Todo modelo Pydantic público de contrato HTTP deve ficar em `src/models/<dominio>/{requests,response}/`.
- Modelos de persistência devem ficar em `src/models/<dominio>/persistence/`.
- Tipos compartilhados do domínio devem ficar em `src/models/<dominio>/commons/`.
- Contratos compartilhados de `meta`, `links` e helpers reutilizáveis devem ficar em `src/models/utils/`.
- Não crie pacote intermediário `data` dentro do domínio, salvo quando uma feature justificar explicitamente essa fronteira extra.
- Um arquivo deve conter preferencialmente um modelo público principal.
- Todo campo deve usar `Field`.
- Todo `Field` deve ter `description` clara, forte e orientada a contrato.
- `Field` descreve campos de modelos Pydantic de request/response; metadata de query params de rota deve ficar no endpoint com `Query`.
- Campos `str` devem ter `min_length` e `max_length`.
- Campos `int` e `float` devem ter `ge`/`gt` e `le`/`lt`, exceto quando houver justificativa documentada.
- Campos opcionais devem explicar quando podem ser `None`.
- Modelos públicos devem usar `ConfigDict(extra="forbid")`.
- Modelos com strings devem usar `str_strip_whitespace=True`, salvo quando espaços forem parte do valor.
- Não exponha campos sensíveis em responses.
- Requests e responses devem ser modelos diferentes.
- Modelos de banco de dados devem ser internos e não podem ser retornados diretamente por endpoint.
- Modelos de banco de dados não devem carregar exemplos OpenAPI; exemplos pertencem aos modelos públicos de request/response.
- Não crie arquivos/domínios ou nomes públicos próprios baseados em `DataWrapper`, `Wrapper` ou `List`.
- Envelopes, listas e paginação que pertencem ao contrato de response devem ficar em `src/models/<dominio>/response/*_response.py`.
- Envelopes usados por `GET` devem incluir `data`, `meta` e `links`, inclusive para recurso único não paginado.
- `meta` em `GET` deve seguir o padrão Open Finance: apenas campos de paginação (`total_records`, `total_pages`, `page`, `page_size`). Não inclua metadados operacionais da aplicação em `meta`.
- `POST`, `PUT` e `PATCH` de sucesso retornam envelope com apenas `data`; `meta` e `links` não são retornados nessas operações.
- A montagem dinâmica de `meta` e `links` em rotas `GET` deve usar helper assíncrono compartilhado em `src/models/utils/`.

## Estrutura Recomendada

```text
src/
└── models/
    ├── users/
    │   ├── requests/
    │   │   └── user_create_request.py
    │   ├── response/
    │   │   └── user_create_response.py
    │   ├── persistence/
    │   │   └── user_record.py
    │   └── commons/
    │       └── user_status.py
    ├── health/
    │   └── response/
    │       └── health_response.py
    └── utils/
        ├── links.py
        ├── meta.py
        └── response_context.py
```

## Exemplo Completo de `UserResponse`

```python
from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    """Representa a resposta pública de um usuário.

    Parameters
    ----------
    id : str
        Identificador único, estável e público do usuário.
    status : str
        Estado operacional atual do usuário.

    Notes
    -----
    Este modelo deve conter apenas dados seguros para resposta HTTP.
    Informações sensíveis, credenciais e metadados internos não devem
    ser adicionados aqui.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(
        ...,
        description="Identificador único, estável e público do usuário.",
        min_length=1,
        max_length=64,
        examples=["usr_01HX7F9A4K8P2M6Q3R5S7T9V0W"],
    )
    status: str = Field(
        ...,
        description="Estado operacional atual do usuário dentro do ciclo de vida da conta.",
        min_length=6,
        max_length=8,
        pattern="^(active|inactive|blocked)$",
        examples=["active"],
    )
```

## Exemplo Completo de Envelope de `GET`

```python
from pydantic import BaseModel, ConfigDict, Field

from src.models.utils.links import ResponseLinks
from src.models.utils.meta import ResponseMeta


class UserEnvelopeResponse(BaseModel):
    """Envelope de leitura para resposta de usuário.

    Parameters
    ----------
    data : UserResponse
        Objeto principal retornado pela operação.
    meta : ResponseMeta
        Metadados de paginação.
    links : ResponseLinks
        Links públicos relacionados à resposta.

    Notes
    -----
    Use este envelope em rotas `GET`. Em leituras não paginadas, `meta`
    permanece presente com campos de paginação ausentes ou `None`.
    Esta classe deve ficar em `src/models/users/response/user_response.py`.
    """

    model_config = ConfigDict(extra="forbid")

    data: UserResponse = Field(
        ...,
        description="Dados públicos do usuário retornado pela operação.",
    )
    meta: ResponseMeta = Field(
        ...,
        description="Metadados de paginação.",
    )
    links: ResponseLinks = Field(
        ...,
        description="Links públicos relacionados à resposta.",
    )
```

## Exemplo de Envelope de Mutação (`POST`)

```python
from pydantic import BaseModel, ConfigDict, Field


class UserCreatedResponse(BaseModel):
    """Envelope de criação sem meta nem links.

    Notes
    -----
    Rotas `POST`, `PUT` e `PATCH` retornam apenas `data`.
    """

    model_config = ConfigDict(extra="forbid")

    data: UserResponse = Field(
        ...,
        description="Recurso criado ou alterado pela operação.",
    )
```

## Checklist

- [ ] O modelo está em `src/models/<dominio>/{requests,response,persistence,commons}/` ou, se compartilhado, em `src/models/utils/`.
- [ ] Requests ficam em `requests/`; responses e envelopes ficam em `response/`.
- [ ] Todo campo usa `Field`.
- [ ] Todo campo tem descrição forte.
- [ ] Nenhuma metadata de query param foi colocada em `Field`.
- [ ] Strings possuem `min_length` e `max_length`.
- [ ] Números possuem limite inferior e superior.
- [ ] Responses não expõem dados sensíveis.
- [ ] Envelopes de `GET` incluem `data`, `meta` e `links`.
- [ ] `meta` de `GET` contém apenas campos de paginação Open Finance.
- [ ] `POST`, `PUT` e `PATCH` retornam apenas `data`, sem `meta` nem `links`.
- [ ] `meta` e `links` de `GET` são montados por helper assíncrono compartilhado.
- [ ] Modelos internos de banco não vazam para endpoints.
- [ ] Exemplos OpenAPI ficam nos modelos públicos de request/response.
- [ ] Endpoints isolados, como health, não usam envelope Open Finance.
