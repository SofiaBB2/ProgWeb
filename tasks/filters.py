import django_filters

from .models import Armazenamento_Residuo


class ArmazenamentoResiduoFilter(django_filters.FilterSet):
    residuo = django_filters.CharFilter(
        field_name="id_gerado__id_residuo__substancia__nome",
        lookup_expr="icontains",
        label="Resíduo",
    )
    local = django_filters.CharFilter(
        field_name="local__local",
        lookup_expr="icontains",
        label="Local",
    )
    situacao = django_filters.CharFilter(
        field_name="situacao__nome",
        lookup_expr="icontains",
        label="Situação",
    )

    class Meta:
        model = Armazenamento_Residuo
        fields = ["residuo", "local", "situacao"]