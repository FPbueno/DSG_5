# NOVO FLUXO DE NEGÓCIO - WorkaFlow

## Visão Geral

Sistema de marketplace com dois tipos de perfil: Cliente e Prestador de Serviço.

---

## Perfis de Usuário

### 1. Cliente

- Solicita orçamentos para serviços
- Compara orçamentos recebidos
- Escolhe prestador preferido

### 2. Prestador de Serviço

- Visualiza solicitações da sua área
- Recebe sugestão de valor do ML
- Envia orçamento com limites

---

## Fluxo Principal

### Etapa 1: Solicitação de Orçamento (Cliente)

**Ação:** Cliente cria solicitação de orçamento

**Dados informados:**

- Categoria do serviço
- Descrição detalhada
- Localização
- Prazo desejado
- Informações adicionais

### Etapa 2: Visualização de Solicitações (Prestador)

**Ação:** Sistema filtra solicitações por área de atuação

**Critérios de filtro:**

- Categoria corresponde à especialidade do prestador
- Localização compatível
- Status: aguardando orçamentos

**Prestador visualiza:**

- Detalhes da solicitação
- Dados do cliente (nome, avaliação)
- Sugestão de valor do ML

### Etapa 3: Cálculo do ML (Sistema)

**Ação:** ML analisa solicitação e define limites de preço

**Entrada:**

- Descrição do serviço
- Categoria
- Localização
- Histórico de preços

**Saída (visível apenas para prestador):**

- Valor mínimo (limite inferior)
- Valor sugerido (valor médio de mercado)
- Valor máximo (limite superior)

**Regra:** Limites servem como orientação para o prestador

### Etapa 4: Criação de Orçamento (Prestador)

**Ação:** Prestador define valor do orçamento

**Prestador visualiza:**

- Limites do ML (mínimo, sugerido, máximo)
- Campo para inserir valor único

**Campos do orçamento:**

- Valor proposto (único valor)
- Prazo de execução
- Observações
- Condições

**Validações:**

- Valor >= Valor Mínimo (do ML)
- Valor <= Valor Máximo (do ML)
- Prazo informado

**Importante:** Cliente vê apenas o valor final, NÃO vê os limites

### Etapa 5: Recebimento de Orçamentos (Cliente)

**Ação:** Cliente visualiza orçamentos recebidos

**Informações exibidas por orçamento:**

- Nome do prestador
- Avaliação do prestador
- Valor proposto (valor único, sem limites)
- Prazo de execução
- Observações

**Cliente NÃO vê:**

- Limites do ML (mínimo/máximo)
- Valor sugerido pelo sistema

**Cliente pode:**

- Comparar orçamentos lado a lado
- Ver perfil completo do prestador
- Aceitar um orçamento
- Recusar orçamentos

### Etapa 6: Seleção de Orçamento (Cliente)

**Ação:** Cliente escolhe orçamento preferido

**Resultado:**

- Orçamento aceito: status muda para "Aceito"
- Outros orçamentos: status muda para "Não selecionado"
- Prestador selecionado é notificado
- Cliente recebe confirmação

---

## Regras de Negócio

### Limites de Preço (ML)

1. ML calcula 3 valores:

   - **Mínimo:** Prestador NÃO pode cobrar menos
   - **Sugerido:** Valor recomendado (mercado)
   - **Máximo:** Prestador NÃO pode cobrar mais

2. Fórmula (exemplo):

   - Mínimo = Valor Sugerido × 0.7
   - Sugerido = Predição do ML
   - Máximo = Valor Sugerido × 1.5

3. Validação no backend:
   - Rejeitar orçamento se valor < mínimo
   - Rejeitar orçamento se valor > máximo

### Filtros de Solicitações

1. Prestador vê apenas solicitações:

   - Da sua categoria/especialidade
   - Na sua região de atuação
   - Com status "Aguardando orçamentos"

2. Cliente vê apenas prestadores:
   - Que enviaram orçamento
   - Com perfil ativo/verificado

