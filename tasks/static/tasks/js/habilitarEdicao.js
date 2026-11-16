document.addEventListener('DOMContentLoaded', function() {

    const btnEditar = document.getElementById('btn-toggle-edit');
    const btnSalvar = document.getElementById('btn-save');
    const btnCancelar = document.getElementById('btn-cancel');
    const btnExcluir = document.getElementById('btn-delete');

    const spansTexto = document.querySelectorAll('.texto-display');
    const inputsEdicao = document.querySelectorAll('.input-edicao');
    const iconesLapis = document.querySelectorAll('.botao-editar-info');

    let valoresOriginais = [];

    function ativarEdicao() {
        btnEditar.classList.add('hidden');
        btnExcluir.classList.add('hidden'); 
        btnSalvar.classList.remove('hidden');
        btnCancelar.classList.remove('hidden');

        valoresOriginais = [];

        spansTexto.forEach((span, index) => {
            span.classList.add('hidden');
            let input = inputsEdicao[index];
            valoresOriginais.push(input.value);
            input.classList.remove('hidden');
        });

        iconesLapis.forEach(icone => icone.classList.remove('hidden'));
    }

    function cancelarEdicao() {
        btnEditar.classList.remove('hidden');
        btnExcluir.classList.remove('hidden');
        btnSalvar.classList.add('hidden');
        btnCancelar.classList.add('hidden');

        inputsEdicao.forEach((input, index) => {
            input.value = valoresOriginais[index];
            input.classList.add('hidden');
            spansTexto[index].classList.remove('hidden');
        });

        iconesLapis.forEach(icone => icone.classList.add('hidden'));
    }

    if (btnEditar) {
        btnEditar.addEventListener('click', (e) => {
            e.preventDefault();
            ativarEdicao();
        });
    }

    if (btnCancelar) {
        btnCancelar.addEventListener('click', (e) => {
            e.preventDefault();
            cancelarEdicao();
        });
    }

});