# Regras de Campos Pydantic

Use este guia para definir campos Pydantic previsíveis, auditáveis e fáceis de consumir pelo OpenAPI.

## Regra Geral

Todo campo deve declarar:

- tipo explícito;
- `Field(...)`;
- `description` forte;
- mínimo e máximo quando o tipo permitir;
- `examples` quando o valor não for óbvio;
- `pattern` quando houver vocabulário fechado representado como `str`.

Estas regras valem para campos de modelos Pydantic. Query params de endpoints
devem declarar descrição e limites na própria rota com `Query`, porque essa
metadata depende do uso de negócio daquele endpoint.

## Strings

```python
name: str = Field(
    ...,
    description="Nome público do usuário usado para exibição em interfaces e relatórios.",
    min_length=2,
    max_length=120,
    examples=["Maria Oliveira"],
)
```

Use `str` com `pattern` quando o valor precisa continuar simples para serialização, banco ou contratos externos.

```python
status: str = Field(
    ...,
    description="Estado operacional atual do usuário dentro do ciclo de vida da conta.",
    min_length=6,
    max_length=8,
    pattern="^(active|inactive|blocked)$",
    examples=["active"],
)
```

## Inteiros de Modelo

```python
total_records: int = Field(
    ...,
    description="Quantidade total de registros disponíveis para a coleção.",
    ge=1,
    le=100_000,
)
```

## Decimais e Floats

Prefira `Decimal` para dinheiro, taxa financeira e precisão contábil.

```python
score: float = Field(
    ...,
    description="Pontuação calculada para priorização do usuário.",
    ge=0.0,
    le=1.0,
)
```

## Listas

```python
data: list[UserResponse] = Field(
    ...,
    description="Lista de usuários retornados na página atual.",
    min_length=0,
    max_length=200,
)
```

## Opcionais

Todo campo opcional deve explicar quando o valor fica ausente.

```python
deleted_at: str | None = Field(
    None,
    description="Data de exclusão lógica em ISO 8601; ausente quando o usuário está ativo.",
    max_length=32,
)
```

## Proibições

- Não use campo sem `Field`.
- Não use `Any` em contratos públicos sem justificativa.
- Não use `dict` solto quando a estrutura puder virar modelo.
- Não use `Field` para centralizar descrição ou limites de query params de rota; use `Query` dentro do endpoint.
- Não exponha token, senha, segredo, hash, documento ou payload sensível em response.
- Não deixe string sem tamanho máximo.
