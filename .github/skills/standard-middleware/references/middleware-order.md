# Ordem de Middlewares

Use uma ordem previsível para evitar perda de contexto.

## Ordem Recomendada

```text
1. Error boundary global, quando implementado como middleware
2. Correlation ID
3. Tracing
4. Access log
5. Segurança e headers
6. CORS
```

## Regras

- Correlation ID deve rodar cedo para alimentar logs e traces.
- Middleware de access log deve rodar depois da correlação.
- Middleware de tracing deve conseguir observar exceções.
- CORS deve ser registrado de forma compatível com o comportamento esperado do FastAPI/Starlette.
- Não coloque regra de negócio na cadeia de middlewares.
