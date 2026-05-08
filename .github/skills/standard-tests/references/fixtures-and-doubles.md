# Fixtures, Dados e Doubles

Fixtures e doubles devem deixar testes mais claros, não esconder comportamento. Prefira fábricas pequenas e explícitas, com defaults seguros e overrides por teste.

## Fixtures

- Separe fixtures de app, client, settings, banco e usuário autenticado.
- Use escopo curto por padrão.
- Evite fixture que cria muitos dados invisíveis.
- Nomeie fixtures pelo papel no teste.
- Centralize tokens e usuários de teste sem usar segredo real.

## Dados de Teste

- Use builders/factories para payloads repetidos.
- Use dados mínimos para o comportamento.
- Evite snapshots enormes.
- Não use documentos pessoais, tokens ou payloads reais.

## Doubles

- Fake: implementação simples em memória.
- Stub: retorno fixo para cenário específico.
- Spy: registra chamada para assert.
- Mock: simula comportamento ou exceção de dependência.

Use fake para regras de service quando ele deixa o teste mais legível. Use mock para dependências externas, falhas raras ou quando o contrato já é coberto em integração.

## Checklist

- [ ] Fixture não cria estado surpresa.
- [ ] Dados sensíveis não aparecem no teste.
- [ ] Double representa uma fronteira clara.
- [ ] Mock não substitui o comportamento principal sob teste.
- [ ] Factories têm defaults válidos e overrides simples.
