---
name: standard-data-models
description: Padroniza contratos Pydantic em models por domínio, modelos de request/response, envelopes de response, meta, links, paginação, Field obrigatório e validações explícitas.
---
# Standard Data Models - Pydantic e Contratos HTTP

Use esta skill ao criar ou revisar modelos Pydantic, contratos HTTP, envelopes de response, metadados e modelos de paginação.

## Responsabilidade Desta Skill

Esta skill é dona de:

- organização de modelos Pydantic em `src/models/<dominio>/`;
- contratos compartilhados de resposta em `src/models/utils/`, como `meta` e `links`;
- separação de modelos de entrada e saída;
- uso obrigatório de `Field`;
- limites mínimos e máximos por tipo;
- envelopes de response com `data`, `meta` e `links`;
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

## Regras Obrigatórias

- Todos os modelos Pydantic públicos de contrato HTTP de um domínio devem ficar em `src/models/<dominio>/`.
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
- Separe arquivos/domínios apenas por intenção HTTP: request e response.
- Modelos de banco de dados devem ser internos e não podem ser retornados diretamente por endpoint.
- Modelos de banco de dados não devem carregar exemplos OpenAPI; exemplos pertencem aos modelos públicos de request/response.
- Não crie arquivos/domínios ou nomes públicos próprios baseados em `DataWrapper`, `Wrapper` ou `List`.
- Envelopes, listas e paginação que pertencem ao contrato de response devem ficar no arquivo de response do recurso, por exemplo `user_response.py`.

## Estrutura Recomendada

```text
src/
└── models/
    ├── users/
    │   ├── user_create_request.py
    │   └── user_response.py
    └── utils/
        ├── links.py
        └── meta.py
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

## Exemplo Completo de Envelope no Arquivo de Response

```python
from pydantic import BaseModel, ConfigDict, Field


class UserEnvelopeResponse(BaseModel):
    """Envelope de dados para resposta de usuário.

    Parameters
    ----------
    data : UserResponse
        Objeto principal retornado pela operação.

    Notes
    -----
    Use este envelope quando o endpoint retorna apenas o recurso principal,
    sem metadados de paginação, links ou lista de itens.
    Esta classe deve ficar no mesmo arquivo do contrato de response do
    recurso, por exemplo `user_response.py`.
    """

    model_config = ConfigDict(extra="forbid")

    data: UserResponse = Field(
        ...,
        description="Dados públicos do usuário retornado pela operação.",
    )
```

## Checklist

- [ ] O modelo está em `src/models/<dominio>/` ou, se compartilhado, em `src/models/utils/`.
- [ ] O arquivo/domínio diferencia apenas request e response.
- [ ] Todo campo usa `Field`.
- [ ] Todo campo tem descrição forte.
- [ ] Nenhuma metadata de query param foi colocada em `Field`.
- [ ] Strings possuem `min_length` e `max_length`.
- [ ] Números possuem limite inferior e superior.
- [ ] Responses não expõem dados sensíveis.
- [ ] Modelos internos de banco não vazam para endpoints.
- [ ] Exemplos OpenAPI ficam nos modelos públicos de request/response.
- [ ] Envelopes, listas e paginação de response ficam no arquivo `*_response.py` do recurso.
