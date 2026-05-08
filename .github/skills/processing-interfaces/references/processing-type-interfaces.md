# Interfaces por Tipo de Processamento

Use uma interface comum para representar uma família de processamento com múltiplas implementações. Prefira `Protocol` quando quiser tipagem estrutural e baixo acoplamento.

## Estrutura Recomendada

```python
from typing import Protocol


class ProcessingStrategy(Protocol):
    """Define o contrato para uma estratégia de processamento.

    Implementações devem declarar quais tipos suportam e como executam o
    processamento sem expor detalhes técnicos ao chamador.
    """

    @property
    def supported_types(self) -> set[str]:
        """Retorna os tipos aceitos pela estratégia."""

        ...

    async def process(self, payload: ProcessingInput) -> ProcessingResult:
        """Processa uma entrada usando esta estratégia.

        Parameters
        ----------
        payload : ProcessingInput
            Entrada com dados e metadados suficientes para executar a estratégia.

        Returns
        -------
        ProcessingResult
            Resultado normalizado do processamento.

        Raises
        ------
        UnsupportedProcessingTypeError
            Quando a entrada não puder ser processada por esta implementação.
        ProcessingError
            Quando a entrada for aceita, mas o processamento falhar.
        """

        ...
```

## Exemplo para Documentos

Quando o domínio for processamento de documentos, a estratégia pode especializar o contrato com nomes mais expressivos:

```python
class DocumentProcessor(Protocol):
    """Define o contrato para processadores de documentos."""

    @property
    def supported_extensions(self) -> set[str]:
        """Retorna as extensões aceitas pelo processador."""

        ...

    @property
    def supported_mime_types(self) -> set[str]:
        """Retorna os MIME types aceitos pelo processador."""

        ...

    async def extract_text(self, document: DocumentInput) -> ExtractedDocument:
        """Extrai texto normalizado de um documento suportado."""

        ...
```

## Regras

- Interface deve representar capacidade de negócio, não detalhe de biblioteca.
- Use nomes de domínio como `DocumentProcessor`, `ImportStrategy`, `Classifier`, `Extractor` ou `Normalizer`.
- Não exponha bibliotecas externas, clients técnicos ou detalhes de storage no contrato público da interface.
- Defina os critérios de suporte da implementação: tipo, formato, extensão, MIME type, versão ou configuração.
- Normalize chaves de seleção antes de comparar, como extensões minúsculas ou tipos canônicos.
- Se o processamento precisar de biblioteca bloqueante, encapsule esse detalhe fora do endpoint e documente o limite.
- MIME type, extensão ou tipo informado ajudam, mas não devem ser a única defesa contra entrada inválida.

## Quando Usar Classe Abstrata

Use `abc.ABC` apenas quando houver comportamento compartilhado real ou invariantes que todas as implementações devem herdar. Para contratos simples, `Protocol` tende a ser suficiente.
