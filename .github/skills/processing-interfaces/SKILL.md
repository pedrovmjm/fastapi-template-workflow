---
name: processing-interfaces
description: Padroniza interfaces para tipos de processamento em FastAPI, incluindo contratos por estratégia ou formato, seleção via registry/factory, composição com dependency injection, docstrings NumPy em pt-BR e separação entre orquestração, implementação técnica e regra de negócio.
---
# Processing Interfaces

Use esta skill ao criar ou revisar fluxos com múltiplos tipos de processamento que precisam de interfaces claras, como processadores por formato de documento, estratégia de análise, tipo de importação, parser, extractor, classificador ou normalizador.

## Responsabilidade Desta Skill

Esta skill é dona de:

- desenho de interfaces para tipos de processamento;
- desenho de interfaces para services quando houver múltiplas implementações;
- composição de múltiplas estratégias por tipo, formato, MIME type, extensão ou configuração;
- registry ou factory para seleção da implementação correta;
- separação entre orquestração, regra de negócio, implementação técnica e persistência;
- docstrings NumPy em pt-BR para interfaces, registries, services e métodos públicos;
- estratégia de evolução para novos tipos sem alterar endpoints ou chamadores.

Esta skill não é dona de:

- padrão geral de services: use `standard-services`;
- contratos Pydantic públicos: use `standard-data-models`;
- endpoints, upload HTTP, query params e status code: use `standard-endpoints`;
- execução de storage, blob, OCR, banco, parsing técnico pesado ou chamadas externas: use `standard-repositories` e `standard-integrations`;
- ciclo de vida, providers e `Depends`: use `fastapi-best-practices`;
- contrato público de erro: use `standard-errors`;
- regra de docstrings fora deste domínio: use `standard-docstrings`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando desenhar interfaces por tipo de processamento. | [Interfaces por tipo de processamento](references/processing-type-interfaces.md) |
| Quando desenhar contratos para services de processamento. | [Interfaces de services](references/service-interfaces.md) |
| Quando compor services, registry, factory e providers FastAPI. | [Composição e dependency injection](references/composition-and-di.md) |
| Quando documentar interfaces e implementações deste domínio. | [Docstrings para interfaces de processamento](references/docstrings.md) |
| Quando precisar de um exemplo com `.txt` e `.docx`. | [Exemplo de múltiplos formatos](references/multi-format-example.md) |

## Regras Obrigatórias

- O endpoint não deve escolher estratégia nem executar processamento técnico.
- O service de aplicação deve receber registry, factory ou implementações pelo construtor.
- Cada tipo de processamento deve implementar uma interface comum.
- Crie interface de service quando houver múltiplas implementações, boundary entre módulos ou necessidade clara de substituição em testes.
- A escolha da implementação deve ser feita por um registry ou factory injetado.
- Adicione novo tipo criando nova implementação, não alterando regras HTTP.
- Implementações de processamento não devem conhecer `Request`, `Response`, `APIRouter` ou `JSONResponse`.
- Processamento bloqueante deve ser isolado em repository, integração, worker, fila ou executor controlado.
- Métodos públicos devem ser `async def`, tipados e com docstrings NumPy em pt-BR.
- Validações de negócio pertencem ao service; detalhes técnicos pertencem à implementação, repository ou integração.
- Erros conhecidos devem usar exceções de domínio ou de aplicação e serem mapeados por `standard-errors`.

## Checklist

- [ ] Existe uma interface comum para cada família de processamento.
- [ ] Cada tipo tem implementação própria e coesa.
- [ ] O service recebe registry, factory, implementações ou repositories pelo construtor.
- [ ] O endpoint delega para o service sem decidir estratégia.
- [ ] O fluxo permite adicionar novo tipo com baixo impacto.
- [ ] Docstrings explicam intenção, I/O, limites e erros conhecidos.
- [ ] Código bloqueante não roda diretamente no fluxo async sem adaptação.
- [ ] A skill correta foi usada para endpoints, modelos, erros, repositories e integrações.
