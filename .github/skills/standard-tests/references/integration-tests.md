# Testes de Integração

Teste de integração valida se partes reais conversam corretamente. Em FastAPI, isso é essencial para DI, response models, exception handlers, banco, transações, migrations, clients externos e segurança.

## Tipos de Integração

- Endpoint + app factory + DI.
- Endpoint + service + repository fake realista.
- Repository + banco real de teste.
- Migration + schema.
- Client HTTP + mock server/transport.
- Autenticação/autorização + rota protegida.

## Banco de Dados

- Use banco de teste isolado, container ou instância efêmera.
- Aplique migrations antes dos testes quando o risco inclui schema.
- Limpe dados entre testes por transação, truncate ou database temporário.
- Não use banco compartilhado manualmente entre desenvolvedores.

## APIs Externas

- Use mock server, `httpx.MockTransport`, respx ou equivalente.
- Valide método, URL, headers permitidos, timeout e payload.
- Teste mapeamento de status externo para exceção interna.
- Não chame API real em CI comum, salvo sandbox controlado e marcado.

## FastAPI

- Use client assíncrono quando a aplicação é async.
- Monte a aplicação como em produção, com overrides explícitos.
- Valide status code, body, headers relevantes e envelope.
- Teste exception handlers e validation errors.

## Checklist

- [ ] A fronteira real sob risco está incluída.
- [ ] Dependências externas são controladas e determinísticas.
- [ ] Banco/schema é isolado.
- [ ] Contrato público é validado.
- [ ] Erros técnicos são mapeados corretamente.
