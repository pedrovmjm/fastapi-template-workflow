# FastAPI Template Workflow

Template para padronizar workflow de desenvolvimento em projetos FastAPI, combinando **Spec-Driven Development (SDD)**, agents especializados, skills reutilizaveis e um `bootstrap.py` para iniciar uma aplicacao com uma base escalavel.

A ideia do repositorio e servir como ponto de partida para times que querem criar APIs FastAPI com estrutura consistente, boas praticas desde o primeiro commit e rastreabilidade entre especificacao, implementacao, testes e revisoes.

## O Que Este Projeto Entrega

- **Workflow SDD**: organizacao de trabalho por especificacao, design, tarefas e execucao.
- **Agents especializados**: orquestrador, planner, coder, revisores de seguranca, testes, lint e cache.
- **Skills reutilizaveis**: padroes para endpoints, services, repositories, configs, logs, traces, testes, seguranca, banco de dados, cache em memoria e mais.
- **Bootstrap FastAPI**: script para gerar uma aplicacao inicial com configuracao, observabilidade, middlewares, rotas, repositories e testes.
- **Estrutura de projeto padronizada**: separacao clara entre `configs`, `routes`, `services`, `repositories`, `models`, `middlewares` e `observability`.
- **Documentacao em pt-BR**: regras, convencoes e orientacoes escritas para uso no dia a dia do time.

## Quando Usar

Use este template quando voce quiser:

- iniciar uma API FastAPI com base tecnica consistente;
- criar um padrao reutilizavel para varios projetos;
- orientar desenvolvimento com regras claras para agents e Copilot;
- manter rastreabilidade entre requisitos, decisoes e commits;
- reduzir decisoes repetitivas sobre estrutura, logs, configs, clients, banco e testes.

## Como Usar Este Repositorio

Este repositorio pode ser usado de tres formas principais:

1. **Como template de projeto**: rode o `bootstrap.py` para criar uma aplicacao FastAPI inicial em outro diretorio.
2. **Como guia de padroes**: consulte as skills em `.github/skills/` quando estiver implementando endpoints, services, repositories, configs, logs, traces, testes ou seguranca.
3. **Como workflow de desenvolvimento**: use os agents e o SDD para transformar ideias em specs, designs, tarefas e implementacoes rastreaveis.

Nada aqui e obrigatorio para sempre. O objetivo e dar um comeco forte, com escolhas razoaveis e consistentes. Se o time preferir outro nome de pasta, outra estrategia de repository, outro provider, outra convencao de log ou outro jeito de organizar features, pode trocar sem cerimonia.

E se voce nao gostou de algum padrao, tudo bem: reclame com quem inventou o padrao, nao comigo. Eu so deixei a plaquinha organizada na porta. Brincadeiras a parte, use, ajuste, remova e evolua o que fizer sentido para o seu contexto.

## Como Usar o Bootstrap

O arquivo [bootstrap.py](bootstrap.py) e o ponto de entrada para criar a estrutura inicial de uma aplicacao FastAPI.

### Visualizar o Que Sera Criado

```bash
python bootstrap.py --name meu-projeto --domain vendas --dry-run
```

O `--dry-run` mostra os arquivos que seriam gerados sem escrever no disco.

### Criar a Estrutura no Diretorio Atual

```bash
python bootstrap.py --name meu-projeto --domain vendas
```

### Criar em Outro Diretorio

```bash
python bootstrap.py --name meu-projeto --domain vendas --target ../meu-projeto
```

### Definir a Versao Inicial da API

```bash
python bootstrap.py --name meu-projeto --domain vendas --api-version v1
```

Tambem e aceito passar apenas o numero:

```bash
python bootstrap.py --api-version 2
```

Nesse caso o bootstrap normaliza para `v2`.

### Sobrescrever Arquivos Existentes

```bash
python bootstrap.py --force
```

Sem `--force`, arquivos existentes sao preservados e aparecem como `skip` na saida.

## Opcoes do Bootstrap

| Opcao | Descricao |
| --- | --- |
| `--name` | Nome publico da aplicacao. Se omitido, usa o nome do diretorio alvo. |
| `--domain` | Dominio funcional principal. Se omitido, usa o nome do projeto. |
| `--api-version` | Versao inicial da API no formato `v1`, `v2` ou numero inteiro. Padrao: `v1`. |
| `--target` | Diretorio onde a estrutura sera criada. Padrao: diretorio atual. |
| `--force` | Sobrescreve arquivos ja existentes. |
| `--dry-run` | Simula a criacao dos arquivos sem gravar no disco. |

