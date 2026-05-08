# Mapeamento de Erros Externos

Erro externo não deve vazar cru para o contrato público. Traduza status, códigos e timeouts do provider para exceções internas conhecidas, depois deixe `standard-errors` cuidar do envelope público.

## Regras

- Capture timeout, erro de conexão e status HTTP inesperado.
- Preserve metadados seguros: provider, operação, status externo, código externo e correlation id.
- Não inclua token, payload sensível ou response completa em exceção.
- Diferencie erro transitório de erro permanente.
- Mapeie rate limit externo para exceção específica.
- Mapeie autenticação/configuração inválida como falha técnica operacional.

## Categorias

- `ExternalTimeoutError`
- `ExternalConnectionError`
- `ExternalRateLimitError`
- `ExternalAuthenticationError`
- `ExternalValidationError`
- `ExternalUnexpectedError`

Os nomes concretos podem variar por projeto, mas a categorização deve ficar clara.

## Checklist

- [ ] Timeout e conexão são tratados.
- [ ] Status externo vira exceção interna conhecida.
- [ ] Dados sensíveis são omitidos.
- [ ] Erro transitório é distinguido de permanente.
- [ ] Service recebe erro técnico, não response crua.
