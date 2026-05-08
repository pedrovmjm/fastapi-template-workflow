---
name: standard-database
description: Padroniza decisões de persistência SQL e NoSQL em aplicações FastAPI, incluindo lifecycle de sessão/conexão, transações, migrations, índices e fronteiras com repositories.
---
# Standard Database - Persistência SQL e NoSQL

Use esta skill ao criar ou revisar infraestrutura de banco de dados, decisões de modelagem de persistência, transações, migrations, índices ou integração entre repositories e banco.

## Responsabilidade Desta Skill

Esta skill é dona de:

- escolha orientada entre SQL, NoSQL ou persistência híbrida;
- lifecycle de engine, client, conexão, sessão e transação;
- padrões para SQLAlchemy assíncrono, Alembic e entidades ORM;
- padrões para MongoDB, documentos, índices e validação de coleções;
- limites entre modelos de persistência, entidades internas e modelos Pydantic públicos;
- estratégia de migrations, seed técnico e evolução de schema/índices.

Esta skill não é dona de:

- regra de negócio: use `standard-services`;
- execução concreta de queries por caso de uso: use `standard-repositories`;
- criação de settings, `.env` ou singleton provider: use `standard-configs`;
- contratos públicos de request/response: use `standard-data-models`;
- status HTTP e rotas: use `standard-endpoints`;
- políticas de autenticação/autorização: use `standard-security`.

## Tabela de Decisão - Referências

| Quando precisar detalhar | Leia a referência |
| --- | --- |
| Quando precisar aprofundar escolha entre sql, nosql e persistência híbrida. | [Escolha entre SQL, NoSQL e persistência híbrida](references/database-selection.md) |
| Quando precisar aprofundar persistência sql assíncrona. | [Persistência SQL assíncrona](references/sql-persistence.md) |
| Quando usar banco documental ou MongoDB. | [Persistência NoSQL e MongoDB](references/nosql-persistence.md) |
| Quando precisar aprofundar migrations, índices e evolução de dados. | [Migrations, índices e evolução de dados](references/migrations-and-indexes.md) |

## Regras Obrigatórias

- Banco deve ser acessado por repositories, nunca diretamente por endpoints.
- Services devem coordenar casos de uso e transações, mas não montar queries.
- Repositories recebem sessão, conexão, database ou collection pelo construtor.
- Clients globais podem existir apenas como providers configurados, não dentro do repository.
- Modelos públicos Pydantic não devem vazar detalhes de ORM, `ObjectId`, `_id` ou tipos internos.
- SQL deve usar queries parametrizadas ou ORM; nunca concatene entrada do usuário em query.
- MongoDB deve ter índices explícitos para filtros frequentes e restrições de unicidade.
- Unicidade, idempotência e invariantes concorrentes devem ser protegidos no banco, não apenas validados em memória.
- Operações read-check-write devem declarar estratégia contra race condition antes de serem aceitas.
- Toda decisão de persistência deve considerar consistência, consulta, escala, auditoria e custo operacional.

## Concorrência e Race Conditions

Sempre revise fluxos em que duas requests, workers ou retries podem atuar sobre o mesmo recurso ao mesmo tempo. Validação prévia em service ou repository não substitui garantia atômica do banco.

### SQL

- Use constraint única, foreign key, check constraint ou exclusion constraint para invariantes que o banco consegue proteger.
- Prefira `INSERT ... ON CONFLICT`, upsert ou operação atômica equivalente para criação idempotente.
- Evite padrão `SELECT` para verificar existência seguido de `INSERT` sem constraint única correspondente.
- Use `SELECT ... FOR UPDATE`, lock pessimista, coluna de versão ou isolamento maior quando o fluxo altera recurso lido anteriormente.
- Atualizações condicionais devem incluir a condição no próprio `UPDATE`, por exemplo status atual, versão ou ownership.
- Trate violações de constraint e conflitos de serialização como parte esperada do fluxo concorrente, convertendo para erro de domínio adequado.
- Não compartilhe a mesma sessão ou transação entre tasks assíncronas concorrentes.

### MongoDB e Documental

- Use índice único para qualquer unicidade real do domínio.
- Prefira `findOneAndUpdate`, update com filtro condicional, `$inc`, `$setOnInsert` e upsert atômico quando possível.
- Evite verificar existência com `find` e depois inserir sem índice único ou upsert protegido.
- Use campo de versão, `updated_at` esperado ou status atual no filtro quando duas operações podem editar o mesmo documento.
- Use transação MongoDB apenas quando a regra exigir atomicidade entre múltiplos documentos ou coleções.
- Garanta idempotência em comandos sujeitos a retry, webhook, fila ou reprocessamento.

### Redis, Cache e Locks

- Cache não deve ser fonte de verdade para invariantes de negócio.
- Locks distribuídos devem ter TTL, token de posse e liberação segura; não use lock sem expiração.
- Use operação atômica do Redis, como `SET NX EX`, `INCR` ou script Lua, quando o valor controla concorrência.
- Planeje comportamento quando o lock expira, o processo morre ou a operação é repetida.

### Filas, Workers e Eventos

- Mensagens podem ser entregues mais de uma vez; consumers devem ser idempotentes.
- Use chave de idempotência, tabela/coleção de deduplicação ou constraint única para eventos processados.
- Reprocessamento não deve duplicar efeitos colaterais como cobrança, saldo, envio definitivo ou criação de recurso.
- Ordem de eventos não deve ser assumida sem mecanismo explícito de versionamento, sequência ou particionamento.

## Checklist

- [ ] A escolha SQL/NoSQL foi justificada pelo padrão de acesso e consistência.
- [ ] O lifecycle de conexão/sessão está claro.
- [ ] Transações ou garantias de consistência foram definidas.
- [ ] Race conditions foram avaliadas para criação, atualização, retry, worker e webhook.
- [ ] Invariantes concorrentes têm constraint, índice único, upsert, lock, versão ou update condicional.
- [ ] Migrations SQL ou evolução de índices NoSQL foram previstas.
- [ ] Entidades internas não vazam para response pública.
- [ ] Dados sensíveis não são persistidos sem necessidade, criptografia ou mascaramento.
