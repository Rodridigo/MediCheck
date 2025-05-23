# Estrutura do Banco de Dados - Sistema de Receituário de Medicamentos Controlados e Antimicrobianos

## Visão Geral

O modelo de dados foi projetado para atender aos requisitos do sistema de receituário de medicamentos controlados e antimicrobianos, em conformidade com a Portaria 344/98, RDC 471/2021, IN 83/2021 e normas específicas do estado do Rio de Janeiro.

## Entidades Principais

### 1. Usuários

```
Tabela: usuarios
- id (PK): INT AUTO_INCREMENT
- nome: VARCHAR(100) NOT NULL
- cpf: VARCHAR(14) NOT NULL UNIQUE
- crf: VARCHAR(20) NOT NULL UNIQUE
- email: VARCHAR(100) NOT NULL UNIQUE
- senha: VARCHAR(255) NOT NULL
- telefone: VARCHAR(20)
- cargo: VARCHAR(50)
- ativo: BOOLEAN DEFAULT TRUE
- data_cadastro: DATETIME DEFAULT CURRENT_TIMESTAMP
- ultimo_acesso: DATETIME
```

### 2. Medicamentos

```
Tabela: medicamentos
- id (PK): INT AUTO_INCREMENT
- nome_comercial: VARCHAR(100)
- principio_ativo: VARCHAR(100) NOT NULL
- concentracao: VARCHAR(50) NOT NULL
- forma_farmaceutica: VARCHAR(50) NOT NULL
- apresentacao: VARCHAR(100) NOT NULL
- fabricante: VARCHAR(100)
- registro_anvisa: VARCHAR(20)
- tipo_medicamento: ENUM('controlado', 'antimicrobiano', 'ambos', 'comum')
- classe_terapeutica: VARCHAR(100)
- ativo: BOOLEAN DEFAULT TRUE
```

### 3. Classificação de Controle

```
Tabela: classificacao_controle
- id (PK): INT AUTO_INCREMENT
- medicamento_id (FK): INT
- lista_portaria: VARCHAR(10) NOT NULL  # A1, A2, A3, B1, B2, C1, C2, C3, C4, C5, D1, D2, etc.
- tipo_receituario: VARCHAR(50) NOT NULL  # Notificação A, Notificação B, Receita Controle Especial, etc.
- cor_receituario: VARCHAR(20)  # Amarela, Azul, Branca
- validade_receita_dias: INT NOT NULL
- quantidade_maxima_dispensacao: VARCHAR(100) NOT NULL  # Ex: "30 dias de tratamento"
- retencao_receita: BOOLEAN DEFAULT TRUE
- observacoes: TEXT
```

### 4. Antimicrobianos

```
Tabela: antimicrobianos
- id (PK): INT AUTO_INCREMENT
- medicamento_id (FK): INT
- substancia_id (FK): INT
- validade_receita_dias: INT NOT NULL DEFAULT 10  # Conforme RDC 471/2021
- quantidade_maxima_dispensacao: VARCHAR(100) NOT NULL DEFAULT "90 dias de tratamento"
- retencao_receita: BOOLEAN DEFAULT TRUE
- observacoes: TEXT
```

### 5. Substâncias Antimicrobianas

```
Tabela: substancias_antimicrobianas
- id (PK): INT AUTO_INCREMENT
- nome: VARCHAR(100) NOT NULL UNIQUE
- numero_in_83_2021: INT  # Número na lista da IN 83/2021
- ativo: BOOLEAN DEFAULT TRUE
```

### 6. Doses Máximas

```
Tabela: doses_maximas
- id (PK): INT AUTO_INCREMENT
- medicamento_id (FK): INT
- dose_maxima_diaria: DECIMAL(10,2)
- unidade_medida: VARCHAR(20)  # mg, g, mL, etc.
- observacoes: TEXT
```

### 7. Receitas

```
Tabela: receitas
- id (PK): INT AUTO_INCREMENT
- tipo_receita: VARCHAR(50) NOT NULL  # Notificação A, Notificação B, Receita Controle Especial, etc.
- numero_notificacao: VARCHAR(50)  # Quando aplicável
- data_emissao: DATE NOT NULL
- data_dispensacao: DATE NOT NULL
- prescritor_nome: VARCHAR(100) NOT NULL
- prescritor_registro: VARCHAR(20) NOT NULL  # CRM, CRO, etc.
- prescritor_uf: CHAR(2) NOT NULL
- paciente_nome: VARCHAR(100) NOT NULL
- paciente_endereco: VARCHAR(200)
- paciente_documento: VARCHAR(20)
- farmaceutico_id (FK): INT NOT NULL
- observacoes: TEXT
- status: ENUM('aprovada', 'rejeitada', 'pendente') DEFAULT 'pendente'
- motivo_rejeicao: TEXT
- data_cadastro: DATETIME DEFAULT CURRENT_TIMESTAMP
```

