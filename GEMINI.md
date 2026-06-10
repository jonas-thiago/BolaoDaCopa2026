# Bolão da Copa do Mundo 2026

# Diretrizes do Projeto

- **Idioma de Comunicação:** Você deve sempre responder e se comunicar exclusivamente em Português do Brasil (pt-BR).
- **Comentários de Código:** Qualquer código gerado ou refatorado deverá ter seus comentários escritos em português.
- **Explicações:** Ao detalhar a arquitetura ou o funcionamento do sistema, breves as respostas em português.

## Visão geral do projeto
Este é um projeto educacional em Python focado na criação de um pool de apostas (“Bolão”) para a Copa do Mundo de 2026. O aplicativo será construído em Streamlit e permitirá aos usuários prever os vencedores e segundos colocados de cada grupo, com os dados sendo mantidos em um banco de dados.

## Tecnologias Utilizadas
- **Linguagem:** Python
- **Framework de UI:** [Streamlit](https://streamlit.io/)
- **Banco de Dados:** [Supabase](https://supabase.com/) (PostgreSQL)
- **Infraestrutura:** Servidor MCP do Supabase e Agent Skills configurados.

## Requisitos e Funcionalidades Principais
- **Cadastro de Usuários:** Os usuários devem fornecer seu nome, telefone e e-mail para participar.

- **Previsões da Fase de Grupos:**
- Os usuários selecionam os participantes que ficarem em 1º e 2º lugar em cada grupo.
- Para simplificar a arquitetura, os 8 melhores colocados em 3º lugar serão determinados aleatoriamente.
- **Design da UI:** O aplicativo deve ser baseado na imagem de referência encontrada em `picture/tela_de_captura.png`.
- **Objetivo Educacional:** A arquitetura do projeto deve ser simples e acessível.

## Estrutura de Diretórios
- `.lim/`: Contém o escopo e os requisitos iniciais do projeto (`gemini.md`).

- `picture/`: Contém referências de design da interface do usuário (`tela_de_captura.png`).
- `.agents/skills/`: Custom agent skills para Supabase e Postgres.

## Diretrizes de Desenvolvimento
- **Alterações Cirúrgicas:** Concentre-se em atualizações mínimas e eficazes.
- **Validação:** Sempre verifique as alterações com testes ou executando o aplicativo Streamlit após a implementação.
- **Simplicidade:** Priorize um código limpo e legível em vez de padrões arquitetônicos complexos.
- **Integração Supabase:** Utilizar o servidor MCP e skills do Supabase para operações de banco de dados e gerenciamento de esquema.

## Tarefas a Fazer
- [x] Inicializar o ambiente Python e o arquivo `requirements.txt`.
- [x] Configurar a estrutura básica do aplicativo Streamlit.
- [ ] Projetar e implementar o esquema do banco de dados no Supabase (Tabelas para `users` e `predictions`).
- [ ] Implementar a interface do usuário para seleção de fase em grupo com base na imagem de referência.
- [ ] Implementar a lógica de randomização para os terceiros colocados.
- [ ] Integrar o cliente Python do Supabase para persistência de dados.
- [ ] Implementar a lógica de cadastro de usuário e salvamento de palpites.