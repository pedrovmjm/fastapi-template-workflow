# Modelos de Dados e Persistência

Use este guia quando precisar definir modelos usados para representar dados do banco, entidades internas ou documentos de persistência.

## Regra Geral

Modelos de banco descrevem armazenamento e invariantes técnicas. Modelos de request/response descrevem o contrato público da API.

Eles não devem ser o mesmo modelo.

## Responsabilidade

- Modelos de request validam a entrada HTTP.
- Modelos de response expõem dados seguros para clientes.
- Modelos de persistência representam tabelas, documentos, campos internos, chaves, timestamps técnicos e tipos específicos do banco.
- Repositories convertem dados do banco para entidades internas ou modelos esperados pelo service.
- Services podem montar modelos públicos de response a partir de entidades internas, mas não devem expor ORM ou documento cru.

## Regras

- Não retorne modelo ORM, documento MongoDB ou entidade interna diretamente em endpoint.
- Não use modelo de request como entidade de banco.
- Não use modelo de response como entidade de banco.
- Não inclua `_id`, `ObjectId`, campos de versão, locks, hashes, tokens, flags internas ou metadados técnicos em response pública.
- Não coloque exemplos OpenAPI em modelos de persistência.
- Coloque `json_schema_extra` e `Field(examples=...)` apenas em modelos públicos de request/response.
- Validações de contrato HTTP pertencem aos modelos públicos; constraints e índices pertencem ao banco e à skill `standard-database`.
- Conversões entre persistência e response devem ser explícitas em service ou mapper local, nunca implícitas no endpoint.

## Estrutura Recomendada

```text
src/
└── models/
    └── users/
        ├── data/
        │   ├── user_create_request.py
        │   └── user_response.py
        └── persistence/
            └── user_record.py
```

Use `data` para contratos públicos HTTP e `persistence` para modelos internos de armazenamento quando o projeto precisar desse tipo de separação.

## Exemplo de Modelo de Persistência

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserRecord(BaseModel):
    """Representa o registro interno de usuário persistido no banco."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    id: str = Field(..., description="Identificador interno do registro.")
    public_id: str = Field(..., description="Identificador público exposto pela API.")
    email: str = Field(..., description="E-mail normalizado usado para autenticação.")
    password_hash: str = Field(..., description="Hash da senha armazenado internamente.")
    status: str = Field(..., description="Estado operacional persistido do usuário.")
    version: int = Field(..., description="Versão usada para controle concorrente.")
    created_at: datetime = Field(..., description="Data de criação do registro.")
    updated_at: datetime = Field(..., description="Data da última atualização do registro.")
```

## Exemplo de Conversão Para Response

```python
from src.models.users.data.user_response import UserResponse
from src.models.users.persistence.user_record import UserRecord


def to_user_response(record: UserRecord) -> UserResponse:
    return UserResponse(
        id=record.public_id,
        status=record.status,
    )
```

## Checklist

- [ ] O modelo de banco é interno e não aparece como `response_model`.
- [ ] Campos sensíveis ou técnicos ficam fora dos modelos de response.
- [ ] Exemplos OpenAPI ficam nos modelos `*_request.py` e `*_response.py`.
- [ ] Conversões para contrato público são explícitas.
- [ ] Constraints, índices e tipos específicos do banco seguem `standard-database`.
