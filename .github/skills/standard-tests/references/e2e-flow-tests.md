# Testes E2E de Fluxos

Teste E2E de fluxo valida uma jornada completa observável pela API. Ele não deve ser usado para cada detalhe, mas deve proteger caminhos críticos que quebram quando camadas corretas individualmente não funcionam juntas.

## O Que É Um Fluxo

Um fluxo é uma sequência com intenção de negócio, por exemplo:

- criar usuário, autenticar e consultar perfil;
- criar recurso, listar coleção e buscar item por id;
- iniciar pagamento, receber webhook e consultar status;
- enviar solicitação, processar job e observar resultado;
- tentar acessar recurso de outro tenant e receber erro seguro.

## Regras

- Execute pela borda pública da aplicação sempre que possível.
- Use app montada com middlewares, exception handlers e DI realistas.
- Use banco/container/test database quando o fluxo depende de persistência.
- Use providers externos simulados por contrato ou sandbox marcada.
- Valide estados intermediários somente quando forem parte do contrato do fluxo.
- Teste também uma negação importante: autorização, validação ou recurso inexistente.

## Dados e Ambiente

- Cada teste deve criar seus próprios dados.
- Use ids previsíveis apenas dentro do teste.
- Limpe estado ao final ou use ambiente descartável.
- Não dependa de ordem entre fluxos.
- Marque testes lentos quando necessário para separar CI rápido e completo.

## Checklist

- [ ] O teste cobre uma jornada crítica.
- [ ] O fluxo passa por endpoint, service e persistência quando aplicável.
- [ ] Autenticação/autorização realista foi aplicada.
- [ ] Integrações externas foram simuladas por contrato ou sandbox.
- [ ] Resultado final e envelopes foram validados.
- [ ] Há pelo menos um caso negativo para fluxo sensível.
