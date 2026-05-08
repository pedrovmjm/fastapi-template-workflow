# Nomes de Spans

Use nomes estáveis e orientados à responsabilidade.

## Formato

```text
{dominio}.{camada}.{acao}
```

## Exemplos

- `users.endpoint.get_user`
- `users.service.create_user`
- `users.repository.get_by_id`
- `payments.integration.authorize`

## Regras

- Não inclua IDs no nome do span.
- Não use frases variáveis.
- Não coloque status no nome; use atributos.
- Prefira nomes curtos e consistentes.
