# FastAPI Template Workflow

> Um repositório template profissional para projetos FastAPI com boas práticas integradas, agents especializados e skills reutilizáveis. **Pronto para bootstrapping** de aplicações do zero com qualidade enterprise.

## 🚀 O Que É

Este é um **template corporativo** que fornece:

- ✅ **Workflow SDD** (Spec-Driven Development) — metodologia 4 fases para planejar e implementar features com precisão
- ✅ **Agents especializados** — orquestrador + especialistas para revisão de specs, arquitetura, testes e segurança
- ✅ **Skills reutilizáveis** — padrões de código, logs, traces, endpoints, middlewares e docstrings
- ✅ **Bootstrap automático** — scaffolding de projetos FastAPI do zero com estrutura pronta
- ✅ **Rastreabilidade completa** — specs ↔ tarefas ↔ commits atômicos com IDs únicos
- ✅ **Documentação em pt-BR** — tudo em português (código e identificadores técnicos em inglês)

Ideal para:
- 🏢 Equipes que precisam de **processos escaláveis**
- 🔄 Projetos com **múltiplas features paralelas**
- 📋 Contextos que exigem **rastreabilidade** (compliance, auditoria)
- 🛡️ Aplicações que precisam de **boas práticas desde o dia 1**

## 📦 O Que Vem Dentro

### Core (Pronto ✅)

```
.github/
├── agents/              # Orquestrador + especialistas
│   └── 1.md            # Orchestrator (gateway central)
└── skills/             # Padrões reutilizáveis
    ├── spc-driven/     # Skill: Workflow SDD 4 fases
    ├── domain/         # Skill: Padrões de domínio
    ├── standard-*      # Skills: Logs, traces, endpoints, docstrings, middlewares
    └── ...
```

### Estrutura de Specs (Pronto ✅)

```
.specs/
├── project/
│   ├── PROJECT.md          # Visão e goals
│   ├── ROADMAP.md          # Features e milestones
│   └── STATE.md            # Memory: decisões, blockers, lições, TODOs
├── codebase/               # Análise brownfield (p/ projetos existentes)
│   ├── STACK.md            # Tech stack
│   ├── ARCHITECTURE.md     # Padrões arquiteturais
│   ├── CONVENTIONS.md      # Convenções de código
│   ├── STRUCTURE.md        # Layout de diretórios
│   ├── TESTING.md          # Estratégia de testes
│   ├── INTEGRATIONS.md     # Integrações externas
│   └── CONCERNS.md         # Preocupações técnicas
├── features/               # Especificações de features
│   └── [feature-name]/
│       ├── spec.md         # Requisitos rastreáveis
│       ├── context.md      # Decisões em áreas cinzentas
│       ├── design.md       # Arquitetura e componentes
│       └── tasks.md        # Tarefas atômicas
└── quick/                  # Modo rápido (bugs, configs)
    └── [task-id]/
        ├── TASK.md
        └── SUMMARY.md
```

### Aplicação (Em Bootstrap 🚧)

```
src/                    # Estrutura padrão (quando bootstrap estiver pronto)
├── config/            # Configuração por domínio
├── routes/            # Endpoints REST
├── services/          # Lógica de negócio
├── repositories/      # Acesso a dados
├── models/            # Domain models
├── middlewares/       # FastAPI middlewares
├── observability/     # Logs, traces, métricas
└── utils/             # Utilitários compartilhados
```

## 🔄 O Workflow SDD (Spec-Driven Development)

Todo feature segue este fluxo adaptativo:

```
┌─────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  SPECIFY    │ → │  DESIGN  │ → │  TASKS   │ → │ EXECUTE  │
│ (Obrigatório)│   │(Opcional)│    │(Opcional)│    │(Obrigat.)│
└─────────────┘    └──────────┘    └──────────┘    └──────────┘
```

**Dimensionamento automático por escopo:**

| Escopo | Exemplo | Especificar | Design | Tarefas | Executar |
|--------|---------|-------------|--------|---------|----------|
| **Pequeno** | Config, bugfix | Rápido (1 pág) | ✗ | ✗ | ✓ |
| **Médio** | Feature clara | Completo | ✗ | ✗ | ✓ |
| **Grande** | Multi-componente | Completo | ✓ | ✓ | ✓ |
| **Complexo** | Novo domínio | Completo + Discuss | ✓ | ✓ | ✓ + UAT |

## 🤖 Agents e Specialistas

O **Orquestrador** (`orchestrator-sdlc`) roteia cada feature para:

1. **Especialista em specs** — Valida requisitos, clareza e rastreabilidade
2. **Arquiteto** — Revisa decisões de design, componentes, padrões
3. **Engenheiro de testes** — Define plano de testes, casos de cobertura
4. **Security reviewer** — Valida segurança, compliance, boas práticas
5. **DevOps/Infra** — Validações de deployment e observabilidade

*Nota: Agents especializados estão em desenvolvimento. Orquestrador pronto.*

## 🛠️ Skills Disponíveis

### ✅ Prontos para Usar

- **spc-driven** — Workflow 4 fases com memory persistente
- **standard-logs** — Padrão de logging estruturado
- **standard-traces** — Padrão de tracing distribuído
- **standard-endpoints** — Padrão de endpoints REST
- **standard-docstrings** — Padrão de docstrings em Python
- **standard-middleware** — Padrão de middlewares
- **domain** — Padrões de modelagem de domínio

### 🚧 Em Desenvolvimento

- **bootstrap.py** — Script para scaffolding automático
- Templates de spec — Para acelerar criação de features
- Prompts de agents — Instruções especializadas para cada revisor

## 📋 Como Usar Este Template

### 1. **Iniciar um Novo Projeto**