### Estados da Solicitação

- **Aguardando orçamentos:** recém-criada
- **Com orçamentos:** tem pelo menos 1 orçamento
- **Fechada:** cliente aceitou um orçamento
- **Cancelada:** cliente cancelou solicitação

---

## Modelos de Dados

### Cliente

```
id
nome
email
telefone
cpf (criptografado)
endereco
avaliacao_media
created_at
```

### Prestador de Serviço

```
id
nome
email
telefone
cpf/cnpj (criptografado)
categorias[] (áreas de atuação)
regioes_atendimento[]
avaliacao_media
portfolio[]
created_at
```

### Solicitação de Orçamento

```
id
cliente_id
categoria
descricao
localizacao
prazo_desejado
informacoes_adicionais
status
created_at
```

### Orçamento

```
id
solicitacao_id
prestador_id
valor_ml_minimo (interno, só para validação)
valor_ml_sugerido (interno, mostrado só ao prestador)
valor_ml_maximo (interno, só para validação)
valor_proposto (único valor visível ao cliente)
prazo_execucao
observacoes
condicoes
status
created_at
```

---

## Endpoints API

### Cliente

```
POST   /api/v1/solicitacoes/criar
GET    /api/v1/solicitacoes/{id}
GET    /api/v1/solicitacoes/{id}/orcamentos
PUT    /api/v1/solicitacoes/{id}/aceitar-orcamento/{orcamento_id}
DELETE /api/v1/solicitacoes/{id}/cancelar
```

### Prestador

```
GET    /api/v1/solicitacoes/disponiveis
GET    /api/v1/solicitacoes/{id}/calcular-limites
      Output: {valor_minimo, valor_sugerido, valor_maximo} (só prestador vê)
POST   /api/v1/orcamentos/criar
      Input: {valor_proposto} (valor único)
      Validação backend: valor entre mínimo e máximo
GET    /api/v1/orcamentos/meus-orcamentos
```

### ML

```
POST   /api/v1/ml/calcular-limites-preco
      Input: {categoria, descricao, localizacao}
      Output: {valor_minimo, valor_sugerido, valor_maximo}
      Uso: apenas para orientação do prestador
```

---

## Telas Mobile

### Cliente

1. **Criar Solicitação**

   - Formulário com campos do serviço
   - Botão "Solicitar Orçamentos"

2. **Minhas Solicitações**

   - Lista de solicitações
   - Badge com quantidade de orçamentos

3. **Detalhes da Solicitação**

   - Informações da solicitação
   - Lista de orçamentos recebidos

4. **Comparar Orçamentos**
   - Cards com orçamentos lado a lado
   - Botão "Aceitar" em cada card

### Prestador

1. **Solicitações Disponíveis**

   - Lista filtrada por área
   - Botão "Ver Detalhes"

2. **Detalhes da Solicitação**

   - Info do cliente
   - Descrição completa
   - Limites do ML exibidos (orientação)
   - Botão "Enviar Orçamento"

3. **Criar Orçamento**

   - Limites exibidos: "Valor sugerido: R$ X (entre R$ Y e R$ Z)"
   - Campo de valor único
   - Validação em tempo real (se está dentro dos limites)
   - Campos de prazo e observações
   - Ao enviar: apenas valor único vai para o cliente

4. **Meus Orçamentos**
   - Orçamentos enviados
   - Status (aguardando/aceito/recusado)

---

## Notificações

### Cliente recebe:

- Novo orçamento recebido
- Orçamento aceito confirmado
- Prazo de resposta do prestador

### Prestador recebe:

- Nova solicitação na sua área
- Orçamento aceito
- Orçamento não selecionado

---

## Próximos Passos

1. Atualizar modelos do banco (MySQL)
2. Criar novos endpoints da API
3. Atualizar modelos ML para calcular limites
4. Implementar telas no Flutter
5. Adicionar sistema de notificações
6. Implementar filtros e buscas
