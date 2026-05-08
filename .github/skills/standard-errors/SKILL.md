---
name: standard-errors
description: Padroniza contratos de erro em APIs FastAPI, garantindo que toda resposta de erro seja encapsulada em errors com code, title e message.
---
# Standard Errors - Convenção de Erros

Use esta skill ao criar ou revisar erros HTTP, handlers de exceção, responses de erro e modelos Pydantic de erro.

## Responsabilidade Desta Skill

Esta skill é dona de:

- formato público das respostas de erro;
- nomes e conteúdo dos campos de erro;
- padronização de `code`, `title` e `message`;
- exemplos de responses de erro em endpoints;
- consistência entre exceptions, handlers e contratos HTTP.

Esta skill não é dona de:

- códigos HTTP esperados por endpoint: use `standard-endpoints`;
- logs de falha: use `standard-logs`;
- traces e correlação distribuída: use `standard-traces`;
- regras gerais de modelos Pydantic: use `standard-data-models`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar contrato público de erro. | [Contrato público de erro](references/error-contract.md) |
| Quando precisar aprofundar mapeamento de exceções. | [Mapeamento de exceções](references/exception-mapping.md) |
| Quando precisar aprofundar normalização de erros de validação. | [Normalização de erros de validação](references/validation-errors.md) |

## Regras Obrigatórias

- Toda resposta de erro deve ser encapsulada no campo raiz `errors`.
- `errors` deve ser uma lista, mesmo quando houver apenas um erro.
- Cada item de `errors` deve conter sempre `code`, `title` e `message`.
- `code` deve ser o código HTTP/status numérico retornado pela resposta.
- `title` deve ser estável, legível por máquina e em `UPPER_SNAKE_CASE`.
- `message` deve explicar a falha de forma segura, sem expor detalhes internos.
- Não exponha stack trace, SQL, tokens, documentos, payloads sensíveis ou detalhes de infraestrutura.
- Erros de validação devem seguir o mesmo envelope `errors`.
- Não retorne erro solto em `detail`, `error`, `message` ou strings avulsas.

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

## Modelos Recomendados

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
        examples=[404],
    )
    title: str = Field(
        ...,
        description="Identificador estável e legível por máquina que classifica o erro.",
        min_length=1,
        max_length=80,
        pattern="^[A-Z][A-Z0-9_]*$",
        examples=["RESOURCE_NOT_FOUND"],
    )
    message: str = Field(
        ...,
        description="Mensagem segura que explica a falha sem expor detalhes internos.",
        min_length=1,
        max_length=500,
        examples=["O recurso solicitado não foi encontrado."],
    )


class ErrorResponse(BaseModel):
    """Envelope padrão para respostas de erro da API."""

    model_config = ConfigDict(extra="forbid")

    errors: list[ErrorResponseItem] = Field(
        ...,
        description="Lista de erros retornados pela operação.",
        min_length=1,
    )
```

## Exemplo em Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse


async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError) -> JSONResponse:
    """Converte erro de recurso inexistente para o contrato HTTP padrão."""

    return JSONResponse(
        status_code=404,
        content={
            "errors": [
                {
                    "code": 404,
                    "title": "RESOURCE_NOT_FOUND",
                    "message": "O recurso solicitado não foi encontrado.",
                }
            ]
        },
    )
```

## Exemplos de Titles

- `VALIDATION_ERROR`: payload, query param ou path param inválido.
- `RESOURCE_NOT_FOUND`: recurso solicitado não existe ou não está disponível.
- `CONFLICT`: operação conflita com o estado atual do recurso.
- `UNAUTHORIZED`: autenticação ausente ou inválida.
- `FORBIDDEN`: usuário autenticado não tem permissão para a operação.
- `INTERNAL_ERROR`: falha inesperada sem detalhes internos expostos.

## Checklist

- [ ] Response possui campo raiz `errors`.
- [ ] `errors` é uma lista com pelo menos um item.
- [ ] Cada item possui `code`, `title` e `message`.
- [ ] `code` é o código HTTP/status numérico da resposta.
- [ ] `title` está em `UPPER_SNAKE_CASE` e é estável.
- [ ] `message` está em pt-BR.
- [ ] A mensagem não expõe detalhes sensíveis ou internos.
- [ ] Erros de validação seguem o mesmo envelope.
