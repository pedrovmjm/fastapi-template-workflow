---
name: standard-configs
description: Padroniza configs, values_domains, settings, leitura de .env/variáveis de ambiente e criação de singletons assíncronos para banco, blob e outros clients técnicos.
---
# Standard Configs - Settings e Providers

Use esta skill ao criar ou revisar arquivos em `src/configs/` e providers de clients técnicos.

## Responsabilidade Desta Skill

Esta skill é dona de:

- `src/configs/values_domains/`;
- `src/configs/settings.py`;
- leitura de `.env` e variáveis de ambiente;
- modelos de configuração com `Field`;
- providers/singletons de banco, blob e clients externos;
- fechamento de recursos no `lifespan`.

Esta skill não é dona de:

- uso do client em queries ou chamadas externas: use `standard-repositories`;
- regra de negócio: use `standard-services`;
- app factory e registro do lifespan: use `fastapi-best-practices`;
- contratos HTTP: use `standard-endpoints` e `standard-data-models`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar values domains. | [Values domains](references/values-domains.md) |
| Quando precisar aprofundar settings loader. | [Settings loader](references/settings-loader.md) |
| Quando precisar aprofundar provider singletons. | [Provider singletons](references/provider-singletons.md) |
| Quando criar provider de client externo. | [Provider de client externo](references/external-client-provider.md) |

## Regras Obrigatórias

- Configurações por domínio devem ficar em `src/configs/values_domains/`.
- Cada domínio de configuração deve ser um `BaseModel` com `Field`.
- `settings.py` deve centralizar leitura de `.env` e variáveis de ambiente.
- Variáveis de ambiente devem sobrescrever defaults dos `values_domains`.
- Código de service e repository não deve acessar `os.environ`.
- Providers devem criar clients técnicos de forma centralizada.
- Singletons devem ser protegidos contra criação concorrente quando async.
- Clients com `close`/`aclose` devem ter função de fechamento.
- Segredos não devem ter valor default real.

## Estrutura Recomendada

```text
src/
└── configs/
    ├── __init__.py
    ├── settings.py
    ├── external_api.py
    ├── database.py
    ├── blob.py
    └── values_domains/
        ├── __init__.py
        ├── server.py
        ├── external_api.py
        ├── database.py
        └── blob.py
```

## Checklist

- [ ] `values_domains` define modelos e defaults seguros.
- [ ] `settings.py` lê `.env` quando existir e variáveis de ambiente.
- [ ] Providers criam clients centralizados.
- [ ] Services e repositories recebem dependências, não leem ambiente.
- [ ] Clients assíncronos são fechados no shutdown.
- [ ] Segredos não aparecem em logs, traces ou exemplos reais.
