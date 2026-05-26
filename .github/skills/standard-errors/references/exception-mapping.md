# Mapeamento de Exceções

Use esta referência para converter exceções conhecidas em respostas HTTP padronizadas.

## Tabela Recomendada

| Exceção | Status | Title | Log no handler (console) |
| --- | ---: | --- | --- |
| `DomainValidationError` | 422 | `DOMAIN_VALIDATION_ERROR` | `info` (`http.validation.failed`) |
| `ResourceNotFoundError` | 404 | `RESOURCE_NOT_FOUND` | `info` |
| `ConflictError` | 409 | `CONFLICT` | `info` |
| `AuthenticationFailedError` | 401 | `UNAUTHORIZED` | `info` (`http.auth.unauthorized`) |
| `AuthorizationDeniedError` | 403 | `FORBIDDEN` | `info` (`http.auth.forbidden`) |
| `ExternalDependencyError` | 502 | `EXTERNAL_DEPENDENCY_ERROR` | `error` |
| `Exception` (inesperada) | 500 | `INTERNAL_ERROR` | `exception` (`http.internal_error`) |

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
- O handler registra log no console e retorna o envelope `errors[]`; não misture as duas responsabilidades no domínio.
- O handler pode usar `request` para `correlation_id` em logs, mas não deve colocar `Request` no domínio.
- Antes do handler, a camada que falhou registra no console (`warning` para degradação, `error` para falha fatal) sem alterar o envelope HTTP; veja `standard-logs/references/log-levels-vs-http-errors.md`.
- O registro do handler pertence a `fastapi-best-practices` e ao template `src/routes/exception_handlers.py` gerado pelo bootstrap.
