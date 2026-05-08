# OWASP Web e API em FastAPI

Use OWASP como checklist de risco, não como substituto para threat modeling do domínio. Para FastAPI, combine o OWASP Top 10 Web atual com o OWASP API Security Top 10, porque APIs têm falhas específicas de autorização por objeto, função e fluxo de negócio.

## OWASP Top 10 Web 2025

- Broken Access Control: valide posse e permissão no servidor.
- Security Misconfiguration: revise defaults, headers, debug, docs públicas e CORS.
- Software Supply Chain Failures: fixe dependências, escaneie CVEs e proteja pipeline.
- Cryptographic Failures: use TLS, hashing forte para senhas e não invente criptografia.
- Injection: use validação, parametrização e parsers seguros.
- Insecure Design: modele abuso desde o design, não só no patch.
- Authentication Failures: proteja login, sessão, reset de senha e MFA quando aplicável.
- Software or Data Integrity Failures: valide artefatos, webhooks, jobs e atualizações.
- Security Logging and Alerting Failures: registre eventos de segurança sem dados sensíveis.
- Mishandling of Exceptional Conditions: erros devem ser seguros, consistentes e monitoráveis.

## OWASP API Security Top 10 2023

- API1 Broken Object Level Authorization: todo acesso por id precisa validar posse/permissão.
- API2 Broken Authentication: autenticação deve ser robusta, expirar e resistir a brute force.
- API3 Broken Object Property Level Authorization: campos sensíveis exigem controle de leitura e escrita.
- API4 Unrestricted Resource Consumption: limite payload, paginação, concorrência e custo.
- API5 Broken Function Level Authorization: ações administrativas exigem autorização por função/escopo.
- API6 Unrestricted Access to Sensitive Business Flows: proteja fluxos valiosos contra automação abusiva.
- API7 Server Side Request Forgery: valide destinos de chamadas feitas pelo servidor.
- API8 Security Misconfiguration: revise configuração por ambiente.
- API9 Improper Inventory Management: mantenha inventário de versões, rotas e ambientes.
- API10 Unsafe Consumption of APIs: trate APIs externas como não confiáveis.

## Controles Práticos

- Valide `tenant_id`, `user_id`, `account_id` e ids de recurso sempre no servidor.
- Use allowlist para campos atualizáveis; nunca faça mass assignment cego.
- Defina limite de tamanho para body, upload e listas.
- Use paginação obrigatória em coleções.
- Proteja endpoints administrativos por escopo explícito.
- Valide assinatura de webhooks.
- Não exponha stack trace em erro público.
- Faça testes negativos para autorização.

## Checklist de Endpoint

- [ ] A rota exige autenticação quando necessário.
- [ ] A rota valida autorização por objeto e por função.
- [ ] Campos sensíveis não podem ser lidos ou escritos indevidamente.
- [ ] Payload, paginação e custo têm limites.
- [ ] Erros não revelam segredo, query, token ou stack trace.
- [ ] Eventos de segurança relevantes são logados com `correlation_id`.

## Referências Externas

- OWASP Top 10 Web 2025: https://owasp.org/Top10/2025/
- OWASP API Security Top 10 2023: https://owasp.org/API-Security/
