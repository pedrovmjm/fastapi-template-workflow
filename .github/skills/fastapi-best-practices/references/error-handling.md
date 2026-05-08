# Tratamento de Erros

Use handlers para mapear erros conhecidos em respostas previsíveis.

O contrato público do body de erro pertence à skill `standard-errors`. Esta referência define apenas onde registrar handlers e como converter exceções conhecidas sem repetir `try/except` em cada endpoint.

## Regras

- Erros de domínio devem ter tipos próprios.
- Endpoints não devem repetir `try/except` para toda rota.
- Handlers globais devem registrar erro e retornar o contrato público definido por `standard-errors`.
- Mensagens externas devem ser claras, mas sem revelar detalhes internos.
- Erros inesperados devem retornar `500` com mensagem segura.
- `correlation_id` deve ser usado em logs e traces; não adicione ao body de erro salvo decisão explícita em `standard-errors`.

## Exemplo

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class DomainValidationError(Exception):
    """Representa uma violação conhecida de regra de domínio."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


async def domain_validation_error_handler(
    request: Request,
    error: DomainValidationError,
) -> JSONResponse:
    """Converte erro de domínio em resposta HTTP segura.

    Parameters
    ----------
    request : Request
        Requisição que originou o erro.
    error : DomainValidationError
        Erro de domínio capturado.

    Returns
    -------
    JSONResponse
        Resposta HTTP padronizada para falhas de validação de domínio.
    """

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "errors": [
                {
                    "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "title": "DOMAIN_VALIDATION_ERROR",
                    "message": error.message,
                }
            ]
        },
    )


async def register_exception_handlers(app: FastAPI) -> None:
    """Registra handlers de exceção da aplicação.

    Parameters
    ----------
    app : FastAPI
        Aplicação que receberá os handlers.
    """

    app.add_exception_handler(DomainValidationError, domain_validation_error_handler)
```
