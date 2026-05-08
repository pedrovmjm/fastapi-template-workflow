# Exemplo de Múltiplos Formatos

Este exemplo mostra a estrutura esperada para `.txt` e `.docx`. Adapte nomes de modelos, erros e repositories conforme as skills `standard-data-models`, `standard-errors`, `standard-repositories` e `standard-integrations`.

## Organização Recomendada

```text
src/
└── services/
    └── documents/
        ├── document_processing_service.py
        ├── document_processor_registry.py
        └── processors/
            ├── docx_document_processor.py
            ├── document_processor.py
            └── txt_document_processor.py
```

## Interface

```python
from typing import Protocol


class DocumentProcessor(Protocol):
    """Define o contrato para extração de conteúdo de documentos."""

    @property
    def supported_extensions(self) -> set[str]:
        """Retorna extensões aceitas pelo processador."""

        ...

    @property
    def supported_mime_types(self) -> set[str]:
        """Retorna MIME types aceitos pelo processador."""

        ...

    async def extract_text(self, document: DocumentInput) -> ExtractedDocument:
        """Extrai texto de um documento suportado."""

        ...
```

## Processador `.txt`

```python
class TxtDocumentProcessor:
    """Extrai conteúdo textual de documentos `.txt`."""

    @property
    def supported_extensions(self) -> set[str]:
        """Retorna extensões aceitas pelo processador."""

        return {".txt"}

    @property
    def supported_mime_types(self) -> set[str]:
        """Retorna MIME types aceitos pelo processador."""

        return {"text/plain"}

    async def extract_text(self, document: DocumentInput) -> ExtractedDocument:
        """Extrai texto de um documento `.txt`.

        Parameters
        ----------
        document : DocumentInput
            Documento textual recebido pela aplicação.

        Returns
        -------
        ExtractedDocument
            Conteúdo textual extraído e normalizado.

        Raises
        ------
        DocumentProcessingError
            Quando o conteúdo não puder ser decodificado.
        """

        try:
            text = document.content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise DocumentProcessingError("Documento `.txt` inválido.") from error

        return ExtractedDocument(
            text=text.replace("\r\n", "\n").strip(),
            source_extension=".txt",
        )
```

## Processador `.docx`

```python
class DocxDocumentProcessor:
    """Extrai conteúdo textual de documentos `.docx`.

    Notes
    -----
    Se a biblioteca usada para leitura de `.docx` for síncrona, execute a leitura
    por repository, integração, worker ou executor controlado.
    """

    @property
    def supported_extensions(self) -> set[str]:
        """Retorna extensões aceitas pelo processador."""

        return {".docx"}

    @property
    def supported_mime_types(self) -> set[str]:
        """Retorna MIME types aceitos pelo processador."""

        return {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }

    async def extract_text(self, document: DocumentInput) -> ExtractedDocument:
        """Extrai texto de um documento `.docx`.

        Parameters
        ----------
        document : DocumentInput
            Documento Word recebido pela aplicação.

        Returns
        -------
        ExtractedDocument
            Conteúdo textual extraído e normalizado.

        Raises
        ------
        DocumentProcessingError
            Quando o arquivo `.docx` estiver corrompido ou ilegível.
        """

        paragraphs = await self._docx_reader.read_paragraphs(content=document.content)
        return ExtractedDocument(
            text="\n".join(paragraph.strip() for paragraph in paragraphs if paragraph),
            source_extension=".docx",
        )
```

## Observações

- O exemplo usa `DocumentInput`, `ExtractedDocument`, `UnsupportedDocumentError` e `DocumentProcessingError` como nomes de domínio. Defina os modelos e erros nas skills donas.
- Se houver OCR, extração de imagem ou chamada externa, trate como integração técnica e injete um client ou repository.
- Se o documento for grande, evite carregar tudo em memória sem necessidade; use stream, storage temporário ou fila conforme o caso.