## Estrutura Criada Pelo Bootstrap

O bootstrap gera uma aplicacao FastAPI com esta base:

```text
.
├── pyproject.toml
├── .env.example
├── start.py
├── src/
│   ├── main.py
│   ├── configs/
│   │   ├── azure_ad.py
│   │   ├── settings.py
│   │   ├── httpx_client.py
│   │   ├── mongo.py
│   │   ├── sql_database.py
│   │   ├── object_storage.py
│   │   └── values_domains/
│   ├── middlewares/
│   │   ├── api_version.py
│   │   └── correlation_id.py
│   ├── models/
│   │   ├── auth/
│   │   ├── health/
│   │   └── utils/
│   ├── observability/
│   │   ├── correlation.py
│   │   ├── logging/
│   │   └── telemetry/
│   ├── repository/
│   │   ├── microsoft_graph/
│   │   └── object_storage/
│   ├── routes/
│   │   └── health/
│   ├── security/
│   └── services/
│       ├── auth/
│       └── microsoft_graph/
└── tests/
```

### Principais Pecas Geradas

- `pyproject.toml`: dependencias base para FastAPI, Uvicorn, Pydantic, HTTPX, PyJWT, OpenTelemetry, MongoDB, SQLAlchemy, SQLite async e extras para object storage.
- `.env.example`: variaveis organizadas por dominio, como `APP__`, `SERVER__`, `AUTH__`, `LOGGING__`, `TELEMETRY__`, `MONGO__`, `SQL_DATABASE__` e `OBJECT_STORAGE__`.
- `start.py`: entrypoint operacional que carrega settings, configura logs e inicia o Uvicorn.
- `src/main.py`: composicao da aplicacao FastAPI, lifespan, recursos globais, middlewares, rotas e telemetry.
- `src/configs/`: carregamento de settings, clients e providers compartilhados.
- `src/configs/values_domains/`: modelos Pydantic separados por dominio de configuracao.
- `src/middlewares/api_version.py`: resolucao da versao da API por path (`/api-internal/vN`), com header como complemento.
- `src/models/auth/`: contratos internos para usuario autenticado, grupos e superior direto.
- `src/models/utils/`: contratos compartilhados para `meta` e `links` em respostas HTTP, com helper assíncrono para montar o contexto dinâmico de respostas `GET`.
- `src/routes/health/`: endpoint `/api-internal/v1/health` com envelope `data`, `meta` e `links`.
- `src/security/`: validacao JWT Azure AD, dependencies FastAPI e helpers de scopes, roles e grupos.
- `src/observability/`: logging estruturado e setup de tracing OpenTelemetry.
- `src/repository/microsoft_graph/`: chamadas tecnicas ao Microsoft Graph para perfil, manager, grupos diretos e foto.
- `src/repository/object_storage/`: interface, factory e implementacoes para Azure Blob e AWS S3.
- `src/services/`: camada reservada para regras de negocio, auth e enriquecimento opcional via Microsoft Graph.
- `tests/`: ponto inicial para a suite de testes.

## Depois de Gerar o Projeto

Um fluxo inicial comum e:

```bash
python bootstrap.py --name minha-api --domain meu-dominio --target ../minha-api
cd ../minha-api
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e .
python start.py
```

Com a aplicacao rodando, acesse:

- `GET /api-internal/v1/health`
- `/docs`
- `/redoc`

## Workflow SDD

O SDD organiza features em fases adaptaveis:

```text
SPECIFY -> DESIGN -> TASKS -> EXECUTE
```

Nem toda demanda precisa passar por todas as fases. Bugs simples e ajustes pequenos podem usar modo rapido; features maiores devem ter especificacao, desenho tecnico e tarefas atomicas.

A estrutura esperada de specs e:

```text
.specs/
├── project/
│   ├── PROJECT.md
│   ├── ROADMAP.md
│   └── STATE.md
├── codebase/
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── STRUCTURE.md
│   ├── TESTING.md
│   ├── INTEGRATIONS.md
│   └── CONCERNS.md
├── features/
│   └── nome-da-feature/
│       ├── spec.md
│       ├── context.md
│       ├── design.md
│       └── tasks.md
└── quick/
    └── id-da-tarefa/
        ├── TASK.md
        └── SUMMARY.md
```

