# Docstrings para Processamento de Documentos

Use docstrings NumPy em pt-BR, alinhadas à skill `standard-docstrings`.

## Regras

- A primeira linha deve dizer o que a função ou classe representa no domínio.
- Documente limitações relevantes, como formato aceito, I/O, parsing bloqueante ou dependência externa.
- Use `Raises` para erros conhecidos de formato, conteúdo inválido e falha de processamento.
- Use `Notes` quando houver detalhe operacional importante, como executor, OCR ou biblioteca síncrona.
- Não descreva contrato Pydantic em docstring; isso pertence a `standard-data-models`.
- Não documente detalhe trivial, como atribuição direta de atributo.

## Template de Processador

```python
class TxtDocumentProcessor:
    """Extrai conteúdo textual de documentos `.txt`.

    Notes
    -----
    Esta implementação espera conteúdo em bytes e aplica decodificação textual
    antes da normalização de quebras de linha.
    """

    async def extract_text(self, document: DocumentInput) -> ExtractedDocument:
        """Extrai texto de um documento `.txt`.

        Parameters
        ----------
        document : DocumentInput
            Documento textual recebido pela aplicação.

        Returns
        -------
        ExtractedDocument
            Texto extraído com metadados do processamento.

        Raises
        ------
        DocumentProcessingError
            Quando o conteúdo não puder ser decodificado com segurança.
        """

        ...
```

## Template de Service

```python
class DocumentProcessingService:
    """Executa casos de uso de processamento de documentos."""

    async def process_document(self, document: DocumentInput) -> ExtractedDocument:
        """Processa um documento usando o processador compatível.

        Parameters
        ----------
        document : DocumentInput
            Documento com conteúdo e metadados necessários para seleção do parser.

        Returns
        -------
        ExtractedDocument
            Conteúdo extraído e normalizado para uso pela aplicação.

        Raises
        ------
        UnsupportedDocumentError
            Quando nenhum processador compatível estiver disponível.
        DocumentProcessingError
            Quando o processador compatível falhar durante a extração.
        """

        ...
```
