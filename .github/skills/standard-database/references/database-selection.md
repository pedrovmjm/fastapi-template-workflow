# Escolha Entre SQL, NoSQL e Persistência Híbrida

SQL e NoSQL resolvem problemas diferentes. Gostar de NoSQL é uma boa preferência quando o domínio tem documentos naturais, alto volume de escrita, schema evolutivo ou leitura por agregados. Ainda assim, SQL continua valioso quando o sistema depende de relações fortes, integridade referencial, joins frequentes, relatórios consistentes e transações ricas.

## Use SQL Quando

- há relações fortes entre entidades;
- integridade referencial é uma regra central;
- relatórios, filtros combinados e joins são comuns;
- transações ACID cruzam múltiplas tabelas;
- auditoria e rastreabilidade dependem de schema rígido;
- o domínio já é naturalmente tabular.

Exemplos: usuários e permissões, pedidos e pagamentos, ledger financeiro, contratos, backoffice relacional, dados regulatórios.

## Use NoSQL Quando

- o agregado principal cabe bem em um documento;
- o schema muda com frequência;
- a aplicação lê e escreve por chave ou por poucos índices conhecidos;
- alta escala horizontal ou ingestão de eventos é mais importante que joins complexos;
- os dados são semi-estruturados ou variam por tipo de documento;
- a consistência eventual é aceitável em parte do domínio.

Exemplos: perfis enriquecidos, catálogos flexíveis, eventos, snapshots de workflow, respostas de providers, cache persistente, documentos de integração.

## Use Persistência Híbrida Quando

- uma parte do domínio exige transação forte e outra exige documentos flexíveis;
- SQL guarda identidade, autorização, auditoria e estado canônico;
- MongoDB guarda agregados flexíveis, histórico de eventos ou payloads variáveis;
- Redis, OpenSearch, blob storage ou filas complementam casos especializados.

Persistência híbrida deve ter dono claro para cada dado. Evite gravar a mesma verdade em dois bancos sem estratégia de sincronização, reconciliação e observabilidade.

## Perguntas de Decisão

- Qual é o agregado que a API lê e grava com mais frequência?
- Preciso de joins ou posso carregar um documento completo por chave?
- A regra exige transação forte entre múltiplas entidades?
- O schema muda por cliente, provider ou versão?
- Quais campos precisam de índice desde o primeiro deploy?
- Como farei backup, restore, auditoria e migração?
- O dado será usado para analytics, busca textual, cache ou operação transacional?

## Regra Prática

Escolha NoSQL quando o modelo de leitura principal é documento/agregado e a evolução de schema é uma vantagem real. Escolha SQL quando relações, integridade e transação são o centro do domínio. Use ambos quando cada banco tiver uma responsabilidade nítida.
