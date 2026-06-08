---
name: standard-logs
description: Padroniza logging estruturado em pt-BR para aplicações FastAPI assíncronas, com contexto de correlação, eventos nomeados, mensagens orientadas ao negócio e baixa exposição de dados sensíveis.
---
# Standard Logs - Logging Estruturado

Use esta skill ao criar ou revisar logs.

## Logs vs erros HTTP (obrigatório)

- Logs vão para o **console/agregador**; erros HTTP vão no body `errors[]` via handlers (`standard-errors`).
- Não confunda nível de log com status HTTP: `logger.warning` não substitui `403`, e `logger.error` não substitui `500`.
- Services, repositories e security **lançam exceções**; handlers globais **logam e respondem**.
- Detalhe técnico (`error_type`, stack trace) fica no log; mensagem do cliente permanece segura e estável.

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar separar nível de log e resposta HTTP. | [Níveis de log vs erros HTTP](references/log-levels-vs-http-errors.md) |
| Quando precisar aprofundar eventos de log. | [Eventos de log](references/log-events.md) |
| Quando precisar aprofundar o texto da mensagem (`message`). | [Mensagens orientadas ao negócio](references/log-messages.md) |
| Quando precisar aprofundar dados sensíveis em logs. | [Dados sensíveis em logs](references/sensitive-data.md) |
| Quando precisar aprofundar correlação entre logs, traces e erros. | [Correlação entre logs, traces e erros](references/correlation.md) |

## Regras Obrigatórias

- Logs devem ser estruturados e conter evento, camada e identificadores úteis.
- Nunca logue senhas, tokens, documentos, cartões ou payloads sensíveis completos.
- Inclua `correlation_id` quando disponível.
- Inclua `trace_id` e `span_id` automaticamente pelo formatter quando houver span OpenTelemetry ativo.
- Não crie `trace_id` manualmente em middleware, service ou repository; isso pertence ao OpenTelemetry.
- Use níveis de log de forma consistente: `debug`, `info`, `warning`, `error`, `exception`, `critical` (veja [Níveis de log vs erros HTTP](references/log-levels-vs-http-errors.md)).
- `debug`: rastreio técnico verboso; só com `LOGGING__LEVEL=DEBUG`.
- `info`: fluxo normal e resultados esperados.
- `warning`: degradação, dependência opcional ausente, auth inválida, situação que merece alerta no console — **não** rebaixar para `debug`.
- `error`: falha que interrompe a operação (antes do handler HTTP).
- `exception`: falha inesperada com stack trace no handler global.
- Log e resposta HTTP são canais separados; veja [Níveis de log vs erros HTTP](references/log-levels-vs-http-errors.md).
- Mensagens devem ser curtas e em pt-BR.
- Services e repositories podem logar eventos de domínio e infraestrutura, mas endpoints devem ser discretos.
- Services e repositories novos ou alterados devem declarar eventos de log para sucesso relevante, resultado vazio/degradado e falha técnica traduzida, salvo justificativa explícita.
- Use `critical` apenas para falha que compromete continuidade, integridade do sistema ou indisponibilidade ampla.
- Com `logging.json_enabled=false`, o formatter legível no terminal deve manter os mesmos campos estruturados (`event`, `layer`, `correlation_id`, trace e `extra`); só muda a serialização.

## Mensagens orientadas ao negócio

A mensagem humanizada deve explicar **o que importa para operação, suporte ou auditoria**, não o que o código está fazendo por dentro.

- **Inclua na mensagem** (quando seguro e relevante): quem ou o quê foi afetado (usuário, cliente, tenant, integração), qual pedido ou caso de uso (criar pedido, anexar documento, consultar saldo), e o resultado em linguagem de negócio (aprovado, não encontrado, recusado, indisponível).
- **Coloque em `extra`**: identificadores (`user_id`, `order_id`, `tenant_id`), provider, operação técnica, status HTTP, duração, contagem, `error_type` e demais metadados para filtro e dashboards.
- **Evite** mensagens que só descrevem implementação: "listando template", "iniciando decorator", "chamando repository", "processando requisição", "operação concluída" sem dizer o quê nem para quem.
- **Evite** repetir na mensagem o que já está estável em `event`; a mensagem complementa o evento com contexto legível, não o substitui.
- **Em falhas**, diga o que o usuário ou o processo **não conseguiu obter**; detalhe técnico fica em `extra` e no stack trace de `logger.exception`.
- **Não logue** passos puramente técnicos sem valor de negócio (imports, wiring de template, aplicação de middleware genérico) salvo `debug` local e temporário.

Consulte [Mensagens orientadas ao negócio](references/log-messages.md) para exemplos de boa e má prática.

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
        "Conta de usuário criada e disponível para acesso.",
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
        "Não foi possível persistir os dados do usuário solicitado.",
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
import logging

from src.models.users.response.user_response import UserResponse


logger = logging.getLogger("app.services.users")


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

        logger.info(
            "Cadastro de usuário iniciado com os dados informados.",
            extra={
                "event": "user.create_started",
                "layer": "service",
                "correlation_id": correlation_id,
            },
        )
        user = await self._repository.create(payload=payload)
        logger.info(
            "Usuário cadastrado e pronto para uso no sistema.",
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
- [ ] Formatter adiciona `trace_id` e `span_id` quando existe span ativo.
- [ ] Nenhum dado sensível é emitido.
- [ ] Exceções usam `logger.exception` quando há stack trace útil.
- [ ] A mensagem descreve impacto ou pedido de negócio (quem/o quê/resultado), não só etapa técnica.
- [ ] Identificadores e metadados técnicos estão em `extra`, não só na mensagem.
- [ ] Services e repositories relevantes possuem eventos observáveis ou justificativa explícita para silêncio.
