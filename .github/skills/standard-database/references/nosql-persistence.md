# Persistência NoSQL e MongoDB

NoSQL não significa ausência de modelo. Em FastAPI, trate documentos como agregados persistidos com invariantes, índices e contratos internos bem definidos.

## MongoDB Async em Python

Para código novo em 2026, prefira a API async do PyMongo quando o projeto usar MongoDB. Motor deve ser tratado como legado ou caminho de migração, porque a documentação oficial da MongoDB marcou Motor como depreciado em favor da API async do PyMongo.

## Modelagem de Documentos

- Modele documentos para as leituras principais da API.
- Embuta dados quando eles pertencem ao mesmo agregado e mudam juntos.
- Referencie por id quando o dado tem ciclo de vida próprio ou cresce sem limite.
- Evite arrays ilimitados dentro de um único documento.
- Guarde versão de schema quando o formato evolui com frequência.
- Defina campos obrigatórios e defaults na borda de escrita.

## IDs e Tipos Internos

- `_id` e `ObjectId` são detalhes de persistência.
- Responses públicas devem expor `id: str` quando necessário.
- Conversão entre `ObjectId` e `str` deve ficar no repository ou mapper interno.
- Não aceite `_id` arbitrário do cliente sem validação e autorização.

## Índices

- Crie índice para todo filtro frequente.
- Crie índice único para unicidade real do domínio.
- Use TTL index para documentos temporários, sessões, locks ou eventos expirados.
- Revise cardinalidade antes de indexar campos com muitos valores repetidos.
- Não dependa de índice criado manualmente em produção sem registro no versionamento.

## Consistência e Transações

- Prefira atualizar um agregado em um único documento quando possível.
- Use transações MongoDB apenas quando a regra exigir alteração atômica em múltiplos documentos.
- Garanta idempotência para retries de escrita.
- Use optimistic locking ou campo de versão quando duas operações podem editar o mesmo documento.

## Outros NoSQL

- Redis deve ser tratado como cache, fila leve, lock ou estado efêmero, salvo decisão explícita.
- DynamoDB exige modelagem por access pattern e chaves desde o design.
- OpenSearch/Elasticsearch é busca e analytics, não fonte transacional primária.
- Blob storage guarda arquivos e payloads grandes, não substitui banco de consulta.

## Checklist NoSQL

- [ ] O documento representa um agregado claro.
- [ ] Filtros e ordenações têm índices planejados.
- [ ] Unicidade é protegida no banco quando for regra real.
- [ ] Schema/versionamento foi previsto.
- [ ] IDs internos não vazam para modelos públicos.
- [ ] Estratégia de consistência é explícita.

## Referências Externas

- MongoDB Motor Async Driver: https://www.mongodb.com/docs/drivers/motor/
- MongoDB PyMongo Async migration: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/reference/migration/
