from django.db import models

class Situacao(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.nome
    
class Usuario(models.Model):
    nome = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    registro_profissional = models.CharField(max_length=50)
    senha = models.CharField(max_length=128)
    cpf = models.CharField(max_length=11)
    formacao = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    foto = models.ImageField(upload_to='fotos_usuarios/', null=True, blank=True)
    def __str__(self): return self.nome

class Empresa(models.Model):
    nome = models.CharField(max_length=250)
    cnpj = models.CharField(max_length=14)
    nome_fantasia = models.CharField(max_length=250)
    razao_social = models.CharField(max_length=150)
    endereco = models.CharField(max_length=150)
    contato = models.CharField(max_length=150)
    def __str__(self): return self.nome_fantasia

class Frasco(models.Model):
    vol_deposito = models.DecimalField(max_digits=5, decimal_places=2)
    vol_ocupado = models.DecimalField(max_digits=5, decimal_places=2)
    num = models.IntegerField()
    lote = models.IntegerField()

    @property
    def percentual_disponivel_bruto(self):
         if self.vol_deposito > 0:
            volume_livre = self.vol_deposito - self.vol_ocupado
            return volume_livre
         return 0
        
    @property
    def percentual_disponivel(self):
         if self.vol_deposito > 0:
            volume_livre = self.vol_deposito - self.vol_ocupado
            return (volume_livre / self.vol_deposito) * 100
         return 0

    def __str__(self): return f"Frasco {self.num} (Lote: {self.lote})"

class Classificacao(models.Model):
    nome = models.CharField(max_length=150)
    categoria = models.CharField(max_length=150)
    norma_referencia = models.CharField(max_length=150)
    sugestao_tratamento = models.CharField(max_length=150)
    def __str__(self): return self.nome
        
class EstadoFisico(models.Model):
    nome = models.CharField(max_length=50, unique=True) 
    def __str__(self): return self.nome

class GrupoQuimico(models.Model):
    nome = models.CharField(max_length=150)
    estado_fisico = models.ForeignKey(EstadoFisico, on_delete=models.CASCADE, related_name='grupos')
    def __str__(self): return f"{self.nome} ({self.estado_fisico.nome})"

class Substancia(models.Model):
    nome = models.CharField(max_length=250)
    grupo_quimico = models.ForeignKey(GrupoQuimico, on_delete=models.CASCADE, related_name='substancias')
    def __str__(self): return f"{self.nome} ({self.grupo_quimico.nome})"

class ClasseAmbiental(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    def __str__(self): return self.nome

class PerigoPrincipal(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    def __str__(self): return self.nome

class Acondicionamento(models.Model):
    descricao = models.CharField(max_length=250) 
    def __str__(self): return self.descricao

class Residuo(models.Model):

    criado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='residuos_criados',
        null=True,
        blank=True,
    )
    substancia = models.ForeignKey(Substancia, on_delete=models.PROTECT, null=True)
    estado_fisico = models.ForeignKey(EstadoFisico, on_delete=models.PROTECT, null=True)
    grupo_quimico = models.ForeignKey(GrupoQuimico, on_delete=models.PROTECT, null=True)
    classe_ambiental = models.ForeignKey(ClasseAmbiental, on_delete=models.PROTECT, null=True)
    perigo_principal = models.ForeignKey(PerigoPrincipal, on_delete=models.PROTECT, null=True)
    acondicionamento_sugerido = models.ForeignKey(Acondicionamento, on_delete=models.PROTECT, null=True)
    inflamabilidade = models.IntegerField(default=0)
    risco_saude = models.IntegerField(default=0)
    reatividade = models.IntegerField(default=0)
    riscos_especificos = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
      return self.substancia.nome if self.substancia else "Resíduo Sem Nome"
    
class Destinacao(models.Model):
    tipo = models.CharField(max_length=150)
    data_destinacao = models.DateTimeField(auto_now_add=True)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    def __str__(self): return f"Destinação: {self.tipo} ({self.id_empresa.nome_fantasia})"

class Curso(models.Model):
    nome = models.CharField(max_length=250)
    duracao = models.IntegerField()
    ch = models.IntegerField()
    nivel = models.CharField(max_length=20)
    quant_turmas = models.IntegerField()
    def __str__(self): return self.nome

class Geracao(models.Model):
    data_geracao = models.DateTimeField(auto_now_add=True) 
    origem = models.CharField(max_length=150)
    experimento = models.CharField(max_length=250)
    id_destinacao = models.ForeignKey(Destinacao, on_delete=models.CASCADE)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    def __str__(self): return f"Geração {self.origem} - {self.data_geracao.strftime('%d/%m/%Y')}"

class Gerado(models.Model):
    quant = models.DecimalField(max_digits=5, decimal_places=2)
    unidade_medida = models.CharField(max_length=10)
    nivel_risco = models.IntegerField()
    id_residuo = models.ForeignKey(Residuo, on_delete=models.CASCADE)
    id_geracao = models.ForeignKey(Geracao, on_delete=models.CASCADE)
    def __str__(self): return f"{self.quant}{self.unidade_medida} de {self.id_residuo.nome}"

class Armazenamento_instituicao(models.Model):
    volume_total = models.DecimalField(max_digits=5, decimal_places=2)
    volume_atual = models.DecimalField(max_digits=5, decimal_places=2)
    tipo = models.CharField(max_length=150)
    local = models.CharField(max_length=150)
    def __str__(self): return f"{self.local} ({self.tipo})"

class Armazenamento_Residuo(models.Model):
    situacao = models.ForeignKey(Situacao, on_delete=models.PROTECT, null=True, blank=True) 
    data_atualizacao = models.DateTimeField(auto_now=True) 
    local = models.ForeignKey(Armazenamento_instituicao, on_delete=models.CASCADE)
    id_gerado = models.ForeignKey(Gerado, on_delete=models.CASCADE)
    id_frasco = models.ForeignKey(Frasco, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self): return f"Frasco {self.id_frasco.num} em {self.local}"
        
class Instituicao(models.Model):
    nome = models.CharField(max_length=250)
    endereco = models.CharField(max_length=150)
    id_armazenamento_instituicao = models.ForeignKey(Armazenamento_instituicao, on_delete=models.CASCADE)
    cursos = models.ManyToManyField(Curso)
    def __str__(self): return self.nome

class Tecnico(models.Model):
    usuario= models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nivel_formacao = models.CharField(max_length=250)
    especializacao = models.CharField(max_length=150)
    certificacao = models.CharField(max_length=150)
    id_instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    def __str__(self): return f"Técnico: {self.especializacao}"
        
class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cargo = models.CharField(max_length=150)
    id_instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    def __str__(self): return f"Adm: {self.cargo}"