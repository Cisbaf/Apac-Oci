(function () {
    "use strict";

    var CEP_HELP_MESSAGE =
        "Este botão busca automaticamente o endereço correspondente ao CEP informado, " +
        "preenchendo rua, bairro, cidade e UF. Use-o para corrigir ou completar o " +
        "endereço do paciente sem precisar digitar cada campo manualmente. Número e " +
        "complemento continuam sendo preenchidos à mão, pois o CEP não traz essa informação.";

    function buscarCep(button) {
        var inputId = button.getAttribute("data-cep-input");
        var cepInput = document.getElementById(inputId);
        if (!cepInput) {
            return;
        }

        var cep = cepInput.value.replace(/\D/g, "");
        if (cep.length !== 8) {
            alert("CEP inválido");
            return;
        }

        var prefix = inputId.replace("patient_address_postal_code", "");
        var streetField = document.getElementById(prefix + "patient_address_street_name");
        var neighborhoodField = document.getElementById(prefix + "patient_address_neighborhood");
        var cityField = document.getElementById(prefix + "patient_address_city");
        var stateField = document.getElementById(prefix + "patient_address_state");

        var originalLabel = button.textContent;
        button.disabled = true;
        button.textContent = "Buscando...";

        fetch("https://viacep.com.br/ws/" + cep + "/json/")
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data.erro) {
                    alert("CEP não encontrado");
                    return;
                }
                if (streetField) streetField.value = (data.logradouro || "").toLocaleUpperCase("pt-BR");
                if (neighborhoodField) neighborhoodField.value = (data.bairro || "").toLocaleUpperCase("pt-BR");
                if (cityField) cityField.value = (data.localidade || "").toLocaleUpperCase("pt-BR");
                if (stateField) stateField.value = (data.uf || "").toLocaleUpperCase("pt-BR");
            })
            .catch(function () {
                alert("Erro ao buscar CEP, verifique sua conexão");
            })
            .finally(function () {
                button.disabled = false;
                button.textContent = originalLabel;
            });
    }

    document.addEventListener("click", function (event) {
        var searchButton = event.target.closest && event.target.closest(".cep-search-button");
        if (searchButton) {
            event.preventDefault();
            buscarCep(searchButton);
            return;
        }

        var helpButton = event.target.closest && event.target.closest(".cep-help-button");
        if (helpButton) {
            event.preventDefault();
            alert(CEP_HELP_MESSAGE);
        }
    });
})();
