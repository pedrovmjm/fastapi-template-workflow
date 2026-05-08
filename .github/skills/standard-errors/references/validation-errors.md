# Normalização de Erros de Validação

Use este guia para padronizar erros de validação do FastAPI/Pydantic.

## Objetivo

O FastAPI retorna validações em `detail` por padrão. Neste workflow, a API deve normalizar essas falhas para o envelope `errors`.

## Exemplo de Handler

```python
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Converte erros de validação do FastAPI para o envelope padrão.

    Parameters
    ----------
    request : Request
        Requisição que contém dados inválidos.
    exc : RequestValidationError
        Erro de validação emitido pelo FastAPI.

    Returns
    -------
    JSONResponse
        Resposta HTTP `422` no contrato público de erro.
    """

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "errors": [
                {
                    "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "title": "VALIDATION_ERROR",
                    "message": "A requisição possui campos inválidos.",
                }
            ]
        },
    )
```

## Regras

- Não retorne o array bruto de validações do Pydantic ao cliente sem revisão.
- Não exponha valores recebidos no payload.
- Logs podem registrar contagem e localização dos erros, desde que sem dados sensíveis.
- Se o projeto precisar de erros por campo, evolua esta skill antes de implementar.
