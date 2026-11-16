from django.contrib import admin
from .models import (
    Usuario, Empresa, Frasco, Classificacao, Residuo, 
    Destinacao, Curso, Geracao, Gerado, Armazenamento_Residuo,
    Armazenamento_instituicao, Instituicao, Tecnico, Administrador, Situacao,
    EstadoFisico, GrupoQuimico, ClasseAmbiental, 
    PerigoPrincipal, Acondicionamento, Substancia
)

# Registrando todas as tabelas
admin.site.register(Substancia)
admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(Frasco)
admin.site.register(Classificacao)
admin.site.register(Residuo)
admin.site.register(Destinacao)
admin.site.register(Curso)
admin.site.register(Geracao)
admin.site.register(Gerado)
admin.site.register(Armazenamento_Residuo)
admin.site.register(Armazenamento_instituicao)
admin.site.register(Instituicao)
admin.site.register(Tecnico)
admin.site.register(Administrador)
admin.site.register(Situacao)
admin.site.register(EstadoFisico)
admin.site.register(GrupoQuimico)
admin.site.register(ClasseAmbiental)
admin.site.register(PerigoPrincipal)
admin.site.register(Acondicionamento)
