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
