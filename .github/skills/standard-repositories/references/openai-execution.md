# OpenAI Repository

Use repository para encapsular chamadas OpenAI quando um service precisar de geração, classificação, extração ou análise.

## Regras

- Use client assíncrono configurado em `standard-configs`.
- O repository recebe o client pelo construtor.
- O repository não decide regra de negócio do produto.
- O repository não escolhe modelo dinamicamente sem configuração.
- O repository não loga prompt completo quando houver dado sensível.
- O repository retorna resultado técnico tipado ou entidade interna.

## Exemplo

```python
from openai import AsyncOpenAI


class UserAiRepository:
    """Executa chamadas OpenAI relacionadas a usuários.

    Parameters
    ----------
    client : AsyncOpenAI
        Client assíncrono configurado para chamadas OpenAI.
    model : str
        Modelo configurado para geração de respostas.
    """

    def __init__(self, client: AsyncOpenAI, model: str) -> None:
        self._client = client
        self._model = model

    async def summarize_user_notes(self, notes: str) -> str:
        """Resume notas internas de usuário.

        Parameters
        ----------
        notes : str
            Texto que será resumido pelo modelo.

        Returns
        -------
        str
            Resumo textual produzido pelo modelo.
        """

        response = await self._client.responses.create(
            model=self._model,
            input=f"Resuma as notas a seguir de forma objetiva: {notes}",
        )
        return response.output_text
```

## Observação

O SDK Python oficial oferece client assíncrono `AsyncOpenAI`; chamadas assíncronas devem usar `await`.
