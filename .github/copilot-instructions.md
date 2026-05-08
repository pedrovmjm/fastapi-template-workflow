# Copilot Instructions

Responda ao usuario em pt-BR por padrao.

Este repositorio usa custom agents do GitHub Copilot em `.github/agents/` e skills em `.github/skills/`.

Para tarefas FastAPI que envolvam planejamento, implementacao, seguranca, testes ou lint, use o agente `workflow-orchestrator` como ponto de entrada. Ele coordena:

- `sdd-planner` para especificacao, design e plano SDD/SPC.
- `sdd-refiner` para revisar ambiguidade, criterios de aceite, riscos e tarefas.
- `coder-engineer` para implementacao com as skills standard aplicaveis.
- `security-reviewer` para auditoria de seguranca, privacidade, logs, traces e abuso.
- `test-engineer` para criar, ajustar e executar testes depois da revisao de seguranca.
- `lint-engineer` para lint, format e type checks depois dos testes.

O `workflow-orchestrator` nao deve ser invocado automaticamente. Selecione-o explicitamente quando quiser o workflow completo.

O orquestrador so pode coordenar com `read`, `search`, `todo` e `agent`. O alias `agent` representa a capacidade de chamar subagents, isto e, `runSubagents`. Ele nao deve escrever arquivos, rodar comandos, implementar codigo ou executar skills diretamente.

Skills em `.github/skills/` sao referencias de padrao e ownership. O orquestrador deve encaminhar as skills relevantes no prompt dos subagents responsaveis; quem executa planejamento, codigo, revisao ou validacao e sempre um agent especializado.

Antes de alterar codigo, o agent executor deve consultar as skills relevantes em `.github/skills/` e preservar os padroes locais do projeto.

Use `.github/skills/spc-driven/SKILL.md` para dimensionar o fluxo: rapido, medio, grande ou complexo. Para mudancas pequenas, condense o processo, mas mantenha a ordem codigo -> seguranca -> testes -> lint quando houver impacto real.

Ao concluir uma tarefa, reporte arquivos alterados, skills usadas, validacoes executadas e riscos remanescentes.
