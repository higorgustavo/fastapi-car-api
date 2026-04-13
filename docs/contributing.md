# Contribuição

Este guia explica como contribuir com o projeto Car API.

## Tipos de Contribuição

### 1. Reportar Bugs

Encontrou um bug? Abra uma issue com:

- **Título descritivo** do problema
- **Passos para reproduzir** o bug
- **Comportamento esperado** vs **comportamento atual**
- **Screenshots ou logs** (se aplicável)
- **Versão do Python** e sistema operacional

### 2. Sugerir Funcionalidades

Tem uma ideia para melhorar a API? Abra uma issue com:

- **Descrição clara** da funcionalidade
- **Caso de uso** e justificativa
- **Exemplos** de como funcionaria
- **Possíveis implementações** (opcional)

### 3. Corrigir Bugs

1. Verifique issues com label `bug`
2. Comente na issue informando que vai trabalhar nela
3. Crie um fork e implemente a correção
4. Adicione testes que reproduzem o bug e verificam a correção
5. Abra um Pull Request

### 4. Adicionar Funcionalidades

1. Discuta a funcionalidade em uma issue antes de implementar
2. Após aprovação, crie um fork
3. Implemente a funcionalidade com testes
4. Atualize a documentação se necessário
5. Abra um Pull Request

### 5. Melhorar Documentação

A documentação sempre precisa de melhorias:

- Corrigir erros ortográficos
- Adicionar exemplos
- Melhorar explicações
- Traduzir conteúdo
- Criar tutoriais

### 6. Revisar Pull Requests

Ajude revisando PRs de outros contribuidores:

- Verifique qualidade do código
- Teste localmente
- Sugira melhorias
- Aprove mudanças boas

## Workflow de Contribuição

### Passo 1: Fork do Repositório

No GitHub, clique em **Fork** para criar sua cópia do repositório.

### Passo 2: Clonar seu Fork

```bash
git clone https://github.com/seu-usuario/car_api.git
cd car_api
```

### Passo 3: Configurar Remote Upstream

```bash
git remote add upstream https://github.com/original/car_api.git
git fetch upstream
```

### Passo 4: Criar Branch

Crie uma branch descritiva para sua mudança:

```bash
# Para features
git checkout -b feat/adicionar-filtro-preco

# Para correções
git checkout -b/fix/corrigir-validacao-placa

# Para documentação
git checkout -b/docs/melhorar-endpoints
```

### Passo 5: Implementar

Faça suas alterações seguindo os [Guidelines e Padrões](guidelines.md) do projeto.

**Lembre-se de:**
- Escrever testes para novas funcionalidades
- Manter cobertura de testes
- Seguir convenções de código
- Documentar mudanças

### Passo 6: Executar Verificações

Antes de commitar, execute:

```bash
# Linting
poetry run task lint

# Formatação
poetry run task format

# Testes
poetry run pytest
```

### Passo 7: Commit

Faça commits descritivos seguindo o padrão:

```
<tipo>: <descrição curta>

<corpo opcional>
```

**Tipos:**
- `feat` - Nova funcionalidade
- `fix` - Correção de bug
- `docs` - Alterações na documentação
- `style` - Formatação, sem mudança lógica
- `refactor` - Refatoração de código
- `test` - Adição ou correção de testes
- `chore` - Atualizações de build/dependências

**Exemplos:**

```bash
git commit -m "feat: adicionar filtro por faixa de preço em carros"

git commit -m "fix: corrigir validação de placa Mercosul"

git commit -m "docs: adicionar exemplos de autenticação na documentação"
```

### Passo 8: Manter Atualizado

Mantenha sua branch sincronizada com o upstream:

```bash
git fetch upstream
git rebase upstream/main
```

### Passo 9: Push

Envie suas mudanças para seu fork:

```bash
git push origin feat/sua-feature
```

### Passo 10: Abrir Pull Request

1. No GitHub, abra um Pull Request da sua branch para `main`
2. Preencha o template de PR com:
   - **Descrição** das mudanças
   - **Issue relacionada** (se houver)
   - **Tipo de mudança** (feature, bugfix, docs, etc.)
   - **Testes realizados**
   - **Screenshots** (se aplicável)

## Padrões de Código

### Python

Siga rigorosamente os [guidelines do projeto](guidelines.md):

- Type hints em todas as funções
- Aspas simples para strings
- Máximo 79 caracteres por linha
- Async/await para operações de I/O

### Commits

Siga [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adicionar endpoint de transferência de carros

Implementa POST /cars/{id}/transfer para permitir que
proprietários transfiram seus carros para outros usuários.

Closes #42
```

### Pull Requests

**Checklist antes de abrir:**
- [ ] Código segue guidelines do projeto
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Linting passa sem erros
- [ ] Todos os testes passam
- [ ] Mensagem de commit é clara

## Revisão de Código

### O que os revisores verificam:

1. **Correção** - O código faz o que diz?
2. **Testes** - Existem testes adequados?
3. **Qualidade** - Código limpo e legível?
4. **Performance** - Sem problemas de performance óbvios?
5. **Segurança** - Sem vulnerabilidades?
6. **Documentação** - Docs atualizadas?

### Tempo de Resposta

- **Issues**: resposta em até 7 dias
- **Pull Requests**: revisão em até 5 dias úteis

## Código de Conduta

### Nossos Compromissos

- **Respeito** mútuo independente de experiência
- **Feedback construtivo** e útil
- **Foco** no que é melhor para a comunidade
- **Empatia** com novos contribuidores

### Comportamento Aceitável

- Uso de linguagem acolhedora e inclusiva
- Respeito por diferentes pontos de vista
- Aceitação de críticas construtivas
- Foco no melhor para a comunidade

### Comportamento Inaceitável

- Linguagem ou imagens sexualizadas
- Trolling, comentários insultuosos/depreciativos
- Ataques pessoais ou políticos
- Assédio público ou privado
- Publicação de informação privada sem permissão

## Reconhecimento

Contribuidores serão reconhecidos no:

- README do projeto
- Release notes
- Seção de contribuidores no GitHub

## Dúvidas?

Se tiver dúvidas sobre como contribuir:

1. Abra uma issue com a label `question`
2. Entre em contato com mantenedores
3. Consulte a documentação existente

---

**Obrigado por contribuir com o Car API!** 🚗
