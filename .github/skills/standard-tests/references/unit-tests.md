# Testes Unitários

Teste unitário deve ser pequeno, determinístico e focado em comportamento. Ele deve explicar a regra, não reproduzir a implementação linha a linha.

## Onde Aplicar

- services com regra de negócio;
- funções de manipulação de dados;
- validações puras;
- mappers entre entidade interna e modelo público;
- cálculo de paginação, status interno ou decisões de domínio.

## Estrutura

Testes unitários devem espelhar o caminho do arquivo testado a partir de `src`.

```text
src/services/auth/auth.py
tests/unit/services/auth/test_auth.py
.spec/tests/services/auth/auth.md
```

Esse espelhamento torna explícito qual módulo está sendo validado e evita arquivos genéricos de teste difíceis de navegar.

## Doubles Permitidos

- fake repository em memória quando a regra precisa de dados;
- stub para retorno previsível;
- spy simples para validar chamada relevante;
- mock para exceção difícil de produzir.

Evite mock profundo de várias camadas. Se o teste precisa simular muita coisa, provavelmente ele é de integração ou o design está acoplado demais.

## Padrão de Escrita

- Nomeie o teste pelo comportamento esperado.
- Organize em arrange, act e assert.
- Valide resultado e efeito observável.
- Inclua caso feliz, caso vazio e caso de erro relevante.
- Para cada ponto de comportamento testável, escreva pelo menos 3 testes cobrindo cenários felizes e infelizes.
- Mire cerca de 80% de cobertura unitária no escopo testado.
- Prefira dados mínimos e explícitos.

## Relatório

Ao concluir, gere um relatório curto em `.spec/tests/<dominio>/<arquivo_testado>.md` com:

- arquivo testado;
- arquivo de teste;
- cenários felizes;
- cenários infelizes;
- doubles ou fixtures usados;
- comando executado;
- cobertura obtida.

## Checklist

- [ ] O teste espelha a estrutura do arquivo em `src`.
- [ ] O teste cobre uma regra clara.
- [ ] Há pelo menos 3 testes por ponto de comportamento testável.
- [ ] A cobertura unitária mira cerca de 80% no escopo testado.
- [ ] O teste não depende de banco, rede ou relógio real sem controle.
- [ ] O double é pequeno e compreensível.
- [ ] O assert valida comportamento, não detalhe acidental.
- [ ] Casos de erro relevantes foram cobertos.
- [ ] O relatório foi gerado em `.spec/tests/<dominio>/<arquivo_testado>.md`.
