# Dados Sensíveis em Logs

Use esta referência para decidir o que nunca deve aparecer em logs.

## Nunca Logar

- senha;
- token;
- refresh token;
- API key;
- segredo;
- hash de senha;
- documento pessoal;
- cartão;
- payload completo de autenticação;
- header `Authorization`;
- cookie de sessão.

## Permitido Com Cuidado

- identificador público;
- status da operação;
- contagem de itens;
- nome do provider externo;
- duração em milissegundos;
- tipo da exceção.

## Regra Prática

Se o dado permite autenticar, fraudar, identificar uma pessoa sensivelmente ou reconstruir payload privado, ele não deve ir para log.
