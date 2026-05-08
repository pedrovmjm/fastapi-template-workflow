# OWASP LLM e GenAI

Fluxos com LLM devem ser tratados como integrações com entrada e saída não confiáveis. O modelo pode receber prompt malicioso, recuperar contexto contaminado, chamar ferramentas indevidas ou produzir saída perigosa para sistemas downstream.

## OWASP Top 10 para LLM/GenAI 2025

- LLM01 Prompt Injection: entrada direta ou indireta tenta alterar instruções e políticas.
- LLM02 Sensitive Information Disclosure: o modelo ou contexto revela dados sensíveis.
- LLM03 Supply Chain: modelos, datasets, plugins, packages e prompts podem ser comprometidos.
- LLM04 Data and Model Poisoning: dados de treino, fine-tuning ou embeddings podem ser contaminados.
- LLM05 Improper Output Handling: saída do modelo é usada sem validação ou sanitização.
- LLM06 Excessive Agency: o sistema dá autonomia excessiva ao modelo ou agente.
- LLM07 System Prompt Leakage: instruções internas vazam e ajudam bypass.
- LLM08 Vector and Embedding Weaknesses: RAG e embeddings podem recuperar contexto indevido ou malicioso.
- LLM09 Misinformation: resposta incorreta é tratada como verdade operacional.
- LLM10 Unbounded Consumption: prompts, loops ou chamadas geram custo e indisponibilidade.

## Controles Para FastAPI

- Separe system prompt, developer instructions, entrada do usuário e contexto recuperado.
- Nunca coloque segredo, token ou credencial em prompt.
- Reduza dados pessoais antes de enviar ao provider.
- Use allowlist de ferramentas e argumentos.
- Exija confirmação humana ou regra determinística para ações destrutivas.
- Valide output antes de executar código, SQL, comandos, HTML ou chamadas externas.
- Aplique limite de tokens, tempo, tentativas, ferramentas e custo por request.
- Registre metadados seguros: provider, modelo, duração, custo aproximado e categoria da operação.
- Não registre prompt completo quando ele puder conter dados sensíveis.

## RAG e Vetores

- Filtre documentos por tenant, usuário e permissão antes da recuperação.
- Inclua fonte e versão do documento no contexto.
- Trate conteúdo recuperado como dado não confiável, inclusive instruções embutidas.
- Use limites de similaridade, quantidade de chunks e tamanho total.
- Evite misturar bases de tenants no mesmo índice sem isolamento forte.

## Agents e Ferramentas

- Ferramentas devem ter escopo mínimo e validação de argumentos.
- A autorização da ferramenta deve ser revalidada no backend.
- O modelo não deve decidir sozinho permissões de usuário.
- Ações financeiras, destrutivas ou externas devem ter confirmação explícita.
- Loops agentic precisam de limite de passos e motivo de parada observável.

## Checklist LLM

- [ ] Prompt não contém segredo.
- [ ] Dados enviados ao modelo foram minimizados.
- [ ] RAG aplica autorização antes de recuperar contexto.
- [ ] Output é validado antes de uso downstream.
- [ ] Ferramentas têm allowlist, escopo mínimo e limites.
- [ ] Custo, tempo, tokens e tentativas têm limites.
- [ ] Falhas de modelo não geram resposta insegura ou ação parcial silenciosa.

## Referências Externas

- OWASP Top 10 para LLM/GenAI 2025: https://genai.owasp.org/llm-top-10/
