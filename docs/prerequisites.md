# Pré-requisitos

Antes de começar, certifique-se de que sua máquina atenda aos seguintes requisitos:

## Software Necessário

### Python 3.13+

O projeto requer Python versão 3.13 ou superior. Verifique sua versão com:

```bash
python --version
```

Para instalar ou atualizar o Python, visite [python.org](https://www.python.org/downloads/) ou utilize um gerenciador de versões como `pyenv`.

### Poetry 2.0+

O Poetry é utilizado para gerenciamento de dependências e ambiente virtual. Verifique a versão instalada:

```bash
poetry --version
```

Instalação recomendada:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Ou via `pipx`:

```bash
pipx install poetry
```

### Git

Necessário para clonar o repositório e controle de versão:

```bash
git --version
```

## Requisitos do Sistema

| Requisito | Versão Mínima | Observação |
|-----------|--------------|------------|
| Python | 3.13 | Versões inferiores não são compatíveis |
| Poetry | 2.0.0 | Gerenciador de dependências |
| Git | Qualquer | Para clone e versionamento |

## Sistemas Operacionais Suportados

- Linux (distribuições modernas)
- macOS
- Windows (com WSL2 recomendado)

## Conhecimento Recomendado

- Familiaridade com APIs REST
- Conhecimento básico de Python e type hints
- Experiência com banco de dados relacional
- Conceitos de autenticação JWT
