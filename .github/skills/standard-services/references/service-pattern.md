# Padrão de Service

Service é a camada de lógica de negócio. Ela decide como dados devem ser interpretados, combinados e transformados para cumprir um caso de uso.

## O Que Um Service Pode Fazer

- aplicar regra de negócio;
- validar estado de domínio;
- manipular dados recebidos de repositories;
- transformar entidade interna em response público;
- chamar múltiplos repositories;
- orquestrar operações independentes com `asyncio`;
- lançar exceções de domínio conhecidas.

## O Que Um Service Não Deve Fazer

- executar SQL diretamente;
- baixar blob diretamente;
- chamar OpenAI, HTTP externo ou storage diretamente;
- criar client externo;
- montar `JSONResponse`;
- decidir status HTTP;
- ler `.env`;
- acessar `os.environ`;
- importar `Request`, `Response` ou `APIRouter`.

## Organização Recomendada

```text
src/
└── services/
    └── users/
        ├── __init__.py
        └── user_service.py
```

## Regra de Tamanho

Se um método de service começar a fazer muitas coisas, extraia funções privadas assíncronas com nomes de intenção.

```python
class UserService:
    """Executa regras de negócio relacionadas a usuários."""

    async def activate_user(self, user_id: str) -> UserResponse:
        """Ativa um usuário quando as regras de domínio permitem."""

        user = await self._get_existing_user(user_id=user_id)
        await self._ensure_user_can_be_activated(user=user)
        activated_user = await self._user_repository.update_status(
            user_id=user.id,
            status="active",
        )
        return UserResponse(id=activated_user.id, status=activated_user.status)

    async def _get_existing_user(self, user_id: str) -> UserEntity:
        """Busca usuário existente ou lança erro de domínio."""

        ...
```
