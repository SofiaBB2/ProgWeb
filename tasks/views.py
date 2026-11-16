from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core import signing
from django.core.mail import send_mail
from django_filters.views import FilterView
from django.urls import reverse
from django.utils.crypto import salted_hmac
from .models import Frasco
from .filters import ArmazenamentoResiduoFilter
from django.db import transaction
from django.shortcuts import render
from .models import *
from django.contrib import messages
from .forms import (
    RedefinirSenhaForm,
    ResiduoRegistroUpdateForm,
    SolicitacaoRecuperacaoForm,
)
from django.views.decorators.http import require_POST

def home(request):
    return render (request, 'tasks/home.html')

class ResiduoListView(FilterView):
    model = Armazenamento_Residuo
    template_name = 'tasks/residuos.html'
    context_object_name = 'residuos_cadastrados'
    filterset_class = ArmazenamentoResiduoFilter
    paginate_by = 10
    ordering = ('-data_atualizacao',)

    def dispatch(self, request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id or not Usuario.objects.filter(pk=usuario_id).exists():
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        usuario_id = self.request.session['usuario_id']
        return super().get_queryset().filter(
            id_usuario_id=usuario_id,
            id_gerado__id_residuo__criado_por_id=usuario_id,
        ).select_related(
            'id_gerado__id_residuo__substancia',
            'id_gerado__id_residuo__classe_ambiental',
            'id_gerado__id_geracao',
            'local',
            'id_frasco',
            'situacao',
        ).order_by(*self.ordering)


def cadastro_residuos(request):
    usuario_responsavel = Usuario.objects.filter(
        pk=request.session.get('usuario_id')
    ).first()
    if usuario_responsavel is None:
        return redirect('login')

    if request.method == "POST":

        try:
            with transaction.atomic():

                substancia_obj = Substancia.objects.get(id=request.POST.get('substancia_id'))
                estado_fisico_obj = EstadoFisico.objects.get(id=request.POST.get('estado_fisico_id'))
                grupo_quimico_obj = GrupoQuimico.objects.get(id=request.POST.get('grupo_quimico_id'))
                classe_ambiental_obj = ClasseAmbiental.objects.get(id=request.POST.get('classe_ambiental_id'))
                perigo_principal_obj = PerigoPrincipal.objects.get(id=request.POST.get('perigo_principal_id'))
                acondicionamento_obj = Acondicionamento.objects.get(id=request.POST.get('acondicionamento_id'))

                residuo = Residuo.objects.create(
                    criado_por=usuario_responsavel,
                    substancia=substancia_obj, 
                    estado_fisico=estado_fisico_obj,
                    grupo_quimico=grupo_quimico_obj,
                    classe_ambiental=classe_ambiental_obj,
                    perigo_principal=perigo_principal_obj,
                    acondicionamento_sugerido=acondicionamento_obj,
                    inflamabilidade=int(request.POST.get('inflamabilidade') or 0),
                    risco_saude=int(request.POST.get('risco_saude') or 0),
                    reatividade=int(request.POST.get('reatividade') or 0),
                    riscos_especificos=request.POST.get('riscos_especificos'),
                )

                curso_obj = Curso.objects.get(id=request.POST.get('curso_id'))
                destinacao_padrao = Destinacao.objects.first() 

                geracao = Geracao.objects.create(
                    origem=request.POST.get('origem'),
                    experimento=request.POST.get('experimento'),
                    id_curso=curso_obj,
                    id_destinacao=destinacao_padrao
                )

                gerado = Gerado.objects.create(
                    quant=float(request.POST.get('volume').replace(',', '.')),
                    unidade_medida="L",
                    nivel_risco=int(request.POST.get('nivel_risco') or 0),
                    id_residuo=residuo,
                    id_geracao=geracao
                )

                frasco_obj = Frasco.objects.get(id=request.POST.get('frasco_id'))
                local_obj = Armazenamento_instituicao.objects.get(id=request.POST.get('local_id'))
                
                situacao_txt = request.POST.get('situacao') or "Em uso"
                situacao_obj, _ = Situacao.objects.get_or_create(nome=situacao_txt)
                
                Armazenamento_Residuo.objects.create(
                    local=local_obj,
                    situacao=situacao_obj,
                    id_gerado=gerado,
                    id_frasco=frasco_obj,
                    id_usuario=usuario_responsavel
                )
            messages.success(request, 'Resíduo cadastrado com sucesso.')
            return redirect('residuos')

        except Exception:
            messages.error(request, 'Não foi possível cadastrar o resíduo. Confira os dados e tente novamente.')

    context = {
        'frascos': Frasco.objects.all(),
        'cursos': Curso.objects.all(),
        'locais': Armazenamento_instituicao.objects.all(),
        
        'estados_fisicos': EstadoFisico.objects.all(),
        'grupos_quimicos': GrupoQuimico.objects.select_related('estado_fisico').all(),
        
        'substancias': Substancia.objects.select_related('grupo_quimico').all(),
        
        'classes_ambientais': ClasseAmbiental.objects.all(),
        'perigos_principais': PerigoPrincipal.objects.all(),
        'acondicionamentos': Acondicionamento.objects.all(),
    }

    return render(request, 'tasks/cadastro_residuos.html', context)

def relatorios(request):
    return render(request, 'tasks/relatorios.html')

def instituicoes(request):
    lista_instituicoes = Instituicao.objects.select_related('id_armazenamento_instituicao').all()
    
    context = {
        'instituicoes_cadastradas': lista_instituicoes
    }
    return render(request, 'tasks/instituicoes.html', context)

def login(request):
    if request.method == "POST":
        email_digitado = request.POST.get('email')
        senha_digitada = request.POST.get('senha')

        try:
            usuario = Usuario.objects.filter(email__iexact=email_digitado).first()

            if usuario:
                senha_valida = check_password(senha_digitada, usuario.senha)
                if not senha_valida and usuario.senha == senha_digitada:
                    usuario.senha = make_password(senha_digitada)
                    usuario.save(update_fields=['senha'])
                    senha_valida = True

                if senha_valida:

                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nome'] = usuario.nome
                    request.session['usuario_tipo'] = "A definir" 
                    
                    request.session['usuario_primeiro_nome'] = usuario.nome.split()[0]

                    return redirect('home')
                else:
                    messages.error(request, 'Senha incorreta. Tente novamente.')
                    return render(request, 'tasks/login.html')
            
            else:
                messages.error(request, 'E-mail não cadastrado no sistema.')
                return render(request, 'tasks/login.html')

        except Exception as e:
            print(f"ERRO NO LOGIN: {e}")
            messages.error(request, 'Ocorreu um erro no servidor. Tente novamente.')
            return render(request, 'tasks/login.html')

    return render(request, 'tasks/login.html')

def sair(request):
    request.session.flush()
    return redirect('login')

def cadastro_usuario(request):
    if request.method == "POST":
        try:
            nome = request.POST.get('nome')
            cpf = request.POST.get('cpf')
            formacao = request.POST.get('formacao')
            registro_profissional = request.POST.get('registro_profissional')
            status = request.POST.get('status')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            foto = request.FILES.get('foto')

            Usuario.objects.create(
                nome=nome,
                email=email,
                registro_profissional=registro_profissional,
                senha=make_password(senha),
                cpf=cpf,
                formacao=formacao,
                status=status,
                foto=foto
            )

            messages.success(request, 'Seu cadastro foi realizado com sucesso!')
            return redirect('login')

        except Exception as e:
            print(f"ERRO AO SALVAR USUÁRIO: {e}")
            messages.error(request, 'Erro ao realizar o cadastro. Tente novamente.')
            return render(request, 'tasks/cadastro_usuario.html')

    return render(request, 'tasks/cadastro_usuario.html')

def cadastrar_frasco(request):
    return render(request, 'tasks/cadastrar_frasco.html')

def frascos_cadastrados (request):
    
    todos_os_frascos = Frasco.objects.all()

    context = {
        'frascos': todos_os_frascos
    }

    return render(request, 'tasks/frascos_cadastrados.html', context)

def cadastro_sucesso (request):
    return render(request, 'tasks/cadastro_sucesso.html')

def dowload_iniciado (request):
    return render(request, 'tasks/dowload_iniciado.html')

def recuperacao_senha(request):
    form = SolicitacaoRecuperacaoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = Usuario.objects.filter(
            email__iexact=form.cleaned_data['email']
        ).first()
        if usuario:
            token = signing.dumps({
                'usuario_id': usuario.pk,
                'estado_senha': salted_hmac(
                    'tasks.password-reset-state',
                    usuario.senha,
                ).hexdigest(),
            }, salt='tasks.password-reset')
            reset_url = request.build_absolute_uri(
                reverse('redefinir_senha', kwargs={'token': token})
            )
            send_mail(
                subject='Recuperação de acesso ao ResiduoLab',
                message=(
                    f'Olá, {usuario.nome}. Seu identificador de acesso é: {usuario.email}.\n\n'
                    f'Para redefinir sua senha, acesse este link em até uma hora:\n{reset_url}\n\n'
                    'Se você não solicitou esta alteração, ignore esta mensagem.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
                fail_silently=True,
            )
        messages.success(
            request,
            'Se o e-mail estiver cadastrado, enviaremos o identificador de acesso e '
            'as instruções para redefinir a senha.',
        )
        return redirect('recuperacao_senha')

    return render(request, 'tasks/recuperacao_senha.html', {'form': form})


def redefinir_senha(request, token):
    try:
        token_data = signing.loads(
            token,
            salt='tasks.password-reset',
            max_age=3600,
        )
    except signing.BadSignature:
        messages.error(request, 'O link de redefinição é inválido ou expirou.')
        return redirect('recuperacao_senha')

    if not isinstance(token_data, dict):
        messages.error(request, 'O link de redefinição é inválido ou expirou.')
        return redirect('recuperacao_senha')

    usuario = Usuario.objects.filter(pk=token_data.get('usuario_id')).first()
    estado_senha = token_data.get('estado_senha', '')
    estado_atual = salted_hmac(
        'tasks.password-reset-state',
        usuario.senha if usuario else '',
    ).hexdigest()
    if usuario is None or estado_senha != estado_atual:
        messages.error(request, 'O link de redefinição é inválido ou expirou.')
        return redirect('recuperacao_senha')

    form = RedefinirSenhaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario.senha = make_password(form.cleaned_data['senha'])
        usuario.save(update_fields=['senha'])
        messages.success(request, 'Senha redefinida. Entre com seu e-mail e a nova senha.')
        return redirect('login')

    return render(request, 'tasks/redefinir_senha.html', {'form': form})

def detalhe_instituicao(request, id):
    
   
    instituicao_obj = get_object_or_404(Instituicao, id=id)
    
   
    tecnicos_da_instituicao = Tecnico.objects.filter(id_instituicao=instituicao_obj)

    context = {
        'instituicao': instituicao_obj,
        'tecnicos': tecnicos_da_instituicao
    }
    
    return render(request, 'tasks/detalhe_instituicao.html', context)

def detalhe_residuo(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id or not Usuario.objects.filter(pk=usuario_id).exists():
        return redirect('login')

    armazenamento = get_object_or_404(
        Armazenamento_Residuo.objects.select_related(
            'id_gerado__id_residuo__substancia',
            'id_gerado__id_residuo__estado_fisico',
            'id_gerado__id_residuo__classe_ambiental',
            'id_gerado__id_residuo__perigo_principal',
            'id_gerado__id_residuo__acondicionamento_sugerido',
            'id_gerado__id_geracao__id_curso',
            'local',
            'id_frasco',
            'situacao',
            'id_usuario',
        ).filter(
            id_usuario_id=usuario_id,
            id_gerado__id_residuo__criado_por_id=usuario_id,
        ),
        pk=id,
    )

    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'excluir':
            gerado = armazenamento.id_gerado
            residuo = gerado.id_residuo
            geracao = gerado.id_geracao
            with transaction.atomic():
                armazenamento.delete()
                if not Armazenamento_Residuo.objects.filter(id_gerado=gerado).exists():
                    gerado.delete()
                if not Gerado.objects.filter(id_residuo=residuo).exists():
                    residuo.delete()
                if not Gerado.objects.filter(id_geracao=geracao).exists():
                    geracao.delete()
            messages.success(request, 'Registro excluído com sucesso.')
            return redirect('residuos')

        form = ResiduoRegistroUpdateForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            situacao_nome = dados.pop('situacao')
            with transaction.atomic():
                gerado = armazenamento.id_gerado
                geracao = gerado.id_geracao
                residuo = gerado.id_residuo
                gerado.quant = dados['quant']
                gerado.nivel_risco = dados['nivel_risco']
                gerado.save(update_fields=['quant', 'nivel_risco'])
                geracao.origem = dados['origem']
                geracao.experimento = dados['experimento']
                geracao.save(update_fields=['origem', 'experimento'])
                residuo.riscos_especificos = dados['riscos_especificos']
                residuo.save(update_fields=['riscos_especificos'])
                if situacao_nome:
                    armazenamento.situacao, _ = Situacao.objects.get_or_create(
                        nome=situacao_nome
                    )
                else:
                    armazenamento.situacao = None
                armazenamento.save(update_fields=['situacao', 'data_atualizacao'])
            messages.success(request, 'Registro atualizado com sucesso.')
            return redirect('detalhe_residuo', id=id)
    else:
        form = ResiduoRegistroUpdateForm(initial={
            'quant': armazenamento.id_gerado.quant,
            'nivel_risco': armazenamento.id_gerado.nivel_risco,
            'origem': armazenamento.id_gerado.id_geracao.origem,
            'experimento': armazenamento.id_gerado.id_geracao.experimento,
            'situacao': armazenamento.situacao.nome if armazenamento.situacao else '',
            'riscos_especificos': armazenamento.id_gerado.id_residuo.riscos_especificos,
        })

    context = {
        'residuo': armazenamento,
        'form': form,
    }
    return render(request, 'tasks/detalhe_residuo.html', context)


def usuariosCadastrados (request):
    return render(request, 'tasks/usuariosCadastrados.html')

def detalheUsuario(request):
    usuario_logado_id = request.session.get('usuario_id')
    
    if not usuario_logado_id:
        return redirect('login')

    try:
        usuario = Usuario.objects.get(id=usuario_logado_id)
        
        if request.method == "POST":
            usuario.nome = request.POST.get('nome')
            usuario.cpf = request.POST.get('cpf')
            usuario.email = request.POST.get('email')
            usuario.registro_profissional = request.POST.get('registro_profissional')
            usuario.formacao = request.POST.get('formacao')
            usuario.status = request.POST.get('status')
            
            usuario.save()
            
            request.session['usuario_nome'] = usuario.nome
            request.session['usuario_primeiro_nome'] = usuario.nome.split()[0]
            
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('detalheUsuario')

        context = {
            'usuario': usuario
        }
        return render(request, 'tasks/detalheUsuario.html', context)
        
    except Usuario.DoesNotExist:
        request.session.flush()
        return redirect('login')
    

@require_POST
def deletar_usuario(request):
    usuario_logado_id = request.session.get('usuario_id')
    
    if usuario_logado_id:
        try:
            usuario = Usuario.objects.get(id=usuario_logado_id)
            usuario.delete() 
            
            request.session.flush() 
            
            messages.success(request, 'Sua conta foi excluída permanentemente. Sentiremos sua falta!')
        except Exception as e:
            print(f"Erro ao excluir: {e}")
            messages.error(request, 'Não foi possível excluir a conta no momento.')
            
    return redirect('login')

def perfilAdm (request):
    return render(request, 'tasks/perfilAdm.html')

def detalhesRelatorio (request):
    return render(request, 'tasks/detalhesRelatorio.html')