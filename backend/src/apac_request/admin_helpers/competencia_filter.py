# admin/filters.py
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class CompetenciaFilter(SimpleListFilter):
    title = _("Competência")
    parameter_name = "competencia"
    template = "admin/filters/competencia.html"

    def lookups(self, request, model_admin):
        return []  # não exibe opções

    def has_output(self):
        return True  # força renderização do template

    def queryset(self, request, queryset):
        value = request.GET.get(self.parameter_name)

        if not value:
            return queryset

        # -------------------------------
        # 1. Normaliza o formato recebido
        # -------------------------------
        # Possíveis formatos:
        #   "2024-11"       (month picker)
        #   "2024-11-01"    (já convertido via JS)
        #   "2024/11"       (futuras variações)
        normalized = value.strip()

        # Aceita "AAAA-MM"
        if len(normalized) == 7 and normalized.count("-") == 1:
            normalized += "-01"

        # Aceita "AAAA/MM"
        if "/" in normalized and len(normalized) == 7:
            normalized = normalized.replace("/", "-") + "-01"

        # --------------------------------
        # 2. Tenta converter em datetime
        # --------------------------------
        try:
            competencia = datetime.strptime(normalized, "%Y-%m-%d")
        except ValueError:
            # Valor inválido → ignora filtro
            return queryset

        # --------------------------------
        # 3. Filtrar pelo mês e ano
        # --------------------------------
        return queryset.filter(
            request_date__year=competencia.year,
            request_date__month=competencia.month
        )
