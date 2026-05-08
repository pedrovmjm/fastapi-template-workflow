# Persistência SQL Assíncrona

Use SQLAlchemy assíncrono quando o projeto precisar de banco relacional com FastAPI async. O padrão recomendado é engine criado em provider/config, `async_sessionmaker` configurado uma vez e `AsyncSession` curta por request, job ou unidade de trabalho.

## Lifecycle

- Crie `AsyncEngine` no provider de infraestrutura.
- Crie `async_sessionmaker` a partir do engine.
- Abra `AsyncSession` por request ou unidade de trabalho.
- Feche a sessão no final do escopo.
- Não compartilhe a mesma sessão entre tasks concorrentes.

## Transações

- Use transação explícita para comandos que alteram estado.
- Faça commit apenas quando o caso de uso terminar com sucesso.
- Faça rollback em exceções.
- Evite commit dentro de métodos pequenos de repository quando o service precisa coordenar múltiplas operações.
- Use lock ou isolamento adequado quando houver concorrência sobre o mesmo recurso.

## ORM e Entidades

- Entidade ORM representa persistência, não response pública.
- Modelo Pydantic público fica em `standard-data-models`.
- Repository converte ORM para entidade interna ou DTO técnico.
- Lazy loading deve ser evitado em responses; carregue explicitamente o que será usado.
- Relacionamentos devem ser modelados pelo comportamento de consulta, não só pelo diagrama conceitual.

## Queries

- Use SQLAlchemy Core/ORM ou SQL parametrizado.
- Nunca concatene entrada do usuário em SQL.
- Defina paginação e ordenação permitida em listas.
- Evite `SELECT *` em queries críticas.
- Registre métricas de duração e cardinalidade sem logar parâmetros sensíveis.

## Alembic

- Toda mudança de schema deve ter migration.
- Migration deve ser reversível quando possível.
- Seeds técnicos devem ser idempotentes.
- Dados de produção devem ter plano de backfill quando a coluna nova exige preenchimento.

## Checklist SQL

- [ ] Engine e sessionmaker vêm de config/provider.
- [ ] Sessão tem escopo curto e fechamento garantido.
- [ ] Transação está no nível certo do caso de uso.
- [ ] Query é parametrizada.
- [ ] Migration acompanha mudança de schema.
- [ ] ORM não aparece em contrato público.

## Referências Externas

- SQLAlchemy 2.0 AsyncIO: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
