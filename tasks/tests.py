from urllib.parse import urlsplit

from django.contrib.auth.hashers import check_password
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import (
	Acondicionamento,
	Armazenamento_Residuo,
	Armazenamento_instituicao,
	ClasseAmbiental,
	Curso,
	Destinacao,
	Empresa,
	EstadoFisico,
	Frasco,
	Geracao,
	Gerado,
	GrupoQuimico,
	PerigoPrincipal,
	Residuo,
	Situacao,
	Substancia,
	Usuario,
)


class ResiduoOwnershipTests(TestCase):
	def setUp(self):
		self.owner = Usuario.objects.create(nome='Ana', email='ana@example.test')
		self.other_user = Usuario.objects.create(nome='Bruno', email='bruno@example.test')
		self.estado = EstadoFisico.objects.create(nome='Liquido')
		self.grupo = GrupoQuimico.objects.create(nome='Organico', estado_fisico=self.estado)
		self.substancia = Substancia.objects.create(nome='Acetona', grupo_quimico=self.grupo)
		self.classe = ClasseAmbiental.objects.create(nome='Classe I')
		self.perigo = PerigoPrincipal.objects.create(nome='Inflamavel')
		self.acondicionamento = Acondicionamento.objects.create(descricao='Frasco fechado')
		self.empresa = Empresa.objects.create(
			nome='Empresa',
			cnpj='12345678901234',
			nome_fantasia='Empresa',
			razao_social='Empresa Ltda',
			endereco='Rua A',
			contato='contato@example.test',
		)
		self.destinacao = Destinacao.objects.create(tipo='Tratamento', id_empresa=self.empresa)
		self.curso = Curso.objects.create(
			nome='Quimica', duracao=1, ch=1, nivel='Superior', quant_turmas=1
		)
		self.local = Armazenamento_instituicao.objects.create(
			volume_total=100, volume_atual=10, tipo='Armario', local='Laboratorio 1'
		)
		self.frasco = Frasco.objects.create(vol_deposito=10, vol_ocupado=1, num=1, lote=1)
		self.situacao = Situacao.objects.create(nome='Em uso')
		self.owner_record = self.create_record(self.owner)
		self.other_record = self.create_record(self.other_user)
		self.login_as(self.owner)

	def create_record(self, owner):
		residue = Residuo.objects.create(
			criado_por=owner,
			substancia=self.substancia,
			estado_fisico=self.estado,
			grupo_quimico=self.grupo,
			classe_ambiental=self.classe,
			perigo_principal=self.perigo,
			acondicionamento_sugerido=self.acondicionamento,
		)
		generation = Geracao.objects.create(
			origem='Laboratorio',
			experimento='Teste',
			id_destinacao=self.destinacao,
			id_curso=self.curso,
		)
		generated = Gerado.objects.create(
			quant=1,
			unidade_medida='L',
			nivel_risco=1,
			id_residuo=residue,
			id_geracao=generation,
		)
		return Armazenamento_Residuo.objects.create(
			local=self.local,
			situacao=self.situacao,
			id_gerado=generated,
			id_frasco=self.frasco,
			id_usuario=owner,
		)

	def login_as(self, user):
		session = self.client.session
		session['usuario_id'] = user.pk
		session.save()

	def test_list_only_contains_the_logged_in_users_records(self):
		response = self.client.get(reverse('residuos'))

		self.assertEqual(response.status_code, 200)
		records = list(response.context['residuos_cadastrados'])
		self.assertEqual([record.pk for record in records], [self.owner_record.pk])

	def test_create_residue_associates_owner_and_shows_success_message(self):
		response = self.client.post(reverse('cadastro_residuos'), {
			'substancia_id': self.substancia.pk,
			'estado_fisico_id': self.estado.pk,
			'grupo_quimico_id': self.grupo.pk,
			'classe_ambiental_id': self.classe.pk,
			'perigo_principal_id': self.perigo.pk,
			'acondicionamento_id': self.acondicionamento.pk,
			'curso_id': self.curso.pk,
			'volume': '2.5',
			'nivel_risco': '1',
			'frasco_id': self.frasco.pk,
			'local_id': self.local.pk,
			'situacao': 'Em uso',
			'origem': 'Laboratorio',
			'experimento': 'Teste',
		}, follow=True)

		self.assertEqual(response.redirect_chain[-1][0], reverse('residuos'))
		residuo = Residuo.objects.latest('pk')
		self.assertEqual(residuo.criado_por, self.owner)
		self.assertEqual(
			Armazenamento_Residuo.objects.filter(
				id_gerado__id_residuo=residuo,
				id_usuario=self.owner,
			).count(),
			1,
		)
		self.assertContains(response, 'Resíduo cadastrado com sucesso.')

	def test_another_user_cannot_view_update_or_delete_a_record(self):
		detail_url = reverse('detalhe_residuo', args=[self.other_record.pk])

		self.assertEqual(self.client.get(detail_url).status_code, 404)
		self.assertEqual(
			self.client.post(detail_url, {'acao': 'atualizar'}).status_code,
			404,
		)
		self.assertEqual(
			self.client.post(detail_url, {'acao': 'excluir'}).status_code,
			404,
		)
		self.assertTrue(Armazenamento_Residuo.objects.filter(pk=self.other_record.pk).exists())

	def test_owner_can_update_and_delete_a_record(self):
		detail_url = reverse('detalhe_residuo', args=[self.owner_record.pk])
		self.assertEqual(self.client.get(detail_url).status_code, 200)
		response = self.client.post(detail_url, {
			'acao': 'atualizar',
			'quant': '2.50',
			'nivel_risco': '3',
			'origem': 'Laboratorio atualizado',
			'experimento': 'Experimento atualizado',
			'situacao': 'Em analise',
			'riscos_especificos': 'Manter ventilado',
		})

		self.assertRedirects(response, detail_url)
		self.owner_record.refresh_from_db()
		self.assertEqual(self.owner_record.id_gerado.quant, 2.50)
		self.assertEqual(self.owner_record.id_gerado.id_geracao.origem, 'Laboratorio atualizado')
		self.assertEqual(self.owner_record.situacao.nome, 'Em analise')

		response = self.client.post(detail_url, {'acao': 'excluir'})

		self.assertRedirects(response, reverse('residuos'))
		self.assertFalse(Armazenamento_Residuo.objects.filter(pk=self.owner_record.pk).exists())
		self.assertFalse(Residuo.objects.filter(pk=self.owner_record.id_gerado.id_residuo_id).exists())


