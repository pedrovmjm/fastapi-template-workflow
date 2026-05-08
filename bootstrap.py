"""Gera o scaffolding inicial de uma aplicacao FastAPI.

O script mantem a decisao de bootstrap em um unico ponto de entrada, mas
gera a aplicacao em arquivos separados para facilitar manutencao futura.
"""

from __future__ import annotations

import argparse
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path
from string import Template


@dataclass(frozen=True)
class BootstrapConfig:
    """Agrupa opcoes usadas para renderizar o projeto."""

    target_path: Path
    project_name: str
    project_domain: str
    api_version: str
    force: bool
    dry_run: bool


@dataclass(frozen=True)
class FileTemplate:
    """Representa um arquivo que sera criado pelo bootstrap."""

    relative_path: str
    content: str

    def render(self, config: BootstrapConfig) -> str:
        """Renderiza o conteudo do arquivo usando a configuracao informada."""

        return Template(_normalize_template(self.content)).safe_substitute(
            project_name=config.project_name,
            project_domain=config.project_domain,
            api_version=config.api_version,
        )


def _normalize_template(content: str) -> str:
    """Remove indentacao artificial e garante quebra de linha final."""

    return textwrap.dedent(content).strip() + "\n"


def _normalize_name(value: str) -> str:
    """Normaliza nomes livres para um identificador curto de projeto."""

    normalized = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")
    return normalized or "fastapi-app"


def _normalize_api_version(value: str) -> str:
    """Normaliza a versao publica da API para o formato `vN`."""

    normalized = value.strip().lower()
    if re.fullmatch(r"[0-9]+", normalized):
        normalized = f"v{normalized}"

    if not re.fullmatch(r"v[0-9]+", normalized):
        raise ValueError("A versao da API deve seguir o formato 'v1', 'v2' ou numero inteiro.")

    return normalized


