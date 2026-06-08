# Composição da Aplicação

Use este guia para manter a inicialização do FastAPI previsível e testável.

## Estrutura Recomendada

```text
src/
├── configs/
│   └── settings.py
├── middlewares/
├── models/
│   ├── health/
│   │   └── response/
│   │       └── health_response.py
├── db/
├── routes/
│   ├── health/
│       └──health.py 
├── db/
├── routes/
│   ├── health/
│       └── health.py
└── services/
├── start.py
```

## App Factory

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from src.configs.settings import Settings, get_settings
from src.routes import health, users


async def open_resources(app: FastAPI) -> None:
    """Abre recursos globais necessários para a aplicação.

    Parameters
    ----------
    app : FastAPI
        Instância da aplicação que receberá recursos compartilhados em `state`.
    """

    app.state.resources_ready = True


async def close_resources(app: FastAPI) -> None:
    """Fecha recursos globais abertos no ciclo de vida da aplicação.

    Parameters
    ----------
    app : FastAPI
        Instância da aplicação que contém os recursos compartilhados.
    """

    app.state.resources_ready = False


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Gerencia recursos globais da aplicação.

    Parameters
    ----------
    app : FastAPI
        Instância da aplicação FastAPI.

    Yields
    ------
    None
        Controle devolvido ao FastAPI enquanto a aplicação está ativa.
    """

    await open_resources(app=app)
    try:
        yield
    finally:
        await close_resources(app=app)


def _register_routes(app: FastAPI) -> None:
    """Registra todos os routers da aplicação.

    Parameters
    ----------
    app : FastAPI
        Instância da aplicação que receberá os routers.
    """

    app.include_router(health.router)
    app.include_router(users.router)


def _register_middlewares(app: FastAPI, settings: Settings) -> None:
    """Registra os middlewares globais da aplicação.

    Parameters
    ----------
    app : FastAPI
        Instância da aplicação que receberá os middlewares.
    settings : Settings
        Configurações usadas para parametrizar middlewares.
    """

    # Exemplo:
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=settings.cors_allow_origins,
    #     allow_credentials=settings.cors_allow_credentials,
    #     allow_methods=settings.cors_allow_methods,
    #     allow_headers=settings.cors_allow_headers,
    # )


async def create_app() -> FastAPI:
    """Cria e configura a aplicação FastAPI.

    Returns
    -------
    FastAPI
        Aplicação configurada com routers, middlewares e handlers.
    """

    settings = get_settings()
    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
        lifespan=lifespan,
    )

    _register_middlewares(app=app, settings=settings)
    _register_routes(app=app)
    return app
```

## Regras

- `start.py` monta a aplicação; não deve conter regra de negócio.
- Routers ficam em `routes`.
- `create_app` deve apenas compor a aplicação: carregar `settings`, instanciar `FastAPI` e chamar funções de registro.
- Parâmetros públicos do `FastAPI`, como `title`, `description`, `version`, `docs_url`, `redoc_url` e `openapi_url`, devem vir de `settings`.
- Routers são registrados por `_register_routes(app)`, não diretamente no corpo de `create_app`.
- Middlewares são registrados por `_register_middlewares(app, settings)`, mesmo quando houver poucos middlewares.
- Exception handlers são registrados em uma função própria quando houver mais de um.
- Não inicialize conexão global no import do módulo.
