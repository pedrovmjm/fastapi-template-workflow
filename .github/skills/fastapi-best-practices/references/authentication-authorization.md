# Autenticacao e Autorizacao em FastAPI

Use esta referencia para endpoints autenticados, principalmente quando a API usa Azure AD, agora Microsoft Entra ID.

## Fontes oficiais

- Microsoft identity platform, access tokens: https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
- Microsoft identity platform, claims validation: https://learn.microsoft.com/en-us/entra/identity-platform/claims-validation
- FastAPI dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
- FastAPI OAuth2 scopes: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
- FastAPI get current user: https://fastapi.tiangolo.com/tutorial/security/get-current-user/

## Principios

- Autenticacao responde quem e o ator.
- Autorizacao responde o que esse ator pode fazer agora.
- Posse/ACL responde se este recurso especifico pertence, esta compartilhado ou esta liberado para o ator.
- Nenhuma dessas decisoes deve depender de botao escondido no frontend, prompt de LLM ou campo vindo do body.

## Azure AD / Microsoft Entra ID

- Configure issuer/authority, audience, tenant e algoritmos esperados via settings tipadas.
- Valide assinatura, emissor (`iss`), audiencia (`aud`), expiracao (`exp`), validade inicial (`nbf`), algoritmo e tenant (`tid`).
- Rejeite tokens emitidos para outra API. Em tokens v2.0, `aud` normalmente e o client ID da API; em v1.0 pode ser App ID URI.
- Use `oid` ou claim estavel equivalente como identidade interna. Evite usar email como identificador de autorizacao.
- Use `scp` para delegated permissions e `roles` para app roles; nao misture os dois sem decisao explicita.
- Trate `groups` como claim opcional. Se houver overage ou grupos ausentes, busque por Graph/API autorizada ou registre como gap de design.
- Converta claims validas em um contexto interno imutavel, como `UserContext`. Depois disso, services e repositories usam o contexto, nao o JWT cru.

## Dependency injection

- Use uma dependencia de auth para validar token e montar `UserContext`.
- Use `Security` quando o endpoint exigir scopes, pois o FastAPI propaga `SecurityScopes` pela arvore de dependencias.
- Use `Depends` para services, repositories e providers.
- Endpoints publicos devem declarar explicitamente que sao publicos.
- Quando auth for tratada como capacidade transversal, coloque dependencies e helpers em `src/security/dependencies.py`.
- Forneca helpers separados para scopes, roles e grupos: `require_any_scope`, `require_all_scopes`, `require_any_role`, `require_all_roles`, `require_any_group`, `require_all_groups` e `require_user`.

Exemplo de contexto interno:

```python
from pydantic import BaseModel, ConfigDict, Field


class UserContext(BaseModel):
    """Representa o usuario autenticado propagado entre camadas."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    user_id: str = Field(..., description="Identificador interno derivado de tenant e oid.")
    oid: str = Field(..., description="Object ID do usuario no Microsoft Entra ID.")
    tenant_id: str = Field(..., description="Tenant ID que emitiu o token.")
    scopes: frozenset[str] = Field(default_factory=frozenset, description="Scopes do token.")
    roles: frozenset[str] = Field(default_factory=frozenset, description="Roles do token.")
    group_ids: frozenset[str] = Field(default_factory=frozenset, description="IDs de grupos conhecidos.")
    group_names: frozenset[str] = Field(default_factory=frozenset, description="Nomes de grupos conhecidos.")
    groups_overage: bool = Field(False, description="Indica se o token sinalizou overage de grupos.")
    display_name: str | None = Field(None, description="Nome de exibicao enriquecido.")
    mail: str | None = Field(None, description="Email corporativo enriquecido.")
    department: str | None = Field(None, description="Departamento do usuario.")
    job_title: str | None = Field(None, description="Cargo do usuario.")
    office_location: str | None = Field(None, description="Localizacao/escritorio do usuario.")
    photo_url: str | None = Field(None, description="URL interna/proxy para foto do usuario.")
    enrichment_enabled: bool = Field(False, description="Indica se enriquecimento estava habilitado.")
    enrichment_succeeded: bool = Field(False, description="Indica se enriquecimento executou com sucesso.")
    enrichment_error_type: str | None = Field(None, description="Tipo seguro da falha de enriquecimento.")
    correlation_id: str | None = Field(None, description="Correlation id da requisicao.")
```