### 8. Itens da Receita

```
Tabela: itens_receita
- id (PK): INT AUTO_INCREMENT
- receita_id (FK): INT NOT NULL
- medicamento_id (FK): INT NOT NULL
- posologia: VARCHAR(200) NOT NULL
- quantidade: VARCHAR(50) NOT NULL
- duracao_tratamento: VARCHAR(50)  # Ex: "30 dias"
- observacoes: TEXT
- validado: BOOLEAN DEFAULT FALSE
- motivo_rejeicao: TEXT
```

### 9. Histórico de Validação

```
Tabela: historico_validacao
- id (PK): INT AUTO_INCREMENT
- receita_id (FK): INT NOT NULL
- usuario_id (FK): INT NOT NULL
- data_validacao: DATETIME DEFAULT CURRENT_TIMESTAMP
- status_anterior: ENUM('aprovada', 'rejeitada', 'pendente')
- status_novo: ENUM('aprovada', 'rejeitada', 'pendente')
- observacoes: TEXT
```

### 10. Configurações do Sistema

```
Tabela: configuracoes
- id (PK): INT AUTO_INCREMENT
- chave: VARCHAR(50) NOT NULL UNIQUE
- valor: TEXT NOT NULL
- descricao: TEXT
- data_atualizacao: DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

## Relacionamentos

1. **Medicamentos e Classificação de Controle**: Um medicamento controlado pode estar em uma ou mais listas da Portaria 344/98.
2. **Medicamentos e Antimicrobianos**: Um medicamento pode ser um antimicrobiano e estar na lista da IN 83/2021.
3. **Antimicrobianos e Substâncias**: Um antimicrobiano pode conter uma ou mais substâncias da lista da IN 83/2021.
4. **Medicamentos e Doses Máximas**: Um medicamento tem uma dose máxima diária definida.
5. **Receitas e Itens da Receita**: Uma receita pode conter um ou mais medicamentos.
6. **Usuários e Receitas**: Um farmacêutico valida uma ou mais receitas.
7. **Receitas e Histórico de Validação**: Uma receita pode ter múltiplos registros de validação.

## Índices Recomendados

1. Índice em `medicamentos.principio_ativo` para buscas rápidas por substância
2. Índice em `medicamentos.nome_comercial` para buscas por nome comercial
3. Índice em `classificacao_controle.lista_portaria` para filtrar por lista da Portaria 344/98
4. Índice em `receitas.data_emissao` para relatórios por período
5. Índice em `receitas.prescritor_registro` para busca por prescritor
6. Índice em `receitas.paciente_nome` para busca por paciente

## Validações Automáticas

O sistema deve implementar as seguintes validações automáticas:

1. **Validade da Receita**: Verificar se a data de dispensação está dentro do prazo de validade da receita, conforme o tipo de medicamento.
2. **Quantidade Máxima**: Verificar se a quantidade prescrita não excede o limite máximo permitido para dispensação.
3. **Dose Máxima Diária**: Verificar se a posologia não excede a dose máxima diária recomendada.
4. **Tipo de Receituário**: Verificar se o tipo de receituário é adequado para o medicamento prescrito.
5. **Campos Obrigatórios**: Verificar se todos os campos obrigatórios da receita estão preenchidos.

## Considerações de Implementação

1. **Segurança**: Implementar criptografia para dados sensíveis, como senhas de usuários.
2. **Auditoria**: Manter registros de todas as operações realizadas no sistema para fins de auditoria.
3. **Atualizações Normativas**: Projetar o sistema para facilitar atualizações quando houver mudanças na legislação.
4. **Backup**: Implementar rotinas de backup automático do banco de dados.
5. **Escalabilidade**: Projetar o sistema para suportar crescimento no volume de dados e usuários.

## Observações

Este modelo de dados foi projetado com base na legislação vigente (Portaria 344/98, RDC 471/2021, IN 83/2021) e nas normas específicas do estado do Rio de Janeiro. Qualquer alteração na legislação pode requerer ajustes no modelo de dados.
