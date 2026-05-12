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

            [project.optional-dependencies]
            object-storage-azure = [
                "azure-storage-blob>=12.20.0",
                "aiohttp>=3.9.0",
            ]
            object-storage-aws = [
                "aiobotocore>=2.13.0",
            ]
            object-storage = [
                "azure-storage-blob>=12.20.0",
                "aiohttp>=3.9.0",
                "aiobotocore>=2.13.0",
            ]
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
            APP__CORRELATION_ID_HEADER_NAME=X-Correlation-Id
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

            OBJECT_STORAGE__ENABLED=false
            OBJECT_STORAGE__PROVIDER=azure_blob
            OBJECT_STORAGE__CONTAINER_NAME=
            OBJECT_STORAGE__BUCKET_NAME=
            OBJECT_STORAGE__BASE_PREFIX=
            OBJECT_STORAGE__URL_EXPIRES_SECONDS=3600
            OBJECT_STORAGE__MAX_URL_EXPIRES_SECONDS=86400
            OBJECT_STORAGE__CONNECT_TIMEOUT_SECONDS=10
            OBJECT_STORAGE__READ_TIMEOUT_SECONDS=60
            OBJECT_STORAGE__AZURE_CONNECTION_STRING=
            OBJECT_STORAGE__AZURE_ACCOUNT_URL=
            OBJECT_STORAGE__AZURE_ACCOUNT_NAME=
            OBJECT_STORAGE__AZURE_ACCOUNT_KEY=
            OBJECT_STORAGE__AWS_REGION_NAME=us-east-1
            OBJECT_STORAGE__AWS_ACCESS_KEY_ID=
            OBJECT_STORAGE__AWS_SECRET_ACCESS_KEY=
            OBJECT_STORAGE__AWS_SESSION_TOKEN=
            OBJECT_STORAGE__AWS_ENDPOINT_URL=
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

            from src.configs.settings import get_settings, print_settings_variables
            from src.observability.logging.logging import configure_logging


            def main() -> None:
                """Carrega configuracoes operacionais e executa o Uvicorn.

                Notes
                -----
                Este entrypoint fica fora de `src` de proposito: ele pertence ao
                startup do processo, nao a composicao HTTP da aplicacao.
                """

                settings = get_settings()
                print_settings_variables(settings=settings)
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
            from src.configs.object_storage import (
                close_object_storage_client,
                get_object_storage_client,
            )
            from src.configs.settings import Settings, get_settings
            from src.configs.sql_database import close_sql_engine, get_sql_engine
            from src.middlewares.api_version import ApiVersionMiddleware
            from src.middlewares.correlation_id import CorrelationIdMiddleware
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
                app.state.object_storage_client = (
                    await get_object_storage_client(settings=settings)
                    if settings.object_storage.enabled
                    else None
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
                await close_object_storage_client()
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
                app.add_middleware(
                    CorrelationIdMiddleware,
                    header_name=settings.app.correlation_id_header_name,
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
            from src.configs.values_domains.object_storage import ObjectStorageValues
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
                "object_storage": "\\033[94m",
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
                object_storage : ObjectStorageValues
                    Configuracoes do provider de object storage.
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
                object_storage: ObjectStorageValues = Field(
                    default_factory=ObjectStorageValues,
                    description="Configuracoes do provider de object storage.",
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
            "src/configs/object_storage.py",
            '''
            """Provider singleton para object storage assincrono."""

            from __future__ import annotations

            import asyncio
            from typing import Any

            from src.configs.settings import Settings, get_settings


            _object_storage_client: Any | None = None
            _object_storage_client_context: Any | None = None
            _object_storage_client_lock = asyncio.Lock()


            async def get_object_storage_client(settings: Settings | None = None) -> Any:
                """Retorna o singleton assincrono do client de object storage.

                Parameters
                ----------
                settings : Settings | None
                    Configuracoes da aplicacao. Quando omitidas, usa `get_settings()`.

                Returns
                -------
                Any
                    Client assincrono do provider configurado.

                Raises
                ------
                RuntimeError
                    Quando o provider estiver desabilitado ou a dependencia opcional
                    do provider escolhido nao estiver instalada.
                """

                global _object_storage_client

                effective_settings = settings or get_settings()
                if not effective_settings.object_storage.enabled:
                    raise RuntimeError("Object storage esta desabilitado nas configuracoes.")

                if _object_storage_client is None:
                    async with _object_storage_client_lock:
                        if _object_storage_client is None:
                            if effective_settings.object_storage.provider == "azure_blob":
                                _object_storage_client = _create_azure_blob_client(
                                    settings=effective_settings,
                                )
                            else:
                                _object_storage_client = await _create_aws_s3_client(
                                    settings=effective_settings,
                                )

                return _object_storage_client


            def _create_azure_blob_client(settings: Settings) -> Any:
                """Cria client assincrono Azure Blob usando dependencia opcional."""

                try:
                    from azure.storage.blob.aio import BlobServiceClient
                except ImportError as exc:
                    raise RuntimeError(
                        "Instale o extra `object-storage-azure` para usar Azure Blob.",
                    ) from exc

                storage_settings = settings.object_storage
                client_kwargs = {
                    "connection_timeout": storage_settings.connect_timeout_seconds,
                    "read_timeout": storage_settings.read_timeout_seconds,
                }

                if storage_settings.azure_connection_string:
                    return BlobServiceClient.from_connection_string(
                        storage_settings.azure_connection_string,
                        **client_kwargs,
                    )

                if not storage_settings.azure_account_url:
                    raise RuntimeError(
                        "Configure OBJECT_STORAGE__AZURE_ACCOUNT_URL ou "
                        "OBJECT_STORAGE__AZURE_CONNECTION_STRING para usar Azure Blob.",
                    )

                return BlobServiceClient(
                    account_url=storage_settings.azure_account_url,
                    credential=storage_settings.azure_account_key,
                    **client_kwargs,
                )


            async def _create_aws_s3_client(settings: Settings) -> Any:
                """Cria client assincrono AWS S3 usando dependencia opcional."""

                global _object_storage_client_context

                try:
                    from aiobotocore.session import get_session
                    from botocore.config import Config
                except ImportError as exc:
                    raise RuntimeError(
                        "Instale o extra `object-storage-aws` para usar AWS S3.",
                    ) from exc

                storage_settings = settings.object_storage
                session = get_session()
                client_kwargs: dict[str, Any] = {
                    "region_name": storage_settings.aws_region_name,
                    "config": Config(
                        connect_timeout=storage_settings.connect_timeout_seconds,
                        read_timeout=storage_settings.read_timeout_seconds,
                    ),
                }

                if storage_settings.aws_endpoint_url:
                    client_kwargs["endpoint_url"] = storage_settings.aws_endpoint_url
                if storage_settings.aws_access_key_id:
                    client_kwargs["aws_access_key_id"] = storage_settings.aws_access_key_id
                if storage_settings.aws_secret_access_key:
                    client_kwargs["aws_secret_access_key"] = storage_settings.aws_secret_access_key
                if storage_settings.aws_session_token:
                    client_kwargs["aws_session_token"] = storage_settings.aws_session_token

                _object_storage_client_context = session.create_client("s3", **client_kwargs)
                return await _object_storage_client_context.__aenter__()


            async def close_object_storage_client() -> None:
                """Fecha o singleton de object storage quando ele ja foi criado."""

                global _object_storage_client, _object_storage_client_context

                if _object_storage_client_context is not None:
                    await _object_storage_client_context.__aexit__(None, None, None)
                    _object_storage_client_context = None
                    _object_storage_client = None
                    return

                if _object_storage_client is not None:
                    close = getattr(_object_storage_client, "close", None)
                    if close is not None:
                        result = close()
                        if result is not None:
                            await result
                    _object_storage_client = None
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
                correlation_id_header_name: str = Field(
                    "X-Correlation-Id",
                    description="Header HTTP usado para propagar o correlation id da requisicao.",
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
            "src/configs/values_domains/object_storage.py",
            '''
            """Define valores de configuracao do object storage."""

            from typing import Literal

            from pydantic import BaseModel, ConfigDict, Field


            class ObjectStorageValues(BaseModel):
                """Define configuracoes dos providers Azure Blob e AWS S3."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                enabled: bool = Field(
                    False,
                    description="Indica se object storage deve ser inicializado no lifespan.",
                )
                provider: Literal["azure_blob", "aws_s3"] = Field(
                    "azure_blob",
                    description="Provider de object storage usado pela aplicacao.",
                )
                container_name: str | None = Field(
                    None,
                    description="Container padrao usado pelo Azure Blob.",
                    min_length=1,
                    max_length=256,
                )
                bucket_name: str | None = Field(
                    None,
                    description="Bucket padrao usado pelo AWS S3.",
                    min_length=1,
                    max_length=256,
                )
                base_prefix: str | None = Field(
                    None,
                    description="Prefixo base aplicado aos objetos da aplicacao.",
                    min_length=1,
                    max_length=1024,
                )
                url_expires_seconds: int = Field(
                    3_600,
                    description="Duracao padrao de URLs assinadas, em segundos.",
                    ge=1,
                    le=604_800,
                )
                max_url_expires_seconds: int = Field(
                    86_400,
                    description="Duracao maxima permitida para URLs assinadas.",
                    ge=1,
                    le=604_800,
                )
                connect_timeout_seconds: int = Field(
                    10,
                    description="Timeout maximo para conectar ao provider.",
                    ge=1,
                    le=300,
                )
                read_timeout_seconds: int = Field(
                    60,
                    description="Timeout maximo para leitura no provider.",
                    ge=1,
                    le=3_600,
                )
                azure_connection_string: str | None = Field(
                    None,
                    description="Connection string Azure Blob vinda de variavel segura.",
                    min_length=1,
                    max_length=4096,
                )
                azure_account_url: str | None = Field(
                    None,
                    description="URL da conta Azure Blob.",
                    min_length=1,
                    max_length=2048,
                )
                azure_account_name: str | None = Field(
                    None,
                    description="Nome da conta Azure usado para gerar SAS URL.",
                    min_length=1,
                    max_length=128,
                )
                azure_account_key: str | None = Field(
                    None,
                    description="Chave da conta Azure usada para autenticar e gerar SAS URL.",
                    min_length=1,
                    max_length=2048,
                )
                aws_region_name: str = Field(
                    "us-east-1",
                    description="Regiao AWS usada pelo client S3.",
                    min_length=1,
                    max_length=64,
                )
                aws_access_key_id: str | None = Field(
                    None,
                    description="Access key AWS vinda de variavel segura.",
                    min_length=1,
                    max_length=256,
                )
                aws_secret_access_key: str | None = Field(
                    None,
                    description="Secret key AWS vinda de variavel segura.",
                    min_length=1,
                    max_length=512,
                )
                aws_session_token: str | None = Field(
                    None,
                    description="Token de sessao AWS opcional.",
                    min_length=1,
                    max_length=4096,
                )
                aws_endpoint_url: str | None = Field(
                    None,
                    description="Endpoint S3 customizado, util para LocalStack ou MinIO.",
                    min_length=1,
                    max_length=2048,
                )
            ''',
        ),
        FileTemplate(
            "src/middlewares/__init__.py",
            '"""Middlewares HTTP globais da aplicacao."""\n',
        ),
        FileTemplate(
            "src/middlewares/correlation_id.py",
            '''
            """Middleware para propagar correlation id em requests, logs e traces."""

            from __future__ import annotations

            from collections.abc import Awaitable, Callable
            from uuid import uuid4

            from starlette.middleware.base import BaseHTTPMiddleware
            from starlette.requests import Request
            from starlette.responses import Response

            from src.observability.correlation import set_correlation_id


            class CorrelationIdMiddleware(BaseHTTPMiddleware):
                """Propaga correlation id entre request, contexto local e response.

                Parameters
                ----------
                app : object
                    Aplicacao ASGI decorada pelo middleware.
                header_name : str
                    Nome do header HTTP usado para entrada e saida do correlation id.

                Notes
                -----
                O identificador fica em `request.state.correlation_id`, no contexto
                local assíncrono e no header de resposta.
                """

                def __init__(self, app: object, header_name: str = "X-Correlation-Id") -> None:
                    super().__init__(app)
                    self._header_name = header_name

                async def dispatch(
                    self,
                    request: Request,
                    call_next: Callable[[Request], Awaitable[Response]],
                ) -> Response:
                    """Adiciona correlation id ao ciclo da requisicao.

                    Parameters
                    ----------
                    request : Request
                        Requisicao HTTP recebida pela aplicacao.
                    call_next : Callable[[Request], Awaitable[Response]]
                        Proximo handler da cadeia ASGI.

                    Returns
                    -------
                    Response
                        Resposta HTTP com header de correlation id preenchido.
                    """

                    correlation_id = request.headers.get(self._header_name) or str(uuid4())
                    request.state.correlation_id = correlation_id
                    token = set_correlation_id(correlation_id=correlation_id)
                    try:
                        response = await call_next(request)
                    finally:
                        set_correlation_id(correlation_id=None, token=token)

                    response.headers[self._header_name] = correlation_id
                    return response
            ''',
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
            "src/models/utils/__init__.py",
            '"""Modelos utilitarios compartilhados por contratos HTTP."""\n',
        ),
        FileTemplate(
            "src/models/utils/meta.py",
            '''
            """Define metadados reutilizaveis para respostas HTTP."""

            from pydantic import BaseModel, ConfigDict, Field


            class ResponseMeta(BaseModel):
                """Representa metadados publicos associados a uma resposta HTTP."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

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
                    description="Data e hora da resposta no timezone configurado da aplicacao.",
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
                total_records: int | None = Field(
                    None,
                    description="Quantidade total de registros disponiveis; ausente quando a resposta nao e paginada.",
                    ge=0,
                    le=1_000_000,
                    examples=[150],
                )
                total_pages: int | None = Field(
                    None,
                    description="Quantidade total de paginas disponiveis; ausente quando a resposta nao e paginada.",
                    ge=0,
                    le=100_000,
                    examples=[6],
                )
                page: int | None = Field(
                    None,
                    description="Pagina atual solicitada; ausente quando a resposta nao e paginada.",
                    ge=1,
                    le=100_000,
                    examples=[1],
                )
                page_size: int | None = Field(
                    None,
                    description="Quantidade maxima de itens por pagina; ausente quando a resposta nao e paginada.",
                    ge=1,
                    le=200,
                    examples=[25],
                )
            ''',
        ),
        FileTemplate(
            "src/models/utils/links.py",
            '''
            """Define links reutilizaveis para respostas HTTP."""

            from pydantic import BaseModel, ConfigDict, Field


            class ResponseLinks(BaseModel):
                """Representa links publicos associados a uma resposta HTTP."""

                model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

                self: str = Field(
                    ...,
                    description="URL do recurso ou endpoint que produziu a resposta.",
                    min_length=1,
                    max_length=2048,
                    examples=["http://localhost:8000/health"],
                )
                first: str | None = Field(
                    None,
                    description="URL da primeira pagina; ausente quando a resposta nao e paginada.",
                    max_length=2048,
                    examples=["http://localhost:8000/users?page=1&page_size=25"],
                )
                prev: str | None = Field(
                    None,
                    description="URL da pagina anterior; ausente quando nao existe pagina anterior.",
                    max_length=2048,
                    examples=["http://localhost:8000/users?page=1&page_size=25"],
                )
                next: str | None = Field(
                    None,
                    description="URL da proxima pagina; ausente quando nao existe proxima pagina.",
                    max_length=2048,
                    examples=["http://localhost:8000/users?page=3&page_size=25"],
                )
                last: str | None = Field(
                    None,
                    description="URL da ultima pagina; ausente quando a resposta nao e paginada.",
                    max_length=2048,
                    examples=["http://localhost:8000/users?page=6&page_size=25"],
                )
            ''',
        ),
        FileTemplate(
            "src/models/utils/response_context.py",
            '''
            """Monta metadados e links compartilhados por respostas HTTP."""

            from dataclasses import dataclass
            from datetime import datetime
            from math import ceil
            from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

            from fastapi import Request

            from src.configs.settings import Settings
            from src.models.utils.links import ResponseLinks
            from src.models.utils.meta import ResponseMeta


            @dataclass(frozen=True)
            class ResponseContext:
                """Agrupa metadados e links calculados para uma resposta HTTP."""

                meta: ResponseMeta
                links: ResponseLinks


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


            def _resolve_total_pages(total_records: int | None, page_size: int | None) -> int | None:
                """Calcula total de paginas quando dados de paginacao estao disponiveis."""

                if total_records is None or page_size is None:
                    return None

                if total_records == 0:
                    return 0

                return ceil(total_records / page_size)


            def _build_page_url(request: Request, *, page: int, page_size: int) -> str:
                """Monta URL absoluta para uma pagina especifica."""

                return str(request.url.include_query_params(page=page, page_size=page_size))


            async def build_response_context(
                *,
                request: Request,
                settings: Settings,
                total_records: int | None = None,
                total_pages: int | None = None,
                page: int | None = None,
                page_size: int | None = None,
            ) -> ResponseContext:
                """Monta metadados e links dinamicos para uma resposta HTTP.

                Parameters
                ----------
                request : Request
                    Requisicao HTTP usada para obter URL e versao de API resolvida.
                settings : Settings
                    Configuracoes finais da aplicacao usadas nos metadados publicos.
                total_records : int | None
                    Quantidade total de registros quando a resposta for paginada.
                total_pages : int | None
                    Quantidade total de paginas quando ja calculada pelo service.
                page : int | None
                    Pagina atual quando a resposta for paginada.
                page_size : int | None
                    Tamanho da pagina quando a resposta for paginada.

                Returns
                -------
                ResponseContext
                    Contexto contendo `meta` e `links` prontos para o envelope de resposta.
                """

                api_version = getattr(
                    request.state,
                    "api_version",
                    settings.app.default_api_version,
                )
                resolved_total_pages = total_pages
                if resolved_total_pages is None:
                    resolved_total_pages = _resolve_total_pages(
                        total_records=total_records,
                        page_size=page_size,
                    )

                first_url: str | None = None
                prev_url: str | None = None
                next_url: str | None = None
                last_url: str | None = None
                if page is not None and page_size is not None and resolved_total_pages is not None:
                    if resolved_total_pages > 0:
                        first_url = _build_page_url(request, page=1, page_size=page_size)
                        last_url = _build_page_url(
                            request,
                            page=resolved_total_pages,
                            page_size=page_size,
                        )
                    if page > 1:
                        prev_url = _build_page_url(request, page=page - 1, page_size=page_size)
                    if resolved_total_pages > 0 and page < resolved_total_pages:
                        next_url = _build_page_url(request, page=page + 1, page_size=page_size)

                return ResponseContext(
                    meta=ResponseMeta(
                        app_name=settings.app.name,
                        app_version=settings.app.version,
                        api_version=api_version,
                        datetime=_current_configured_datetime(settings=settings),
                        timezone=settings.time.timezone,
                        total_records=total_records,
                        total_pages=resolved_total_pages,
                        page=page,
                        page_size=page_size,
                    ),
                    links=ResponseLinks(
                        self=str(request.url),
                        first=first_url,
                        prev=prev_url,
                        next=next_url,
                        last=last_url,
                    ),
                )
            ''',
        ),
        FileTemplate(
            "src/models/health/health_response.py",
            '''
            """Define contratos de resposta do health check."""

            from pydantic import BaseModel, ConfigDict, Field

            from src.models.utils.links import ResponseLinks
            from src.models.utils.meta import ResponseMeta


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


            class HealthEnvelopeResponse(BaseModel):
                """Envelope publico para resposta do health check."""

                model_config = ConfigDict(extra="forbid")

                data: HealthResponse = Field(
                    ...,
                    description="Dados publicos de saude da aplicacao.",
                )
                meta: ResponseMeta = Field(
                    ...,
                    description="Metadados publicos da resposta.",
                )
                links: ResponseLinks = Field(
                    ...,
                    description="Links publicos relacionados a resposta.",
                )
            ''',
        ),
        FileTemplate(
            "src/observability/__init__.py",
            '"""Configuracoes de observabilidade da aplicacao."""\n',
        ),
        FileTemplate(
            "src/observability/correlation.py",
            '''
            """Mantem correlation id no contexto assincrono atual."""

            from __future__ import annotations

            from contextvars import ContextVar, Token


            _correlation_id: ContextVar[str | None] = ContextVar(
                "correlation_id",
                default=None,
            )


            def get_current_correlation_id() -> str | None:
                """Retorna o correlation id associado ao contexto atual.

                Returns
                -------
                str | None
                    Identificador da requisicao atual ou `None` fora de request.
                """

                return _correlation_id.get()


            def set_correlation_id(
                *,
                correlation_id: str | None,
                token: Token[str | None] | None = None,
            ) -> Token[str | None] | None:
                """Define ou restaura o correlation id do contexto atual.

                Parameters
                ----------
                correlation_id : str | None
                    Identificador a associar ao contexto quando `token` nao for informado.
                token : Token[str | None] | None
                    Token retornado por chamada anterior, usado para restaurar o contexto.

                Returns
                -------
                Token[str | None] | None
                    Token de restauracao quando um novo valor e definido.
                """

                if token is not None:
                    _correlation_id.reset(token)
                    return None

                return _correlation_id.set(correlation_id)
            ''',
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
            from src.observability.correlation import get_current_correlation_id


            _INVALID_TRACE_ID = 0


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

                def _add_trace_context(self, payload: dict[str, Any]) -> None:
                    """Adiciona trace id e span id do span ativo quando disponiveis."""

                    try:
                        from opentelemetry import trace
                    except ImportError:
                        return

                    span = trace.get_current_span()
                    span_context = span.get_span_context()
                    if not span_context.is_valid or span_context.trace_id == _INVALID_TRACE_ID:
                        return

                    payload["trace_id"] = trace.format_trace_id(span_context.trace_id)
                    payload["span_id"] = trace.format_span_id(span_context.span_id)

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
                    if correlation_id is None:
                        correlation_id = get_current_correlation_id()
                    if correlation_id:
                        payload["correlation_id"] = correlation_id
                    self._add_trace_context(payload=payload)

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
            "src/repository/__init__.py",
            '"""Repositories da aplicacao."""\n',
        ),
        FileTemplate(
            "src/repository/object_storage/__init__.py",
            '"""Repositories para object storage."""\n',
        ),
        FileTemplate(
            "src/repository/object_storage/models.py",
            '''
            """Modelos internos usados pelos repositories de object storage."""

            from __future__ import annotations

            from dataclasses import dataclass
            from datetime import datetime
            from typing import Literal


            ObjectStorageAccessPermission = Literal["read", "write"]


            @dataclass(frozen=True, slots=True)
            class ObjectStorageMetadata:
                """Representa metadados tecnicos de um objeto armazenado."""

                key: str
                size: int
                content_type: str | None = None
                etag: str | None = None
                last_modified: datetime | None = None
                metadata: dict[str, str] | None = None


            @dataclass(frozen=True, slots=True)
            class ObjectStorageItem:
                """Representa um item listado em object storage."""

                key: str
                size: int
                etag: str | None = None
                last_modified: datetime | None = None
            ''',
        ),
        FileTemplate(
            "src/repository/object_storage/exceptions.py",
            '''
            """Excecoes tecnicas comuns para repositories de object storage."""


            class ObjectStorageError(RuntimeError):
                """Erro base para falhas tecnicas de object storage."""


            class ObjectStorageConfigurationError(ObjectStorageError):
                """Indica configuracao ausente ou invalida para object storage."""


            class ObjectStorageNotFoundError(ObjectStorageError):
                """Indica que o objeto solicitado nao foi encontrado."""


            class ObjectStoragePermissionError(ObjectStorageError):
                """Indica falha de permissao no provider de object storage."""


            class ObjectStorageConflictError(ObjectStorageError):
                """Indica conflito tecnico ao executar operacao de object storage."""


            class ObjectStorageTransientError(ObjectStorageError):
                """Indica falha transiente do provider de object storage."""
            ''',
        ),
        FileTemplate(
            "src/repository/object_storage/paths.py",
            '''
            """Normaliza chaves e prefixos para providers de object storage."""


            def resolve_object_key(key: str, base_prefix: str | None = None) -> str:
                """Resolve uma chave de objeto aplicando o prefixo base."""

                normalized_key = key.lstrip("/")
                if not normalized_key.strip("/"):
                    raise ValueError("A chave do objeto nao pode ser vazia.")

                normalized_base = (base_prefix or "").strip("/")
                if not normalized_base:
                    return normalized_key

                return f"{normalized_base}/{normalized_key}"


            def resolve_folder_prefix(prefix: str, base_prefix: str | None = None) -> str:
                """Resolve um prefixo de pasta virtual aplicando o prefixo base."""

                normalized_prefix = prefix.strip("/")
                normalized_base = (base_prefix or "").strip("/")
                parts = [part for part in (normalized_base, normalized_prefix) if part]
                resolved = "/".join(parts)
                if not resolved:
                    return ""

                return f"{resolved}/"


            def remove_base_prefix(key: str, base_prefix: str | None = None) -> str:
                """Remove o prefixo base de uma chave fisica retornada pelo provider."""

                normalized_base = (base_prefix or "").strip("/")
                if not normalized_base:
                    return key

                base = f"{normalized_base}/"
                if key.startswith(base):
                    return key[len(base) :]

                return key
            ''',
        ),
        FileTemplate(
            "src/repository/object_storage/interface.py",
            '''
            """Define contrato comum para repositories de object storage."""

            from __future__ import annotations

            from collections.abc import Mapping
            from typing import Protocol

            from src.repository.object_storage.models import (
                ObjectStorageAccessPermission,
                ObjectStorageItem,
                ObjectStorageMetadata,
            )


            class ObjectStorageRepository(Protocol):
                """Contrato tecnico assincrono para object storage."""

                async def upload_object(
                    self,
                    key: str,
                    content: bytes,
                    *,
                    content_type: str | None = None,
                    metadata: Mapping[str, str] | None = None,
                    overwrite: bool = True,
                ) -> ObjectStorageMetadata:
                    """Envia um objeto para o provider configurado.

                    Parameters
                    ----------
                    key : str
                        Chave tecnica do objeto.
                    content : bytes
                        Conteudo bruto a ser armazenado.
                    content_type : str | None
                        Tipo de conteudo opcional.
                    metadata : Mapping[str, str] | None
                        Metadados tecnicos opcionais.
                    overwrite : bool
                        Indica se um objeto existente pode ser sobrescrito.

                    Returns
                    -------
                    ObjectStorageMetadata
                        Metadados tecnicos do objeto enviado.
                    """

                async def download_object(self, key: str) -> bytes:
                    """Baixa o conteudo bruto de um objeto.

                    Parameters
                    ----------
                    key : str
                        Chave tecnica do objeto.

                    Returns
                    -------
                    bytes
                        Conteudo bruto armazenado.
                    """

                async def object_exists(self, key: str) -> bool:
                    """Indica se um objeto existe no provider.

                    Parameters
                    ----------
                    key : str
                        Chave tecnica do objeto.

                    Returns
                    -------
                    bool
                        `True` quando o objeto existir.
                    """

                async def get_object_metadata(self, key: str) -> ObjectStorageMetadata:
                    """Busca metadados tecnicos de um objeto.

                    Parameters
                    ----------
                    key : str
                        Chave tecnica do objeto.

                    Returns
                    -------
                    ObjectStorageMetadata
                        Metadados tecnicos do objeto.
                    """

                async def list_objects(
                    self,
                    prefix: str = "",
                    *,
                    limit: int | None = None,
                ) -> list[ObjectStorageItem]:
                    """Lista objetos por prefixo tecnico.

                    Parameters
                    ----------
                    prefix : str
                        Prefixo usado para filtrar objetos.
                    limit : int | None
                        Quantidade maxima de itens retornados.

                    Returns
                    -------
                    list[ObjectStorageItem]
                        Objetos encontrados.
                    """

                async def delete_object(self, key: str) -> None:
                    """Remove um objeto do provider.

                    Parameters
                    ----------
                    key : str
                        Chave tecnica do objeto.
                    """

                async def create_folder(self, prefix: str) -> None:
                    """Cria uma pasta virtual por meio de marcador de prefixo.

                    Parameters
                    ----------
                    prefix : str
                        Prefixo da pasta virtual.
                    """

                async def delete_folder(self, prefix: str) -> int:
                    """Remove objetos abaixo de uma pasta virtual.

                    Parameters
                    ----------
                    prefix : str
                        Prefixo da pasta virtual.

                    Returns
                    -------
                    int
                        Quantidade de objetos removidos.
                    """

                async def create_access_url(
                    self,
                    key: str,
                    *,
                    permission: ObjectStorageAccessPermission = "read",
                    expires_in_seconds: int | None = None,
                    content_type: str | None = None,
                ) -> str:
                    """Cria uma URL assinada para acesso temporario ao objeto.

                    Parameters
                    ----------
                    key : str
                        Chave tecnica do objeto.
                    permission : ObjectStorageAccessPermission
                        Permissao concedida pela URL.
                    expires_in_seconds : int | None
                        Duracao em segundos. Quando omitida, usa o default configurado.
                    content_type : str | None
                        Tipo de conteudo esperado para URLs de escrita.

                    Returns
                    -------
                    str
                        URL assinada pelo provider.
                    """
            ''',
        ),
        FileTemplate(
            "src/repository/object_storage/azure_blob.py",
            '''
            """Implementa object storage usando Azure Blob."""

            from __future__ import annotations

            from collections.abc import Awaitable, Callable, Mapping
            from datetime import datetime, timedelta, timezone
            from functools import wraps
            import logging
            from typing import Any, TypeVar, cast

            from azure.core.exceptions import (
                AzureError,
                ClientAuthenticationError,
                ResourceExistsError,
                ResourceNotFoundError,
                ServiceRequestError,
                ServiceResponseError,
            )
            from azure.storage.blob import BlobSasPermissions, ContentSettings, generate_blob_sas
            from opentelemetry import trace
            from opentelemetry.trace import Status, StatusCode

            from src.repository.object_storage.exceptions import (
                ObjectStorageConfigurationError,
                ObjectStorageConflictError,
                ObjectStorageNotFoundError,
                ObjectStoragePermissionError,
                ObjectStorageTransientError,
            )
            from src.repository.object_storage.models import (
                ObjectStorageAccessPermission,
                ObjectStorageItem,
                ObjectStorageMetadata,
            )
            from src.repository.object_storage.paths import (
                remove_base_prefix,
                resolve_folder_prefix,
                resolve_object_key,
            )
            from src.observability.correlation import get_current_correlation_id


            OperationFunc = TypeVar("OperationFunc", bound=Callable[..., Awaitable[Any]])
            logger = logging.getLogger("app.repository.object_storage.azure_blob")
            tracer = trace.get_tracer("app.repository.object_storage.azure_blob")


            def _traced_operation(operation: str) -> Callable[[OperationFunc], OperationFunc]:
                """Instrumenta uma operacao tecnica de object storage.

                Parameters
                ----------
                operation : str
                    Nome estavel da operacao executada pelo repository.

                Returns
                -------
                Callable[[OperationFunc], OperationFunc]
                    Decorator que adiciona span e log seguro de falha.
                """

                def decorator(func: OperationFunc) -> OperationFunc:
                    @wraps(func)
                    async def wrapper(*args: Any, **kwargs: Any) -> Any:
                        with tracer.start_as_current_span(
                            f"object_storage.repository.{operation}",
                        ) as span:
                            span.set_attribute("app.layer", "repository")
                            span.set_attribute("app.provider", "azure_blob")
                            span.set_attribute("app.operation", operation)
                            correlation_id = get_current_correlation_id()
                            if correlation_id is not None:
                                span.set_attribute("app.correlation_id", correlation_id)
                            try:
                                logger.info(
                                    "Operacao de object storage iniciada.",
                                    extra={
                                        "event": "object_storage.operation_started",
                                        "layer": "repository",
                                        "provider": "azure_blob",
                                        "operation": operation,
                                        "correlation_id": correlation_id,
                                    },
                                )
                                result = await func(*args, **kwargs)
                                span.set_attribute("app.result", "success")
                                logger.info(
                                    "Operacao de object storage concluida.",
                                    extra={
                                        "event": "object_storage.operation_succeeded",
                                        "layer": "repository",
                                        "provider": "azure_blob",
                                        "operation": operation,
                                        "correlation_id": correlation_id,
                                    },
                                )
                                return result
                            except Exception as error:
                                span.record_exception(error)
                                span.set_status(Status(StatusCode.ERROR, type(error).__name__))
                                span.set_attribute("app.result", "failed")
                                logger.warning(
                                    "Falha em operacao de object storage.",
                                    extra={
                                        "event": "object_storage.operation_failed",
                                        "layer": "repository",
                                        "provider": "azure_blob",
                                        "operation": operation,
                                        "error_type": type(error).__name__,
                                        "correlation_id": correlation_id,
                                    },
                                )
                                raise

                    return cast(OperationFunc, wrapper)

                return decorator


            class AzureBlobStorageRepository:
                """Executa operacoes tecnicas de object storage no Azure Blob.

                Parameters
                ----------
                blob_service_client : Any
                    Client assincrono `BlobServiceClient` configurado pela camada de configs.
                container_name : str
                    Nome do container usado pela aplicacao.
                base_prefix : str | None
                    Prefixo base aplicado a todas as chaves.
                account_name : str | None
                    Nome da conta Azure usado para gerar SAS URL.
                account_key : str | None
                    Chave da conta Azure usada para gerar SAS URL.
                default_url_expires_seconds : int
                    Duracao padrao de URLs assinadas.
                max_url_expires_seconds : int
                    Duracao maxima permitida para URLs assinadas.
                """

                def __init__(
                    self,
                    blob_service_client: Any,
                    *,
                    container_name: str,
                    base_prefix: str | None = None,
                    account_name: str | None = None,
                    account_key: str | None = None,
                    default_url_expires_seconds: int = 3_600,
                    max_url_expires_seconds: int = 86_400,
                ) -> None:
                    self._client = blob_service_client
                    self._container_name = container_name
                    self._base_prefix = base_prefix
                    self._account_name = account_name
                    self._account_key = account_key
                    self._default_url_expires_seconds = default_url_expires_seconds
                    self._max_url_expires_seconds = max_url_expires_seconds

                @_traced_operation("upload_object")
                async def upload_object(
                    self,
                    key: str,
                    content: bytes,
                    *,
                    content_type: str | None = None,
                    metadata: Mapping[str, str] | None = None,
                    overwrite: bool = True,
                ) -> ObjectStorageMetadata:
                    """Envia um objeto para o Azure Blob."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)
                    blob_client = self._client.get_blob_client(
                        container=self._container_name,
                        blob=object_key,
                    )
                    content_settings = (
                        ContentSettings(content_type=content_type) if content_type else None
                    )

                    try:
                        await blob_client.upload_blob(
                            data=content,
                            overwrite=overwrite,
                            content_settings=content_settings,
                            metadata=dict(metadata or {}),
                        )
                        return await self.get_object_metadata(key=key)
                    except ResourceExistsError as exc:
                        raise ObjectStorageConflictError(
                            "Objeto ja existe no Azure Blob.",
                        ) from exc
                    except ClientAuthenticationError as exc:
                        raise ObjectStoragePermissionError(
                            "Permissao negada pelo Azure Blob.",
                        ) from exc
                    except (ServiceRequestError, ServiceResponseError) as exc:
                        raise ObjectStorageTransientError(
                            "Falha transiente ao enviar objeto para Azure Blob.",
                        ) from exc
                    except AzureError as exc:
                        raise ObjectStorageTransientError(
                            "Falha tecnica ao enviar objeto para Azure Blob.",
                        ) from exc

                @_traced_operation("download_object")
                async def download_object(self, key: str) -> bytes:
                    """Baixa o conteudo bruto de um objeto no Azure Blob."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)
                    blob_client = self._client.get_blob_client(
                        container=self._container_name,
                        blob=object_key,
                    )

                    try:
                        stream = await blob_client.download_blob()
                        return await stream.readall()
                    except ResourceNotFoundError as exc:
                        raise ObjectStorageNotFoundError(
                            "Objeto nao encontrado no Azure Blob.",
                        ) from exc
                    except ClientAuthenticationError as exc:
                        raise ObjectStoragePermissionError(
                            "Permissao negada pelo Azure Blob.",
                        ) from exc
                    except (ServiceRequestError, ServiceResponseError) as exc:
                        raise ObjectStorageTransientError(
                            "Falha transiente ao baixar objeto do Azure Blob.",
                        ) from exc
                    except AzureError as exc:
                        raise ObjectStorageTransientError(
                            "Falha tecnica ao baixar objeto do Azure Blob.",
                        ) from exc

                @_traced_operation("object_exists")
                async def object_exists(self, key: str) -> bool:
                    """Indica se um objeto existe no Azure Blob."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)
                    blob_client = self._client.get_blob_client(
                        container=self._container_name,
                        blob=object_key,
                    )

                    try:
                        return await blob_client.exists()
                    except ClientAuthenticationError as exc:
                        raise ObjectStoragePermissionError(
                            "Permissao negada pelo Azure Blob.",
                        ) from exc
                    except AzureError as exc:
                        raise ObjectStorageTransientError(
                            "Falha tecnica ao verificar objeto no Azure Blob.",
                        ) from exc

                @_traced_operation("get_object_metadata")
                async def get_object_metadata(self, key: str) -> ObjectStorageMetadata:
                    """Busca metadados tecnicos de um objeto no Azure Blob."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)
                    blob_client = self._client.get_blob_client(
                        container=self._container_name,
                        blob=object_key,
                    )

                    try:
                        properties = await blob_client.get_blob_properties()
                    except ResourceNotFoundError as exc:
                        raise ObjectStorageNotFoundError(
                            "Objeto nao encontrado no Azure Blob.",
                        ) from exc
                    except ClientAuthenticationError as exc:
                        raise ObjectStoragePermissionError(
                            "Permissao negada pelo Azure Blob.",
                        ) from exc
                    except AzureError as exc:
                        raise ObjectStorageTransientError(
                            "Falha tecnica ao buscar metadados no Azure Blob.",
                        ) from exc

                    content_settings = getattr(properties, "content_settings", None)
                    return ObjectStorageMetadata(
                        key=key,
                        size=int(getattr(properties, "size", 0) or 0),
                        content_type=getattr(content_settings, "content_type", None),
                        etag=getattr(properties, "etag", None),
                        last_modified=getattr(properties, "last_modified", None),
                        metadata=dict(getattr(properties, "metadata", {}) or {}),
                    )

                @_traced_operation("list_objects")
                async def list_objects(
                    self,
                    prefix: str = "",
                    *,
                    limit: int | None = None,
                ) -> list[ObjectStorageItem]:
                    """Lista objetos por prefixo tecnico no Azure Blob."""

                    resolved_prefix = resolve_folder_prefix(
                        prefix=prefix,
                        base_prefix=self._base_prefix,
                    )
                    container_client = self._client.get_container_client(self._container_name)
                    items: list[ObjectStorageItem] = []

                    try:
                        async for blob in container_client.list_blobs(
                            name_starts_with=resolved_prefix,
                        ):
                            items.append(
                                ObjectStorageItem(
                                    key=remove_base_prefix(
                                        key=str(blob.name),
                                        base_prefix=self._base_prefix,
                                    ),
                                    size=int(getattr(blob, "size", 0) or 0),
                                    etag=getattr(blob, "etag", None),
                                    last_modified=getattr(blob, "last_modified", None),
                                ),
                            )
                            if limit is not None and len(items) >= limit:
                                break
                    except ClientAuthenticationError as exc:
                        raise ObjectStoragePermissionError(
                            "Permissao negada pelo Azure Blob.",
                        ) from exc
                    except AzureError as exc:
                        raise ObjectStorageTransientError(
                            "Falha tecnica ao listar objetos no Azure Blob.",
                        ) from exc

                    return items

                @_traced_operation("delete_object")
                async def delete_object(self, key: str) -> None:
                    """Remove um objeto do Azure Blob."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)
                    blob_client = self._client.get_blob_client(
                        container=self._container_name,
                        blob=object_key,
                    )

                    try:
                        await blob_client.delete_blob()
                    except ResourceNotFoundError:
                        return
                    except ClientAuthenticationError as exc:
                        raise ObjectStoragePermissionError(
                            "Permissao negada pelo Azure Blob.",
                        ) from exc
                    except AzureError as exc:
                        raise ObjectStorageTransientError(
                            "Falha tecnica ao remover objeto do Azure Blob.",
                        ) from exc

                @_traced_operation("create_folder")
                async def create_folder(self, prefix: str) -> None:
                    """Cria uma pasta virtual no Azure Blob."""

                    folder_key = prefix.strip("/")
                    if not folder_key:
                        raise ValueError("O prefixo da pasta nao pode ser vazio.")

                    await self.upload_object(key=f"{folder_key}/", content=b"", overwrite=True)

                @_traced_operation("delete_folder")
                async def delete_folder(self, prefix: str) -> int:
                    """Remove objetos abaixo de uma pasta virtual no Azure Blob."""

                    objects = await self.list_objects(prefix=prefix)
                    for item in objects:
                        await self.delete_object(key=item.key)

                    return len(objects)

                @_traced_operation("create_access_url")
                async def create_access_url(
                    self,
                    key: str,
                    *,
                    permission: ObjectStorageAccessPermission = "read",
                    expires_in_seconds: int | None = None,
                    content_type: str | None = None,
                ) -> str:
                    """Cria uma SAS URL temporaria para um blob."""

                    del content_type

                    if not self._account_key:
                        raise ObjectStorageConfigurationError(
                            "Configure OBJECT_STORAGE__AZURE_ACCOUNT_KEY para gerar SAS URL.",
                        )

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)
                    blob_client = self._client.get_blob_client(
                        container=self._container_name,
                        blob=object_key,
                    )
                    account_name = self._account_name or getattr(blob_client, "account_name", None)
                    if not account_name:
                        raise ObjectStorageConfigurationError(
                            "Configure OBJECT_STORAGE__AZURE_ACCOUNT_NAME para gerar SAS URL.",
                        )

                    ttl = self._resolve_url_ttl(expires_in_seconds=expires_in_seconds)
                    starts_at = datetime.now(timezone.utc)
                    expires_at = starts_at + timedelta(seconds=ttl)
                    sas_token = generate_blob_sas(
                        account_name=account_name,
                        container_name=self._container_name,
                        blob_name=object_key,
                        account_key=self._account_key,
                        permission=BlobSasPermissions(
                            read=permission == "read",
                            write=permission == "write",
                            create=permission == "write",
                        ),
                        start=starts_at,
                        expiry=expires_at,
                    )
                    return f"{blob_client.url}?{sas_token}"

                def _resolve_url_ttl(self, expires_in_seconds: int | None) -> int:
                    """Resolve a duracao efetiva de uma URL assinada."""

                    requested_ttl = expires_in_seconds or self._default_url_expires_seconds
                    if requested_ttl <= 0:
                        raise ValueError("A expiracao da URL deve ser positiva.")

                    return min(requested_ttl, self._max_url_expires_seconds)
            ''',
        ),
        FileTemplate(
            "src/repository/object_storage/aws_s3.py",
            '''
            """Implementa object storage usando AWS S3."""

            from __future__ import annotations

            from collections.abc import Awaitable, Callable, Mapping
            from functools import wraps
            import logging
            from typing import Any, TypeVar, cast

            from botocore.exceptions import ClientError, EndpointConnectionError
            from opentelemetry import trace
            from opentelemetry.trace import Status, StatusCode

            from src.repository.object_storage.exceptions import (
                ObjectStorageConflictError,
                ObjectStorageNotFoundError,
                ObjectStoragePermissionError,
                ObjectStorageTransientError,
            )
            from src.repository.object_storage.models import (
                ObjectStorageAccessPermission,
                ObjectStorageItem,
                ObjectStorageMetadata,
            )
            from src.repository.object_storage.paths import (
                remove_base_prefix,
                resolve_folder_prefix,
                resolve_object_key,
            )
            from src.observability.correlation import get_current_correlation_id


            OperationFunc = TypeVar("OperationFunc", bound=Callable[..., Awaitable[Any]])
            logger = logging.getLogger("app.repository.object_storage.aws_s3")
            tracer = trace.get_tracer("app.repository.object_storage.aws_s3")


            def _traced_operation(operation: str) -> Callable[[OperationFunc], OperationFunc]:
                """Instrumenta uma operacao tecnica de object storage.

                Parameters
                ----------
                operation : str
                    Nome estavel da operacao executada pelo repository.

                Returns
                -------
                Callable[[OperationFunc], OperationFunc]
                    Decorator que adiciona span e log seguro de falha.
                """

                def decorator(func: OperationFunc) -> OperationFunc:
                    @wraps(func)
                    async def wrapper(*args: Any, **kwargs: Any) -> Any:
                        with tracer.start_as_current_span(
                            f"object_storage.repository.{operation}",
                        ) as span:
                            span.set_attribute("app.layer", "repository")
                            span.set_attribute("app.provider", "aws_s3")
                            span.set_attribute("app.operation", operation)
                            correlation_id = get_current_correlation_id()
                            if correlation_id is not None:
                                span.set_attribute("app.correlation_id", correlation_id)
                            try:
                                logger.info(
                                    "Operacao de object storage iniciada.",
                                    extra={
                                        "event": "object_storage.operation_started",
                                        "layer": "repository",
                                        "provider": "aws_s3",
                                        "operation": operation,
                                        "correlation_id": correlation_id,
                                    },
                                )
                                result = await func(*args, **kwargs)
                                span.set_attribute("app.result", "success")
                                logger.info(
                                    "Operacao de object storage concluida.",
                                    extra={
                                        "event": "object_storage.operation_succeeded",
                                        "layer": "repository",
                                        "provider": "aws_s3",
                                        "operation": operation,
                                        "correlation_id": correlation_id,
                                    },
                                )
                                return result
                            except Exception as error:
                                span.record_exception(error)
                                span.set_status(Status(StatusCode.ERROR, type(error).__name__))
                                span.set_attribute("app.result", "failed")
                                logger.warning(
                                    "Falha em operacao de object storage.",
                                    extra={
                                        "event": "object_storage.operation_failed",
                                        "layer": "repository",
                                        "provider": "aws_s3",
                                        "operation": operation,
                                        "error_type": type(error).__name__,
                                        "correlation_id": correlation_id,
                                    },
                                )
                                raise

                    return cast(OperationFunc, wrapper)

                return decorator


            class AwsS3ObjectStorageRepository:
                """Executa operacoes tecnicas de object storage no AWS S3.

                Parameters
                ----------
                s3_client : Any
                    Client assincrono S3 configurado pela camada de configs.
                bucket_name : str
                    Nome do bucket usado pela aplicacao.
                base_prefix : str | None
                    Prefixo base aplicado a todas as chaves.
                default_url_expires_seconds : int
                    Duracao padrao de URLs assinadas.
                max_url_expires_seconds : int
                    Duracao maxima permitida para URLs assinadas.
                """

                def __init__(
                    self,
                    s3_client: Any,
                    *,
                    bucket_name: str,
                    base_prefix: str | None = None,
                    default_url_expires_seconds: int = 3_600,
                    max_url_expires_seconds: int = 86_400,
                ) -> None:
                    self._client = s3_client
                    self._bucket_name = bucket_name
                    self._base_prefix = base_prefix
                    self._default_url_expires_seconds = default_url_expires_seconds
                    self._max_url_expires_seconds = max_url_expires_seconds

                @_traced_operation("upload_object")
                async def upload_object(
                    self,
                    key: str,
                    content: bytes,
                    *,
                    content_type: str | None = None,
                    metadata: Mapping[str, str] | None = None,
                    overwrite: bool = True,
                ) -> ObjectStorageMetadata:
                    """Envia um objeto para o AWS S3."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)
                    if not overwrite and await self.object_exists(key=key):
                        raise ObjectStorageConflictError("Objeto ja existe no AWS S3.")

                    params: dict[str, Any] = {
                        "Bucket": self._bucket_name,
                        "Key": object_key,
                        "Body": content,
                        "Metadata": dict(metadata or {}),
                    }
                    if content_type:
                        params["ContentType"] = content_type

                    try:
                        await self._client.put_object(**params)
                        return await self.get_object_metadata(key=key)
                    except ClientError as exc:
                        self._raise_client_error(
                            exc=exc,
                            transient_message="Falha tecnica ao enviar objeto para AWS S3.",
                        )
                    except EndpointConnectionError as exc:
                        raise ObjectStorageTransientError(
                            "Falha de conexao ao enviar objeto para AWS S3.",
                        ) from exc

                @_traced_operation("download_object")
                async def download_object(self, key: str) -> bytes:
                    """Baixa o conteudo bruto de um objeto no AWS S3."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)

                    try:
                        response = await self._client.get_object(
                            Bucket=self._bucket_name,
                            Key=object_key,
                        )
                        async with response["Body"] as stream:
                            return await stream.read()
                    except ClientError as exc:
                        self._raise_client_error(
                            exc=exc,
                            not_found_message="Objeto nao encontrado no AWS S3.",
                            transient_message="Falha tecnica ao baixar objeto do AWS S3.",
                        )
                    except EndpointConnectionError as exc:
                        raise ObjectStorageTransientError(
                            "Falha de conexao ao baixar objeto do AWS S3.",
                        ) from exc

                @_traced_operation("object_exists")
                async def object_exists(self, key: str) -> bool:
                    """Indica se um objeto existe no AWS S3."""

                    try:
                        await self.get_object_metadata(key=key)
                    except ObjectStorageNotFoundError:
                        return False

                    return True

                @_traced_operation("get_object_metadata")
                async def get_object_metadata(self, key: str) -> ObjectStorageMetadata:
                    """Busca metadados tecnicos de um objeto no AWS S3."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)

                    try:
                        response = await self._client.head_object(
                            Bucket=self._bucket_name,
                            Key=object_key,
                        )
                    except ClientError as exc:
                        self._raise_client_error(
                            exc=exc,
                            not_found_message="Objeto nao encontrado no AWS S3.",
                            transient_message="Falha tecnica ao buscar metadados no AWS S3.",
                        )
                    except EndpointConnectionError as exc:
                        raise ObjectStorageTransientError(
                            "Falha de conexao ao buscar metadados no AWS S3.",
                        ) from exc

                    return ObjectStorageMetadata(
                        key=key,
                        size=int(response.get("ContentLength", 0) or 0),
                        content_type=response.get("ContentType"),
                        etag=response.get("ETag"),
                        last_modified=response.get("LastModified"),
                        metadata=dict(response.get("Metadata", {}) or {}),
                    )

                @_traced_operation("list_objects")
                async def list_objects(
                    self,
                    prefix: str = "",
                    *,
                    limit: int | None = None,
                ) -> list[ObjectStorageItem]:
                    """Lista objetos por prefixo tecnico no AWS S3."""

                    resolved_prefix = resolve_folder_prefix(
                        prefix=prefix,
                        base_prefix=self._base_prefix,
                    )
                    items: list[ObjectStorageItem] = []
                    continuation_token: str | None = None

                    try:
                        while True:
                            page_size = min(limit - len(items), 1000) if limit else 1000
                            params: dict[str, Any] = {
                                "Bucket": self._bucket_name,
                                "Prefix": resolved_prefix,
                                "MaxKeys": page_size,
                            }
                            if continuation_token:
                                params["ContinuationToken"] = continuation_token

                            response = await self._client.list_objects_v2(**params)
                            for item in response.get("Contents", []):
                                items.append(
                                    ObjectStorageItem(
                                        key=remove_base_prefix(
                                            key=str(item["Key"]),
                                            base_prefix=self._base_prefix,
                                        ),
                                        size=int(item.get("Size", 0) or 0),
                                        etag=item.get("ETag"),
                                        last_modified=item.get("LastModified"),
                                    ),
                                )

                            if limit is not None and len(items) >= limit:
                                return items
                            if not response.get("IsTruncated"):
                                return items

                            continuation_token = response.get("NextContinuationToken")
                    except ClientError as exc:
                        self._raise_client_error(
                            exc=exc,
                            transient_message="Falha tecnica ao listar objetos no AWS S3.",
                        )
                    except EndpointConnectionError as exc:
                        raise ObjectStorageTransientError(
                            "Falha de conexao ao listar objetos no AWS S3.",
                        ) from exc

                @_traced_operation("delete_object")
                async def delete_object(self, key: str) -> None:
                    """Remove um objeto do AWS S3."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)

                    try:
                        await self._client.delete_object(Bucket=self._bucket_name, Key=object_key)
                    except ClientError as exc:
                        self._raise_client_error(
                            exc=exc,
                            transient_message="Falha tecnica ao remover objeto do AWS S3.",
                        )
                    except EndpointConnectionError as exc:
                        raise ObjectStorageTransientError(
                            "Falha de conexao ao remover objeto do AWS S3.",
                        ) from exc

                @_traced_operation("create_folder")
                async def create_folder(self, prefix: str) -> None:
                    """Cria uma pasta virtual no AWS S3."""

                    folder_key = prefix.strip("/")
                    if not folder_key:
                        raise ValueError("O prefixo da pasta nao pode ser vazio.")

                    await self.upload_object(key=f"{folder_key}/", content=b"", overwrite=True)

                @_traced_operation("delete_folder")
                async def delete_folder(self, prefix: str) -> int:
                    """Remove objetos abaixo de uma pasta virtual no AWS S3."""

                    objects = await self.list_objects(prefix=prefix)
                    if not objects:
                        return 0

                    for start in range(0, len(objects), 1000):
                        chunk = objects[start : start + 1000]
                        await self._client.delete_objects(
                            Bucket=self._bucket_name,
                            Delete={
                                "Objects": [{"Key": item.key} for item in chunk],
                                "Quiet": True,
                            },
                        )

                    return len(objects)

                @_traced_operation("create_access_url")
                async def create_access_url(
                    self,
                    key: str,
                    *,
                    permission: ObjectStorageAccessPermission = "read",
                    expires_in_seconds: int | None = None,
                    content_type: str | None = None,
                ) -> str:
                    """Cria uma presigned URL temporaria para um objeto S3."""

                    object_key = resolve_object_key(key=key, base_prefix=self._base_prefix)
                    ttl = self._resolve_url_ttl(expires_in_seconds=expires_in_seconds)
                    client_method = "get_object" if permission == "read" else "put_object"
                    params: dict[str, Any] = {
                        "Bucket": self._bucket_name,
                        "Key": object_key,
                    }
                    if permission == "write" and content_type:
                        params["ContentType"] = content_type

                    return await self._client.generate_presigned_url(
                        ClientMethod=client_method,
                        Params=params,
                        ExpiresIn=ttl,
                        HttpMethod="GET" if permission == "read" else "PUT",
                    )

                def _resolve_url_ttl(self, expires_in_seconds: int | None) -> int:
                    """Resolve a duracao efetiva de uma URL assinada."""

                    requested_ttl = expires_in_seconds or self._default_url_expires_seconds
                    if requested_ttl <= 0:
                        raise ValueError("A expiracao da URL deve ser positiva.")

                    return min(requested_ttl, self._max_url_expires_seconds)

                def _raise_client_error(
                    self,
                    *,
                    exc: ClientError,
                    not_found_message: str = "Objeto nao encontrado no AWS S3.",
                    transient_message: str,
                ) -> None:
                    """Traduz erro do botocore para excecao tecnica conhecida."""

                    error_code = str(exc.response.get("Error", {}).get("Code", ""))
                    if error_code in {"404", "NoSuchKey", "NotFound"}:
                        raise ObjectStorageNotFoundError(not_found_message) from exc
                    if error_code in {"401", "403", "AccessDenied", "InvalidAccessKeyId"}:
                        raise ObjectStoragePermissionError(
                            "Permissao negada pelo AWS S3.",
                        ) from exc
                    if error_code in {"BucketAlreadyExists", "BucketAlreadyOwnedByYou"}:
                        raise ObjectStorageConflictError(
                            "Conflito tecnico no AWS S3.",
                        ) from exc

                    raise ObjectStorageTransientError(transient_message) from exc
            ''',
        ),
        FileTemplate(
            "src/repository/object_storage/factory.py",
            '''
            """Cria repositories de object storage a partir de settings e clients."""

            from __future__ import annotations

            from typing import Any

            from src.configs.settings import Settings
            from src.repository.object_storage.exceptions import (
                ObjectStorageConfigurationError,
            )
            from src.repository.object_storage.interface import ObjectStorageRepository


            def build_object_storage_repository(
                *,
                client: Any,
                settings: Settings,
            ) -> ObjectStorageRepository:
                """Cria repository de object storage para o provider configurado.

                Parameters
                ----------
                client : Any
                    Client assincrono criado pela camada de configs.
                settings : Settings
                    Configuracoes finais da aplicacao.

                Returns
                -------
                ObjectStorageRepository
                    Repository tecnico do provider configurado.
                """

                storage_settings = settings.object_storage
                if storage_settings.provider == "azure_blob":
                    if not storage_settings.container_name:
                        raise ObjectStorageConfigurationError(
                            "Configure OBJECT_STORAGE__CONTAINER_NAME para usar Azure Blob.",
                        )

                    from src.repository.object_storage.azure_blob import (
                        AzureBlobStorageRepository,
                    )

                    return AzureBlobStorageRepository(
                        client,
                        container_name=storage_settings.container_name,
                        base_prefix=storage_settings.base_prefix,
                        account_name=storage_settings.azure_account_name,
                        account_key=storage_settings.azure_account_key,
                        default_url_expires_seconds=storage_settings.url_expires_seconds,
                        max_url_expires_seconds=storage_settings.max_url_expires_seconds,
                    )

                if not storage_settings.bucket_name:
                    raise ObjectStorageConfigurationError(
                        "Configure OBJECT_STORAGE__BUCKET_NAME para usar AWS S3.",
                    )

                from src.repository.object_storage.aws_s3 import AwsS3ObjectStorageRepository

                return AwsS3ObjectStorageRepository(
                    client,
                    bucket_name=storage_settings.bucket_name,
                    base_prefix=storage_settings.base_prefix,
                    default_url_expires_seconds=storage_settings.url_expires_seconds,
                    max_url_expires_seconds=storage_settings.max_url_expires_seconds,
                )
            ''',
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

            import logging
            from typing import Annotated

            from fastapi import APIRouter, Depends, Request, status
            from opentelemetry import trace

            from src.configs.settings import Settings, get_settings
            from src.models.health.health_response import (
                HealthEnvelopeResponse,
                HealthResponse,
            )
            from src.models.utils.response_context import build_response_context


            router = APIRouter(tags=["health"])
            logger = logging.getLogger("app.routes.health")
            tracer = trace.get_tracer("app.routes.health")


            @router.get(
                "/health",
                response_model=HealthEnvelopeResponse,
                response_model_exclude_none=True,
                status_code=status.HTTP_200_OK,
                summary="Verifica a saude da aplicacao.",
                description="Retorna metadados publicos para probes e diagnostico basico.",
                responses={200: {"description": "Aplicacao saudavel."}},
            )
            async def get_health(
                request: Request,
                settings: Annotated[Settings, Depends(get_settings)],
            ) -> HealthEnvelopeResponse:
                """Retorna a disponibilidade publica minima da aplicacao.

                Este endpoint existe para probes de infraestrutura, diagnostico operacional
                basico e validacao da versao de API resolvida para a requisicao. Ele nao
                executa regras de negocio nem valida dependencias externas profundas; a
                intencao de negocio e responder rapidamente se o processo HTTP esta ativo e
                qual contexto publico da aplicacao gerou a resposta.

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

                correlation_id = getattr(request.state, "correlation_id", None)
                with tracer.start_as_current_span("health.endpoint.get_health") as span:
                    span.set_attribute("app.layer", "endpoint")
                    span.set_attribute("app.operation", "get_health")
                    if correlation_id is not None:
                        span.set_attribute("app.correlation_id", correlation_id)

                    logger.info(
                        "Health check recebido.",
                        extra={
                            "event": "health.request_received",
                            "layer": "endpoint",
                            "correlation_id": correlation_id,
                        },
                    )
                    response_context = await build_response_context(
                        request=request,
                        settings=settings,
                    )
                    span.set_attribute("app.result", "ok")
                    logger.info(
                        "Health check respondido com sucesso.",
                        extra={
                            "event": "health.request_succeeded",
                            "layer": "endpoint",
                            "status": "ok",
                            "correlation_id": correlation_id,
                        },
                    )
                    return HealthEnvelopeResponse(
                        data=HealthResponse(
                            status="ok",
                        ),
                        meta=response_context.meta,
                        links=response_context.links,
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
