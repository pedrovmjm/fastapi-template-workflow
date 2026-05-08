# Portao de Decisao para Cache em Memoria

Use este guia antes de implementar qualquer cache local.

## Perguntas Obrigatorias

- Qual custo real sera evitado: latencia, CPU, banco, API externa, serializacao ou leitura repetida?
- Qual e a fonte de verdade e como o valor pode ser recomputado?
- Qual staleness maximo e aceitavel?
- O cache pode ser diferente entre workers sem quebrar o contrato?
- Qual e a cardinalidade esperada das chaves?
- Qual e o tamanho aproximado dos valores?
- Existe padrao ou helper local para cache no projeto?
- Como o cache sera limpo em testes e invalidado em producao?

## Bons Candidatos

- Tabelas pequenas de referencia, como mapeamentos estaveis e metadata.
- Computacoes puras com entradas pequenas e imutaveis.
- Chamadas idempotentes a APIs externas com baixa taxa de mudanca.
- Descoberta de configuracao, schema ou capabilities com TTL curto.
- Deduplicacao curta de rajadas identicas.
- Dados auxiliares de health/status que nao escondam falha real de readiness.

## Candidatos Ruins

- Autorizacao, permissoes, escopos ou posse de recurso.
- Billing, estoque, compliance, saldo ou qualquer decisao financeira.
- Dados por usuario com alta cardinalidade e sem limite.
- Payloads grandes, arquivos completos ou respostas multi-MB.
- Dados sensiveis, secrets, tokens ou credenciais.
- Objetos vivos: sessao de banco, conexao, socket, lock, request, response, generator ou ORM attached.

## Quando Preferir Cache Distribuido

Prefira Redis, Memcached, banco ou outro cache compartilhado quando:

- varios processos precisam ver o mesmo valor;
- invalidacao precisa propagar entre workers;
- o volume de dados ultrapassa memoria segura por processo;
- e necessario rate limiting, deduplicacao ou locks distribuidos;
- reiniciar o processo nao pode apagar o cache.

## Decisao Conservadora

Se houver duvida entre simplicidade e cache, nao cacheie ainda. Primeiro meca ou descreva o gargalo, reduza chamadas duplicadas de forma local e mantenha a implementacao correta sem cache. Cache deve melhorar performance sem virar regra de negocio escondida.
