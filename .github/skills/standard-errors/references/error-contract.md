# Contrato Público de Erro

Use este contrato para toda resposta HTTP de erro.

## Formato Obrigatório

```json
{
  "errors": [
    {
      "code": 404,
      "title": "RESOURCE_NOT_FOUND",
      "message": "O recurso solicitado não foi encontrado."
    }
  ]
}
```

## Regras

- O campo raiz deve ser `errors`.
- `errors` deve ser uma lista.
- Cada item deve conter `code`, `title` e `message`.
- `code` deve ser o mesmo status HTTP numérico da resposta.
- `title` deve ser estável, em `UPPER_SNAKE_CASE` e adequado para automação.
- `message` deve ser em pt-BR, segura e compreensível para o consumidor da API.
- Não inclua `stack`, `traceback`, SQL, token, documento, payload sensível ou detalhe de infraestrutura.

## Modelo Pydantic

```python
from pydantic import BaseModel, ConfigDict, Field


class ErrorResponseItem(BaseModel):
    """Representa um erro público retornado pela API."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    code: int = Field(
        ...,
        description="Código HTTP/status numérico retornado pela resposta.",
        ge=100,
        le=599,
    )
    title: str = Field(
        ...,
        description="Identificador estável e legível por máquina que classifica o erro.",
        min_length=1,
        max_length=80,
        pattern="^[A-Z][A-Z0-9_]*$",
    )
    message: str = Field(
        ...,
        description="Mensagem segura que explica a falha sem expor detalhes internos.",
        min_length=1,
        max_length=500,
    )


class ErrorResponse(BaseModel):
    """Envelope padrão para respostas de erro da API."""

    model_config = ConfigDict(extra="forbid")

    errors: list[ErrorResponseItem] = Field(
        ...,
        description="Lista de erros retornados pela operação.",
        min_length=1,
        max_length=100,
    )
```
