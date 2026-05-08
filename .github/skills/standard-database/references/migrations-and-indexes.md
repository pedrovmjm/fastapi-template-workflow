# Migrations, Índices e Evolução de Dados

Toda persistência evolui. SQL muda por migrations de schema; NoSQL muda por evolução de documentos, índices e backfills. O importante é que a mudança seja versionada, reversível quando possível e segura para deploy progressivo.

## SQL

- Use Alembic para criar e revisar migrations.
- Separe mudança estrutural de backfill pesado quando necessário.
- Evite migration longa que bloqueia tabela crítica em horário de tráfego.
- Crie índices de forma compatível com o banco e o volume de produção.
- Planeje deploy em etapas para colunas obrigatórias: adicionar nullable, preencher, validar, tornar obrigatória.

## NoSQL

- Versione criação de índices em script idempotente.
- Registre índices esperados junto ao módulo do domínio.
- Faça backfill de documentos antigos com job controlado.
- Mantenha leitores compatíveis com versão antiga e nova durante a transição.
- Remova campos antigos somente depois de confirmar que não há consumidores.

## Dados e Seeds

- Seed técnico deve ser idempotente.
- Seed de ambiente local não deve conter segredo real.
- Dados de teste não devem virar dependência oculta de produção.
- Backfill deve registrar progresso, falhas e possibilidade de retomar.

## Checklist de Mudança

- [ ] A mudança funciona em deploy rolling.
- [ ] Leitura aceita formato antigo e novo quando necessário.
- [ ] Escrita produz o novo formato.
- [ ] Índices foram planejados antes da carga crescer.
- [ ] Existe plano de rollback ou mitigação.
- [ ] Observabilidade cobre falha, duração e volume processado.
