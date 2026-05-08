# Settings Loader

Use `settings.py` como ponto único de montagem da configuração final.

## Regra de Precedência

```text
1. defaults em values_domains
2. arquivo .env, quando existir
3. variáveis de ambiente do processo
```

O loader não deve repetir defaults dos `values_domains`. Defaults, coerção e validação
pertencem aos modelos `ServerValues`, `ExternalApiValues` e demais domínios. O papel do
loader é apenas descobrir as fontes, montar um payload aninhado e deixar o Pydantic
construir `Settings`.

A convenção de nomes deve ser derivada da árvore de `Settings` usando `__` para
separar domínio e campo: `external_api.api_key` vira `EXTERNAL_API__API_KEY`,
`external_api.base_url` vira `EXTERNAL_API__BASE_URL`, `server.reload` vira
`SERVER__RELOAD` e assim por diante.

## Exemplo

```python
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from dotenv import dotenv_values
from pydantic import BaseModel, ConfigDict, Field

from src.configs.values_domains.external_api import ExternalApiValues
from src.configs.values_domains.server import ServerValues


class Settings(BaseModel):
    """Agrupa configurações finais da aplicação.

    Parameters
    ----------
    is_local : bool
        Indica se a configuração foi carregada a partir de `.env` local.
    server : ServerValues
        Configurações HTTP do servidor.
    external_api : ExternalApiValues
        Configurações do provider externo.
    """

    model_config = ConfigDict(extra="forbid")

    is_local: bool = Field(
        False,
        description="Indica se a aplicação carregou um `.env` local.",
    )
    server: ServerValues = Field(
        default_factory=ServerValues,
        description="Configurações HTTP do servidor.",
    )
    external_api: ExternalApiValues = Field(
        default_factory=ExternalApiValues,
        description="Configurações do provider externo.",
    )


def _find_env_file(start_path: Path | None = None) -> Path | None:
    """Procura `.env` no diretório atual e nos diretórios pais."""

    current_path = start_path or Path.cwd()
    if current_path.is_file():
        current_path = current_path.parent

    for directory in (current_path, *current_path.parents):
        env_path = directory / ".env"
        if env_path.exists():
            return env_path

    return None


def _iter_env_settings_paths() -> Iterator[tuple[str, tuple[str, ...]]]:
    """Deriva nomes de ambiente a partir dos domínios declarados em `Settings`."""

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
    """Define um valor em um dicionário aninhado."""

    current = payload
    for key in path[:-1]:
        current = current.setdefault(key, {})

    current[path[-1]] = value


async def load_settings(env_path: Path | None = None) -> Settings:
    """Carrega settings a partir de defaults, `.env` e ambiente.

    Parameters
    ----------
    env_path : Path | None
        Caminho opcional do arquivo `.env`. Quando omitido, o loader procura
        automaticamente um `.env` no repositório a partir do diretório atual.

    Returns
    -------
    Settings
        Configurações finais da aplicação.
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
            _set_nested_value(payload=payload, path=settings_path, value=value)

    return Settings.model_validate(payload)
```

## Regras

- Apenas `settings.py` lê `.env` e `os.environ`.
- Não espalhe leitura de ambiente em providers, services ou repositories.
- Não duplique defaults no loader; defaults ficam nos `values_domains`.
- Não instancie `ServerValues()` ou `ExternalApiValues()` no loader para buscar fallback.
- Não mantenha mapas manuais como `ENV_TO_SETTINGS`; derive os nomes a partir dos
  campos declarados em `Settings`.
- Use `__` para separar domínio e campo em variáveis de ambiente, como
  `SERVER__RELOAD` e `EXTERNAL_API__BASE_URL`.
- Deixe o Pydantic normalizar tipos simples ao validar `Settings`.
- Quando `.env` não existir no repositório, `settings.is_local` deve ser `False` e os
  valores devem vir dos defaults e das variáveis de ambiente do processo.
- Falhas de configuração obrigatória devem aparecer no startup.
