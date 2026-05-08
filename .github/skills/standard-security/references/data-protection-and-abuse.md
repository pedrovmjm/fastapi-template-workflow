# Proteção de Dados, Secrets e Abuso

Segurança também é reduzir o valor que um atacante consegue extrair ou abusar. Minimize dados, limite custo, proteja secrets e registre eventos úteis para detecção.

## Dados Sensíveis

- Colete apenas o necessário.
- Mascare documento, e-mail, telefone, cartão e identificadores sensíveis quando possível.
- Nunca retorne segredo, token, hash de senha ou credencial.
- Não persista payload bruto de autenticação, webhook ou LLM sem necessidade clara.
- Defina retenção para dados temporários.

## Secrets

- Secrets devem vir de ambiente seguro, secret manager ou provider configurado.
- Secrets não entram em código, fixture, log, trace, prompt ou response.
- Rotacione segredo quando houver vazamento ou suspeita.
- Separe secrets por ambiente.
- Evite compartilhar a mesma API key entre serviços com permissões diferentes.

## CORS

- Use allowlist explícita por ambiente.
- Evite `*` com credenciais.
- Não trate CORS como autorização.
- Revise métodos e headers permitidos.

## Rate Limiting e Abuse Prevention

- Aplique limite em login, refresh, reset de senha e endpoints caros.
- Limite upload, payload, paginação, concorrência e tempo de execução.
- Use idempotency key em operações sensíveis a retry.
- Detecte automação abusiva em fluxos de negócio valiosos.
- Proteja chamadas LLM por custo, tokens, usuário e tenant.

## Checklist

- [ ] Dados sensíveis foram classificados.
- [ ] Secrets não aparecem em código, logs, traces ou prompts.
- [ ] CORS está restrito por ambiente.
- [ ] Rate limiting cobre autenticação e endpoints caros.
- [ ] Retenção de payloads sensíveis foi definida.
- [ ] Eventos de abuso são observáveis sem expor dados privados.
