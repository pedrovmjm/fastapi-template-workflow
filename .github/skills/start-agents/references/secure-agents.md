# Agentes Seguros

Use esta referencia para revisar seguranca e testes de agentes.

## Regras

- O modelo sugere; a aplicacao autoriza.
- Tools e nodes fazem checagem server-side antes de I/O, mutacao ou consulta sensivel.
- Nao confie em instrucao do usuario para trocar `user_id`, `tenant_id`, role, grupo ou escopo.
- Use allowlist de tools por agente e por caso de uso.
- Limite tamanho de input, numero de tool calls, tempo de execucao e custo quando aplicavel.
- Separe tools de leitura e escrita.
- Para escrita, prefira idempotencia, confirmacao e logs de auditoria seguros.
- Outputs de LLM sao dados nao confiaveis ate serem validados.

## Quando usar HITL

HITL (human-in-the-loop) deve ser usado quando uma acao proposta pelo agente precisa de revisao humana antes de executar. HITL nao substitui autorizacao server-side: a tool/node ainda deve validar role, escopo, tenant e posse do recurso no handler.

Use HITL nos casos:

- Acao destrutiva, irreversivel ou dificil de desfazer: deletar, cancelar, encerrar, revogar, sobrescrever ou executar migracao.
- Side effect externo: enviar email, mensagem, webhook, notificacao, ticket, chamada para API de terceiro ou publicacao.
- Operacao financeira, juridica, compliance, compra, reembolso, transferencia, assinatura ou mudanca contratual.
- Exposicao, exportacao ou compartilhamento de dado sensivel, PII, segredo, documento bruto ou dados de outro tenant.
- Alteracao de permissao, role, grupo, tenant, owner, policy, chave, token, configuracao de seguranca ou allowlist.
- Execucao de codigo, SQL, shell, HTTP generico, leitura/escrita de filesystem ou operacao administrativa.
- Acao com baixa confianca do modelo, argumento ambiguo, recurso nao encontrado com certeza ou impacto acima de limite configurado.

## Exemplos HITL

### OpenAI Agents SDK

```python
from agents import Agent, Runner, function_tool


@function_tool(needs_approval=True)
async def cancel_order(order_id: int, reason: str) -> str:
    # Ainda valide ActorContext, escopo, tenant e posse dentro do service/tool.
    return f"Order {order_id} canceled: {reason}"


agent = Agent(
    name="Support agent",
    instructions="Help support users and pause for approval before risky actions.",
    tools=[cancel_order],
)

result = await Runner.run(agent, "Cancele o pedido 123 por fraude.")

if result.interruptions:
    state = result.to_state()
    interruption = result.interruptions[0]

    if reviewer_approved:
        state.approve(interruption)
    else:
        state.reject(
            interruption,
            rejection_message="Cancelamento negado pelo revisor humano.",
        )

    result = await Runner.run(agent, state)
```

### LangGraph / LangChain

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


def cancel_order(order_id: int, reason: str) -> str:
    # Ainda valide ActorContext, escopo, tenant e posse dentro do service/tool.
    return f"Order {order_id} canceled: {reason}"


agent = create_agent(
    model=model,
    tools=[cancel_order],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"cancel_order": {"allowed_decisions": ["approve", "reject"]}},
            description_prefix="Acao sensivel aguardando aprovacao",
        )
    ],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": correlation_id}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Cancele o pedido 123 por fraude."}]},
    config=config,
    version="v2",
)

if result.interrupts:
    decision = {"type": "approve"} if reviewer_approved else {
        "type": "reject",
        "message": "Cancelamento negado pelo revisor humano.",
    }
    result = agent.invoke(
        Command(resume={"decisions": [decision]}),
        config=config,
        version="v2",
    )
```

## Anti-padroes

- Tool `execute_sql`, `http_request`, `run_shell` ou `read_file` exposta sem sandbox e sem allowlist.
- Autorizar acesso porque o prompt diz que o usuario e admin.
- Passar token bruto para o agente ou para a tool.
- Registrar prompt completo em log/tracing de producao.
- Usar historico da conversa como fonte de posse de recurso.

## Testes negativos

- Agent run sem contexto autenticado falha antes de chamar tool sensivel.
- Tool sem scope necessario retorna negacao antes de I/O.
- Tool com recurso de outro usuario retorna negacao.
- Tool com tenant errado retorna negacao.
- Tool destrutiva sem confirmacao retorna negacao.
- Prompt injection tentando alterar usuario, tenant ou permissao nao altera contexto autenticado.
- Trace/log de run nao inclui token, prompt completo ou payload sensivel.

## Checklist

- [ ] Tools sao estreitas, tipadas e com escopo minimo.
- [ ] Side effects possuem confirmacao quando necessario.
- [ ] Autorizacao nao depende de prompt.
- [ ] Logs/traces nao vazam dado sensivel.
- [ ] Testes negativos cobrem abuso, prompt injection e autorizacao.
