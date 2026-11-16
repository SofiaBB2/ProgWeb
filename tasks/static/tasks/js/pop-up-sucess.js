document.addEventListener('DOMContentLoaded', function() {
    const dadosAlerta = document.getElementById('dados-alerta');

    if (dadosAlerta) {
        const tipo = dadosAlerta.getAttribute('data-tipo');
        const texto = dadosAlerta.getAttribute('data-texto');

        if (tipo === 'success') {
            Swal.fire({
                title: 'Tudo Certo!',
                text: texto,
                icon: 'success',
                confirmButtonColor: '#28a745',
                confirmButtonText: 'Continuar'
            });
        } else if (tipo === 'error') {
            Swal.fire({
                title: 'Ops!',
                text: texto,
                icon: 'error',
                confirmButtonColor: '#dc3545',
                confirmButtonText: 'Tentar Novamente'
            });
        }
    }
});