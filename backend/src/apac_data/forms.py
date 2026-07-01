from django import forms
from django.utils.html import format_html

from .choices import STREET_TYPE_CHOICES
from .models import ApacDataModel


class CepSearchWidget(forms.TextInput):
    """TextInput com um botão "Buscar CEP" ao lado, usado no Django Admin."""

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        input_id = (attrs or {}).get("id", "")
        button = format_html(
            '<button type="button" class="cep-search-button" '
            'data-cep-input="{}">Buscar CEP</button>',
            input_id,
        )
        help_button = format_html(
            '<button type="button" class="cep-help-button" '
            'title="O que é isso?" aria-label="O que é isso?">?</button>'
        )
        return format_html(
            '<span class="cep-search-wrapper">{}{}{}</span>', html, button, help_button
        )


class ApacDataInlineForm(forms.ModelForm):
    class Meta:
        model = ApacDataModel
        fields = "__all__"
        widgets = {
            "patient_address_postal_code": CepSearchWidget(attrs={"data-cep-search": "true"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        valor_atual = self.instance.patient_address_street_type if self.instance.pk else None
        codigos_validos = {code for code, _ in STREET_TYPE_CHOICES}

        if valor_atual and valor_atual not in codigos_validos:
            field = self.fields["patient_address_street_type"]
            field.choices = [
                (valor_atual, f"{valor_atual} (legado — não está na lista oficial)"),
            ] + list(field.choices)