## Agents

Os agents em `.github/agents/` orientam a execucao do workflow:

- `workflow-orchestrator`: coordena o fluxo e direciona o trabalho.
- `sdd-planner`: ajuda a transformar demanda em especificacao, design e tarefas.
- `coder-engineer`: implementa alteracoes no codigo.
- `security-reviewer`: revisa riscos de seguranca, dados sensiveis e abuso.
- `test-engineer`: planeja e ajusta testes.
- `lint-engineer`: valida lint, formatacao e type checks.
- `cache-reviewer`: avalia decisoes de cache em memoria.
- `sdd-refiner`: refina specs e decisoes do fluxo SDD.

## Skills

As skills em `.github/skills/` documentam padroes reutilizaveis. As principais incluem:

- `spc-driven`: workflow SDD e referencias para specify, design, tasks, implementacao e handoff.
- `fastapi-best-practices`: composicao FastAPI, dependency injection, auth/autorizacao, async e tratamento de erros.
- `standard-configs`: settings, values domains e providers.
- `standard-endpoints`: routers, status codes, query params e documentacao de endpoints.
- `standard-services`: padroes para camada de service.
- `standard-repositories`: padroes para repositories e execucao de queries/blob/openai.
- `standard-data-models`: contratos de request/response e modelos de persistencia.
- `standard-database`: selecao de banco, SQL, NoSQL, migrations e indexes.
- `standard-integrations`: HTTP clients, webhooks, resiliencia e observabilidade.
- `standard-logs`: eventos de log, correlacao e dados sensiveis.
- `standard-traces`: traces, spans, correlacao e atributos seguros.
- `standard-middleware`: ordem de middlewares, correlation ID e security headers.
- `standard-errors`: contrato de erro, validacoes e mapeamento de excecoes.
- `standard-security`: OWASP API, autenticacao, autorizacao e protecao de dados.
- `standard-tests`: estrategia de testes unitarios, integracao, fixtures e e2e.
- `start-agents`: boas praticas para OpenAI Agents SDK, LangGraph, tools, guardrails, logs, traces e agentes seguros.
- `standard-docstrings`: docstrings no estilo NumPy.
- `in-memory-cache`: decisao, implementacao e revisao de cache local.
- `processing-interfaces`: interfaces para processamento e composicao por DI.
- `conversation-conventions`: atualizacao de convencoes a partir de feedback da conversa.

## Como Evoluir Uma Feature

1. Registre ou atualize a spec em `.specs/features/<feature>/spec.md`.
2. Use as skills relevantes para definir padroes de endpoints, services, repositories, models, logs, traces e testes.
3. Quebre a entrega em tarefas pequenas quando a feature envolver mais de um componente.
4. Implemente o menor slice vertical possivel.
5. Rode testes, lint e revisoes relevantes.
6. Mantenha commits ou notas de execucao referenciando os requisitos quando aplicavel.

## Ciclo Completo de Desenvolvimento com Agents

O fluxo recomendado e sequencial. O `workflow-orchestrator` coordena as etapas, mas nao implementa codigo, nao roda comandos e nao faz commit. Ele chama um agent por vez, incorpora o resultado e so entao decide o proximo passo. Isso mantem rastreabilidade e evita que planejamento, implementacao, revisao e validacao se misturem.

```text
TAREFA RECEBIDA
  -> TRIAGEM DE ESCOPO
  -> SPEC / QUICK TASK
  -> DESIGN E TASKS, quando necessario
  -> APROVACAO DO PLANO
  -> CODIGO
  -> REVISAO DE SEGURANCA
  -> TESTES
  -> LINT / FORMAT / TYPE CHECK
  -> RESUMO DE VALIDACAO
  -> COMMIT COM APROVACAO
  -> PR COM APROVACAO
```

### 1. Receber e classificar a tarefa

Ao receber uma demanda, o primeiro passo e entender o tamanho real da mudanca:

- **Modo rapido**: ajuste pequeno, em ate 3 arquivos, sem novo endpoint, contrato publico, entidade, tabela, repository ou service. Registre em `.specs/quick/<id>/TASK.md` quando precisar de rastro.
- **Feature media**: comportamento claro, mas com impacto em codigo de aplicacao. Crie `.specs/features/<feature>/spec.md`.
- **Feature grande ou complexa**: varios componentes, duvidas de dominio, banco, auth, integracoes, cache, agents ou risco relevante. Use `spec.md`, `design.md` e `tasks.md`.

