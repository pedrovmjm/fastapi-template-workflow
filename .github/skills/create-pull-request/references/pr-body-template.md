# Template de Corpo de Pull Request

Use este template como referencia para montar o corpo do PR. Remova secoes que nao se aplicam e mantenha o texto fiel ao diff.

```markdown
## Resumo
- 

## Contexto
- Motivo da mudanca:
- Problema resolvido:
- Decisoes relevantes:

## Escopo
- Incluido:
- Fora do escopo:

## Responsabilidade unica
- O PR tem uma unica responsabilidade revisavel? Sim/Nao
- Areas alteradas:
- Por que essas areas pertencem ao mesmo PR:
- Se nao pertencem, plano de divisao sugerido:

## Rastreabilidade
- Spec: `.specs/features/<slug>/spec.md` ou N/A
- Design/tasks/handoff: `.specs/features/<slug>/...` ou N/A
- Issues: N/A

## Alteracoes principais
- Codigo:
- Configuracao:
- Documentacao/skills:
- Testes:

## Mapa de escopo
| Area | Arquivos | Motivo |
|------|----------|--------|
| CORS | `...` | ... |
| Logging/tracing | `...` | ... |
| Agents | `...` | ... |

## Impacto no template FastAPI
| Area | Impacto | Detalhes |
|------|---------|----------|
| Rotas/endpoints | Sim/Nao | `src/routes/...` |
| Services/domain | Sim/Nao | `src/services/...` |
| Repositories/persistencia | Sim/Nao | `src/repository/...` |
| Modelos/contratos | Sim/Nao | `src/models/...`; envelopes `data`, `meta`, `links` |
| Configuracoes | Sim/Nao | `.env.example`, `src/configs/settings.py`, `src/configs/values_domains/...` |
| Erros publicos | Sim/Nao | contrato `errors[]` |
| Logs/traces | Sim/Nao | eventos, correlation ID, atributos seguros |
| Middlewares | Sim/Nao | ordem, auth, CORS, security headers |
| Seguranca | Sim/Nao | authN/authZ, secrets, dados sensiveis, OWASP |
| CI/CD/infra | Sim/Nao | workflows, Docker, bootstrap |

## Compatibilidade
- Breaking changes: Nao/Sim, detalhes
- Migracao necessaria: Nao/Sim, detalhes
- Variaveis de ambiente novas/alteradas: Nao/Sim, detalhes
- Mudancas de schema/banco: Nao/Sim, detalhes

## Validacoes
| Check | Status | Comando/Detalhes |
|-------|--------|------------------|
| Testes | PASS/FAIL/N/A | `python -m pytest tests/ -q --tb=short` |
| Lint | PASS/FAIL/N/A | `python -m ruff check .` |
| Format | PASS/FAIL/N/A | `python -m ruff format --check .` |
| Type check | PASS/FAIL/N/A | `...` |
| Build/bootstrap | PASS/FAIL/N/A | `python bootstrap.py --dry-run ...` ou `python -m compileall bootstrap.py` |

## Evidencias manuais
- Como validar localmente:
- Resultado esperado:
- Observacoes:

## Riscos e mitigacoes
- Risco:
- Mitigacao:
- Risco residual:

## Checklist
- [ ] O PR descreve fielmente o diff.
- [ ] O titulo cobre todas as areas alteradas; nao reduz o escopo real.
- [ ] O PR tem uma unica responsabilidade ou explica por que um escopo amplo e necessario.
- [ ] Mudancas independentes foram separadas em PRs menores quando possivel.
- [ ] O PR nao inclui `Co-authored-by`, `Generated-by`, `Created with` ou autoria atribuida a ferramentas de IA.
- [ ] Testes/lint foram executados ou a impossibilidade foi explicada.
- [ ] Specs/docs foram atualizadas quando o comportamento mudou.
- [ ] `.env.example` e `src/configs/values_domains/` foram atualizados se houve nova config.
- [ ] Nenhum secret, token, PII ou dado sensivel foi adicionado ao diff.
- [ ] Logs/traces nao incluem payloads sensiveis.
- [ ] Endpoints `GET` com body mantem envelope `data`, `meta`, `links`.
- [ ] Erros publicos seguem contrato `errors[]`.
- [ ] O escopo esta limitado ao objetivo do PR.

## Observacoes para reviewers
- Pontos que merecem atencao:
- Trade-offs aceitos:
- Follow-ups sugeridos:
```
