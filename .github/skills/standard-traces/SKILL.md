---
name: standard-traces
description: Padroniza tracing e observabilidade para fluxos FastAPI assíncronos, com spans por responsabilidade, atributos seguros e propagação de correlation_id.
---
# Standard Traces - Observabilidade

Use esta skill ao instrumentar endpoints, services, repositories e integrações externas.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar nomes de spans. | [Nomes de spans](references/span-naming.md) |
| Quando precisar aprofundar atributos seguros. | [Atributos seguros](references/safe-attributes.md) |
| Quando precisar aprofundar erros em traces. | [Erros em traces](references/trace-errors.md) |
| Quando precisar aprofundar correlação com logs, erros e middleware. | [Correlação em traces](references/correlation.md) |

## Regras Obrigatórias

- Crie spans por responsabilidade: endpoint, service, repository e integração externa.
- Não registre dados sensíveis em atributos de trace.
- Inclua `correlation_id`, método HTTP, rota e identificadores públicos quando disponíveis.
- Obtenha `correlation_id` do contexto da requisição; não gere IDs de correlação dentro de spans.
- Use nomes estáveis para spans, como `users.service.create_user`.
- Marque erros no span e relance a exceção para tratamento global.
- Operações assíncronas paralelas devem criar spans próprios quando representarem I/O relevante.
- Services e repositories novos ou alterados devem criar spans em operações relevantes de caso de uso, I/O, query, blob ou integração técnica, salvo justificativa explícita.

## Exemplo de Instrumentação

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from src.models.users.user_response import UserResponse

tracer = trace.get_tracer("app.users")


class UserService:
    """Executa casos de uso de usuário com tracing padronizado."""

    async def get_user_response(
        self,
        user_id: str,
        correlation_id: str | None,
    ) -> UserResponse | None:
        """Busca um usuário com span de observabilidade.

        Parameters
        ----------
        user_id : str
            Identificador público do usuário.
        correlation_id : str | None
            Identificador de correlação da requisição.

        Returns
        -------
        UserResponse | None
            Usuário encontrado ou `None`.

        Raises
        ------
        Exception
            Relança falhas da camada de persistência após registrar o erro no span.
        """

        with tracer.start_as_current_span("users.service.get_user_response") as span:
            span.set_attribute("app.layer", "service")
            span.set_attribute("app.user_id", user_id)
            if correlation_id is not None:
                span.set_attribute("app.correlation_id", correlation_id)

            try:
                user = await self._repository.get_by_id(user_id=user_id)
                if user is None:
                    span.set_attribute("app.result", "not_found")
                    return None

                span.set_attribute("app.result", "found")
                return UserResponse(id=user.id, status=user.status)
            except Exception as error:
                span.record_exception(error)
                span.set_status(Status(StatusCode.ERROR, str(error)))
                raise
```

## Exemplo com `asyncio.gather`

```python
import asyncio


async def load_dashboard(user_id: str, correlation_id: str | None) -> UserDashboardResponse:
    """Carrega dados de painel em paralelo com spans independentes.

    Parameters
    ----------
    user_id : str
        Identificador público do usuário.
    correlation_id : str | None
        Identificador de correlação da requisição.

    Returns
    -------
    UserDashboardResponse
        Dados consolidados para apresentação do painel.
    """

    with tracer.start_as_current_span("users.service.load_dashboard") as span:
        span.set_attribute("app.layer", "service")
        span.set_attribute("app.user_id", user_id)
        if correlation_id is not None:
            span.set_attribute("app.correlation_id", correlation_id)

        profile_task = asyncio.create_task(
            get_user_response(user_id=user_id, correlation_id=correlation_id)
        )
        sessions_task = asyncio.create_task(
            count_active_sessions(user_id=user_id, correlation_id=correlation_id)
        )

        profile, sessions = await asyncio.gather(profile_task, sessions_task)
        return UserDashboardResponse(profile=profile, active_sessions=sessions)
```

## Checklist

- [ ] Span tem nome estável e orientado à responsabilidade.
- [ ] Atributos não expõem dados sensíveis.
- [ ] Erros são registrados no span e relançados.
- [ ] `correlation_id` é propagado quando disponível.
- [ ] Operações paralelas relevantes possuem rastreamento próprio.
- [ ] Services e repositories relevantes possuem spans próprios ou justificativa explícita para ausência de span.
