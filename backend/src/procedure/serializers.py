from rest_framework import serializers
from .models import ProcedureModel, CidModel, ProcedureRequirementGroup

class CidSerializer(serializers.ModelSerializer):

    class Meta:
        model = CidModel
        fields = '__all__'



class ProcedureRequirementGroupSerializer(serializers.ModelSerializer):
    member_ids = serializers.PrimaryKeyRelatedField(source="members", many=True, read_only=True)

    class Meta:
        model = ProcedureRequirementGroup
        fields = ["id", "description", "minimum", "member_ids"]


class ProcedureSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    cid = serializers.SerializerMethodField()
    secondary_cids = serializers.SerializerMethodField()
    requirement_groups = serializers.SerializerMethodField()

    class Meta:
        model = ProcedureModel
        fields = '__all__'

    def get_cid(self, obj):
        return [CidSerializer(cid).data for cid in CidModel.objects.filter(procedure=obj).order_by("name")]

    def get_requirement_groups(self, obj):
        """Regras "exige ao menos N destes M" (atributos 057, 067-070, T-040).
        `member_ids` referencia os `id` que aparecem em `children` — o
        formulário casa os dois pra saber quais itens satisfazem qual grupo."""
        groups = obj.requirement_groups.prefetch_related("members")
        return ProcedureRequirementGroupSerializer(groups, many=True).data

    def get_secondary_cids(self, obj):
        """CIDs de causas associadas (atributo SIGTAP 043, T-036) aceitos por este
        procedimento. Só é relevante quando `requires_secondary_cid` é True."""
        return [
            CidSerializer(cid).data
            for cid in CidModel.objects.filter(secondary_of_procedure=obj).order_by("name")
        ]

    def get_children(self, obj):
        if obj.parent_links.exists():
            return []
        sub_procedures = []
        links = obj.secondary_links.select_related("child").order_by("-mandatory")
        for link in links:
            data = ProcedureSerializer(link.child, context=self.context).data
            # `mandatory`/`max_quantity` são do par (T-037), não do procedimento
            # em si — sobrescrevem aqui o que `fields = '__all__'` traria.
            data["mandatory"] = link.mandatory
            data["max_quantity"] = link.max_quantity
            sub_procedures.append(data)
        return sub_procedures