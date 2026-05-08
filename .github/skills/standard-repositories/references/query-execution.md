# Queries e Persistência

Use este guia para repositories que executam banco de dados.

## Regras

- Use client ou sessão assíncrona.
- Parametrize queries.
- Não concatene dados do usuário em SQL.
- Retorne entidade interna, primitivo tipado ou `None`.
- Não retorne rows crus para service quando isso vaza detalhe de banco.
- Não abra conexão dentro do método quando a conexão vem de provider.

## Exemplo

```python
class UserRepository:
    """Executa queries de usuários."""

    async def count_active_sessions(self, user_id: str) -> int:
        """Conta sessões ativas de um usuário.

        Parameters
        ----------
        user_id : str
            Identificador público do usuário.

        Returns
        -------
        int
            Quantidade de sessões ativas.
        """

        value = await self._database.fetch_val(
            "SELECT COUNT(*) FROM sessions WHERE user_id = :user_id AND active = TRUE",
            {"user_id": user_id},
        )
        return int(value or 0)
```
