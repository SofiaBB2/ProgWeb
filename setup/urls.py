"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from tasks.views import home
from tasks.views import ResiduoListView
from tasks.views import cadastro_residuos
from tasks.views import relatorios
from tasks.views import instituicoes
from tasks.views import login
from tasks.views import cadastro_usuario
from tasks.views import cadastrar_frasco
from tasks.views import frascos_cadastrados
from tasks.views import cadastro_sucesso
from tasks.views import dowload_iniciado
from tasks.views import recuperacao_senha
from tasks.views import redefinir_senha
from tasks.views import detalhe_instituicao
from tasks.views import detalhe_residuo
from tasks.views import usuariosCadastrados
from tasks.views import detalheUsuario
from tasks.views import perfilAdm
from tasks.views import detalhesRelatorio
from tasks.views import sair
from tasks.views import deletar_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("residuos/", ResiduoListView.as_view(), name="residuos"),
    path("cadastro-residuos/", cadastro_residuos, name="cadastro_residuos"),
    path("relatorios/", relatorios, name="relatorios"),
    path("instituicoes/", instituicoes, name="instituicoes"),
    path("login/", login, name="login"),
    path("cadastro-usuario/", cadastro_usuario, name="cadastro_usuario"),
    path("cadastro-frasco/", cadastrar_frasco, name="cadastrar_frasco"),
    path("frascos-cadastrados/", frascos_cadastrados, name="frascos_cadastrados"),
    path("cadastro-sucesso/", cadastro_sucesso, name="cadastro_sucesso"),
    path("dowload-sucesso/", dowload_iniciado, name="dowload_iniciado"),
    path("recuperacao_senha/", recuperacao_senha, name="recuperacao_senha"),
    path("redefinir-senha/<str:token>/", redefinir_senha, name="redefinir_senha"),
    path("detalhe-instituicao/<int:id>", detalhe_instituicao, name="detalhe_instituicao"),
    path("detalhe-residuo/<int:id>", detalhe_residuo, name="detalhe_residuo"), #nessa url eu passo o ID para fazer a requisicao
    path("usuarios-cadastrados/", usuariosCadastrados, name="usuariosCadastrados"),
    path("detalhe-usuario/", detalheUsuario, name="detalheUsuario"),
    path("perfil-adm/", perfilAdm, name="perfilAdm"),
    path("detalhes-ralatorio/", detalhesRelatorio, name="detalhesRelatorio"),
    path('sair/', sair, name='sair'),
    path('deletar-usuario/', deletar_usuario, name='deletar_usuario'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#necessario pra carregar a imagem