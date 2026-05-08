# Estratégia de Testes

A cobertura deve seguir o risco do comportamento. Nem tudo precisa de E2E, mas fluxos críticos não devem depender apenas de mocks. Use uma pirâmide pragmática: muitos testes unitários, bons testes de integração nas fronteiras e poucos E2E cobrindo jornadas essenciais.

## Níveis de Teste

- Unitário: valida uma função, método ou service isolado.
- Integração: valida duas ou mais partes reais trabalhando juntas, como endpoint + DI, repository + banco, ou client + contrato externo simulado.
- E2E de fluxo: valida uma jornada completa pela API, com a aplicação montada e dependências realistas ou containers controlados.

## Quando Usar Cada Nível

- Use unitário para regras puras, validações, transformação de dados e decisões de negócio.
- Use integração quando o risco está em DI, serialização, banco, transação, migration, auth, OpenAPI, clients ou mapeamento de erro.
- Use E2E quando o risco está no fluxo completo: criar recurso, consultar, atualizar, autorizar, integrar e observar o resultado final.

## O Que Não Fazer

- Não testar só o mock.
- Não mockar o próprio código que deveria ser verificado.
- Não escrever E2E para toda variação pequena quando um unitário resolveria.
- Não depender de ordem global entre testes.
- Não usar dados reais de produção.

## Matriz Prática

| Área | Unitário | Integração | E2E |
| --- | --- | --- | --- |
| Service | Regras e transformação | Service com repositories fake realistas | Fluxo que passa pelo endpoint |
| Endpoint | Validação leve via client | Router, DI, response model, erro | Jornada API completa |
| Repository | Mappers puros | Banco real/test database | Fluxo com persistência realista |
| Client externo | Mapeamento de request/response | HTTP mock server/transport | Fluxo com sandbox quando existir |
| Segurança | Decisões de permissão | Token/DI/rota | Tentativa permitida e negada no fluxo |

## Checklist

- [ ] O nível de teste corresponde ao risco.
- [ ] Fluxos críticos têm E2E.
- [ ] Fronteiras técnicas têm integração.
- [ ] Regras de negócio têm unitários claros.
- [ ] Testes são determinísticos e independentes.
