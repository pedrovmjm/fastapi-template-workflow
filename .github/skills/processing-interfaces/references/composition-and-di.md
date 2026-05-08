# Composição e Dependency Injection

Componha estratégias no provider FastAPI ou em uma factory de aplicação. O service deve receber dependências prontas pelo construtor.

## Registry de Estratégias

```python
class ProcessingStrategyRegistry:
    """Seleciona estratégias por tipo de processamento.

    Parameters
    ----------
    strategies : list[ProcessingStrategy]
        Estratégias disponíveis para processamento.
    """

    def __init__(self, strategies: list[ProcessingStrategy]) -> None:
        self._strategies = strategies

    def get_strategy(self, payload: ProcessingInput) -> ProcessingStrategy:
        """Retorna a estratégia compatível com a entrada.

        Parameters
        ----------
        payload : ProcessingInput
            Entrada com metadados usados para seleção da estratégia.

        Returns
        -------
        ProcessingStrategy
            Estratégia compatível com o tipo de processamento solicitado.

        Raises
        ------
        UnsupportedProcessingTypeError
            Quando nenhuma estratégia compatível estiver registrada.
        """

        processing_type = payload.processing_type.lower()

        for strategy in self._strategies:
            if processing_type in strategy.supported_types:
                return strategy

        raise UnsupportedProcessingTypeError(processing_type=processing_type)
```

## Service de Orquestração

```python
class ProcessingService:
    """Orquestra processamentos enviados à aplicação.

    Parameters
    ----------
    strategy_registry : ProcessingStrategyRegistry
        Registry usado para selecionar a estratégia compatível.
    """

    def __init__(self, strategy_registry: ProcessingStrategyRegistry) -> None:
        self._strategy_registry = strategy_registry

    async def process(self, payload: ProcessingInput) -> ProcessingResult:
        """Processa uma entrada e retorna o resultado normalizado.

        Parameters
        ----------
        payload : ProcessingInput
            Entrada recebida pela aplicação.

        Returns
        -------
        ProcessingResult
            Resultado normalizado para uso pela regra de negócio.

        Notes
        -----
        Esta função orquestra I/O ou processamento assíncrono por meio da estratégia
        selecionado.
        """

        strategy = self._strategy_registry.get_strategy(payload=payload)
        return await strategy.process(payload=payload)
```

## Provider FastAPI

```python
from fastapi import Depends


async def get_processing_strategy_registry() -> ProcessingStrategyRegistry:
    """Cria o registry de estratégias de processamento.

    Returns
    -------
    ProcessingStrategyRegistry
        Registry configurado com as estratégias disponíveis.
    """

    return ProcessingStrategyRegistry(
        strategies=[
            TxtExtractionStrategy(),
            DocxExtractionStrategy(),
        ]
    )


async def get_processing_service(
    strategy_registry: ProcessingStrategyRegistry = Depends(
        get_processing_strategy_registry
    ),
) -> ProcessingService:
    """Cria o service de processamento.

    Parameters
    ----------
    strategy_registry : ProcessingStrategyRegistry
        Registry injetado pelo FastAPI.

    Returns
    -------
    ProcessingService
        Serviço pronto para executar processamentos.
    """

    return ProcessingService(strategy_registry=strategy_registry)
```

## Regras

- Provider monta dependências; não executa regra de negócio.
- Registry seleciona estratégia; não executa processamento.
- Service orquestra caso de uso; não instancia estratégias diretamente.
- Estratégia executa processamento específico; não decide status HTTP nem monta response.
- Dependências devem ser substituíveis em testes com `app.dependency_overrides`.
