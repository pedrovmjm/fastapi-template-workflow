# Timeout, Retry e Circuit Breaker

Integrações falham. O padrão deve limitar espera, custo e efeito cascata. Retry sem critério pode duplicar operações e piorar incidentes.

## Timeout

- Defina timeout explícito por integração.
- Separe connect/read/write/pool quando a biblioteca suportar.
- Use timeout menor para endpoints síncronos de usuário e maior para jobs controlados.
- Não deixe request externo sem limite.

## Retry

- Use retry para falhas transitórias: timeout, conexão, `429`, `502`, `503`, `504`.
- Não retry em `400`, `401`, `403`, validação ou erro permanente.
- Use backoff com jitter.
- Limite tentativas.
- Faça retry de escrita apenas com idempotency key ou garantia equivalente.

## Circuit Breaker e Bulkhead

- Use circuit breaker em providers instáveis ou críticos.
- Use limite de concorrência para proteger pool e custo.
- Defina fallback somente quando o domínio aceita resposta degradada.
- Exponha estado degradado em logs/traces/metrics sem vazar dados.

## Checklist

- [ ] Timeout explícito existe.
- [ ] Retry é limitado e idempotente.
- [ ] Backoff com jitter foi considerado.
- [ ] Escritas externas não duplicam efeito.
- [ ] Falha do provider não derruba fluxo além do necessário.
