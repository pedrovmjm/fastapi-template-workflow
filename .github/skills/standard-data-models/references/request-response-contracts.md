# Contratos Request e Response

Use modelos diferentes para entrada e saída. Requests expressam intenção do cliente. Responses expressam contrato público da API.

## Nomenclatura

- `UserCreateRequest`: entrada para criação.
- `UserUpdateRequest`: entrada para atualização total ou parcial quando definido.
- `UserResponse`: saída pública de um recurso.

Separe arquivos/domínios apenas por intenção HTTP:

- requests ficam em arquivos `*_request.py`;
- responses ficam em arquivos `*_response.py`;
- envelopes, listas e paginação que pertencem a response ficam no mesmo arquivo de response do recurso, por exemplo `user_response.py`;
- não crie arquivos/domínios ou nomes públicos separados como `data_wrapper_user_response.py`, `DataWrapperUserResponse`, `user_list_response.py` ou `UserListResponse`.

## Request de Criação

```python
from pydantic import BaseModel, ConfigDict, Field


class UserCreateRequest(BaseModel):
    """Representa os dados necessários para criar um usuário.

    Parameters
    ----------
    name : str
        Nome público do usuário.
    email : str
        Endereço eletrônico usado para contato e autenticação.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "Maria Oliveira",
                    "email": "maria.oliveira@example.com",
                }
            ]
        },
    )

    name: str = Field(
        ...,
        description="Nome público do usuário usado para exibição.",
        min_length=2,
        max_length=120,
        examples=["Maria Oliveira"],
    )
    email: str = Field(
        ...,
        description="Endereço eletrônico principal do usuário.",
        min_length=6,
        max_length=254,
        examples=["maria.oliveira@example.com"],
    )
```

## Response Público

```python
from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    """Representa os dados públicos de um usuário."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "usr_01HX7F9A4K8P2M6Q3R5S7T9V0W",
                    "status": "active",
                }
            ]
        },
    )

    id: str = Field(
        ...,
        description="Identificador único, estável e público do usuário.",
        min_length=1,
        max_length=64,
    )
    status: str = Field(
        ...,
        description="Estado operacional atual do usuário.",
        min_length=6,
        max_length=8,
        pattern="^(active|inactive|blocked)$",
    )
```

## Regras de Separação

- Request nunca deve herdar de Response só para reaproveitar campos.
- Response nunca deve conter senha, hash, token, segredo ou flags internas.
- Modelos de persistência não devem ser retornados diretamente por endpoint.
- Um service pode montar `UserResponse`, mas não deve montar `JSONResponse`.
- Um endpoint pode envelopar dados, mas não deve transformar entidade complexa manualmente.
- Quando o endpoint precisar de envelope ou coleção paginada, o modelo continua pertencendo ao domínio de response e deve ficar no arquivo `*_response.py` do recurso.
- Prefira nomes públicos terminados em `Response`, sem codificar `DataWrapper` ou `List` no nome do contrato.
- Mantenha contratos do domínio em `src/models/<dominio>/`; use `src/models/utils/` apenas para helpers compartilhados como `meta` e `links`.
