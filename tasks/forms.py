from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class ResiduoRegistroUpdateForm(forms.Form):
    quant = forms.DecimalField(
        label='Quantidade',
        max_digits=5,
        decimal_places=2,
        min_value=0,
    )
    nivel_risco = forms.IntegerField(label='Nível de risco', min_value=0, max_value=4)
    origem = forms.CharField(label='Origem', max_length=150)
    experimento = forms.CharField(label='Experimento', max_length=250)
    situacao = forms.CharField(label='Situação', max_length=50, required=False)
    riscos_especificos = forms.CharField(
        label='Riscos específicos',
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )


class SolicitacaoRecuperacaoForm(forms.Form):
    email = forms.EmailField(label='E-mail cadastrado')


class RedefinirSenhaForm(forms.Form):
    senha = forms.CharField(
        label='Nova senha',
        min_length=8,
        widget=forms.PasswordInput,
    )
    confirmar_senha = forms.CharField(
        label='Confirmar nova senha',
        widget=forms.PasswordInput,
    )

    def clean(self):
        dados = super().clean()
        senha = dados.get('senha')
        confirmar_senha = dados.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', 'As senhas não coincidem.')
        if senha:
            try:
                validate_password(senha)
            except ValidationError as error:
                self.add_error('senha', error)

        return dados