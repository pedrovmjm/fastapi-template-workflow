# Blob e Storage

Use repository para executar leitura e escrita de blobs quando o service precisa de arquivos ou objetos.

## Regras

- O client de blob entra pelo construtor.
- O repository não decide regra de negócio sobre o conteúdo.
- O repository pode validar existência técnica.
- O repository deve retornar bytes, stream tipado ou metadado interno.
- Não logue conteúdo do blob.

## Exemplo

```python
class UserDocumentRepository:
    """Executa operações técnicas em blobs de documentos de usuário."""

    def __init__(self, blob_client: BlobClient) -> None:
        self._blob_client = blob_client

    async def download_user_document(self, blob_name: str) -> bytes:
        """Baixa um documento armazenado em blob.

        Parameters
        ----------
        blob_name : str
            Nome técnico do blob a ser baixado.

        Returns
        -------
        bytes
            Conteúdo bruto do blob.
        """

        return await self._blob_client.download_blob(name=blob_name)
```