`user_id` deve ser derivado como `f"{tenant_id}:{oid}"`. Claims como email,
`name` e `preferred_username` podem enriquecer display, mas nao devem ser chave
de autorizacao.

O arquivo recomendado para esse contrato e `src/models/auth/user.py`. Neste
template, `src/models/` pode guardar contratos Pydantic internos estaveis por
dominio, desde que responses publicas continuem separadas dos modelos internos.

## Enriquecimento via Microsoft Graph

- O enriquecimento deve ser opcional por settings.
- Quando desabilitado, use apenas claims validadas do token.
- Quando habilitado e bem-sucedido, acrescente dados extras ao `UserContext`.
- Quando falhar, continue com o contexto basico do token e registre log/trace seguro.
- Se uma decisao de autorizacao depender de dado ausente por falha de enriquecimento, negue acesso; nao libere permissao por falta de informacao.
- O enriquecimento deve buscar propriedades do usuario, como superior direto, departamento, cargo, localizacao, email, foto e outros campos uteis de perfil.
- Nao busque grupos transitivos por default; quando grupos forem necessarios, busque grupos diretos e compare por ID ou display name.
- Prefira service em `src/services/microsoft_graph/` ou `src/services/auth/` para orquestrar enriquecimento e repository em `src/repository/microsoft_graph/` para chamadas Graph.
- `src/security/` e aceitavel como pasta transversal para JWT, dependencies e helpers de permissao se o projeto escolher tratar auth como capacidade similar a `src/observability/`.

## Responsabilidade por camada

### Endpoint

- Valida autenticacao e permissao minima declarativa.
- Injeta `UserContext`, `correlation_id` e service.
- Nao aceita `user_id`, `tenant_id`, `roles`, `groups` ou `scopes` do body como fonte de autorizacao.
- Nao concentra regra de posse complexa no handler HTTP.

### Service

- Decide se o ator pode executar o caso de uso.
- Valida escopo funcional, role/grupo, tenant, estado do recurso e politica de produto.
- Chama repository com filtros de seguranca.
- Traduz negacao em erro de dominio mapeavel para `403` ou `404`.

### Repository

- Aplica filtros de owner, tenant, grupo ou ACL na query.
- Prefere metodos com autorizacao explicita no nome, como `get_accessible_by_actor`, `list_for_tenant`, `exists_owned_by_actor`.
- Nao retorna entidade sensivel ampla para o service filtrar em memoria quando o banco suporta filtro.
- Nao decide politica de produto, mas garante que a query respeita o contexto recebido.

Exemplo de query autorizada:

```python
async def get_accessible_document(
    self,
    *,
    document_id: str,
    current_user: UserContext,
) -> DocumentEntity | None:
    """Busca documento apenas quando o usuario autenticado tem acesso direto."""

    query = (
        select(DocumentEntity)
        .where(DocumentEntity.id == document_id)
        .where(DocumentEntity.tenant_id == current_user.tenant_id)
        .where(
            or_(
                DocumentEntity.owner_id == current_user.oid,
                DocumentEntity.group_id.in_(current_user.group_ids),
            )
        )
    )
```

## Erros esperados

- `401 Unauthorized`: token ausente, malformado, expirado, assinatura invalida, issuer/audience invalido.
- `403 Forbidden`: ator autenticado, mas sem scope, role, grupo, tenant ou posse do recurso.
- `404 Not Found`: pode ocultar existencia de recurso quando a regra de produto exigir; registre internamente a negacao como evento de autorizacao.

## Logs, traces e testes

- Use `standard-logs` e `standard-traces` para formato, eventos e atributos seguros.
- Registre decisao, camada, operacao, motivo, `correlation_id`, `tenant_id`, tipo de recurso e identificador publico quando seguro.
- Nunca registre token, claims completas, cookie, segredo, payload sensivel ou dados pessoais desnecessarios.
- Teste token ausente, expirado, assinatura invalida, audience/issuer incorretos, sem scope, tenant errado, recurso de outro usuario, grupo ausente e tentativa de sobrescrever identidade pelo payload.

## Checklist

- [ ] Endpoint protegido declara dependencia de auth e permissao minima.
- [ ] Token e claims foram validados no servidor.
- [ ] Claims foram normalizadas para contexto interno.
- [ ] Service valida permissao, tenant, grupo/role e posse.
- [ ] Repository filtra por owner, tenant, grupo ou ACL.
- [ ] Logs/traces registram decisao sem dados sensiveis.
- [ ] Testes negativos cobrem BOLA, BFLA, tenant errado e grupo ausente.
