# Autenticação, Autorização e Escopos

Autenticação responde quem é o ator. Autorização responde o que esse ator pode fazer agora, neste recurso, neste tenant e com estes dados. Não misture as duas decisões.

## Autenticação

- Valide assinatura, emissor, audiência, expiração e algoritmo do token.
- Rejeite tokens expirados, ausentes ou malformados.
- Proteja login, refresh e reset de senha contra brute force.
- Use cookies seguros quando a sessão depender de navegador.
- Não aceite usuário vindo apenas de header interno sem proteção de gateway.

## Autorização

- Verifique permissão no servidor para cada ação sensível.
- Valide posse do recurso em endpoints com path param.
- Use escopos ou roles explícitos para ações administrativas.
- Aplique controle por tenant antes de buscar ou alterar dados.
- Proteja campos sensíveis em leitura e escrita.
- Evite autorização implícita baseada em convenção de rota.

## BOLA e BFLA

BOLA acontece quando um usuário acessa objeto de outro usuário alterando um id. BFLA acontece quando uma função é acessada sem permissão adequada. Em APIs, esses dois riscos precisam de teste negativo específico.

## Checklist

- [ ] Token é validado completamente.
- [ ] Usuário/tenant do token não pode ser sobrescrito pelo payload.
- [ ] Todo id de recurso passa por checagem de posse ou permissão.
- [ ] Ação administrativa exige escopo ou role.
- [ ] Campos sensíveis têm regra de leitura e escrita.
- [ ] Testes cobrem usuário sem permissão e recurso de outro usuário.
