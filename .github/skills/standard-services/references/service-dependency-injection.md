# Dependency Injection em Services

Use injeção por construtor para tornar services testáveis e desacoplados.

## Regra Principal

O service recebe dependências prontas. Ele não cria repository, client de banco, client OpenAI, client de blob ou settings.

## Exemplo

```python
from src.repository.users.user_repository import UserRepository
from src.repository.users.user_summary_repository import UserSummaryRepository


class UserService:
    """Executa casos de uso de usuários."""

    def __init__(
        self,
        user_repository: UserRepository,
        summary_repository: UserSummaryRepository,
    ) -> None:
        self._user_repository = user_repository
        self._summary_repository = summary_repository
```

## Provider FastAPI

O provider pertence à composição da aplicação, mas pode montar o service.

```python
from fastapi import Depends

from src.repository.users.user_repository import UserRepository
from src.services.users.user_service import UserService


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Cria o service de usuários com dependências injetadas."""

    return UserService(user_repository=user_repository)
```

## Testes

Em testes, injete fakes ou mocks no construtor.

```python
service = UserService(user_repository=fake_user_repository)
```