def build_file_templates() -> list[FileTemplate]:
    """Monta os templates de arquivos gerados pelo bootstrap."""

    return [
        FileTemplate(
            "pyproject.toml",
            """
            [project]
            name = "$project_name"
            version = "0.1.0"
            description = "Aplicacao FastAPI gerada pelo bootstrap."
            requires-python = ">=3.10"
            dependencies = [
                "fastapi>=0.115.0",
                "httpx>=0.27.0",
                "opentelemetry-api>=1.25.0",
                "opentelemetry-exporter-otlp-proto-http>=1.25.0",
                "opentelemetry-instrumentation-fastapi>=0.46b0",
                "opentelemetry-instrumentation-httpx>=0.46b0",
                "opentelemetry-instrumentation-pymongo>=0.46b0",
                "opentelemetry-instrumentation-sqlalchemy>=0.46b0",
                "opentelemetry-sdk>=1.25.0",
                "pydantic>=2.0.0",
                "pymongo>=4.9.0",
                "python-dotenv>=1.0.0",
                "SQLAlchemy>=2.0.0",
                "aiosqlite>=0.19.0",
                "uvicorn[standard]>=0.30.0",
            ]

            [tool.pytest.ini_options]
            pythonpath = ["."]
            testpaths = ["tests"]
            """,
        ),
        FileTemplate(
            ".env.example",
            """
            APP__NAME=$project_name
            APP__DOMAIN=$project_domain
            APP__DESCRIPTION=API FastAPI gerada pelo bootstrap.
            APP__VERSION=0.1.0
            APP__ENVIRONMENT=local
            APP__DEFAULT_API_VERSION=$api_version
            APP__API_VERSION_HEADER_NAME=X-API-Version
            APP__DOCS_URL=/docs
            APP__REDOC_URL=/redoc
            APP__OPENAPI_URL=/openapi.json

            TIME__TIMEZONE=America/Sao_Paulo

            SERVER__HOST=0.0.0.0
            SERVER__PORT=8000
            SERVER__RELOAD=false
            SERVER__WORKERS=1
            SERVER__LOOP=auto
            SERVER__LOG_LEVEL=info
            SERVER__PROXY_HEADERS=true
            SERVER__FORWARDED_ALLOW_IPS=*
            SERVER__TIMEOUT_KEEP_ALIVE_SECONDS=5
            SERVER__LIMIT_CONCURRENCY=0

            HTTPX_CLIENT__TIMEOUT_SECONDS=30
            HTTPX_CLIENT__CONNECT_TIMEOUT_SECONDS=10
            HTTPX_CLIENT__MAX_CONNECTIONS=100
            HTTPX_CLIENT__MAX_KEEPALIVE_CONNECTIONS=20

            LOGGING__LEVEL=INFO
            LOGGING__JSON_ENABLED=true

            TELEMETRY__ENABLED=true
            TELEMETRY__SERVICE_NAME=$project_name
            TELEMETRY__SERVICE_NAMESPACE=$project_domain
            TELEMETRY__EXPORTER=console
            TELEMETRY__SAMPLE_RATE=1.0
            TELEMETRY__EXCLUDED_URLS=/health
            TELEMETRY__INSTRUMENT_FASTAPI=true
            TELEMETRY__FASTAPI_EXCLUDE_INTERNAL_SPANS=true
            TELEMETRY__INSTRUMENT_HTTPX=true
            TELEMETRY__HTTPX_INSTRUMENTATION_MODE=managed_client
            TELEMETRY__INSTRUMENT_MONGO=true
            TELEMETRY__INSTRUMENT_SQLALCHEMY=true
            TELEMETRY__CAPTURE_REQUEST_HEADERS=x-request-id,x-correlation-id,x-api-version
            TELEMETRY__CAPTURE_RESPONSE_HEADERS=x-request-id,x-correlation-id,x-api-version
            TELEMETRY__SANITIZE_FIELDS=authorization,cookie,set-cookie,password,token,api_key,access_token,refresh_token
            TELEMETRY__OTLP_TRACES_ENDPOINT=http://localhost:4318/v1/traces
            TELEMETRY__OTLP_HEADERS=
            TELEMETRY__OTLP_TIMEOUT_SECONDS=10
            TELEMETRY__DYNATRACE_ENDPOINT=
            TELEMETRY__DYNATRACE_API_TOKEN=

            MONGO__ENABLED=false
            MONGO__URL=mongodb://localhost:27017
            MONGO__DATABASE_NAME=$project_name
            MONGO__CONNECT_TIMEOUT_MS=10000
            MONGO__SERVER_SELECTION_TIMEOUT_MS=10000
            MONGO__MAX_POOL_SIZE=100

            SQL_DATABASE__ENABLED=true
            SQL_DATABASE__URL=sqlite+aiosqlite:///:memory:
            SQL_DATABASE__ECHO=false
            """,
        ),
        FileTemplate(
            "src/__init__.py",
            '"""Pacote principal da aplicacao FastAPI."""\n',
        ),
        FileTemplate(
            "start.py",
            '''
            """Inicia a aplicacao FastAPI via Uvicorn."""

            import uvicorn

            from src.configs.settings import get_settings
            from src.observability.logging.logging import configure_logging


            def main() -> None:
                """Carrega configuracoes operacionais e executa o Uvicorn.

                Notes
                -----
                Este entrypoint fica fora de `src` de proposito: ele pertence ao
                startup do processo, nao a composicao HTTP da aplicacao.
                """

                settings = get_settings()
                configure_logging(settings=settings)
                workers = 1 if settings.server.reload else settings.server.workers

                uvicorn.run(
                    "src.main:app",
                    host=settings.server.host,
                    port=settings.server.port,
                    reload=settings.server.reload,
                    workers=workers,
                    loop=settings.server.loop,
                    log_level=settings.server.log_level,
                    log_config=None,
                    proxy_headers=settings.server.proxy_headers,
                    forwarded_allow_ips=settings.server.forwarded_allow_ips,
                    timeout_keep_alive=settings.server.timeout_keep_alive_seconds,
                    limit_concurrency=settings.server.limit_concurrency or None,
                )


            if __name__ == "__main__":
                main()
            ''',
        ),
        FileTemplate(
            "src/main.py",
            '''
            """Compoe a aplicacao FastAPI e registra recursos globais."""

            from collections.abc import AsyncIterator
            from contextlib import asynccontextmanager
            import logging

            from fastapi import FastAPI

            from src.configs.httpx_client import close_httpx_client, get_httpx_client
            from src.configs.mongo import close_mongo_client, get_mongo_client
            from src.configs.settings import Settings, get_settings
            from src.configs.sql_database import close_sql_engine, get_sql_engine
            from src.middlewares.api_version import ApiVersionMiddleware
            from src.observability.logging.logging import configure_logging
            from src.observability.telemetry.setup import configure_telemetry
            from src.routes.health import health


            logger = logging.getLogger("app.main")


            async def open_resources(app: FastAPI) -> None:
                """Abre recursos globais usados pela aplicacao.

                Parameters
                ----------
                app : FastAPI
                    Instancia FastAPI que recebera recursos compartilhados.

                Notes
                -----
                Esta funcao cria o singleton HTTPX de forma assincrona para que
                o fechamento fique centralizado no ciclo de vida da aplicacao.
                """

                settings = get_settings()
                app.state.settings = settings
                app.state.httpx_client = await get_httpx_client(settings=settings)
                app.state.mongo_client = (
                    await get_mongo_client(settings=settings) if settings.mongo.enabled else None
                )
                app.state.sql_engine = (
                    await get_sql_engine(settings=settings) if settings.sql_database.enabled else None
                )
                logger.info(
                    "Aplicacao iniciada.",
                    extra={
                        "event": "application.started",
                        "layer": "application",
                        "app_name": settings.app.name,
                        "api_version": settings.app.default_api_version,
                    },
                )


            async def close_resources(app: FastAPI) -> None:
                """Fecha recursos globais usados pela aplicacao.

                Parameters
                ----------
                app : FastAPI
                    Instancia FastAPI que contem recursos compartilhados.
                """

                await close_httpx_client()
                await close_mongo_client()
                await close_sql_engine()
                logger.info(
                    "Aplicacao encerrada.",
                    extra={
                        "event": "application.stopped",
                        "layer": "application",
                    },
                )


            @asynccontextmanager
            async def lifespan(app: FastAPI) -> AsyncIterator[None]:
                """Gerencia abertura e fechamento de recursos globais.

                Parameters
                ----------
                app : FastAPI
                    Instancia FastAPI em execucao.

                Yields
                ------
                None
                    Controle devolvido ao FastAPI enquanto a aplicacao esta ativa.
                """

                await open_resources(app=app)
                try:
                    yield
                finally:
                    await close_resources(app=app)


            def _register_middlewares(app: FastAPI, settings: Settings) -> None:
                """Registra middlewares globais da aplicacao.

                Parameters
                ----------
                app : FastAPI
                    Instancia FastAPI que recebera middlewares.
                settings : Settings
                    Configuracoes usadas para parametrizar middlewares.
                """

                app.add_middleware(
                    ApiVersionMiddleware,
                    default_api_version=settings.app.default_api_version,
                    header_name=settings.app.api_version_header_name,
                )


            def _register_routes(app: FastAPI) -> None:
                """Registra routers publicos da aplicacao.

                Parameters
                ----------
                app : FastAPI
                    Instancia FastAPI que recebera rotas.
                """

                app.include_router(health.router)


            def create_app() -> FastAPI:
                """Cria e configura a aplicacao FastAPI.

                Returns
                -------
                FastAPI
                    Aplicacao configurada com settings, middlewares, rotas e lifespan.
                """

                settings = get_settings()
                configure_logging(settings=settings)

                app = FastAPI(
                    title=settings.app.name,
                    description=settings.app.description,
                    version=settings.app.version,
                    docs_url=settings.app.docs_url,
                    redoc_url=settings.app.redoc_url,
                    openapi_url=settings.app.openapi_url,
                    lifespan=lifespan,
                )
                app.state.settings = settings
                configure_telemetry(app=app, settings=settings)

                _register_middlewares(app=app, settings=settings)
                _register_routes(app=app)
                return app


            app = create_app()
            ''',
        ),
        FileTemplate(
            "src/configs/__init__.py",
            '"""Configuracoes e providers tecnicos da aplicacao."""\n',
        ),
        FileTemplate(
            "src/configs/settings.py",
            '''
            """Carrega settings a partir de defaults, `.env` e ambiente."""

            from __future__ import annotations

            import json
            import os
            import sys
            from collections.abc import Iterator
            from functools import lru_cache
            from pathlib import Path
            from typing import Any, get_args, get_origin

            from dotenv import dotenv_values
            from pydantic import BaseModel, ConfigDict, Field

            from src.configs.values_domains.app import AppValues
            from src.configs.values_domains.httpx_client import HttpxClientValues
            from src.configs.values_domains.logging import LoggingValues
            from src.configs.values_domains.mongo import MongoValues
            from src.configs.values_domains.server import ServerValues
            from src.configs.values_domains.sql_database import SqlDatabaseValues
            from src.configs.values_domains.telemetry import TelemetryValues
            from src.configs.values_domains.time import TimeValues


            _RESET = "\\033[0m"
            _BOLD = "\\033[1m"
            _DIM = "\\033[2m"
            _DOMAIN_COLORS = {
                "app": "\\033[36m",
                "server": "\\033[35m",
                "time": "\\033[32m",
                "httpx_client": "\\033[34m",
                "logging": "\\033[33m",
                "telemetry": "\\033[95m",
                "mongo": "\\033[92m",
                "sql_database": "\\033[96m",
            }
            _LOCAL_COLOR = "\\033[32m"
            _PRD_COLOR = "\\033[31m"
            _STAGE_COLOR = "\\033[33m"


            class Settings(BaseModel):
                """Agrupa as configuracoes finais da aplicacao.

                Parameters
                ----------
                is_local : bool
                    Indica se um arquivo `.env` local foi carregado.
                app : AppValues
                    Configuracoes publicas e operacionais da aplicacao.
                server : ServerValues
                    Configuracoes operacionais do processo Uvicorn.
                time : TimeValues
                    Configuracoes de timezone usadas por respostas e agendamentos.
                httpx_client : HttpxClientValues
                    Configuracoes globais do client HTTP assicrono.
                logging : LoggingValues
                    Configuracoes de logging estruturado.
                telemetry : TelemetryValues
                    Configuracoes de instrumentacao OpenTelemetry.
                mongo : MongoValues
                    Configuracoes do provider MongoDB.
                sql_database : SqlDatabaseValues
                    Configuracoes do banco SQL da aplicacao.
                """

                model_config = ConfigDict(extra="forbid")

                is_local: bool = Field(
                    False,
                    description="Indica se a aplicacao carregou um arquivo `.env` local.",
                )
                app: AppValues = Field(
                    default_factory=AppValues,
                    description="Configuracoes publicas e operacionais da aplicacao.",
                )
                server: ServerValues = Field(
                    default_factory=ServerValues,
                    description="Configuracoes operacionais do processo Uvicorn.",
                )
                time: TimeValues = Field(
                    default_factory=TimeValues,
                    description="Configuracoes de timezone usadas pela aplicacao.",
                )
                httpx_client: HttpxClientValues = Field(
                    default_factory=HttpxClientValues,
                    description="Configuracoes globais do client HTTP assincrono.",
                )
                logging: LoggingValues = Field(
                    default_factory=LoggingValues,
                    description="Configuracoes de logging estruturado.",
                )
                telemetry: TelemetryValues = Field(
                    default_factory=TelemetryValues,
                    description="Configuracoes de instrumentacao OpenTelemetry.",
                )
                mongo: MongoValues = Field(
                    default_factory=MongoValues,
                    description="Configuracoes do provider MongoDB.",
                )
                sql_database: SqlDatabaseValues = Field(
                    default_factory=SqlDatabaseValues,
                    description="Configuracoes do banco SQL da aplicacao.",
                )


            def _find_env_file(start_path: Path | None = None) -> Path | None:
                """Procura `.env` no diretorio atual e nos diretorios pais.

                Parameters
                ----------
                start_path : Path | None
                    Caminho inicial usado na busca. Quando omitido, usa `Path.cwd()`.

                Returns
                -------
                Path | None
                    Caminho do `.env` encontrado ou `None`.
                """

                current_path = start_path or Path.cwd()
                if current_path.is_file():
                    current_path = current_path.parent

                for directory in (current_path, *current_path.parents):
                    env_path = directory / ".env"
                    if env_path.exists():
                        return env_path

                return None


            def _iter_env_settings_paths() -> Iterator[tuple[str, tuple[str, ...]]]:
                """Deriva nomes de ambiente a partir dos dominios de `Settings`.

                Yields
                ------
                tuple[str, tuple[str, ...]]
                    Nome da variavel de ambiente e caminho dentro de `Settings`.
                """

                for domain_name, domain_field in Settings.model_fields.items():
                    domain_type = domain_field.annotation
                    if not isinstance(domain_type, type) or not issubclass(domain_type, BaseModel):
                        continue

                    for value_name in domain_type.model_fields:
                        env_name = f"{domain_name}__{value_name}".upper()
                        yield env_name, (domain_name, value_name)


            def _set_nested_value(
                payload: dict[str, Any],
                path: tuple[str, ...],
                value: Any,
            ) -> None:
                """Define um valor em um dicionario aninhado.

                Parameters
                ----------
                payload : dict[str, Any]
                    Payload acumulado para validacao do Pydantic.
                path : tuple[str, ...]
                    Caminho aninhado do campo em `Settings`.
                value : Any
                    Valor bruto vindo de `.env` ou ambiente.
                """

                current = payload
                for key in path[:-1]:
                    current = current.setdefault(key, {})

                current[path[-1]] = value


            def _coerce_env_value(
                domain_type: type[BaseModel],
                value_name: str,
                value: Any,
            ) -> Any:
                """Converte valores textuais de ambiente para contratos compostos."""

                if not isinstance(value, str):
                    return value

                field_annotation = domain_type.model_fields[value_name].annotation
                if not value.strip() and type(None) in get_args(field_annotation):
                    return None

                if get_origin(field_annotation) is list:
                    stripped_value = value.strip()
                    if not stripped_value:
                        return []

                    if stripped_value.startswith("["):
                        return json.loads(stripped_value)

                    return [item.strip() for item in stripped_value.split(",") if item.strip()]

                return value


            def _colorize(value: str, color: str, enabled: bool) -> str:
                """Aplica cor ANSI quando a saida colorida estiver habilitada."""

                if not enabled:
                    return value

                return f"{color}{value}{_RESET}"


            def _server_runtime_label(settings: Settings) -> tuple[str, str]:
                """Resolve o rotulo visual do ambiente do servidor."""

                environment = settings.app.environment.lower()
                if environment == "production":
                    return "PRD SERVER", _PRD_COLOR

                if settings.is_local or environment in {"local", "development", "test"}:
                    return "LOCAL SERVER", _LOCAL_COLOR

                return f"{environment.upper()} SERVER", _STAGE_COLOR


            def _iter_settings_domains(settings: Settings) -> Iterator[tuple[str, BaseModel]]:
                """Itera apenas dominios Pydantic aninhados em `Settings`."""

                for domain_name in Settings.model_fields:
                    domain_value = getattr(settings, domain_name)
                    if isinstance(domain_value, BaseModel):
                        yield domain_name, domain_value


            def print_settings_variables(
                settings: Settings | None = None,
                *,
                use_colors: bool | None = None,
            ) -> None:
                """Imprime variaveis carregadas no terminal, agrupadas por dominio.

                Parameters
                ----------
                settings : Settings | None
                    Settings ja carregadas. Quando omitido, usa `get_settings()`.
                use_colors : bool | None
                    Controla cores ANSI. Quando omitido, usa cores apenas em TTY.
                """

                effective_settings = settings or get_settings()
                colors_enabled = sys.stdout.isatty() if use_colors is None else use_colors
                runtime_label, runtime_color = _server_runtime_label(effective_settings)
                environment = effective_settings.app.environment
                source = ".env + ambiente" if effective_settings.is_local else "ambiente/defaults"

                print(_colorize(runtime_label, f"{_BOLD}{runtime_color}", colors_enabled))
                print(f"{_colorize('environment', _DIM, colors_enabled)} = {environment}")
                print(f"{_colorize('source', _DIM, colors_enabled)}      = {source}")

                for domain_name, domain_value in _iter_settings_domains(effective_settings):
                    color = _DOMAIN_COLORS.get(domain_name, _BOLD)
                    domain_title = domain_name.upper()
                    print()
                    print(_colorize(domain_title, f"{_BOLD}{color}", colors_enabled))

                    for value_name, value in domain_value.model_dump().items():
                        env_name = f"{domain_name}__{value_name}".upper()
                        print(f"  {_colorize(env_name, color, colors_enabled)}={value}")


            def load_settings(env_path: Path | None = None) -> Settings:
                """Carrega settings com precedencia `.env` menor que ambiente.

                Parameters
                ----------
                env_path : Path | None
                    Caminho opcional do arquivo `.env`. Quando omitido, o loader
                    procura automaticamente no diretorio atual e pais.

                Returns
                -------
                Settings
                    Configuracoes finais validadas.
                """

                requested_env_path = env_path or _find_env_file()
                discovered_env_path = (
                    requested_env_path
                    if requested_env_path is not None and requested_env_path.exists()
                    else None
                )
                env_file_values = dotenv_values(discovered_env_path) if discovered_env_path else {}
                source = {**env_file_values, **os.environ}
                payload: dict[str, Any] = {"is_local": discovered_env_path is not None}

                for env_name, settings_path in _iter_env_settings_paths():
                    value = source.get(env_name)
                    if value is not None:
                        domain_name, value_name = settings_path
                        domain_type = Settings.model_fields[domain_name].annotation
                        parsed_value = _coerce_env_value(
                            domain_type=domain_type,
                            value_name=value_name,
                            value=value,
                        )
                        _set_nested_value(payload=payload, path=settings_path, value=parsed_value)

                return Settings.model_validate(payload)


            @lru_cache(maxsize=1)
            def get_settings() -> Settings:
                """Retorna settings cacheadas para uso por rotas e providers.

                Returns
                -------
                Settings
                    Instancia unica de configuracao validada.
                """

                return load_settings()


            if __name__ == "__main__":
                print_settings_variables()
            ''',
        ),
        FileTemplate(
            "src/configs/httpx_client.py",
            '''
            """Provider singleton para o client HTTPX assincrono."""

            from __future__ import annotations

            import asyncio

            import httpx

            from src.configs.settings import Settings, get_settings
            from src.observability.telemetry.instrumentations import instrument_httpx_client


            _httpx_client: httpx.AsyncClient | None = None
            _streaming_httpx_client: httpx.AsyncClient | None = None
            _httpx_client_lock = asyncio.Lock()
            _streaming_httpx_client_lock = asyncio.Lock()


            async def get_httpx_client(settings: Settings | None = None) -> httpx.AsyncClient:
                """Retorna o singleton assincrono do client HTTPX.

                Parameters
                ----------
                settings : Settings | None
                    Configuracoes da aplicacao. Quando omitidas, usa `get_settings()`.

                Returns
                -------
                httpx.AsyncClient
                    Client HTTP assincrono com timeout e limites explicitos.
                """

                global _httpx_client

                effective_settings = settings or get_settings()
                if _httpx_client is None:
                    async with _httpx_client_lock:
                        if _httpx_client is None:
                            timeout = httpx.Timeout(
                                timeout=effective_settings.httpx_client.timeout_seconds,
                                connect=effective_settings.httpx_client.connect_timeout_seconds,
                            )
                            limits = httpx.Limits(
                                max_connections=effective_settings.httpx_client.max_connections,
                                max_keepalive_connections=(
                                    effective_settings.httpx_client.max_keepalive_connections
                                ),
                            )
                            _httpx_client = httpx.AsyncClient(timeout=timeout, limits=limits)
                            instrument_httpx_client(client=_httpx_client, settings=effective_settings)

                return _httpx_client


            async def get_streaming_httpx_client(
                settings: Settings | None = None,
            ) -> httpx.AsyncClient:
                """Retorna um client HTTPX dedicado a SSE e streaming.

                Parameters
                ----------
                settings : Settings | None
                    Configuracoes da aplicacao. Quando omitidas, usa `get_settings()`.

                Returns
                -------
                httpx.AsyncClient
                    Client HTTP sem spans por chunk, pensado para span manual de inicio/fim.
                """

                global _streaming_httpx_client

                effective_settings = settings or get_settings()
                if _streaming_httpx_client is None:
                    async with _streaming_httpx_client_lock:
                        if _streaming_httpx_client is None:
                            timeout = httpx.Timeout(
                                timeout=effective_settings.httpx_client.timeout_seconds,
                                connect=effective_settings.httpx_client.connect_timeout_seconds,
                            )
                            limits = httpx.Limits(
                                max_connections=effective_settings.httpx_client.max_connections,
                                max_keepalive_connections=(
                                    effective_settings.httpx_client.max_keepalive_connections
                                ),
                            )
                            _streaming_httpx_client = httpx.AsyncClient(
                                timeout=timeout,
                                limits=limits,
                            )

                return _streaming_httpx_client


            async def close_httpx_client() -> None:
                """Fecha os singletons HTTPX quando eles ja foram criados."""

                global _httpx_client, _streaming_httpx_client

                if _httpx_client is not None:
                    await _httpx_client.aclose()
                    _httpx_client = None
                if _streaming_httpx_client is not None:
                    await _streaming_httpx_client.aclose()
                    _streaming_httpx_client = None
            ''',
        ),
        FileTemplate(
            "src/configs/mongo.py",
            '''
            """Provider singleton para MongoDB."""

            from __future__ import annotations

            import asyncio
            from typing import Any

            from src.configs.settings import Settings, get_settings


            _mongo_client: Any | None = None
            _mongo_client_lock = asyncio.Lock()


            async def get_mongo_client(settings: Settings | None = None) -> Any:
                """Retorna o singleton do client MongoDB.

                Parameters
                ----------
                settings : Settings | None
                    Configuracoes da aplicacao. Quando omitidas, usa `get_settings()`.

                Returns
                -------
                Any
                    Instancia `AsyncIOMotorClient` configurada.

                Raises
                ------
                RuntimeError
                    Quando a dependencia `motor` nao estiver instalada.
                """

                global _mongo_client

                effective_settings = settings or get_settings()
                if _mongo_client is None:
                    async with _mongo_client_lock:
                        if _mongo_client is None:
                            try:
                                from pymongo import AsyncMongoClient
                            except ImportError as exc:
                                raise RuntimeError(
                                    "Instale as dependencias do pyproject para usar MongoDB.",
                                ) from exc

                            _mongo_client = AsyncMongoClient(
                                effective_settings.mongo.url,
                                connectTimeoutMS=effective_settings.mongo.connect_timeout_ms,
                                serverSelectionTimeoutMS=(
                                    effective_settings.mongo.server_selection_timeout_ms
                                ),
                                maxPoolSize=effective_settings.mongo.max_pool_size,
                            )

                return _mongo_client


            async def get_mongo_database(settings: Settings | None = None) -> Any:
                """Retorna o database MongoDB configurado.

                Parameters
                ----------
                settings : Settings | None
                    Configuracoes da aplicacao. Quando omitidas, usa `get_settings()`.

                Returns
                -------
                Any
                    Database assincrono do Motor.
                """

                effective_settings = settings or get_settings()
                client = await get_mongo_client(settings=effective_settings)
                return client[effective_settings.mongo.database_name]


            async def close_mongo_client() -> None:
                """Fecha o singleton MongoDB quando ele ja foi criado."""

                global _mongo_client

                if _mongo_client is not None:
                    await _mongo_client.close()
                    _mongo_client = None
            ''',
        ),
        FileTemplate(
            "src/configs/sql_database.py",
            '''
            """Provider singleton para banco SQLAlchemy assincrono."""

            from __future__ import annotations

            import asyncio
            from typing import Any

            from src.configs.settings import Settings, get_settings
            from src.observability.telemetry.instrumentations import instrument_sqlalchemy_engine


            _sql_engine: Any | None = None
            _sql_engine_lock = asyncio.Lock()


            def _is_sqlite_memory_url(url: str) -> bool:
                """Indica se a URL usa SQLite em memoria."""

                return url.startswith("sqlite+aiosqlite:///:memory:")


            async def get_sql_engine(settings: Settings | None = None) -> Any:
                """Retorna o singleton do engine SQLAlchemy assincrono.

                Parameters
                ----------
                settings : Settings | None
                    Configuracoes da aplicacao. Quando omitidas, usa `get_settings()`.

                Returns
                -------
                Any
                    Engine assincrono SQLAlchemy configurado.

                Raises
                ------
                RuntimeError
                    Quando as dependencias SQLAlchemy/aiosqlite nao estiverem instaladas.
                """

                global _sql_engine

                effective_settings = settings or get_settings()
                if _sql_engine is None:
                    async with _sql_engine_lock:
                        if _sql_engine is None:
                            try:
                                from sqlalchemy.ext.asyncio import create_async_engine
                                from sqlalchemy.pool import StaticPool
                            except ImportError as exc:
                                raise RuntimeError(
                                    "Instale as dependencias do pyproject para usar SQLAlchemy.",
                                ) from exc

                            engine_kwargs: dict[str, Any] = {"echo": effective_settings.sql_database.echo}
                            if _is_sqlite_memory_url(effective_settings.sql_database.url):
                                engine_kwargs["poolclass"] = StaticPool
                                engine_kwargs["connect_args"] = {"check_same_thread": False}

                            _sql_engine = create_async_engine(
                                effective_settings.sql_database.url,
                                **engine_kwargs,
                            )
                            instrument_sqlalchemy_engine(
                                engine=_sql_engine.sync_engine,
                                settings=effective_settings,
                            )

                return _sql_engine


            async def close_sql_engine() -> None:
                """Fecha o singleton SQLAlchemy quando ele ja foi criado."""

                global _sql_engine

                if _sql_engine is not None:
                    await _sql_engine.dispose()
                    _sql_engine = None
            ''',
        ),
        FileTemplate(
            "src/configs/values_domains/__init__.py",
            '"""Dominios de valores usados pelo loader de settings."""\n',
        ),
        FileTemplate(
            "src/configs/values_domains/app.py",
            '''
            """Define valores de configuracao da aplicacao."""

            from pydantic import BaseModel, ConfigDict, Field


            class AppValues(BaseModel):
                """Define metadados publicos e operacionais da aplicacao."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                name: str = Field(
                    "$project_name",
                    description="Nome publico da aplicacao usado no OpenAPI.",
                    min_length=1,
                    max_length=80,
                )
                domain: str = Field(
                    "$project_domain",
                    description="Dominio funcional principal atendido pela aplicacao.",
                    min_length=1,
                    max_length=80,
                )
                description: str = Field(
                    "API FastAPI gerada pelo bootstrap.",
                    description="Descricao publica exibida na documentacao OpenAPI.",
                    min_length=1,
                    max_length=240,
                )
                version: str = Field(
                    "0.1.0",
                    description="Versao semantica da aplicacao.",
                    min_length=1,
                    max_length=32,
                )
                environment: str = Field(
                    "local",
                    description="Ambiente operacional atual da aplicacao.",
                    min_length=4,
                    max_length=11,
                    pattern="^(local|development|staging|production|test)$",
                )
                default_api_version: str = Field(
                    "$api_version",
                    description="Versao padrao da API quando a requisicao nao informa uma versao.",
                    min_length=2,
                    max_length=8,
                    pattern="^v[0-9]+$",
                )
                api_version_header_name: str = Field(
                    "X-API-Version",
                    description="Header HTTP usado para propagar a versao identificada da API.",
                    min_length=1,
                    max_length=64,
                )
                docs_url: str | None = Field(
                    "/docs",
                    description="Path publico da documentacao Swagger UI ou `None` para desativar.",
                    min_length=1,
                    max_length=128,
                )
                redoc_url: str | None = Field(
                    "/redoc",
                    description="Path publico da documentacao ReDoc ou `None` para desativar.",
                    min_length=1,
                    max_length=128,
                )
                openapi_url: str | None = Field(
                    "/openapi.json",
                    description="Path publico do schema OpenAPI ou `None` para desativar.",
                    min_length=1,
                    max_length=128,
                )
            ''',
        ),
        FileTemplate(
            "src/configs/values_domains/server.py",
            '''
            """Define valores operacionais do servidor Uvicorn."""

            from pydantic import BaseModel, ConfigDict, Field


            class ServerValues(BaseModel):
                """Define configuracoes de startup do processo HTTP."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                host: str = Field(
                    "0.0.0.0",
                    description="Interface em que o servidor HTTP deve escutar.",
                    min_length=7,
                    max_length=45,
                )
                port: int = Field(
                    8000,
                    description="Porta HTTP usada pelo servidor.",
                    ge=1,
                    le=65535,
                )
                reload: bool = Field(
                    False,
                    description="Indica se o servidor deve reiniciar em alteracoes locais.",
                )
                workers: int = Field(
                    1,
                    description="Quantidade de processos worker do Uvicorn.",
                    ge=1,
                    le=64,
                )
                loop: str = Field(
                    "auto",
                    description="Implementacao de event loop usada pelo Uvicorn.",
                    min_length=4,
                    max_length=7,
                    pattern="^(auto|asyncio|uvloop)$",
                )
                log_level: str = Field(
                    "info",
                    description="Nivel de log usado pelo Uvicorn.",
                    min_length=4,
                    max_length=8,
                    pattern="^(debug|info|warning|error|critical)$",
                )
                proxy_headers: bool = Field(
                    True,
                    description="Indica se headers de proxy devem ser considerados pelo Uvicorn.",
                )
                forwarded_allow_ips: str = Field(
                    "*",
                    description="Lista de IPs autorizados para headers encaminhados por proxy.",
                    min_length=1,
                    max_length=512,
                )
                timeout_keep_alive_seconds: int = Field(
                    5,
                    description="Tempo maximo em segundos para manter conexoes HTTP ociosas.",
                    ge=1,
                    le=300,
                )
                limit_concurrency: int = Field(
                    0,
                    description="Limite de requisicoes concorrentes; `0` desativa o limite.",
                    ge=0,
                    le=100_000,
                )
            ''',
        ),
        FileTemplate(
            "src/configs/values_domains/time.py",
            '''
            """Define valores de tempo e timezone da aplicacao."""

            from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

            from pydantic import BaseModel, ConfigDict, Field, field_validator


            class TimeValues(BaseModel):
                """Define o timezone usado por respostas e tarefas da aplicacao."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                timezone: str = Field(
                    "America/Sao_Paulo",
                    description="Timezone IANA usado para gerar datetimes publicos da aplicacao.",
                    min_length=1,
                    max_length=64,
                    examples=["America/Sao_Paulo"],
                )

                @field_validator("timezone")
                @classmethod
                def validate_timezone(cls, value: str) -> str:
                    """Valida se o timezone existe na base IANA local."""

                    try:
                        ZoneInfo(value)
                    except ZoneInfoNotFoundError as exc:
                        raise ValueError(f"Timezone invalido: {value}") from exc

                    return value
            ''',
        ),
        FileTemplate(
            "src/configs/values_domains/httpx_client.py",
            '''
            """Define valores globais para clients HTTPX."""

            from pydantic import BaseModel, ConfigDict, Field


            class HttpxClientValues(BaseModel):
                """Define limites e timeouts do client HTTP assincrono."""

                model_config = ConfigDict(extra="forbid")

                timeout_seconds: float = Field(
                    30.0,
                    description="Timeout maximo total em segundos para chamadas HTTP externas.",
                    gt=0.0,
                    le=300.0,
                )
                connect_timeout_seconds: float = Field(
                    10.0,
                    description="Timeout maximo em segundos para abertura de conexao HTTP.",
                    gt=0.0,
                    le=120.0,
                )
                max_connections: int = Field(
                    100,
                    description="Quantidade maxima de conexoes HTTP simultaneas.",
                    ge=1,
                    le=10_000,
                )
                max_keepalive_connections: int = Field(
                    20,
                    description="Quantidade maxima de conexoes HTTP mantidas em keep-alive.",
                    ge=0,
                    le=10_000,
                )
            ''',
        ),
        FileTemplate(
            "src/configs/values_domains/logging.py",
            '''
            """Define valores de logging da aplicacao."""

            from pydantic import BaseModel, ConfigDict, Field


            class LoggingValues(BaseModel):
                """Define configuracoes do logging estruturado."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                level: str = Field(
                    "INFO",
                    description="Nivel minimo de log emitido pela aplicacao.",
                    min_length=4,
                    max_length=8,
                    pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
                )
                json_enabled: bool = Field(
                    True,
                    description="Indica se os logs devem ser emitidos em JSON estruturado.",
                )
            ''',
        ),
        FileTemplate(
            "src/configs/values_domains/telemetry.py",
            '''
            """Define valores de instrumentacao OpenTelemetry."""

            from pydantic import BaseModel, ConfigDict, Field


            class TelemetryValues(BaseModel):
                """Define exportadores, sampling e instrumentacoes automaticas."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                enabled: bool = Field(
                    True,
                    description="Indica se a instrumentacao OpenTelemetry deve ser configurada.",
                )
                service_name: str = Field(
                    "$project_name",
                    description="Nome do servico usado como atributo `service.name`.",
                    min_length=1,
                    max_length=128,
                )
                service_namespace: str = Field(
                    "$project_domain",
                    description="Namespace funcional usado para agrupar servicos relacionados.",
                    min_length=1,
                    max_length=128,
                )
                exporter: str = Field(
                    "console",
                    description="Exportador de traces usado pela aplicacao.",
                    min_length=4,
                    max_length=16,
                    pattern="^(none|console|otlp_http|dynatrace)$",
                )
                sample_rate: float = Field(
                    1.0,
                    description="Percentual de traces amostrados, entre 0.0 e 1.0.",
                    ge=0.0,
                    le=1.0,
                )
                excluded_urls: list[str] = Field(
                    default_factory=lambda: ["/health"],
                    description="Paths ou regexes separados por virgula que nao devem gerar spans FastAPI.",
                    min_length=0,
                    max_length=100,
                )
                instrument_fastapi: bool = Field(
                    True,
                    description="Indica se a aplicacao FastAPI deve ser instrumentada automaticamente.",
                )
                fastapi_exclude_internal_spans: bool = Field(
                    True,
                    description="Indica se spans internos ASGI de receive/send devem ser omitidos.",
                )
                instrument_httpx: bool = Field(
                    True,
                    description="Indica se clients HTTPX devem gerar spans automaticamente.",
                )
                httpx_instrumentation_mode: str = Field(
                    "managed_client",
                    description="Modo de instrumentacao HTTPX: desativado, global ou apenas client gerenciado.",
                    min_length=6,
                    max_length=14,
                    pattern="^(disabled|global|managed_client)$",
                )
                instrument_mongo: bool = Field(
                    True,
                    description="Indica se operacoes PyMongo/Mongo devem ser instrumentadas.",
                )
                instrument_sqlalchemy: bool = Field(
                    True,
                    description="Indica se engines SQLAlchemy devem ser instrumentadas.",
                )
                capture_request_headers: list[str] = Field(
                    default_factory=lambda: [
                        "x-request-id",
                        "x-correlation-id",
                        "x-api-version",
                    ],
                    description="Headers seguros de request capturados em spans HTTP.",
                    min_length=0,
                    max_length=100,
                )
                capture_response_headers: list[str] = Field(
                    default_factory=lambda: [
                        "x-request-id",
                        "x-correlation-id",
                        "x-api-version",
                    ],
                    description="Headers seguros de response capturados em spans HTTP.",
                    min_length=0,
                    max_length=100,
                )
                sanitize_fields: list[str] = Field(
                    default_factory=lambda: [
                        "authorization",
                        "cookie",
                        "set-cookie",
                        "password",
                        "token",
                        "api_key",
                        "access_token",
                        "refresh_token",
                    ],
                    description="Campos e headers que devem ser mascarados pela instrumentacao.",
                    min_length=0,
                    max_length=100,
                )
                otlp_traces_endpoint: str = Field(
                    "http://localhost:4318/v1/traces",
                    description="Endpoint OTLP HTTP/protobuf usado para exportar traces.",
                    min_length=1,
                    max_length=2048,
                )
                otlp_headers: str | None = Field(
                    None,
                    description="Headers OTLP no formato `chave=valor,chave2=valor2`, quando necessarios.",
                    min_length=1,
                    max_length=2048,
                )
                otlp_timeout_seconds: float = Field(
                    10.0,
                    description="Timeout maximo em segundos para exportacao OTLP.",
                    gt=0.0,
                    le=120.0,
                )
                dynatrace_endpoint: str | None = Field(
                    None,
                    description="Base URL OTLP da Dynatrace, sem segredo embutido.",
                    min_length=1,
                    max_length=2048,
                )
                dynatrace_api_token: str | None = Field(
                    None,
                    description="Token Dynatrace usado apenas no header Authorization.",
                    min_length=1,
                    max_length=4096,
                )
            ''',
        ),
        FileTemplate(
            "src/configs/values_domains/mongo.py",
            '''
            """Define valores de configuracao do MongoDB."""

            from pydantic import BaseModel, ConfigDict, Field


            class MongoValues(BaseModel):
                """Define configuracoes do provider MongoDB."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                enabled: bool = Field(
                    False,
                    description="Indica se o provider MongoDB deve ser inicializado no lifespan.",
                )
                url: str = Field(
                    "mongodb://localhost:27017",
                    description="URL de conexao MongoDB sem credenciais reais no codigo.",
                    min_length=1,
                    max_length=2048,
                )
                database_name: str = Field(
                    "$project_name",
                    description="Nome do database MongoDB usado pela aplicacao.",
                    min_length=1,
                    max_length=128,
                )
                connect_timeout_ms: int = Field(
                    10_000,
                    description="Timeout maximo em milissegundos para abrir conexoes MongoDB.",
                    ge=100,
                    le=300_000,
                )
                server_selection_timeout_ms: int = Field(
                    10_000,
                    description="Timeout maximo em milissegundos para selecionar servidor MongoDB.",
                    ge=100,
                    le=300_000,
                )
                max_pool_size: int = Field(
                    100,
                    description="Quantidade maxima de conexoes MongoDB no pool.",
                    ge=1,
                    le=10_000,
                )
            ''',
        ),
        FileTemplate(
            "src/configs/values_domains/sql_database.py",
            '''
            """Define valores de configuracao do banco SQL."""

            from pydantic import BaseModel, ConfigDict, Field


            class SqlDatabaseValues(BaseModel):
                """Define configuracoes do provider SQLAlchemy."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                enabled: bool = Field(
                    True,
                    description="Indica se o banco SQL deve ser inicializado no lifespan.",
                )
                url: str = Field(
                    "sqlite+aiosqlite:///:memory:",
                    description="URL SQLAlchemy do banco SQL, com SQLite em memoria por default.",
                    min_length=1,
                    max_length=2048,
                )
                echo: bool = Field(
                    False,
                    description="Indica se o SQLAlchemy deve emitir statements SQL em log.",
                )
            ''',
        ),
        FileTemplate(
            "src/middlewares/__init__.py",
            '"""Middlewares HTTP globais da aplicacao."""\n',
        ),
        FileTemplate(
            "src/middlewares/api_version.py",
            '''
            """Middleware para identificar e propagar a versao da API."""

            from __future__ import annotations

            from collections.abc import Awaitable, Callable
            import re

            from starlette.middleware.base import BaseHTTPMiddleware
            from starlette.requests import Request
            from starlette.responses import Response


            _API_VERSION_PATTERN = re.compile(r"^v[0-9]+$")


            class ApiVersionMiddleware(BaseHTTPMiddleware):
                """Identifica a versao da API para cada requisicao.

                Parameters
                ----------
                app : object
                    Aplicacao ASGI decorada pelo middleware.
                default_api_version : str
                    Versao usada quando header e path nao informam uma versao valida.
                header_name : str
                    Nome do header HTTP usado para entrada e saida da versao.

                Notes
                -----
                A versao identificada fica em `request.state.api_version` e tambem
                volta na resposta pelo header configurado.
                """

                def __init__(
                    self,
                    app: object,
                    default_api_version: str,
                    header_name: str = "X-API-Version",
                ) -> None:
                    super().__init__(app)
                    self._default_api_version = default_api_version
                    self._header_name = header_name

                async def dispatch(
                    self,
                    request: Request,
                    call_next: Callable[[Request], Awaitable[Response]],
                ) -> Response:
                    """Adiciona a versao identificada ao ciclo da requisicao.

                    Parameters
                    ----------
                    request : Request
                        Requisicao HTTP recebida pela aplicacao.
                    call_next : Callable[[Request], Awaitable[Response]]
                        Proximo handler da cadeia ASGI.

                    Returns
                    -------
                    Response
                        Resposta HTTP com header de versao preenchido.
                    """

                    api_version = self._resolve_api_version(request=request)
                    request.state.api_version = api_version

                    response = await call_next(request)
                    response.headers[self._header_name] = api_version
                    return response

                def _resolve_api_version(self, request: Request) -> str:
                    """Resolve a versao por header, path ou fallback configurado."""

                    header_version = request.headers.get(self._header_name)
                    if header_version:
                        normalized_header_version = header_version.strip().lower()
                        if _API_VERSION_PATTERN.fullmatch(normalized_header_version):
                            return normalized_header_version

                    path_version = self._extract_path_version(path=request.url.path)
                    if path_version is not None:
                        return path_version

                    return self._default_api_version

                @staticmethod
                def _extract_path_version(path: str) -> str | None:
                    """Extrai a versao quando o primeiro segmento do path e `vN`."""

                    first_segment = path.strip("/").split("/", maxsplit=1)[0].lower()
                    if _API_VERSION_PATTERN.fullmatch(first_segment):
                        return first_segment

                    return None
            ''',
        ),
        FileTemplate(
            "src/models/__init__.py",
            '"""Modelos publicos e internos da aplicacao."""\n',
        ),
        FileTemplate(
            "src/models/health/__init__.py",
            '"""Modelos do endpoint de health check."""\n',
        ),
        FileTemplate(
            "src/models/health/data/__init__.py",
            '"""Contratos HTTP do endpoint de health check."""\n',
        ),
        FileTemplate(
            "src/models/health/data/health_response.py",
            '''
            """Define contratos de resposta do health check."""

            from pydantic import BaseModel, ConfigDict, Field


            class HealthResponse(BaseModel):
                """Representa dados publicos de saude da aplicacao."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                status: str = Field(
                    ...,
                    description="Estado operacional publico da aplicacao.",
                    min_length=2,
                    max_length=2,
                    pattern="^ok$",
                    examples=["ok"],
                )
                app_name: str = Field(
                    ...,
                    description="Nome publico da aplicacao.",
                    min_length=1,
                    max_length=80,
                    examples=["$project_name"],
                )
                app_version: str = Field(
                    ...,
                    description="Versao semantica atual da aplicacao.",
                    min_length=1,
                    max_length=32,
                    examples=["0.1.0"],
                )
                api_version: str = Field(
                    ...,
                    description="Versao da API identificada para a requisicao.",
                    min_length=2,
                    max_length=8,
                    pattern="^v[0-9]+$",
                    examples=["$api_version"],
                )
                datetime: str = Field(
                    ...,
                    description="Data e hora do health check no timezone configurado da aplicacao.",
                    min_length=20,
                    max_length=64,
                    examples=["2026-05-08T14:25:00-03:00"],
                )
                timezone: str = Field(
                    ...,
                    description="Timezone IANA usado para gerar o campo `datetime`.",
                    min_length=1,
                    max_length=64,
                    examples=["America/Sao_Paulo"],
                )


            class HealthEnvelopeResponse(BaseModel):
                """Envelope publico para resposta do health check."""

                model_config = ConfigDict(extra="forbid")

                data: HealthResponse = Field(
                    ...,
                    description="Dados publicos de saude da aplicacao.",
                )
            ''',
        ),
        FileTemplate(
            "src/observability/__init__.py",
            '"""Configuracoes de observabilidade da aplicacao."""\n',
        ),
        FileTemplate(
            "src/observability/logging/__init__.py",
            '"""Logging estruturado da aplicacao."""\n',
        ),
        FileTemplate(
            "src/observability/telemetry/__init__.py",
            '"""Instrumentacao OpenTelemetry da aplicacao."""\n',
        ),
        FileTemplate(
            "src/observability/telemetry/exporters.py",
            '''
            """Cria exportadores OpenTelemetry a partir de settings."""

            from __future__ import annotations

            from typing import Any

            from src.configs.settings import Settings


            def _parse_headers(raw_headers: str | None) -> dict[str, str] | None:
                """Converte headers textuais para o formato aceito pelo exporter OTLP."""

                if raw_headers is None or not raw_headers.strip():
                    return None

                headers: dict[str, str] = {}
                for item in raw_headers.replace(";", ",").split(","):
                    if not item.strip() or "=" not in item:
                        continue

                    key, value = item.split("=", maxsplit=1)
                    headers[key.strip()] = value.strip()

                return headers or None


            def _dynatrace_traces_endpoint(base_endpoint: str) -> str:
                """Normaliza a URL Dynatrace para o endpoint de traces OTLP HTTP."""

                normalized_endpoint = base_endpoint.rstrip("/")
                if normalized_endpoint.endswith("/v1/traces"):
                    return normalized_endpoint

                return f"{normalized_endpoint}/v1/traces"


            def create_span_processor(settings: Settings) -> Any | None:
                """Cria o processador de spans configurado.

                Parameters
                ----------
                settings : Settings
                    Configuracoes finais contendo exporter e credenciais.

                Returns
                -------
                Any | None
                    Processador de spans pronto para o `TracerProvider` ou `None`.
                """

                exporter_name = settings.telemetry.exporter
                if exporter_name == "none":
                    return None

                from opentelemetry.sdk.trace.export import (
                    BatchSpanProcessor,
                    ConsoleSpanExporter,
                )

                if exporter_name == "console":
                    return BatchSpanProcessor(ConsoleSpanExporter())

                from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                    OTLPSpanExporter,
                )

                if exporter_name == "otlp_http":
                    exporter = OTLPSpanExporter(
                        endpoint=settings.telemetry.otlp_traces_endpoint,
                        headers=_parse_headers(settings.telemetry.otlp_headers),
                        timeout=settings.telemetry.otlp_timeout_seconds,
                    )
                    return BatchSpanProcessor(exporter)

                if exporter_name == "dynatrace":
                    if not settings.telemetry.dynatrace_endpoint:
                        raise ValueError("Configure TELEMETRY__DYNATRACE_ENDPOINT para usar Dynatrace.")
                    if not settings.telemetry.dynatrace_api_token:
                        raise ValueError("Configure TELEMETRY__DYNATRACE_API_TOKEN para usar Dynatrace.")

                    exporter = OTLPSpanExporter(
                        endpoint=_dynatrace_traces_endpoint(
                            settings.telemetry.dynatrace_endpoint,
                        ),
                        headers={
                            "Authorization": (
                                f"Api-Token {settings.telemetry.dynatrace_api_token}"
                            ),
                        },
                        timeout=settings.telemetry.otlp_timeout_seconds,
                    )
                    return BatchSpanProcessor(exporter)

                raise ValueError(f"Exporter OpenTelemetry nao suportado: {exporter_name}")
            ''',
        ),
        FileTemplate(
            "src/observability/telemetry/instrumentations.py",
            '''
            """Registra instrumentacoes automaticas OpenTelemetry."""

            from __future__ import annotations

            import logging
            from typing import Any

            from src.configs.settings import Settings


            logger = logging.getLogger("app.telemetry")
            _httpx_global_instrumented = False
            _mongo_instrumented = False
            _instrumented_httpx_clients: set[int] = set()
            _instrumented_sql_engines: set[int] = set()


            def _excluded_urls(settings: Settings) -> str | None:
                """Retorna URLs excluidas no formato esperado pelos instrumentadores."""

                if not settings.telemetry.excluded_urls:
                    return None

                return ",".join(settings.telemetry.excluded_urls)


            def instrument_fastapi_application(
                app: Any,
                settings: Settings,
                tracer_provider: Any,
            ) -> None:
                """Instrumenta a aplicacao FastAPI quando habilitado."""

                if not settings.telemetry.enabled or not settings.telemetry.instrument_fastapi:
                    return

                try:
                    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
                except ImportError:
                    logger.warning(
                        "Instrumentacao FastAPI indisponivel.",
                        extra={"event": "telemetry.fastapi.unavailable", "layer": "observability"},
                    )
                    return

                kwargs = {
                    "tracer_provider": tracer_provider,
                    "excluded_urls": _excluded_urls(settings=settings),
                    "http_capture_headers_server_request": (
                        settings.telemetry.capture_request_headers
                    ),
                    "http_capture_headers_server_response": (
                        settings.telemetry.capture_response_headers
                    ),
                    "http_capture_headers_sanitize_fields": settings.telemetry.sanitize_fields,
                }
                if settings.telemetry.fastapi_exclude_internal_spans:
                    kwargs["exclude_spans"] = ["receive", "send"]

                try:
                    FastAPIInstrumentor.instrument_app(app, **kwargs)
                except TypeError:
                    FastAPIInstrumentor.instrument_app(
                        app,
                        tracer_provider=tracer_provider,
                        excluded_urls=_excluded_urls(settings=settings),
                    )


            def instrument_httpx_global(settings: Settings, tracer_provider: Any) -> None:
                """Instrumenta todos os clients HTTPX quando o modo global estiver ativo."""

                global _httpx_global_instrumented

                if (
                    not settings.telemetry.enabled
                    or not settings.telemetry.instrument_httpx
                    or settings.telemetry.httpx_instrumentation_mode != "global"
                    or _httpx_global_instrumented
                ):
                    return

                try:
                    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
                except ImportError:
                    logger.warning(
                        "Instrumentacao HTTPX indisponivel.",
                        extra={"event": "telemetry.httpx.unavailable", "layer": "observability"},
                    )
                    return

                try:
                    HTTPXClientInstrumentor().instrument(tracer_provider=tracer_provider)
                except TypeError:
                    HTTPXClientInstrumentor().instrument()
                _httpx_global_instrumented = True


            def instrument_httpx_client(client: Any, settings: Settings) -> None:
                """Instrumenta apenas o client HTTPX gerenciado pela aplicacao."""

                client_id = id(client)
                if (
                    not settings.telemetry.enabled
                    or not settings.telemetry.instrument_httpx
                    or settings.telemetry.httpx_instrumentation_mode != "managed_client"
                    or client_id in _instrumented_httpx_clients
                ):
                    return

                try:
                    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
                except ImportError:
                    logger.warning(
                        "Instrumentacao HTTPX indisponivel.",
                        extra={"event": "telemetry.httpx.unavailable", "layer": "observability"},
                    )
                    return

                HTTPXClientInstrumentor.instrument_client(client)
                _instrumented_httpx_clients.add(client_id)


            def instrument_mongo_global(settings: Settings, tracer_provider: Any) -> None:
                """Instrumenta operacoes PyMongo/Mongo quando habilitado."""

                global _mongo_instrumented

                if (
                    not settings.telemetry.enabled
                    or not settings.telemetry.instrument_mongo
                    or _mongo_instrumented
                ):
                    return

                try:
                    from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
                except ImportError:
                    logger.warning(
                        "Instrumentacao Mongo indisponivel.",
                        extra={"event": "telemetry.mongo.unavailable", "layer": "observability"},
                    )
                    return

                PymongoInstrumentor().instrument(tracer_provider=tracer_provider)
                _mongo_instrumented = True


            def instrument_sqlalchemy_engine(engine: Any, settings: Settings) -> None:
                """Instrumenta um engine SQLAlchemy especifico."""

                engine_id = id(engine)
                if (
                    not settings.telemetry.enabled
                    or not settings.telemetry.instrument_sqlalchemy
                    or engine_id in _instrumented_sql_engines
                ):
                    return

                try:
                    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
                except ImportError:
                    logger.warning(
                        "Instrumentacao SQLAlchemy indisponivel.",
                        extra={"event": "telemetry.sql.unavailable", "layer": "observability"},
                    )
                    return

                SQLAlchemyInstrumentor().instrument(engine=engine)
                _instrumented_sql_engines.add(engine_id)
            ''',
        ),
        FileTemplate(
            "src/observability/telemetry/setup.py",
            '''
            """Configura OpenTelemetry para a aplicacao FastAPI."""

            from __future__ import annotations

            import logging
            from typing import Any

            from src.configs.settings import Settings
            from src.observability.telemetry.exporters import create_span_processor
            from src.observability.telemetry.instrumentations import (
                instrument_fastapi_application,
                instrument_httpx_global,
                instrument_mongo_global,
            )


            logger = logging.getLogger("app.telemetry")
            _telemetry_configured = False


            def _resource_attributes(settings: Settings) -> dict[str, Any]:
                """Monta atributos seguros do recurso OpenTelemetry."""

                return {
                    "service.name": settings.telemetry.service_name,
                    "service.namespace": settings.telemetry.service_namespace,
                    "service.version": settings.app.version,
                    "deployment.environment": settings.app.environment,
                    "app.domain": settings.app.domain,
                }


            def configure_telemetry(app: Any, settings: Settings) -> None:
                """Configura provider, exporter e instrumentacoes OpenTelemetry.

                Parameters
                ----------
                app : Any
                    Aplicacao FastAPI que sera instrumentada.
                settings : Settings
                    Configuracoes finais da aplicacao.
                """

                global _telemetry_configured

                if not settings.telemetry.enabled or _telemetry_configured:
                    return

                try:
                    from opentelemetry import trace
                    from opentelemetry.sdk.resources import Resource
                    from opentelemetry.sdk.trace import TracerProvider
                    from opentelemetry.sdk.trace.sampling import (
                        ParentBased,
                        TraceIdRatioBased,
                    )
                except ImportError:
                    logger.warning(
                        "OpenTelemetry indisponivel; instrumentacao nao configurada.",
                        extra={"event": "telemetry.unavailable", "layer": "observability"},
                    )
                    return

                resource = Resource.create(_resource_attributes(settings=settings))
                tracer_provider = TracerProvider(
                    resource=resource,
                    sampler=ParentBased(TraceIdRatioBased(settings.telemetry.sample_rate)),
                )

                try:
                    span_processor = create_span_processor(settings=settings)
                except ImportError:
                    logger.warning(
                        "Exporter OpenTelemetry indisponivel.",
                        extra={"event": "telemetry.exporter.unavailable", "layer": "observability"},
                    )
                    span_processor = None

                if span_processor is not None:
                    tracer_provider.add_span_processor(span_processor)

                trace.set_tracer_provider(tracer_provider)
                instrument_fastapi_application(
                    app=app,
                    settings=settings,
                    tracer_provider=tracer_provider,
                )
                instrument_httpx_global(settings=settings, tracer_provider=tracer_provider)
                instrument_mongo_global(settings=settings, tracer_provider=tracer_provider)
                _telemetry_configured = True
            ''',
        ),
        FileTemplate(
            "src/observability/telemetry/streaming.py",
            '''
            """Helpers para instrumentar SSE e streaming sem span por chunk."""

            from __future__ import annotations

            from collections.abc import AsyncIterator, Mapping
            from contextlib import asynccontextmanager
            from typing import Any
            from urllib.parse import urlparse


            def _get_tracer() -> Any | None:
                """Retorna o tracer ativo quando OpenTelemetry estiver disponivel."""

                try:
                    from opentelemetry import trace
                except ImportError:
                    return None

                return trace.get_tracer("app.httpx.streaming")


            def _safe_url_attributes(url: str) -> dict[str, str]:
                """Extrai atributos de URL sem expor query string."""

                parsed_url = urlparse(url)
                return {
                    "url.scheme": parsed_url.scheme,
                    "server.address": parsed_url.hostname or "",
                    "url.path": parsed_url.path or "/",
                }


            def _merge_headers(headers: Any | None) -> dict[str, str]:
                """Normaliza headers para permitir injecao de contexto distribuido."""

                if headers is None:
                    return {}

                if isinstance(headers, Mapping):
                    return {str(key): str(value) for key, value in headers.items()}

                return {str(key): str(value) for key, value in dict(headers).items()}


            @asynccontextmanager
            async def stream_request_with_telemetry(
                client: Any,
                method: str,
                url: str,
                **kwargs: Any,
            ) -> AsyncIterator[Any]:
                """Executa streaming HTTPX com um span unico de inicio e fim.

                Parameters
                ----------
                client : Any
                    Client HTTPX assincrono usado para abrir o stream.
                method : str
                    Metodo HTTP usado na requisicao.
                url : str
                    URL de destino. Query string nao e registrada em atributos.
                **kwargs : Any
                    Argumentos repassados para `client.stream`.

                Yields
                ------
                Any
                    Response HTTPX aberta para consumo incremental pelo chamador.

                Notes
                -----
                Esta funcao nao cria spans por evento SSE ou chunk. O span recebe
                apenas um evento de inicio e um evento de fim da conexao.
                """

                tracer = _get_tracer()
                if tracer is None:
                    async with client.stream(method=method, url=url, **kwargs) as response:
                        yield response
                    return

                from opentelemetry import propagate
                from opentelemetry.trace import Status, StatusCode

                headers = _merge_headers(kwargs.pop("headers", None))
                propagate.inject(headers)
                kwargs["headers"] = headers

                with tracer.start_as_current_span("httpx.stream") as span:
                    span.set_attribute("http.request.method", method.upper())
                    span.set_attribute("http.stream", True)
                    for key, value in _safe_url_attributes(url=url).items():
                        span.set_attribute(key, value)
                    span.add_event("httpx.stream.start")

                    try:
                        async with client.stream(method=method, url=url, **kwargs) as response:
                            span.set_attribute("http.response.status_code", response.status_code)
                            yield response
                    except Exception as exc:
                        span.record_exception(exc)
                        span.set_status(Status(StatusCode.ERROR))
                        raise
                    finally:
                        span.add_event("httpx.stream.end")
            ''',
        ),
        FileTemplate(
            "src/observability/logging/logging.py",
            '''
            """Configura logging estruturado da aplicacao."""

            from __future__ import annotations

            import json
            import logging
            from typing import Any

            from src.configs.settings import Settings


            _STANDARD_LOG_RECORD_ATTRS = {
                "args",
                "asctime",
                "created",
                "exc_info",
                "exc_text",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "msg",
                "name",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "stack_info",
                "thread",
                "threadName",
            }
            _SENSITIVE_LOG_KEYS = {
                "authorization",
                "password",
                "secret",
                "token",
                "api_key",
                "access_token",
                "refresh_token",
            }


            class JsonLogFormatter(logging.Formatter):
                """Formata registros de log em JSON estruturado."""

                def format(self, record: logging.LogRecord) -> str:
                    """Serializa um registro de log em JSON seguro.

                    Parameters
                    ----------
                    record : logging.LogRecord
                        Registro emitido pela biblioteca `logging`.

                    Returns
                    -------
                    str
                        Linha JSON pronta para escrita no handler configurado.
                    """

                    payload: dict[str, Any] = {
                        "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
                        "level": record.levelname,
                        "logger": record.name,
                        "message": record.getMessage(),
                        "event": getattr(record, "event", "application.log"),
                        "layer": getattr(record, "layer", "application"),
                    }

                    correlation_id = getattr(record, "correlation_id", None)
                    if correlation_id:
                        payload["correlation_id"] = correlation_id

                    for key, value in record.__dict__.items():
                        if key in _STANDARD_LOG_RECORD_ATTRS or key in payload:
                            continue
                        if key.lower() in _SENSITIVE_LOG_KEYS:
                            continue
                        payload[key] = value

                    if record.exc_info:
                        payload["exception"] = self.formatException(record.exc_info)

                    return json.dumps(payload, default=str, ensure_ascii=False)


            def configure_logging(settings: Settings) -> None:
                """Configura handlers e formato de logging da aplicacao.

                Parameters
                ----------
                settings : Settings
                    Configuracoes finais contendo nivel e formato de log.
                """

                root_logger = logging.getLogger()
                root_logger.handlers.clear()

                handler = logging.StreamHandler()
                if settings.logging.json_enabled:
                    handler.setFormatter(JsonLogFormatter())
                else:
                    handler.setFormatter(
                        logging.Formatter(
                            "%(asctime)s %(levelname)s %(name)s %(message)s",
                        ),
                    )

                root_logger.addHandler(handler)
                root_logger.setLevel(settings.logging.level)
                logging.getLogger("uvicorn.access").setLevel(settings.logging.level)
            ''',
        ),
        FileTemplate(
            "src/repositories/__init__.py",
            '"""Repositories da aplicacao."""\n',
        ),
        FileTemplate(
            "src/routes/__init__.py",
            '"""Rotas HTTP da aplicacao."""\n',
        ),
        FileTemplate(
            "src/routes/health/__init__.py",
            '"""Router de health check."""\n',
        ),
        FileTemplate(
            "src/routes/health/health.py",
            '''
            """Expoe endpoint publico de health check."""

            from datetime import datetime
            from typing import Annotated
            from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

            from fastapi import APIRouter, Depends, Request, status

            from src.configs.settings import Settings, get_settings
            from src.models.health.data.health_response import (
                HealthEnvelopeResponse,
                HealthResponse,
            )


            router = APIRouter(tags=["health"])


            def _current_configured_datetime(settings: Settings) -> str:
                """Retorna data e hora no timezone configurado.

                Parameters
                ----------
                settings : Settings
                    Configuracoes finais contendo o timezone da aplicacao.

                Returns
                -------
                str
                    Datetime ISO 8601 com offset do timezone configurado.

                Raises
                ------
                ZoneInfoNotFoundError
                    Quando o timezone configurado nao existir no sistema.
                """

                try:
                    timezone = ZoneInfo(settings.time.timezone)
                except ZoneInfoNotFoundError:
                    raise

                return datetime.now(tz=timezone).isoformat(timespec="seconds")


            @router.get(
                "/health",
                response_model=HealthEnvelopeResponse,
                status_code=status.HTTP_200_OK,
                summary="Verifica a saude da aplicacao.",
                description="Retorna metadados publicos para probes e diagnostico basico.",
                responses={200: {"description": "Aplicacao saudavel."}},
            )
            async def get_health(
                request: Request,
                settings: Annotated[Settings, Depends(get_settings)],
            ) -> HealthEnvelopeResponse:
                """Retorna o estado publico de saude da aplicacao.

                Parameters
                ----------
                request : Request
                    Requisicao HTTP usada para obter a versao resolvida pelo middleware.
                settings : Settings
                    Configuracoes finais injetadas pelo FastAPI.

                Returns
                -------
                HealthEnvelopeResponse
                    Envelope com status operacional e versoes publicas.
                """

                api_version = getattr(
                    request.state,
                    "api_version",
                    settings.app.default_api_version,
                )
                return HealthEnvelopeResponse(
                    data=HealthResponse(
                        status="ok",
                        app_name=settings.app.name,
                        app_version=settings.app.version,
                        api_version=api_version,
                        datetime=_current_configured_datetime(settings=settings),
                        timezone=settings.time.timezone,
                    ),
                )
            ''',
        ),
        FileTemplate(
            "src/services/__init__.py",
            '"""Services de dominio da aplicacao."""\n',
        ),
        FileTemplate(
            "tests/__init__.py",
            '"""Suite de testes da aplicacao."""\n',
        ),
    ]


