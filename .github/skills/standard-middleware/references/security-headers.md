# Headers de Segurança

Use headers de segurança em middleware dedicado, sem misturar com CORS ou autenticação.

## Headers Recomendados

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: no-referrer`
- `Cache-Control: no-store` para endpoints sensíveis

## Regras

- Não sobrescreva headers definidos explicitamente por uma rota sem decisão clara.
- Não coloque política de autenticação dentro do middleware de headers.
- Documente exceções por rota quando existirem.
- Revise impacto em Swagger/OpenAPI antes de endurecer políticas globais.
