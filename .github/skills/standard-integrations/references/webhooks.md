# Webhooks e Idempotência

Webhook é entrada externa e não confiável. Ele precisa de validação de assinatura, idempotência e processamento seguro antes de alterar estado de negócio.

## Regras

- Valide assinatura do provider quando disponível.
- Valide timestamp para reduzir replay attack.
- Guarde event id ou idempotency key.
- Responda rápido e processe trabalho pesado em job quando necessário.
- Aceite eventos duplicados sem duplicar efeito.
- Registre evento recebido com metadados seguros.
- Não confie em status do webhook sem reconciliar quando o domínio exigir.

## Processamento

- Parseie payload em modelo interno.
- Valide tipo de evento permitido.
- Verifique se o recurso pertence ao tenant/conta esperada quando aplicável.
- Execute mudança de estado de forma idempotente.
- Guarde payload bruto apenas se houver necessidade e política de retenção.

## Checklist

- [ ] Assinatura e timestamp são validados.
- [ ] Evento duplicado é seguro.
- [ ] Tipos de evento são allowlist.
- [ ] Trabalho pesado não bloqueia resposta.
- [ ] Payload sensível tem retenção definida.
