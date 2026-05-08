# Fronteiras Entre Service e Repository

Use este guia para impedir acoplamento entre domínio, persistência e HTTP.

## Service

O service coordena casos de uso.

Responsabilidades:

- aplicar regra de negócio;
- chamar repositories e integrações;
- orquestrar operações independentes;
- transformar entidades internas em contratos públicos quando apropriado;
- lançar erros de domínio conhecidos.

Não deve:

- importar `Request`, `Response`, `APIRouter` ou `JSONResponse`;
- decidir status HTTP;
- montar headers;
- abrir conexão de banco manualmente quando isso pertence ao provider;
- acessar variáveis de ambiente diretamente.

## Repository

O repository isola persistência.

Responsabilidades:

- consultar dados;
- persistir dados;
- traduzir resultados técnicos em entidades internas;
- encapsular detalhes de SQL, ORM, cache ou driver.

Não deve:

- retornar modelo Pydantic de response;
- conhecer envelopes `data`, `meta` e `links`;
- aplicar status HTTP;
- conter regra de autorização de rota;
- logar payload sensível.

## Exemplo de Service

```python
from src.models.users.data.user_response import UserResponse
from src.repository.users.user_repository import UserRepository


class UserService:
    """Coordena casos de uso relacionados a usuários."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def get_user_response(self, user_id: str) -> UserResponse | None:
        """Busca um usuário e retorna seu contrato público.

        Parameters
        ----------
        user_id : str
            Identificador público do usuário.

        Returns
        -------
        UserResponse | None
            Contrato público quando o usuário existe; caso contrário, `None`.
        """

        user = await self._repository.get_by_id(user_id=user_id)
        if user is None:
            return None

        return UserResponse(id=user.id, status=user.status)
```

## Exemplo de Repository

```python
from src.repository.users.entities import UserEntity


class UserRepository:
    """Fornece acesso persistente aos dados de usuário."""

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """Busca um usuário pelo identificador público.

        Parameters
        ----------
        user_id : str
            Identificador público do usuário.

        Returns
        -------
        UserEntity | None
            Entidade interna quando encontrada; caso contrário, `None`.
        """

        ...
```