@override_settings(
	EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
	DEFAULT_FROM_EMAIL='no-reply@example.test',
)
class PasswordRecoveryTests(TestCase):
	def setUp(self):
		self.user = Usuario.objects.create(
			nome='Maria Exemplo',
			email='maria@example.test',
			registro_profissional='CRQ',
			senha='senha-legada',
			cpf='12345678901',
			formacao='Quimica',
			status='Ativo',
		)

	def test_email_receives_login_identifier_and_valid_reset_link(self):
		page = self.client.get(reverse('recuperacao_senha'))
		self.assertEqual(page.status_code, 200)
		self.assertContains(page, 'E-mail cadastrado')

		response = self.client.post(reverse('recuperacao_senha'), {'email': self.user.email})

		self.assertRedirects(response, reverse('recuperacao_senha'))
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].to, [self.user.email])
		self.assertIn(self.user.nome, mail.outbox[0].body)
		self.assertIn(self.user.email, mail.outbox[0].body)

		reset_url = next(
			line for line in mail.outbox[0].body.splitlines()
			if line.startswith('http://') or line.startswith('https://')
		)
		reset_path = urlsplit(reset_url).path
		self.assertEqual(self.client.get(reset_path).status_code, 200)

		response = self.client.post(reset_path, {
			'senha': 'Nova!Senha#2026',
			'confirmar_senha': 'Nova!Senha#2026',
		})
		self.assertRedirects(response, reverse('login'))

		self.user.refresh_from_db()
		self.assertTrue(check_password('Nova!Senha#2026', self.user.senha))
		self.assertRedirects(
			self.client.get(reset_path),
			reverse('recuperacao_senha'),
		)
		response = self.client.post(reverse('login'), {
			'email': self.user.email,
			'senha': 'Nova!Senha#2026',
		})
		self.assertRedirects(response, reverse('home'))

	def test_unknown_email_gets_same_response_without_sending_email(self):
		response = self.client.post(
			reverse('recuperacao_senha'),
			{'email': 'nao-cadastrado@example.test'},
		)

		self.assertRedirects(response, reverse('recuperacao_senha'))
		self.assertEqual(len(mail.outbox), 0)

	def test_legacy_password_is_upgraded_after_successful_login(self):
		response = self.client.post(reverse('login'), {
			'email': self.user.email,
			'senha': 'senha-legada',
		})

		self.assertRedirects(response, reverse('home'))
		self.user.refresh_from_db()
		self.assertTrue(check_password('senha-legada', self.user.senha))

	def test_invalid_reset_token_is_rejected(self):
		response = self.client.get(reverse('redefinir_senha', kwargs={'token': 'invalido'}))

		self.assertRedirects(response, reverse('recuperacao_senha'))
