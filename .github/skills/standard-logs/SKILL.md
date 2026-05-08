---
name: standard-logs
description: Padroniza logging estruturado em pt-BR para aplicações FastAPI assíncronas, com contexto de correlação, eventos nomeados e baixa exposição de dados sensíveis.
---
# Standard Logs - Logging Estruturado

Use esta skill ao criar ou revisar logs.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar eventos de log. | [Eventos de log](references/log-events.md) |
| Quando precisar aprofundar dados sensíveis em logs. | [Dados sensíveis em logs](references/sensitive-data.md) |
| Quando precisar aprofundar correlação entre logs, traces e erros. | [Correlação entre logs, traces e erros](references/correlation.md) |

## Regras Obrigatórias

- Logs devem ser estruturados e conter evento, camada e identificadores úteis.
- Nunca logue senhas, tokens, documentos, cartões ou payloads sensíveis completos.
- Inclua `correlation_id` quando disponível.
- Use níveis de log de forma consistente: `debug`, `info`, `warning`, `error`, `exception`.
- Mensagens devem ser curtas e em pt-BR.
- Services e repositories podem logar eventos de domínio e infraestrutura, mas endpoints devem ser discretos.

## Exemplo de Logger

```python
import logging
from typing import Any


logger = logging.getLogger("app.users")


async def log_user_created(user_id: str, correlation_id: str | None) -> None:
    """Registra a criação bem-sucedida de um usuário.

    Parameters
    ----------
    user_id : str
        Identificador público do usuário criado.
    correlation_id : str | None
        Identificador de correlação da requisição atual, quando disponível.
    """

    logger.info(
        "Usuário criado com sucesso.",
        extra={
            "event": "user.created",
            "layer": "service",
            "user_id": user_id,
            "correlation_id": correlation_id,
        },
    )


async def log_repository_error(operation: str, error: Exception, context: dict[str, Any]) -> None:
    """Registra falha de infraestrutura sem expor dados sensíveis.

    Parameters
    ----------
    operation : str
        Nome lógico da operação que falhou.
    error : Exception
        Exceção capturada durante a operação.
    context : dict[str, Any]
        Contexto seguro para diagnóstico.
    """

    logger.exception(
        "Falha ao executar operação de persistência.",
        extra={
            "event": "repository.error",
            "layer": "repository",
            "operation": operation,
            "error_type": type(error).__name__,
            **context,
        },
    )
```

## Exemplo em Service

```python
from src.logger import logger
from src.models.users.data.user_response import UserResponse


class UserService:
    """Executa casos de uso relacionados a usuários."""

    async def create_user(self, payload: UserCreateRequest, correlation_id: str | None) -> UserResponse:
        """Cria um usuário e registra eventos relevantes.

        Parameters
        ----------
        payload : UserCreateRequest
            Dados validados para criação.
        correlation_id : str | None
            Identificador de correlação da requisição.

        Returns
        -------
        UserResponse
            Dados públicos do usuário criado.
        """

        user = await self._repository.create(payload=payload)
        logger.info(
            "Usuário criado com sucesso.",
            extra={
                "event": "user.created",
                "layer": "service",
                "user_id": user.id,
                "correlation_id": correlation_id,
            },
        )
        return UserResponse(id=user.id, status=user.status)
```

## Checklist

- [ ] Log contém `event` e `layer`.
- [ ] Log inclui `correlation_id` quando disponível.
- [ ] Nenhum dado sensível é emitido.
- [ ] Exceções usam `logger.exception` quando há stack trace útil.
- [ ] Mensagens são curtas, em pt-BR e orientadas a evento.
