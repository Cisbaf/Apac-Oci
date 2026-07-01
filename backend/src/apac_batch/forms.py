import re
from django import forms
from django.db import transaction
from datetime import date
from city.models import CityModel
from .models import ApacBatchModel

FORMATO_FAIXA = re.compile(r'^\d{13}$')


def parse_faixas(raw: str) -> list[str]:
    """
    Extrai os números de faixa do texto bruto no formato:
      "332670197467-3 | 332670197468-4
      "332670197471-7 | 332670197472-8

    Retorna lista de strings sem hífen: ['3326701974673', '3326701974684', ...]
    Replica exatamente o comportamento do código manual atual.
    """
    numeros = []
    for linha in raw.strip().splitlines():
        linha = linha.replace('"', '')
        partes = linha.split('|')
        for parte in partes:
            parte = parte.strip().replace('-', '')
            if parte:
                numeros.append(parte)
    return numeros


class ImportFaixasForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=CityModel.objects.all(),
        label="Cidade",
        empty_label="Selecione a cidade...",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantidade_esperada = forms.IntegerField(
        label="Quantidade esperada",
        min_value=1,
        help_text="Informe a quantidade de faixas que consta no documento recebido.",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    faixas_raw = forms.CharField(
        label="Faixas",
        widget=forms.Textarea(attrs={
            'rows': 10,
            'style': 'font-family: monospace;',
            'class': 'form-control'
        }),
        help_text='Cole o texto no formato: "332670197467-3 | 332670197468-4 | ...'
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fixed_city = None

        if user is not None and not user.is_superuser:
            # Administradores não escolhem a cidade: é sempre a do próprio usuário.
            self.fixed_city = user.city
            del self.fields['city']

    def get_city(self):
        return self.fixed_city or self.cleaned_data.get('city')

    def clean(self):
        cleaned = super().clean()

        if self.user is not None and not self.user.is_superuser and self.fixed_city is None:
            raise forms.ValidationError(
                "Seu usuário não possui uma cidade associada. Contate o administrador do sistema."
            )

        raw = cleaned.get('faixas_raw', '')
        quantidade_esperada = cleaned.get('quantidade_esperada')

        if not raw or not quantidade_esperada:
            return cleaned

        numeros = parse_faixas(raw)
        erros = []

        # 1. Validação de formato (deve ser exatamente 13 dígitos numéricos)
        invalidos = [n for n in numeros if not FORMATO_FAIXA.match(n)]
        if invalidos:
            lista = ', '.join(invalidos)
            erros.append(
                f"As seguintes faixas estão em formato inválido (esperado: 13 dígitos numéricos): {lista}"
            )

        # 2. Validação de quantidade
        if len(numeros) != quantidade_esperada:
            erros.append(
                f"Quantidade não confere: esperado {quantidade_esperada}, "
                f"encontrado {len(numeros)} faixa(s)."
            )

        # 3. Validação de duplicatas no banco
        existentes = list(ApacBatchModel.objects.filter(
            batch_number__in=numeros
        ).values_list('batch_number', flat=True))

        if existentes:
            lista = ', '.join(existentes)
            erros.append(
                f"As seguintes faixas já estão registradas e não podem ser inseridas: {lista}"
            )

        # 4. Validação de duplicatas dentro do próprio input
        vistos = set()
        duplicados_input = set()
        for n in numeros:
            if n in vistos:
                duplicados_input.add(n)
            vistos.add(n)

        if duplicados_input:
            lista = ', '.join(duplicados_input)
            erros.append(
                f"As seguintes faixas aparecem mais de uma vez no texto colado: {lista}"
            )

        if erros:
            raise forms.ValidationError(erros)

        # Armazena os números parseados para uso na view
        cleaned['numeros_parseados'] = numeros
        return cleaned

    def salvar(self):
        """
        Insere todas as faixas atomicamente.
        Só deve ser chamado após form.is_valid().
        expire_in = último dia do ano vigente.
        """
        city = self.get_city()
        numeros = self.cleaned_data['numeros_parseados']
        expire_in = date(date.today().year, 12, 31)

        with transaction.atomic():
            ApacBatchModel.objects.bulk_create([
                ApacBatchModel(
                    batch_number=numero,
                    city=city,
                    expire_in=expire_in
                )
                for numero in numeros
            ])

        return len(numeros)
