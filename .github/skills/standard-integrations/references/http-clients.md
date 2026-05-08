# Clients HTTP Assíncronos

Clients externos devem ser pequenos, tipados e focados no contrato do provider. Eles não devem conter regra de negócio do domínio; essa decisão pertence ao service.

## Regras

- Use `httpx.AsyncClient` como client HTTP assíncrono em aplicação async.
- Configure base URL, headers padrão e timeout no provider.
- Configure `httpx.Timeout` explicitamente, usando valores vindos de `settings`.
- Defina configurações globais do HTTP client em um value domain dedicado, como `src/configs/values_domains/httpx_client.py`.
- Injete o client no repository ou integration client.
- Tipar request e response com modelos internos quando o contrato for relevante.
- Não retorne response crua do HTTP client para o service.
- Não monte URL com concatenação insegura de entrada do usuário.

## Estrutura Recomendada

- `src/integrations/{provider}/client.py` para client dedicado, quando existir camada de integração.
- `src/repository/{dominio}/` quando a integração é tratada como execução técnica de um caso de uso.
- `src/configs/providers/` para singleton, settings e factory.

## Checklist

- [ ] Client tem base URL controlada.
- [ ] Timeout está configurado.
- [ ] Request/response são tipados quando necessário.
- [ ] Headers sensíveis não são logados.
- [ ] Service não conhece detalhes de HTTP externo.
