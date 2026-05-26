# Mensagens de Log Orientadas ao Negócio

A mensagem (`message`) deve responder, em uma frase curta em pt-BR: **o que aconteceu no mundo real**, para **quem** e com **qual resultado**. Detalhes técnicos, filtros e identificadores vão em `extra`; a mensagem não deve repetir o nome do método, arquivo ou template.

## Regras

- Descreva o **efeito de negócio** ou o **pedido do usuário/sistema**, não a etapa técnica interna.
- Inclua na mensagem, quando fizer sentido e for seguro: **ator** (usuário, integração, job), **ação** (criou, consultou, cancelou), **objeto de negócio** (pedido, contrato, arquivo) e **resultado** (sucesso, vazio, recusado, timeout).
- Use `extra` para identificadores (`user_id`, `order_id`, `tenant_id`), contadores, status HTTP, provider, duração e tipo de erro.
- Evite mensagens que só narram infraestrutura: "listando template", "chamando repository", "decorator executado", "iniciando operação".
- Evite mensagens genéricas que poderiam ser de qualquer endpoint: "requisição processada", "operação concluída", "sucesso".
- Em falhas, diga **o que não foi possível entregar ao negócio** e use `error_type` / `status_code` em `extra`, não na mensagem como dump técnico.
- Não coloque PII, credenciais ou payload completo na mensagem; use identificadores públicos ou mascarados em `extra`.

## Boa vs má prática

| Evitar | Preferir |
| --- | --- |
| "Listando templates do bootstrap." | "Consulta de modelos de documento concluída sem resultados para o tenant." |
| "Operacao de object storage iniciada." | "Upload do arquivo de fatura iniciado para o cliente." |
| "Health check recebido." | "Verificação de disponibilidade da API solicitada pelo monitoramento." |
| "Chamando Microsoft Graph." | "Enriquecimento do perfil do usuário autenticado falhou no provedor de identidade." |
| "Decorator de telemetria aplicado." | *(não logar; é ruído técnico)* |

## Exemplo — sucesso

```python
logger.info(
    "Pedido 1042 aprovado para o cliente Acme após validação de estoque.",
    extra={
        "event": "order.approved",
        "layer": "service",
        "order_id": "1042",
        "customer_id": "acme-001",
        "correlation_id": correlation_id,
    },
)
```

## Exemplo — falha com contexto de negócio

```python
logger.warning(
    "Não foi possível anexar o comprovante ao processo do usuário autenticado.",
    extra={
        "event": "attachment.upload_failed",
        "layer": "service",
        "user_id": user_id,
        "process_id": process_id,
        "provider": "azure_blob",
        "error_type": type(error).__name__,
        "correlation_id": correlation_id,
    },
)
```

## Exemplo — resultado vazio relevante

```python
logger.info(
    "Nenhum pedido pendente encontrado para o vendedor na janela solicitada.",
    extra={
        "event": "order.list_empty",
        "layer": "service",
        "seller_id": seller_id,
        "window_days": window_days,
        "correlation_id": correlation_id,
    },
)
```

## Checklist da mensagem

- [ ] Um leitor de negócio ou suporte entende o que aconteceu sem abrir o código.
- [ ] A mensagem não é só o nome de uma função, decorator, template ou camada.
- [ ] Identificadores e metadados técnicos estão em `extra`, não concatenados na frase.
- [ ] Nenhum dado sensível aparece na mensagem.
