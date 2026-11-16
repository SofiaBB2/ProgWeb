# Deploy no Google App Engine

O arquivo `app.yaml` descreve o serviço, mas contém valores `REPLACE_...` de propósito. Substitua esses identificadores e crie os recursos Google Cloud antes do deploy. Não grave senhas, chaves de conta ou a `SECRET_KEY` no repositório.

## Recursos necessários

- Projeto Google Cloud com faturamento e App Engine Standard na região escolhida.
- Instância Cloud SQL for MySQL, banco e usuário próprios para a aplicação.
- Bucket Cloud Storage para as fotos de perfil.
- SMTP de um provedor real para e-mails de recuperação.
- Segredos no Secret Manager: `residuolab-django-secret-key`, `residuolab-db-password` e `residuolab-smtp-password`.

Ative as APIs App Engine, Cloud SQL Admin, Secret Manager, Cloud Storage e IAM Credentials. Conceda à conta de serviço usada pelo App Engine os papéis mínimos: Cloud SQL Client, Secret Manager Secret Accessor e permissões de leitura/gravação no bucket. Para URLs assinadas das fotos, configure também a permissão necessária de assinatura de blobs da conta de serviço.

Configure no `app.yaml` o ID do projeto, a conexão `PROJECT:REGION:INSTANCE`, banco, usuário, bucket e dados públicos do SMTP. Os três valores secretos devem ser criados no Secret Manager, não no YAML.

## Migrações e publicação

Depois de configurar o SDK e autenticar no projeto:

```powershell
gcloud init
gcloud config set project PROJECT_ID
gcloud app create --region=REGION
gcloud services enable appengine.googleapis.com sqladmin.googleapis.com secretmanager.googleapis.com storage.googleapis.com iamcredentials.googleapis.com
```

Antes de publicar, aplique as migrações ao Cloud SQL usando o Cloud SQL Auth Proxy na máquina de desenvolvimento. Com o proxy ouvindo em `127.0.0.1:3306`, defina as variáveis abaixo somente na sessão local do PowerShell; não as grave em arquivos versionados:

```powershell
$env:USE_CLOUD_SQL = 'true'
$env:DB_HOST = '127.0.0.1'
$env:DB_PORT = '3306'
$env:INSTANCE_CONNECTION_NAME = 'PROJECT_ID:REGION:INSTANCE'
$env:DB_NAME = 'DATABASE_NAME'
$env:DB_USER = 'DATABASE_USER'
$env:DB_PASSWORD = 'SECRET_VALUE'
.venv\Scripts\python.exe manage.py migrate
```

Depois de substituir os valores de configuração e confirmar as permissões:

```powershell
gcloud app deploy app.yaml
gcloud app browse
```

A URL final depende do ID e da região do projeto e só existe depois de um deploy bem-sucedido. O ambiente local deste workspace não tem `gcloud` instalado/autenticado nem um projeto/instância GCP informados, portanto o deploy e a URL ainda precisam ser realizados pelo operador do projeto.