O agent principal desta etapa e o `sdd-planner`. Ele consulta as skills aplicaveis, identifica padroes existentes e transforma o pedido em requisitos, decisoes e criterios de aceite.

### 2. Planejar antes de codificar

Para mudancas nao triviais, o planejamento deve deixar claro:

- objetivo e fora de escopo;
- requisitos e criterios de aceite;
- arquivos ou camadas provaveis;
- skills que definem o padrao tecnico;
- riscos de seguranca, dados, cache, logs, traces ou compatibilidade;
- comandos esperados de validacao.

Quando a feature cria contrato publico, endpoint, entidade, banco, repository ou service, a implementacao so deve comecar depois de aprovacao explicita do plano. Se houver ambiguidade, use `sdd-refiner` para revisar clareza, dependencias, tarefas atomicas e aderencia as skills.

### 3. Implementar o menor slice vertical

Depois da aprovacao, o `coder-engineer` implementa o menor slice vertical seguro. Ele deve:

- ler a spec, design, tasks e codigo existente antes de editar;
- seguir a arquitetura local em `routes`, `services`, `repository`, `models`, `configs`, `middlewares` e `observability`;
- manter rotas finas, services com orquestracao de negocio e repositories com execucao tecnica;
- usar docstrings em pt-BR no formato definido por `standard-docstrings` para APIs publicas novas ou alteradas;
- preservar logs, traces, correlation id e protecao de dados sensiveis quando aplicavel;
- registrar `SPEC_DEVIATION` quando precisar divergir do plano aprovado.

O `coder-engineer` nao cria nem executa testes, nao roda lint e nao faz commit. Ele devolve o que mudou, quais cenarios precisam de teste e um plano sugerido de commits incrementais.

### 4. Revisar seguranca antes de fechar comportamento

Depois da implementacao, o `security-reviewer` verifica riscos como:

- autenticacao, autorizacao, roles, grupos, tenant e posse de recurso;
- BOLA/BFLA em rotas com ids ou acoes por recurso;
- vazamento de secrets, tokens, dados pessoais, payloads sensiveis, stack traces ou `str(exc)`;
- CORS, rate limiting, abuso, SSRF, injection, path traversal, uploads e chamadas externas;
- logs e traces sem dados sensiveis;
- riscos de LLM, agents, tools e prompt injection quando houver fluxo agentico;
- cache em memoria com permissoes stale, dados sensiveis ou comportamento inconsistente em multi-worker.

Se houver findings, o fluxo volta para correcao antes de seguir para testes finais.

### 5. Testar proporcionalmente ao risco

O `test-engineer` transforma criterios de aceite e findings de seguranca em testes. Ele escolhe o nivel adequado:

- unitario para regras isoladas;
- integracao para fronteiras reais, como banco, clients, repositories, rotas e DI;
- E2E para fluxos criticos de usuario ou API.

Sempre que possivel, ele executa os comandos reais do projeto, por exemplo:

```bash
python3 -m pytest
```

O resultado precisa trazer comando exato, exit code e resumo do output. Nao se declara suite aprovada sem evidencia executada.

### 6. Rodar lint, format e type check

Depois de testes e correcoes relevantes, o `lint-engineer` descobre os comandos configurados no projeto em `README.md`, `pyproject.toml`, `Makefile`, `tox.ini`, `.github/workflows/` ou scripts. Quando existirem, ele executa lint, format check e type check, por exemplo:

```bash
python3 -m ruff check .
python3 -m ruff format --check .
npm run typecheck
```

Use apenas os comandos que realmente existem no projeto alvo. Se algum check nao estiver configurado, registre a lacuna em vez de fingir validacao.

### 7. Consolidar validacao

Antes de versionar, consolide:

- arquivos alterados;
- requisitos ou tarefas cobertos;
- comandos executados, exit code e resumo;
- revisao de seguranca;
- riscos restantes;
- `SPEC_DEVIATION`, se houver;
- plano de commits sugerido.

Esse resumo e o gate que separa "codigo feito" de "entrega pronta para commit".

### 8. Commitar com Conventional Commits

Commits usam a skill `conventional-commit` e exigem aprovacao explicita do usuario. O agent deve primeiro apresentar:

- branch atual;
- spec ou tarefa relacionada;
- arquivos que entrarao e arquivos excluidos;
- validacoes feitas;
- mensagem ou plano de commits.