```bash
# Clonar template
git clone <this-repo> meu-projeto
cd meu-projeto

# Criar projeto FastAPI (quando bootstrap estiver pronto)
python bootstrap.py --name="meu-projeto" --domain="vendas"
```

### 2. **Especificar uma Nova Feature**

```bash
# Criar spec a partir do template
.specs/features/nova-feature/spec.md
```

Estrutura básica:

```markdown
# Feature: [Nome da Feature]

## Requisitos
- [REQ-001] Descrição do requisito
- [REQ-002] Outro requisito

## Aceitação
- [ ] Critério 1
- [ ] Critério 2

## Arquivos Impactados
- `src/services/novo_servico.py`
- `src/routes/novo_endpoint.py`
```

### 3. **Executar Workflow SDD**

```bash
# No VS Code, invocar skill:
# @spc "Especificar a feature de autenticação"
# → Spec-Driven workflow inicia automaticamente
```

O workflow vai:
- ✓ Gerar spec completo com IDs rastreáveis
- ✓ Rotar para especialistas (conforme necessário)
- ✓ Gerar tarefas atômicas
- ✓ Executar com verificações inline
- ✓ Criar commit atômico com referência a REQs

### 4. **Implementar com Rastreabilidade**

Cada tarefa gera um commit:

```bash
git log --oneline

# Saída esperada:
feat(auth): [REQ-001, REQ-002] Implementar autenticação OAuth2
feat(auth): [REQ-001] Adicionar token refresh
feat(auth): [REQ-002] Validar escopos
```

## 🏗️ Estrutura de Diretórios

```
.
├── README.md                    # Este arquivo
├── .github/
│   ├── agents/                  # Orquestradores especializados
│   ├── skills/                  # Skills e padrões reutilizáveis
│   ├── prompts/                 # Instruções de agents (em dev)
│   └── instructions/            # Customizações VS Code
├── .specs/                      # Especificações e planejamento
│   ├── project/                 # Visão, roadmap, state
│   ├── codebase/                # Análise brownfield
│   ├── features/                # Especificações de features
│   └── quick/                   # Tarefas rápidas
├── src/                         # Aplicação FastAPI (quando bootstrapped)
│   ├── config/
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   └── observability/
├── tests/                       # Suite de testes
├── docker/                      # Docker setup
├── requirements.txt             # Dependências Python
└── pyproject.toml              # Configuração do projeto
```

## 🎯 Status Atual

### ✅ Pronto para Usar
- [x] Workflow SDD (4 fases adaptativo)
- [x] Skill completa com 200+ linhas de documentação
- [x] Estrutura de specs definida
- [x] Orquestrador base
- [x] 7 skills de padrões de código

### 🚧 Em Progresso
- [ ] `bootstrap.py` — scaffolding automático
- [ ] Agents especializados (3+ agentes)
- [ ] Prompts de agents prontos
- [ ] Aplicação de exemplo completa

### 📋 Roadmap

**Fase 0 (Foundation — Agora)**
- [ ] Completar bootstrap.py
- [ ] Criar templates de spec
- [ ] Documentar walkthrough de primeira feature

**Fase 1 (MVP — T+2 semanas)**
- [ ] Agents especializados funcional
- [ ] Exemplo completo (auth + CRUD)
- [ ] Documentação de deployment

**Fase 2 (Production Ready — T+4 semanas)**
- [ ] Observabilidade completa (logs, traces, métricas)
- [ ] CI/CD automatizado
- [ ] Exemplos de integração (BD, cache, queues)

## 💡 Exemplos

### Exemplo 1: Feature Pequena (Modo Rápido)

**Tarefa:** Adicionar novo campo à tabela de usuários

```bash
@spc "Adicionar campo 'telefone' aos usuários"
```

→ Workflow rápido: Implementa diretamente sem design/tasks formais

### Exemplo 2: Feature Média

**Tarefa:** Implementar system de notificações por email

```bash
@spc "Especificar feature de notificações por email"
```

→ Gera spec + design + tarefas + valida design antes de implementar

### Exemplo 3: Feature Complexa

**Tarefa:** Integrar pagamento com Stripe

```bash
@spc "Especificar integração de pagamento Stripe com webhooks"
```

→ Workflow completo: Discuss áreas cinzentas → Design detalhado → Tarefas atômicas → UAT interativo → Deploy seguro

## 📚 Documentação Detalhada

- [Skill SDD (Spec-Driven Development)](/.github/skills/spc-driven/SKILL.md) — Workflow completo
- [Skills de Padrões](/.github/skills/) — Logs, traces, endpoints, middlewares
- [Especificações do Projeto](/.specs/project/) — Visão, roadmap, decisões
- [Análise de Codebase](/.specs/codebase/) — Stack, arquitetura, conventions

## 🤝 Contributing

Contribuições são bem-vindas! Para adicionar novas skills ou especialistas:

1. Crie diretório `/.github/skills/[skill-name]/`
2. Adicione `SKILL.md` com frontmatter YAML
3. Documente em pt-BR com exemplos
4. Teste com @spc ou nome da skill

## 📄 Licença

Este template é fornecido como-é. Use livremente em seus projetos.

---

**Próximos passos:**
1. Leia [.specs/project/PROJECT.md](.specs/project/PROJECT.md) para visão do projeto
2. Explore [.github/skills/spc-driven/SKILL.md](.github/skills/spc-driven/SKILL.md) para entender o workflow
3. Experimente: `@spc "Especificar primeira feature"` no VS Code

**Dúvidas?** Veja a documentação em [.specs/](.specs/) ou revise os exemplos em [.github/skills/](.github/skills/).

🚀 **Bora construir algo incrível!**
