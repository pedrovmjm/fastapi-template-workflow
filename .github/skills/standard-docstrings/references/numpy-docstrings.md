# Docstrings NumPy em pt-BR

Use docstrings para explicar contrato, intenção, efeitos e riscos. Não use docstring para narrar cada linha do código.

## Seções Permitidas

- `Parameters`: parâmetros recebidos.
- `Returns`: valor retornado.
- `Yields`: valores produzidos por generators ou context managers.
- `Raises`: exceções conhecidas.
- `Examples`: exemplos curtos quando ajudam o uso.
- `Notes`: decisões, efeitos colaterais e limites.

## Função Assíncrona

```python
async def count_active_sessions(user_id: str) -> int:
    """Conta sessões ativas de um usuário.

    Parameters
    ----------
    user_id : str
        Identificador público do usuário.

    Returns
    -------
    int
        Quantidade de sessões ativas encontradas.

    Notes
    -----
    Esta função executa I/O na camada de persistência e deve ser aguardada.
    """
```

## Classe

```python
class UserService:
    """Coordena casos de uso relacionados a usuários.

    Parameters
    ----------
    repository : UserRepository
        Repositório usado para leitura e persistência de usuários.

    Notes
    -----
    Esta classe não conhece detalhes HTTP e não deve retornar `JSONResponse`.
    """
```

## Regras de Escrita

- A primeira linha deve caber em uma leitura rápida.
- `Parameters` deve explicar significado, não apenas repetir o nome.
- `Returns` deve dizer o que acontece em casos vazios, como `None` ou lista vazia.
- `Raises` deve listar apenas exceções relevantes para o chamador.
- `Notes` deve ser usado para I/O, concorrência, efeitos colaterais ou decisões importantes.
