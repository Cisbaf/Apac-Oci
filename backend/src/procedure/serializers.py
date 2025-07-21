from rest_framework import serializers
from .models import ProcedureModel, CidModel

class CidSerializer(serializers.ModelSerializer):

    class Meta:
        model = CidModel
        fields = '__all__'



class ProcedureSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    cid = serializers.SerializerMethodField()

    class Meta:
        model = ProcedureModel
        fields = '__all__'

    def get_cid(self, obj):
        return [CidSerializer(cid).data for cid in CidModel.objects.filter(procedure=obj).order_by("name")]

    def get_children(self, obj):
        if obj.parent == None:
            children = ProcedureModel.objects.filter(parent=obj).order_by("-mandatory")
            sub_produces = [ProcedureSerializer(child, context=self.context).data for child in children]
            return sub_produces
        return []