def write_files(config: BootstrapConfig, templates: list[FileTemplate]) -> list[Path]:
    """Cria arquivos do projeto no destino configurado."""

    written_files: list[Path] = []
    for file_template in templates:
        destination = config.target_path / file_template.relative_path
        content = file_template.render(config=config)

        if destination.exists() and not config.force:
            print(f"skip   {destination.relative_to(config.target_path)}")
            continue

        print(f"{'would' if config.dry_run else 'write'}  {destination.relative_to(config.target_path)}")
        written_files.append(destination)

        if config.dry_run:
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    return written_files


def parse_args() -> argparse.Namespace:
    """Interpreta argumentos de linha de comando do bootstrap."""

    parser = argparse.ArgumentParser(
        description="Gera a estrutura inicial de uma aplicacao FastAPI.",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Nome publico da aplicacao. Padrao: nome do diretorio alvo.",
    )
    parser.add_argument(
        "--domain",
        default=None,
        help="Dominio funcional principal da aplicacao. Padrao: nome do projeto.",
    )
    parser.add_argument(
        "--api-version",
        default="v1",
        help="Versao inicial da API no formato v1, v2 ou numero inteiro.",
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Diretorio onde a estrutura sera criada.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescreve arquivos existentes.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra arquivos que seriam criados sem escrever no disco.",
    )
    return parser.parse_args()


def main() -> None:
    """Executa o bootstrap a partir dos argumentos de linha de comando."""

    args = parse_args()
    target_path = Path(args.target).resolve()
    project_name = _normalize_name(args.name or target_path.name)
    project_domain = _normalize_name(args.domain or project_name)
    api_version = _normalize_api_version(args.api_version)

    config = BootstrapConfig(
        target_path=target_path,
        project_name=project_name,
        project_domain=project_domain,
        api_version=api_version,
        force=args.force,
        dry_run=args.dry_run,
    )
    templates = build_file_templates()
    written_files = write_files(config=config, templates=templates)

    action = "simulados" if config.dry_run else "criados"
    print(f"\n{len(written_files)} arquivos {action} em {config.target_path}")


if __name__ == "__main__":
    main()
