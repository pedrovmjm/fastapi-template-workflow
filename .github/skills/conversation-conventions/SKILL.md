---
name: conversation-conventions
description: Analisa a conversa com o usuário para identificar regras, convenções, correções ou preferências recorrentes que devem complementar skills existentes, referências usadas por elas ou documentos de convenção do projeto. Use quando o usuário pedir para transformar feedback da conversa em padrão reutilizável, ajustar uma skill a partir de uma correção, ou decidir onde registrar uma nova regra.
---
# Conversation Conventions - Atualização de Padrões por Feedback

Use esta skill quando a conversa revelar uma regra, convenção, preferência ou correção que deve ser preservada para trabalhos futuros.

## Objetivo

Transformar feedback do usuário em melhoria reutilizável, decidindo se a regra deve:

- complementar uma skill existente em `.github/skills/`;
- complementar uma referência usada por uma skill, como arquivos em `references/`;
- atualizar documentação de convenções do projeto, como `.specs/codebase/CONVENTIONS.md`;
- permanecer apenas como decisão local da tarefa atual.

## Quando Acionar

Acione esta skill quando o usuário pedir algo como:

- "guarde essa regra";
- "corrija a skill";
- "isso deveria estar no padrão";
- "da próxima vez faça assim";
- "verifique se essa convenção complementa outra skill";
- "olhe a conversa e atualize as regras";
- "essa correção deve virar referência?".

## Regras Obrigatórias

- Leia a conversa recente antes de editar qualquer padrão.
- Separe preferência pontual de convenção reutilizável.
- Não duplique regras já existentes; complemente o arquivo mais específico.
- Prefira atualizar a skill diretamente quando a regra muda o comportamento principal dela.
- Prefira atualizar `references/` quando a regra é detalhada, extensa, situacional ou usada por uma fase específica da skill.
- Prefira atualizar `.specs/codebase/CONVENTIONS.md` quando a regra descreve a base de código, não uma skill.
- Preserve o idioma e o estilo do arquivo atualizado.
- Registre exemplos apenas quando eles reduzirem ambiguidade.
- Não crie uma nova skill se uma skill existente já cobre claramente o mesmo domínio.

## Fluxo de Decisão

1. **Extrair feedback**
   - Identifique frases do usuário que expressem correção, restrição, preferência ou padrão.
   - Reescreva cada item como uma regra objetiva e verificável.

2. **Classificar escopo**
   - `Global`: vale para qualquer tarefa do repositório.
   - `Skill-specific`: vale para uma skill ou família de skills.
   - `Reference-specific`: vale para uma fase, template, checklist ou documento auxiliar.
   - `Task-local`: vale apenas para a solicitação atual.

3. **Localizar destino**
   - Busque skills relacionadas em `.github/skills/`.
   - Leia o `SKILL.md` candidato e seus links diretos de `references/` quando relevantes.
   - Verifique se `.specs/codebase/CONVENTIONS.md` existe antes de criar ou sugerir atualização de convenções gerais.

4. **Escolher ação**
   - Atualize `SKILL.md` quando a regra altera gatilhos, regras obrigatórias, checklist ou fluxo central.
   - Atualize uma referência quando a regra detalha uma etapa já delegada para arquivo auxiliar.
   - Atualize documentação de projeto quando a regra descreve arquitetura, estrutura, testes, estilo ou operação da base.
   - Se a regra for ambígua ou conflitar com padrões existentes, apresente a decisão necessária antes de editar.

5. **Aplicar e validar**
   - Faça a menor edição suficiente.
   - Remova redundâncias criadas pela edição.
   - Revise se a nova regra ficou acionável, sem depender da memória da conversa.

## Critérios de Reutilização

Uma regra deve virar padrão quando pelo menos um destes critérios for verdadeiro:

- corrige um erro que pode se repetir;
- define preferência explícita do usuário para trabalhos futuros;
- reduz ambiguidade em uma skill existente;
- altera a forma correta de gerar código, docs, specs, testes ou revisão;
- deve ser aplicada por outros agentes ou sessões.

Mantenha como decisão local quando:

- depende de um arquivo, bug ou feature específico;
- é uma exceção temporária;
- contradiz uma regra mais forte sem intenção clara de substituição;
- não tem formulação verificável.

## Checklist

- [ ] Feedback da conversa foi convertido em regra objetiva.
- [ ] A regra foi comparada com skills e referências existentes.
- [ ] O destino escolhido é o mais específico possível.
- [ ] Não há duplicação desnecessária entre skill, referência e documentação.
- [ ] A edição preserva idioma, tom e estrutura do arquivo.
- [ ] A resposta final informa quais arquivos foram atualizados e por quê.
