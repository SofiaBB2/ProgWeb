document.addEventListener('DOMContentLoaded', function() {

    const senha = document.getElementById('senha');
    const confirmaSenha = document.getElementById('confirma_senha');
    const botaoCadastrar = document.getElementById('botao_cadastrar');
    const mensagemErro = document.getElementById('mensagem_erro_senha');
    const campoCPF = document.getElementById('campoCPF');
    const avisoCPF = document.getElementById('aviso-cpf'); 

    const validarSenhas = function() {
        if (senha.value === confirmaSenha.value && senha.value !== '') {
            mensagemErro.textContent = 'As senhas coincidem!';
            mensagemErro.style.color = '#07631f'; 
            confirmaSenha.style.borderColor = '#07631f';
            senha.style.borderColor = '#07631f';
            botaoCadastrar.disabled = false; 
        } else if (confirmaSenha.value === '') {
            mensagemErro.textContent = '';
            confirmaSenha.style.borderColor = '#ced4da'; 
            senha.style.borderColor = '#ced4da';
            botaoCadastrar.disabled = true; 
        } else {
            mensagemErro.textContent = 'As senhas não coincidem.';
            mensagemErro.style.color = '#dc3545'; 
            confirmaSenha.style.borderColor = '#dc3545';
            senha.style.borderColor = '#dc3545';
            botaoCadastrar.disabled = true;
        }
    };

    senha.addEventListener('keyup', validarSenhas);
    confirmaSenha.addEventListener('keyup', validarSenhas);
    botaoCadastrar.disabled = true;

    if (campoCPF) {
        campoCPF.addEventListener('blur', function(e) {
            let cpfDigitado = e.target.value;
            
            if (cpfDigitado.length > 0) {
                if (validarCPF(cpfDigitado)) {
                    campoCPF.style.borderColor = "#28a745"; 
                    if (avisoCPF) avisoCPF.classList.add('d-none');
                } else {
                    campoCPF.style.borderColor = "#dc3545";
                    if (avisoCPF) avisoCPF.classList.remove('d-none');
                    e.target.value = ''; 
                }
            } else {
                campoCPF.style.borderColor = "";
                if (avisoCPF) avisoCPF.classList.add('d-none');
            }
        });
    }

    function validarCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false; 
        
        let soma = 0, resto;
        
        for (let i = 1; i <= 9; i++) soma += parseInt(cpf.substring(i-1, i)) * (11 - i);
        resto = (soma * 10) % 11;
        if ((resto == 10) || (resto == 11)) resto = 0;
        if (resto != parseInt(cpf.substring(9, 10))) return false;
        
        soma = 0;
        for (let i = 1; i <= 10; i++) soma += parseInt(cpf.substring(i-1, i)) * (12 - i);
        resto = (soma * 10) % 11;
        if ((resto == 10) || (resto == 11)) resto = 0;
        if (resto != parseInt(cpf.substring(10, 11))) return false;
        
        return true;
    }
});