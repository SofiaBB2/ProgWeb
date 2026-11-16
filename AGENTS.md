# Orientações para agentes

## Projeto

- Este repositório contém um projeto Django (`setup`) e o app principal `tasks`.
- A interface e as mensagens para usuários devem ser escritas em português do Brasil.
- Antes de alterar modelos, views ou templates, leia a implementação próxima e preserve mudanças preexistentes.

## Django e dados

- Use o ambiente virtual do projeto no Windows: `.venv\Scripts\python.exe manage.py <comando>`.
- Mudanças em modelos devem incluir uma migração. Revise migrações de dados, especialmente a associação de registros existentes a usuários.
- A autenticação da aplicação usa o modelo `tasks.Usuario` e `request.session['usuario_id']`; não presuma que `request.user` representa a conta da aplicação.
- Novas senhas devem ser armazenadas com `make_password` e verificadas com `check_password`. Não envie nem registre senhas em texto puro. O login converte senhas legadas quando autenticadas com sucesso.
- Para registros pertencentes a usuários, aplique a restrição do proprietário na listagem, no detalhe e em toda operação de alteração ou exclusão. Não confie apenas em IDs recebidos pela URL.
- Ações que alteram dados devem usar POST, CSRF e validação no servidor.
- Use o framework de mensagens do Django para informar o resultado de operações e mostre as mensagens nos templates envolvidos.
- Listagens filtráveis devem seguir `.agents/skills/django-filter-listagens/SKILLS.md`: `FilterSet`, `FilterView`, formulário compartilhado e paginação que mantém os parâmetros.

## Validação

- Execute os testes do app com `.venv\Scripts\python.exe manage.py test tasks`.
- Verifique migrações com `.venv\Scripts\python.exe manage.py makemigrations --check --dry-run`.
- Execute `manage.py check` quando possível. Se um erro preexistente bloquear a verificação, documente-o e não o silencie sem limitar explicitamente o diagnóstico.
- Testes de e-mail devem usar o backend em memória; não dependa de SMTP real.
- Não afirme que e-mails de produção estão configurados sem verificar as variáveis SMTP do ambiente.

## Git

- Não faça commit, não crie branches e não descarte alterações existentes sem solicitação explícita.
- Antes de propor uma mensagem de commit, confira o diff relevante e siga `.agents/skills/git-commit-messages/SKILL.md`.
