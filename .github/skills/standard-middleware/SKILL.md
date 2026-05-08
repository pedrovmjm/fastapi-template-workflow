---
name: standard-middleware
description: Padroniza criação de middlewares FastAPI/Starlette com responsabilidade única, execução assíncrona, tipagem explícita, contexto de requisição e exemplos completos.
---
# Standard Middleware - FastAPI

Use esta skill ao criar middlewares HTTP.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar ordem de middlewares. | [Ordem de middlewares](references/middleware-order.md) |
| Quando propagar ou gerar correlation id. | [Correlation ID](references/correlation-id.md) |
| Quando precisar aprofundar headers de segurança. | [Headers de segurança](references/security-headers.md) |

## Regras Obrigatórias

- Cada middleware deve resolver uma única preocupação: correlação, logging, segurança, tracing, compressão ou métricas.
- Middlewares devem ser assíncronos e tipados.
- Não coloque regra de negócio em middleware.
- Não leia corpo da requisição sem necessidade explícita.
- Preserve headers existentes e adicione apenas os headers sob responsabilidade do middleware.
- Falhas inesperadas devem ser logadas e relançadas para o handler global.
- IDs de correlação devem ser propagados por `request.state` e header HTTP.
- Registre middlewares por uma função `_register_middlewares(app, settings)`, conforme o fluxo de composição da aplicação.
- Não registre middlewares diretamente no corpo de `create_app`.
- Parâmetros configuráveis de middlewares devem vir de `Settings`, não de literais espalhados pela factory.

## Exemplo de Middleware de Correlação

```python
from collections.abc import Awaitable, Callable
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Propaga um identificador de correlação por requisição.

    Parameters
    ----------
    app : object
        Aplicação ASGI decorada pelo middleware.
    header_name : str
        Nome do header HTTP usado para entrada e saída do identificador.

    Notes
    -----
    O identificador fica disponível em `request.state.correlation_id` para
    logs, traces e handlers posteriores.
    """

    def __init__(self, app: object, header_name: str = "X-Correlation-Id") -> None:
        super().__init__(app)
        self._header_name = header_name

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Adiciona o identificador de correlação ao ciclo da requisição.

        Parameters
        ----------
        request : Request
            Requisição HTTP recebida pela aplicação.
        call_next : Callable[[Request], Awaitable[Response]]
            Próximo handler da cadeia ASGI.

        Returns
        -------
        Response
            Resposta HTTP com o header de correlação preenchido.
        """

        correlation_id = request.headers.get(self._header_name) or str(uuid4())
        request.state.correlation_id = correlation_id

        response = await call_next(request)
        response.headers[self._header_name] = correlation_id
        return response
```

## Exemplo de Registro na Aplicação

```python
from fastapi import FastAPI

from src.configs.settings import Settings, get_settings
from src.middlewares.correlation_id import CorrelationIdMiddleware


def _register_middlewares(app: FastAPI, settings: Settings) -> None:
    """Registra os middlewares globais da aplicação.

    Parameters
    ----------
    app : FastAPI
        Instância da aplicação que receberá os middlewares.
    settings : Settings
        Configurações usadas para parametrizar middlewares.
    """

    app.add_middleware(
        CorrelationIdMiddleware,
        header_name=settings.correlation_id_header_name,
    )


async def create_app() -> FastAPI:
    """Cria e configura a aplicação FastAPI.

    Returns
    -------
    FastAPI
        Aplicação configurada com middlewares e demais componentes.
    """

    settings = get_settings()
    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
    )

    _register_middlewares(app=app, settings=settings)
    return app
```

## Ordem Recomendada

```text
1. Error handling global
2. Correlation ID
3. Tracing
4. Logging de acesso
5. Segurança e headers
6. CORS
```

## Checklist

- [ ] Middleware tem uma única responsabilidade.
- [ ] `dispatch` é assíncrono e tipado.
- [ ] Não existe regra de negócio no middleware.
- [ ] Headers adicionados são documentados.
- [ ] Dados compartilhados usam `request.state`.
- [ ] Falhas não são engolidas silenciosamente.
- [ ] Registro acontece em `_register_middlewares(app, settings)`.
- [ ] `create_app` apenas carrega `settings`, instancia `FastAPI` e chama funções de registro.
- [ ] Configurações de middleware vêm de `Settings`.
