document.addEventListener('DOMContentLoaded', function() {
    const selectEstado = document.getElementById('campoEstadoFisico');
    const selectGrupo = document.getElementById('campoGrupoQuimico');
    const selectSubstancia = document.getElementById('campoSubstancia');

    const grupos = [];
    Array.from(selectGrupo.options).forEach(opt => {
        if(opt.value !== "") {
            grupos.push({
                value: opt.value,
                text: opt.text,
                estadoId: opt.getAttribute('data-estado')
            });
        }
    });

    const substancias = [];
    Array.from(selectSubstancia.options).forEach(opt => {
        if(opt.value !== "") {
            substancias.push({
                value: opt.value,
                text: opt.text,
                grupoId: opt.getAttribute('data-grupo')
            });
        }
    });

    function resetSelect(selectElement, defaultText) {
        selectElement.innerHTML = '';
        const defaultOption = document.createElement('option');
        defaultOption.value = "";
        defaultOption.text = defaultText;
        defaultOption.disabled = true;
        defaultOption.selected = true;
        selectElement.appendChild(defaultOption);
    }

    selectEstado.addEventListener('change', function() {
        const estadoEscolhido = this.value;

        resetSelect(selectGrupo, "Selecione um Grupo Químico");
        resetSelect(selectSubstancia, "Aguardando Grupo Químico");
        
        selectSubstancia.disabled = true;

        const gruposFiltrados = grupos.filter(g => g.estadoId === estadoEscolhido);
        
        gruposFiltrados.forEach(grupo => {
            const opt = document.createElement('option');
            opt.value = grupo.value;
            opt.text = grupo.text;
            selectGrupo.appendChild(opt);
        });

        selectGrupo.disabled = false; 
    });


    selectGrupo.addEventListener('change', function() {
        const grupoEscolhido = this.value;

        resetSelect(selectSubstancia, "Selecione a Substância");

        const subsFiltradas = substancias.filter(s => s.grupoId === grupoEscolhido);
        
        subsFiltradas.forEach(sub => {
            const opt = document.createElement('option');
            opt.value = sub.value;
            opt.text = sub.text;
            selectSubstancia.appendChild(opt);
        });

        selectSubstancia.disabled = false; 
    });
    
    resetSelect(selectGrupo, "Aguardando Estado Físico");
    resetSelect(selectSubstancia, "Aguardando Grupo Químico");
});