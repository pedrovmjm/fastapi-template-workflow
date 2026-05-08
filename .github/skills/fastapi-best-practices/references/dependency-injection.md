# Dependency Injection

Use dependências pequenas, explícitas e fáceis de trocar em testes.

## Provider de Service

```python
from fastapi import Depends

from src.repository.users.user_repository import UserRepository
from src.services.users.user_service import UserService


async def get_user_repository() -> UserRepository:
    """Cria o repositório de usuários para a requisição atual.

    Returns
    -------
    UserRepository
        Repositório configurado para acesso aos dados de usuário.
    """

    return UserRepository()


async def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Cria o service de usuários com suas dependências.

    Parameters
    ----------
    repository : UserRepository
        Repositório injetado pelo FastAPI.

    Returns
    -------
    UserService
        Serviço pronto para executar casos de uso de usuário.
    """

    return UserService(repository=repository)
```

## Regras

- Provider não deve executar regra de negócio.
- Provider não deve consultar dados do usuário final.
- Provider pode montar dependências técnicas.
- Dependências devem ser substituíveis via `app.dependency_overrides` em testes.
- Evite singleton manual sem necessidade clara.
