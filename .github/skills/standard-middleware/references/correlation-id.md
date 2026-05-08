# Correlation ID

Use Correlation ID para rastrear uma requisição entre logs, traces e respostas.

## Regras

- Header padrão: `X-Correlation-Id`.
- Se o cliente enviar um valor válido, propague.
- Se o cliente não enviar, gere um UUID.
- Guarde em `request.state.correlation_id`.
- Retorne o valor no header da resposta.
- Não use correlation ID como autenticação, autorização ou chave de negócio.

## Validação Recomendada

- Aceite apenas valores com tamanho razoável.
- Remova espaços ao redor.
- Gere um novo ID se o valor recebido for vazio.
