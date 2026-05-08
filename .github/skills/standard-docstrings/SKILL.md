---
name: standard-docstrings
description: Define docstrings obrigatórias em pt-BR no formato NumPy para módulos, classes, funções, endpoints, middlewares, services e repositories, sem definir contratos de dados.
---
# Standard Docstrings - NumPy em pt-BR

Use esta skill para documentar código Python com docstrings fortes, claras e padronizadas no formato NumPy.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando escrever documentação de código no padrão do projeto. | [Docstrings NumPy em pt-BR](references/numpy-docstrings.md) |

## Regras Obrigatórias

- Escreva docstrings em pt-BR.
- Use formato NumPy para módulos, classes, funções e métodos públicos.
- A primeira linha deve ser uma frase objetiva no imperativo conceitual ou descritiva.
- Documente `Parameters`, `Returns`, `Raises`, `Examples` e `Notes` quando aplicável.
- Não repita o óbvio; explique intenção, contrato, limites e efeitos.
- Toda função assíncrona deve deixar claro se executa I/O, consulta externa ou orquestra tarefas.
- Para modelos Pydantic, documente apenas a intenção do modelo; regras de `Field`, limites e wrappers pertencem à skill `standard-data-models`.

## Template de Função

```python
async def get_user(user_id: str) -> UserResponse | None:
    """Busca a resposta pública de um usuário.

    Parameters
    ----------
    user_id : str
        Identificador público do usuário que será consultado.

    Returns
    -------
    UserResponse | None
        Dados públicos do usuário quando encontrado; caso contrário, `None`.

    Raises
    ------
    RepositoryUnavailableError
        Quando a camada de persistência não puder responder à consulta.

    Notes
    -----
    Esta função executa I/O e deve ser aguardada pelo chamador.
    """
```

## Template de Endpoint

```python
@router.get("/{user_id}", response_model=DataWrapperUserResponse)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> DataWrapperUserResponse | Response:
    """Retorna um usuário pelo identificador público.

    Parameters
    ----------
    user_id : str
        Identificador público informado na rota.
    service : UserService
        Serviço de domínio injetado pelo FastAPI.

    Returns
    -------
    DataWrapperUserResponse | Response
        Resposta HTTP `200` com o usuário encontrado ou `204` sem corpo.
    """
```

## Checklist

- [ ] A docstring está em pt-BR.
- [ ] A docstring usa seções NumPy com nomes em inglês técnico.
- [ ] O texto descreve contrato, não implementação trivial.
- [ ] Funções assíncronas documentam efeito de I/O ou orquestração.
- [ ] A docstring não tenta substituir validação, tipagem ou contrato Pydantic.
