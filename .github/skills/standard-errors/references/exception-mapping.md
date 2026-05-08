# Mapeamento de Exceções

Use esta referência para converter exceções conhecidas em respostas HTTP padronizadas.

## Tabela Recomendada

| Exceção | Status | Title |
| --- | ---: | --- |
| `DomainValidationError` | 422 | `DOMAIN_VALIDATION_ERROR` |
| `ResourceNotFoundError` | 404 | `RESOURCE_NOT_FOUND` |
| `ConflictError` | 409 | `CONFLICT` |
| `AuthenticationError` | 401 | `UNAUTHORIZED` |
| `AuthorizationError` | 403 | `FORBIDDEN` |
| `ExternalDependencyError` | 502 | `EXTERNAL_DEPENDENCY_ERROR` |
| `UnexpectedApplicationError` | 500 | `INTERNAL_ERROR` |

## Handler

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse


async def resource_not_found_handler(
    request: Request,
    exc: ResourceNotFoundError,
) -> JSONResponse:
    """Converte recurso inexistente no contrato público de erro.

    Parameters
    ----------
    request : Request
        Requisição que originou o erro.
    exc : ResourceNotFoundError
        Exceção de domínio capturada.

    Returns
    -------
    JSONResponse
        Resposta HTTP padronizada para recurso inexistente.
    """

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "errors": [
                {
                    "code": status.HTTP_404_NOT_FOUND,
                    "title": "RESOURCE_NOT_FOUND",
                    "message": "O recurso solicitado não foi encontrado.",
                }
            ]
        },
    )
```

## Regras

- O handler não deve expor `str(exc)` quando a exceção carregar detalhe interno.
- O handler pode usar `request` para logs, mas não deve colocar `Request` no domínio.
- O registro do handler pertence a `fastapi-best-practices`.