Formato recomendado:

```text
<type>(<scope>): <description>

Refs: <id-da-spec-ou-requisito>
```

Exemplos:

```text
feat(auth): adicionar bootstrap de Azure AD
fix(cors): ajustar origens permitidas
docs(workflow): documentar ciclo de desenvolvimento
test(health): cobrir envelope do endpoint de health
```

Quando a entrega tiver responsabilidades diferentes, prefira commits incrementais. Exemplo: um commit para configs, outro para services/routes e outro para testes ou docs. O commit so acontece depois de resposta explicita como `sim`, `pode commitar` ou `aprovado`.

### 9. Abrir Pull Request

PR e um gate separado do commit. Aprovacao para commitar nao autoriza abrir PR automaticamente.

Use `create-pull-request` para:

- revisar branch, base e commits incluidos;
- verificar se a branch tem responsabilidade unica;
- montar titulo fiel ao diff;
- preencher corpo com resumo, validacoes, impacto, riscos e rastreabilidade;
- pedir aprovacao explicita antes de `git push` e `gh pr create`.

Se a branch mistura responsabilidades independentes, recomende dividir em PRs menores. Se o time decidir manter um PR unico, o titulo e o corpo devem declarar o escopo completo.

### 10. Revisar PR

Depois do PR aberto, use `pr-review` quando quiser uma revisao multi-persona. Ela pode avaliar, por exemplo:

- impacto de backend;
- riscos de seguranca;
- qualidade de testes;
- riscos de operacao ou DevOps;
- prontidao para merge.

### Mapa Rapido de Agents

| Momento | Agent/skill | Responsabilidade |
| --- | --- | --- |
| Coordenacao geral | `workflow-orchestrator` | Sequenciar etapas e handoffs, sem editar ou executar comandos. |
| Planejamento | `sdd-planner` | Criar spec, design, tarefas e criterios de aceite. |
| Refinamento | `sdd-refiner` | Revisar clareza, riscos, dependencias e rastreabilidade. |
| Implementacao | `coder-engineer` | Alterar codigo e docs do slice aprovado. |
| Seguranca | `security-reviewer` | Auditar auth, dados sensiveis, logs, traces, abuso e LLM/agents. |
| Testes | `test-engineer` | Criar, ajustar e executar testes proporcionais ao risco. |
| Qualidade estatica | `lint-engineer` | Executar lint, format check e type check. |
| Cache | `cache-reviewer` | Avaliar TTL, invalidacao, memoria, multi-worker e testes. |
| Commit | `conventional-commit` | Preparar commits incrementais com aprovacao explicita. |
| Pull Request | `create-pull-request` | Preparar e abrir PR com aprovacao explicita. |
| Revisao de PR | `pr-review` | Revisar PR por perfis especializados. |

Exemplo de pedido para agent:

```text
@spc "Especificar e implementar a feature de cadastro de clientes"
```

Para tarefas menores:

```text
@spc "Adicionar campo telefone no cadastro de clientes"
```

## Estrutura Deste Repositorio

```text
.
├── README.md
├── bootstrap.py
├── .github/
│   ├── agents/
│   ├── skills/
│   ├── prompts/
│   └── copilot-instructions.md
└── .specs/
    ├── project/
    ├── codebase/
    ├── features/
    └── quick/
```

## Boas Praticas Esperadas

- manter nomes tecnicos em ingles e documentacao em pt-BR;
- separar rotas, services, repositories, models e configs;
- usar settings tipadas em vez de acessar ambiente diretamente espalhado pelo codigo;
- centralizar clients externos e recursos globais no ciclo de vida da aplicacao;
- evitar logs com dados sensiveis;
- adicionar testes proporcionais ao risco da mudanca;
- preferir alteracoes pequenas, rastreaveis e revisaveis.

Essas praticas sao recomendacoes iniciais. Elas existem para reduzir atrito, nao para travar o projeto. Quando uma regra atrapalhar mais do que ajudar, documente a decisao, ajuste o padrao e siga o jogo.

## Proximos Passos

1. Execute `python bootstrap.py --dry-run` para ver a estrutura gerada.
2. Crie uma aplicacao em um diretorio alvo com `python bootstrap.py --target ../minha-api`.
3. Leia `.github/skills/spc-driven/SKILL.md` para entender o fluxo SDD.
4. Use os agents e skills como guia para implementar a primeira feature real.
