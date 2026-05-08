# Padrão de Repository

Repository é a camada de execução técnica usada pelo service.

## O Que Um Repository Pode Fazer

- executar query;
- chamar procedure;
- ler ou escrever blob;
- chamar API externa por client já configurado;
- chamar OpenAI por meio de client configurado;
- converter resultado técnico em entidade interna;
- capturar erro técnico e relançar exceção técnica conhecida.

## O Que Um Repository Não Deve Fazer

- decidir regra de negócio;
- montar response público;
- retornar wrapper `data`;
- decidir status HTTP;
- ler `.env`;
- criar client global;
- definir política de timeout, retry, circuit breaker ou webhook;
- aplicar autorização do usuário final.

## Entidades Internas

Entidades internas podem ser dataclasses para desacoplar repository de Pydantic público.

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserEntity:
    """Representa usuário como entidade interna de persistência."""

    id: str
    status: str
```
