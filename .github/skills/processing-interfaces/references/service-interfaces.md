# Interfaces de Services

Use interfaces de service quando o domínio exigir múltiplas implementações, substituição clara em testes, boundary entre módulos ou composição plugável. Não crie interface apenas para repetir uma única classe concreta sem benefício real.

## Quando Criar Interface

- Há mais de uma implementação para o mesmo caso de uso, como processamento local, assíncrono por fila ou mockado.
- Outro módulo precisa depender de um contrato estável sem conhecer a implementação.
- Testes precisam substituir o service completo, não apenas seus repositories.
- A aplicação seleciona uma estratégia de processamento por configuração ou ambiente.

## Quando Evitar

- Existe apenas uma implementação e ela não cruza boundary relevante.
- A interface teria os mesmos métodos da classe concreta sem reduzir acoplamento.
- O problema é apenas injetar repository ou client; nesse caso use construtor no service concreto.

## Contrato de Service Genérico

```python
from typing import Protocol


class ProcessingServicePort(Protocol):
    """Define o contrato de processamento da aplicação."""

    async def process(self, payload: ProcessingInput) -> ProcessingResult:
        """Processa uma entrada enviada à aplicação.

        Parameters
        ----------
        payload : ProcessingInput
            Entrada com conteúdo e metadados necessários para processamento.

        Returns
        -------
        ProcessingResult
            Resultado normalizado para uso pela aplicação.

        Raises
        ------
        UnsupportedProcessingTypeError
            Quando o tipo solicitado não estiver disponível.
        ProcessingError
            Quando a entrada for aceita, mas falhar durante o processamento.
        """

        ...
```

## Exemplo de Documento

```python
class DocumentProcessingServicePort(Protocol):
    """Define o contrato de processamento de documentos da aplicação."""

    async def process_document(self, document: DocumentInput) -> ExtractedDocument:
        """Processa um documento enviado à aplicação."""

        ...
```

## Implementação

```python
class ProcessingService:
    """Executa o caso de uso de processamento.

    Parameters
    ----------
    strategy_registry : ProcessingStrategyRegistry
        Registry usado para selecionar a estratégia compatível.
    """

    def __init__(self, strategy_registry: ProcessingStrategyRegistry) -> None:
        self._strategy_registry = strategy_registry

    async def process(self, payload: ProcessingInput) -> ProcessingResult:
        """Processa uma entrada usando a estratégia compatível.

        Parameters
        ----------
        payload : ProcessingInput
            Entrada com conteúdo e metadados necessários para processamento.

        Returns
        -------
        ProcessingResult
            Resultado normalizado para uso pela aplicação.
        """

        strategy = self._strategy_registry.get_strategy(payload=payload)
        return await strategy.process(payload=payload)
```

## Regras

- Nomeie a interface como contrato do domínio, por exemplo `ProcessingServicePort` ou `DocumentProcessingServicePort`.
- Endpoints podem depender do contrato quando isso ajudar testes ou seleção de implementação.
- Providers FastAPI podem retornar o tipo da interface e construir a implementação concreta.
- A interface não deve expor detalhes de `Depends`, HTTP, storage, banco ou biblioteca de parsing.
- Não duplique docstrings extensas entre interface e implementação sem necessidade; a interface documenta contrato e a implementação documenta particularidades.
