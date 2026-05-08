# Provider de Client Externo

Use este padrão para criar um client técnico externo que será injetado em
repositories. A referência deve ser adaptada ao domínio real do provider, como
`payments`, `maps`, `notifications`, `ai` ou outro client de integração.

## Values Domain

```python
from pydantic import BaseModel, ConfigDict, Field


class ExternalApiValues(BaseModel):
    """Define configurações do provider externo.

    Parameters
    ----------
    api_key : str | None
        Chave de API usada para autenticação.
    base_url : str
        URL base da API externa.
    timeout_seconds : float
        Timeout máximo por chamada.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    api_key: str | None = Field(
        None,
        description="Chave de API usada para autenticação no provider externo.",
        min_length=1,
        max_length=512,
    )
    base_url: str = Field(
        "https://api.example.com",
        description="URL base da API externa.",
        min_length=1,
        max_length=2048,
    )
    timeout_seconds: float = Field(
        30.0,
        description="Timeout máximo em segundos para chamadas ao provider externo.",
        gt=0.0,
        le=300.0,
    )
```

## Provider

```python
import asyncio

from external_sdk import AsyncExternalClient

from src.configs.settings import Settings

_external_api_client: AsyncExternalClient | None = None
_external_api_client_lock = asyncio.Lock()


async def get_external_api_client(settings: Settings) -> AsyncExternalClient:
    """Retorna singleton assíncrono do client externo.

    Parameters
    ----------
    settings : Settings
        Configurações finais da aplicação.

    Returns
    -------
    AsyncExternalClient
        Client externo assíncrono configurado.
    """

    global _external_api_client
    if _external_api_client is None:
        async with _external_api_client_lock:
            if _external_api_client is None:
                _external_api_client = AsyncExternalClient(
                    api_key=settings.external_api.api_key,
                    base_url=settings.external_api.base_url,
                    timeout=settings.external_api.timeout_seconds,
                )

    return _external_api_client


async def close_external_api_client() -> None:
    """Fecha o client externo quando ele já foi criado."""

    global _external_api_client
    if _external_api_client is not None:
        await _external_api_client.aclose()
        _external_api_client = None
```

## Regras

- Nomeie o arquivo do provider pelo domínio técnico: `src/configs/{provider}.py`.
- Nomeie o values domain pelo mesmo domínio: `src/configs/values_domains/{provider}.py`.
- Repository recebe o client pelo construtor.
- Service nunca cria client técnico diretamente.
- Segredos, como `{PROVIDER}_API_KEY`, devem vir de `.env` ou variável de ambiente.
- Defaults de configuração devem ficar no values domain, não no provider.
- O provider não deve ler `os.environ` nem `.env`.
- Dados sensíveis enviados ao provider não devem ser logados.
- Quando o SDK expuser `close`/`aclose`, crie função `close_*_client` e registre no
  shutdown/lifespan.
