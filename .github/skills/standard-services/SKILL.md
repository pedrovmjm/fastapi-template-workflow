---
name: standard-services
description: Padroniza services FastAPI como camada de lógica de negócio, manipulação de dados, orquestração assíncrona, dependency injection por construtor, docstrings NumPy e funções com responsabilidade única.
---
# Standard Services - Lógica de Negócio

Use esta skill ao criar ou revisar classes em `src/services/`.

## Responsabilidade Desta Skill

Esta skill é dona de:

- padrão de service;
- lógica de negócio;
- manipulação e transformação de dados;
- orquestração assíncrona entre repositories;
- dependency injection por construtor;
- funções pequenas, tipadas e com responsabilidade única;
- retorno de modelos públicos definidos em `standard-data-models`.

Esta skill não é dona de:

- execução de query, blob ou chamada externa: use `standard-repositories`;
- criação de clients e singletons: use `standard-configs`;
- status HTTP e `APIRouter`: use `standard-endpoints`;
- contrato de erro: use `standard-errors`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar definir estrutura, assinatura e responsabilidade de services. | [Padrão de service](references/service-pattern.md) |
| Quando precisar injetar repositories, providers ou clients em services. | [Dependency injection em services](references/service-dependency-injection.md) |
| Quando services precisarem transformar, combinar ou preparar dados. | [Manipulação de dados](references/data-manipulation.md) |

## Regras Obrigatórias

- Todo método público de service deve ser `async def`.
- Toda função deve ter tipos de entrada e retorno.
- Toda função pública deve ter docstring NumPy em pt-BR.
- Cada método deve executar uma responsabilidade de negócio clara.
- O service pode manipular dados, consolidar resultados e aplicar regras.
- O service pode chamar múltiplos repositories.
- O service deve receber dependências pelo construtor.
- O service não deve instanciar repository, client externo ou singleton diretamente.
- O service não deve importar `Request`, `Response`, `APIRouter` ou `JSONResponse`.
- O service não deve decidir status HTTP.
- Operações independentes devem usar `asyncio`.

## Exemplo Base

```python
import asyncio

from src.models.users.data.user_response import UserResponse
from src.repository.users.user_repository import UserRepository


class UserService:
    """Executa regras de negócio relacionadas a usuários.

    Parameters
    ----------
    user_repository : UserRepository
        Repositório usado para leitura e persistência de usuários.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def get_user_response(self, user_id: str) -> UserResponse | None:
        """Busca um usuário e retorna seu contrato público.

        Parameters
        ----------
        user_id : str
            Identificador público do usuário.

        Returns
        -------
        UserResponse | None
            Dados públicos do usuário quando encontrado; caso contrário, `None`.
        """

        user = await self._user_repository.get_by_id(user_id=user_id)
        if user is None:
            return None

        return UserResponse(id=user.id, status=user.status)

    async def load_user_context(self, user_id: str) -> UserContext:
        """Carrega contexto de usuário com operações independentes.

        Parameters
        ----------
        user_id : str
            Identificador público do usuário.

        Returns
        -------
        UserContext
            Contexto consolidado para decisões de negócio.
        """

        profile_task = asyncio.create_task(self._user_repository.get_by_id(user_id=user_id))
        sessions_task = asyncio.create_task(
            self._user_repository.count_active_sessions(user_id=user_id)
        )

        profile, active_sessions = await asyncio.gather(profile_task, sessions_task)
        return UserContext(profile=profile, active_sessions=active_sessions)
```

## Checklist

- [ ] Service está em `src/services/{dominio}/`.
- [ ] Dependências entram pelo construtor.
- [ ] Métodos públicos são assíncronos, tipados e documentados.
- [ ] Cada método possui uma responsabilidade de negócio clara.
- [ ] Service não instancia repository ou client externo diretamente.
- [ ] Service não conhece detalhes HTTP.
- [ ] Operações independentes usam `asyncio`.
