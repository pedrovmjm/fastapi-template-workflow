# Manipulação de Dados em Services

Use o service para transformar dados técnicos em informação de negócio.

## Permitido

- combinar resultados de múltiplos repositories;
- aplicar filtros de negócio;
- calcular campos derivados;
- decidir transições de estado;
- montar response público a partir de entidades internas;
- normalizar dados antes de persistir, quando a normalização é regra de negócio.

## Não Permitido

- aplicar regra de paginação HTTP;
- montar links HTTP;
- serializar manualmente JSON;
- executar query diretamente;
- esconder erro de infraestrutura como sucesso;
- manipular payload sensível sem necessidade.

## Exemplo

```python
class UserService:
    """Executa regras de negócio relacionadas a usuários."""

    async def summarize_user(self, user_id: str) -> UserSummaryResponse:
        """Monta um resumo público do usuário.

        Parameters
        ----------
        user_id : str
            Identificador público do usuário.

        Returns
        -------
        UserSummaryResponse
            Resumo público consolidado a partir de fontes internas.
        """

        user = await self._user_repository.get_by_id(user_id=user_id)
        if user is None:
            raise ResourceNotFoundError()

        active_sessions = await self._user_repository.count_active_sessions(
            user_id=user_id
        )
        return UserSummaryResponse(
            id=user.id,
            status=user.status,
            has_active_session=active_sessions > 0,
        )
```
