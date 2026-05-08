# Values Domains

Use `values_domains` para declarar a forma e os defaults seguros das configurações.

## Exemplo `server.py`

```python
from pydantic import BaseModel, ConfigDict, Field


class ServerValues(BaseModel):
    """Define configurações HTTP do servidor.

    Parameters
    ----------
    host : str
        Interface em que o servidor deve escutar.
    port : int
        Porta HTTP usada pelo servidor.
    reload : bool
        Indica se o servidor deve reiniciar automaticamente em desenvolvimento.
    """

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
        description="Indica se o servidor deve reiniciar automaticamente em desenvolvimento.",
    )
```

## Regras

- Um arquivo por domínio de configuração.
- Use `BaseModel`, não dicionário solto.
- Todo campo deve usar `Field`.
- Defaults devem ser seguros.
- Segredos devem começar como `None` ou vir obrigatoriamente do ambiente.
