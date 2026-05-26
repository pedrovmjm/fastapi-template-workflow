# Níveis de Log vs Erros HTTP

Use esta referência para separar o que vai para o **console** (operadores e desenvolvedores) do que vai para o **cliente HTTP** (contrato público em `errors[]`).

São **dois canais independentes**. O nível do log no console não define o status HTTP, e o status HTTP não substitui o log.

## Duas saídas distintas

| Saída | Destino | Responsável |
| --- | --- | --- |
| Log estruturado | Console / agregador (Datadog, Loki, etc.) | `logging` + `standard-logs` |
| Erro HTTP | Body JSON da resposta | `standard-errors` + handlers em `src/routes/exception_handlers.py` |

**Nunca** use `logger.warning` ou `logger.error` *no lugar* de montar a resposta HTTP correta.  
**Nunca** rebaixe `warning` para `debug` só para “sumir” do console — ajuste `LOGGING__LEVEL` ou o evento.  
**Nunca** coloque stack trace, SQL, token ou detalhe interno no body de erro.

## Quando usar cada nível de log (console)

| Nível | Use para | Exemplos |
| --- | --- | --- |
| `debug` | Rastreio técnico verboso; passos internos; só relevante com `LOGGING__LEVEL=DEBUG` | parâmetros de wiring, cache hit/miss detalhado |
| `info` | Fluxo normal e resultado esperado de negócio | `user.created`, `application.started` |
| `warning` | Situação anormal mas tolerada, dependência opcional ausente, degradação, tentativa de auth inválida | `telemetry.httpx.unavailable`, `auth.token_rejected`, `auth.user_enrichment_failed` |
| `error` | Falha técnica que interrompe a operação (antes do handler HTTP) | `object_storage.operation_failed`, `microsoft_graph.user_profile_failed` |
| `exception` | Bug ou falha inesperada com stack trace no handler global | `http.internal_error` |
| `critical` | Indisponibilidade ampla ou perda de integridade | raro |

### O que **não** confundir

| Errado | Certo |
| --- | --- |
| “Vou usar `warning` no log *como* se fosse debug” | Use `debug` quando for diagnóstico verboso; use `warning` quando for alerta operacional real |
| “Vou trocar `warning` por `debug` para não poluir” | Mantenha `warning`; filtre no agregador ou suba o nível mínimo só em dev |
| “Logou `warning`, então o cliente recebe aviso” | Cliente recebe o envelope `errors[]` do handler (`401`, `403`, `500`, etc.) |

## O que o cliente HTTP recebe

1. Camadas de domínio (`service`, `repository`, `security`) lançam **exceções tipadas**.
2. Endpoints **não** montam JSON de erro manualmente nem usam `HTTPException` com `detail` solto no domínio.
3. Handlers globais convertem exceção → envelope `errors[]` com `code`, `title`, `message` seguros.
4. O handler pode registrar log adicional (`info` para 4xx esperado, `exception` para 500).

## Exemplo auth (dois canais ao mesmo tempo)

```text
security: logger.warning("auth.token_rejected")   → console
security: raise AuthenticationFailedError       → handler
handler:  logger.info("http.auth.unauthorized")  → console
handler:  JSON 401 + errors[]                     → cliente
```

O `warning` no console e o `401` na API coexistem; um não substitui o outro.

## Fluxo recomendado

```text
Repository/Service
  → logger.warning|error (console, conforme degradação ou falha)
  → raise DomainError(...)
       ↓
Handler global
  → logger.info|exception (console, resumo HTTP)
  → JSONResponse com errors[]
```

## Anti-padrões

| Evitar | Preferir |
| --- | --- |
| Rebaixar `warning` → `debug` para reduzir ruído | Manter o nível semântico correto |
| `logger.warning` *em vez de* handler HTTP | Log **e** handler, cada um no seu canal |
| `HTTPException(detail=...)` no service/repository | Exceção de domínio + handler |
| Mensagem de log igual ao body HTTP | Log com `event`/`error_type`; body com mensagem segura fixa |
| Expor `str(exc)` no JSON de erro | Mensagem estável em pt-BR no handler |

## Configuração de console

- `LOGGING__LEVEL` controla o mínimo exibido (`INFO` no template: mostra `info`, `warning`, `error`, …).
- `SERVER__LOG_LEVEL` controla logs do Uvicorn separadamente.
- Use `LOGGING__LEVEL=DEBUG` em local **somente** quando precisar de eventos `debug` reais.
