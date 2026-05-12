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
- Docstrings de endpoints devem explicar a intenção de negócio da rota: qual operação ela habilita, qual estado de negócio consulta ou altera e quais limites de escopo são deliberados.
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
@router.get("/{user_id}", response_model=UserEnvelopeResponse)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> UserEnvelopeResponse | Response:
    """Consulta a visão pública de um usuário pelo identificador.

    Este endpoint atende telas e integrações que precisam verificar o estado
    atual de uma conta já criada. Ele não altera dados de negócio e retorna
    `204` quando o identificador não representa um usuário disponível para
    exposição pública.

    Parameters
    ----------
    user_id : str
        Identificador público informado na rota.
    service : UserService
        Serviço de domínio injetado pelo FastAPI.

    Returns
    -------
    UserEnvelopeResponse | Response
        Resposta HTTP `200` com o usuário encontrado ou `204` sem corpo.
    """
```

## Checklist

- [ ] A docstring está em pt-BR.
- [ ] A docstring usa seções NumPy com nomes em inglês técnico.
- [ ] O texto descreve contrato, não implementação trivial.
- [ ] Funções assíncronas documentam efeito de I/O ou orquestração.
- [ ] Endpoints explicam intenção de negócio e limites da operação.
- [ ] A docstring não tenta substituir validação, tipagem ou contrato Pydantic.
