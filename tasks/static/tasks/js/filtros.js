document.addEventListener('DOMContentLoaded', function() {
    
   // =======================================================
// PARTE 1: LÓGICA DOS DROPDOWNS DE FILTRO E ORDENAÇÃO
// =======================================================
const filterButton = document.querySelector('.botao-filtrar');
const filterDropdown = document.getElementById('dropdown-filtro');
const sortButton = document.querySelector('.botao-ordenar');
const sortDropdown = document.getElementById('dropdown-ordenar');

function toggleDropdown(dropdownToOpen, dropdownToClose) {
    if (dropdownToClose) dropdownToClose.classList.remove('show');
    if (dropdownToOpen) dropdownToOpen.classList.toggle('show');
}

if (filterButton && filterDropdown) {
    filterButton.addEventListener('click', function(event) {
        event.stopPropagation(); // Impede que o clique chegue na window
        toggleDropdown(filterDropdown, sortDropdown);
    });
}

if (sortButton && sortDropdown) {
    sortButton.addEventListener('click', function(event) {
        event.stopPropagation(); // Impede que o clique chegue na window
        toggleDropdown(sortDropdown, filterDropdown);
    });
}

// Fechar ao clicar fora, mas permitir clicar DENTRO do menu
window.addEventListener('click', function(event) {
    // Se o clique NÃO foi dentro de um container de dropdown
    if (!event.target.closest('.dropdown-container')) {
        if (filterDropdown) filterDropdown.classList.remove('show');
        if (sortDropdown) sortDropdown.classList.remove('show');
    }
});

    // =======================================================
    // PARTE 2: LÓGICA PARA LIMPAR A BARRA DE BUSCA
    // =======================================================
    const campoBusca = document.getElementById('campo-busca');
    const botaoLimparBusca = document.getElementById('botao-limpar-busca');

    if (campoBusca && botaoLimparBusca) {

        // Mostra ou esconde o botão 'x' conforme o usuário digita
        campoBusca.addEventListener('input', function() {
            if (campoBusca.value.length > 0) {
                botaoLimparBusca.style.display = 'block'; // Mostra o botão
            } else {
                botaoLimparBusca.style.display = 'none'; // Esconde o botão
            }
        });

        // Limpa o campo e esconde o 'x' quando ele é clicado
        botaoLimparBusca.addEventListener('click', function() {
            campoBusca.value = ''; // Limpa o texto do input
            botaoLimparBusca.style.display = 'none'; // Esconde o botão
            campoBusca.focus(); // Opcional: foca no campo de busca novamente
        });
    }

});