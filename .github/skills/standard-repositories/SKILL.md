---
name: standard-repositories
description: Padroniza repositories como camada de execução técnica usada por services para queries, blobs, clients já configurados e chamadas OpenAI, sem regra de negócio.
---
# Standard Repositories - Execução Técnica

Use esta skill ao criar ou revisar classes em `src/repository/`.

## Responsabilidade Desta Skill

Esta skill é dona de:

- execução de queries;
- leitura e escrita de blobs;
- chamadas técnicas a clients externos já definidos pela camada de integrações/configs;
- chamadas OpenAI via client configurado;
- tratamento técnico de erros;
- retorno de entidades internas ou resultados técnicos tipados.

Esta skill não é dona de:

- regra de negócio: use `standard-services`;
- criação de clients/singletons: use `standard-configs`;
- política de integrações externas, timeout, retry, circuit breaker e webhooks: use `standard-integrations`;
- status HTTP: use `standard-endpoints`;
- contratos públicos de response: use `standard-data-models`;
- contrato público de erro: use `standard-errors`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar padrão de repository. | [Padrão de repository](references/repository-pattern.md) |
| Quando precisar aprofundar queries e persistência. | [Queries e persistência](references/query-execution.md) |
| Quando precisar aprofundar blob e storage. | [Blob e storage](references/blob-execution.md) |
| Quando precisar aprofundar openai repository. | [OpenAI repository](references/openai-execution.md) |

## Regras Obrigatórias

- Todo método público de repository deve ser `async def`.
- Toda função deve ter tipos de entrada e retorno.
- Toda função pública deve ter docstring NumPy em pt-BR.
- Repository não deve conter regra de negócio.
- Repository não deve retornar `JSONResponse`, wrappers ou modelos HTTP públicos.
- Repository deve receber client/conexão pelo construtor.
- Repository não deve criar singleton diretamente.
- Repository não deve definir política de retry, circuit breaker ou webhook; siga `standard-integrations`.
- Tratamento de erro deve traduzir falhas técnicas em exceções técnicas conhecidas.
- Dados sensíveis não devem ser logados.

## Exemplo Base

```python
from src.repository.users.entities import UserEntity


class UserRepository:
    """Executa operações técnicas de persistência de usuários.

    Parameters
    ----------
    database : DatabaseClient
        Client assíncrono de banco configurado pela camada de configs.
    """

    def __init__(self, database: DatabaseClient) -> None:
        self._database = database

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """Busca usuário pelo identificador público.

        Parameters
        ----------
        user_id : str
            Identificador público do usuário.

        Returns
        -------
        UserEntity | None
            Entidade interna quando encontrada; caso contrário, `None`.
        """

        row = await self._database.fetch_one(
            "SELECT id, status FROM users WHERE id = :user_id",
            {"user_id": user_id},
        )
        if row is None:
            return None

        return UserEntity(id=row["id"], status=row["status"])
```

## Checklist

- [ ] Repository está em `src/repository/{dominio}/`.
- [ ] Métodos públicos são assíncronos, tipados e documentados.
- [ ] Repository executa operação técnica, não regra de negócio.
- [ ] Clients/conexões entram pelo construtor.
- [ ] Nenhum contrato HTTP é retornado diretamente.
- [ ] Falhas técnicas são tratadas ou traduzidas.
