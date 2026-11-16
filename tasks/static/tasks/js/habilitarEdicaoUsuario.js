document.addEventListener('DOMContentLoaded', function() {

    // Encontra TODOS os cards de usuário na página
    const todosOsCards = document.querySelectorAll('.card-usuario');

    // Para cada card, adiciona a funcionalidade de edição
    todosOsCards.forEach(card => {
        // Encontra os botões DENTRO de cada card
        const botaoEditar = card.querySelector('.botao-editar-usuario');
        const botaoSalvar = card.querySelector('.botao-salvar');
        const botaoCancelar = card.querySelector('.botao-cancelar');

        const containerBotoesPadrao = card.querySelector('.botoes-padrao');
        const containerBotoesEdicao = card.querySelector('.botoes-edicao');
        
        // Encontra todos os ícones de lápis DENTRO do card
        const iconesEdicao = card.querySelectorAll('.icone-editar-campo');

        // Função para entrar no modo de edição (para este card específico)
        function entrarModoEdicao() {
            containerBotoesPadrao.classList.add('hidden');
            containerBotoesEdicao.classList.remove('hidden');
            iconesEdicao.forEach(icon => icon.classList.remove('hidden'));
        }

        // Função para sair do modo de edição (para este card específico)
        function sairModoEdicao() {
            containerBotoesPadrao.classList.remove('hidden');
            containerBotoesEdicao.classList.add('hidden');
            iconesEdicao.forEach(icon => icon.classList.add('hidden'));
            
            // Aqui você também adicionaria a lógica para reverter
            // os campos de texto caso o usuário cancele
        }

        // Adiciona os eventos de clique aos botões
        botaoEditar.addEventListener('click', (event) => {
            event.preventDefault(); // Impede o link de navegar
            entrarModoEdicao();
        });

        botaoCancelar.addEventListener('click', (event) => {
            event.preventDefault();
            sairModoEdicao();
        });

        botaoSalvar.addEventListener('click', (event) => {
            event.preventDefault();
            // Aqui iria a sua lógica para salvar os dados
            alert('Dados do usuário salvos! (simulação)');
            sairModoEdicao();
        });
    });

});