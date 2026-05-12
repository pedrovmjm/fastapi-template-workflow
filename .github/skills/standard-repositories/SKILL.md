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
- contrato público de erro: use `standard-errors`;
- formato detalhado de logs e spans: use `standard-logs` e `standard-traces`.

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
- Operações de I/O, query, blob ou chamada técnica devem criar span de repository conforme `standard-traces`.
- Falhas técnicas traduzidas devem registrar log estruturado com `logger.warning`, `logger.error` ou `logger.exception`, sem payload sensível.
- Logs e spans devem conter metadados seguros de operação, provider, camada e resultado quando disponíveis.
- Dados sensíveis não devem ser logados.

## Exemplo Base

```python
import logging

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from src.observability.correlation import get_current_correlation_id
from src.repository.users.entities import UserEntity


logger = logging.getLogger("app.repository.users")
tracer = trace.get_tracer("app.repository.users")


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

        correlation_id = get_current_correlation_id()
        with tracer.start_as_current_span("users.repository.get_by_id") as span:
            span.set_attribute("app.layer", "repository")
            span.set_attribute("app.operation", "get_by_id")
            span.set_attribute("app.user_id", user_id)
            if correlation_id is not None:
                span.set_attribute("app.correlation_id", correlation_id)

            logger.info(
                "Consulta de usuário iniciada.",
                extra={
                    "event": "user_repository.lookup_started",
                    "layer": "repository",
                    "operation": "get_by_id",
                    "user_id": user_id,
                    "correlation_id": correlation_id,
                },
            )
            try:
                row = await self._database.fetch_one(
                    "SELECT id, status FROM users WHERE id = :user_id",
                    {"user_id": user_id},
                )
                if row is None:
                    span.set_attribute("app.result", "not_found")
                    logger.info(
                        "Consulta de usuário sem resultado.",
                        extra={
                            "event": "user_repository.not_found",
                            "layer": "repository",
                            "operation": "get_by_id",
                            "user_id": user_id,
                            "correlation_id": correlation_id,
                        },
                    )
                    return None

                span.set_attribute("app.result", "found")
                logger.info(
                    "Consulta de usuário concluída.",
                    extra={
                        "event": "user_repository.lookup_succeeded",
                        "layer": "repository",
                        "operation": "get_by_id",
                        "user_id": user_id,
                        "correlation_id": correlation_id,
                    },
                )
                return UserEntity(id=row["id"], status=row["status"])
            except Exception as error:
                span.record_exception(error)
                span.set_status(Status(StatusCode.ERROR, type(error).__name__))
                logger.exception(
                    "Falha técnica ao consultar usuário.",
                    extra={
                        "event": "user_repository.lookup_failed",
                        "layer": "repository",
                        "operation": "get_by_id",
                        "user_id": user_id,
                        "error_type": type(error).__name__,
                        "correlation_id": correlation_id,
                    },
                )
                raise
```

## Checklist

- [ ] Repository está em `src/repository/{dominio}/`.
- [ ] Métodos públicos são assíncronos, tipados e documentados.
- [ ] Repository executa operação técnica, não regra de negócio.
- [ ] Clients/conexões entram pelo construtor.
- [ ] Nenhum contrato HTTP é retornado diretamente.
- [ ] Falhas técnicas são tratadas ou traduzidas.
- [ ] Logs estruturados seguem `standard-logs` ou há justificativa explícita para ausência de log.
- [ ] Spans de repository seguem `standard-traces` ou há justificativa explícita para ausência de span.
