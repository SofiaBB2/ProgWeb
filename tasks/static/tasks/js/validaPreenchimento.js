document.addEventListener('DOMContentLoaded', function() {
    // Seleciona o formulário pelo ID
    const formFrasco = document.getElementById('form-frasco');

    if (formFrasco) {
        formFrasco.addEventListener('submit', function(event) {
            
            // Seleciona os campos e a div de erro
            const idFrasco = document.getElementById('idFrasco').value.trim();
            const volumeTotal = document.getElementById('volumeTotal').value.trim();
            const volumeOcupado = document.getElementById('volumeOcupado').value.trim();
            const divErro = document.getElementById('mensagens-erro');
            
            divErro.textContent = ''; // Limpa erros antigos

            // 1. Validação de campos vazios
            if (idFrasco === '' || volumeTotal === '' || volumeOcupado === '') {
                divErro.textContent = 'Por favor, preencha todos os campos obrigatórios.';
                event.preventDefault(); // IMPEDE O ENVIO PORQUE ACHOU UM ERRO
                return;
            }

            // 2. Validação de volumes
            const volTotalNum = parseFloat(volumeTotal.replace(',', '.'));
            const volOcupadoNum = parseFloat(volumeOcupado.replace(',', '.'));

            if (isNaN(volTotalNum) || isNaN(volOcupadoNum)) {
                divErro.textContent = 'Os volumes devem ser números válidos.';
                event.preventDefault(); // IMPEDE O ENVIO PORQUE ACHOU UM ERRO
                return;
            }

            if (volOcupadoNum > volTotalNum) {
                divErro.textContent = 'O volume ocupado não pode ser maior que o volume total.';
                event.preventDefault(); // IMPEDE O ENVIO PORQUE ACHOU UM ERRO
                return;
            }

            // Se o código chegou até aqui, significa que não houve erros.
            // Não fazemos nada e simplesmente deixamos o envio original do formulário continuar.
            console.log('Validação OK! Deixando o formulário ser enviado...');
        });
    }
});

