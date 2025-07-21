import os
import django

# 1. Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# 2. Configura o Django
django.setup()

# 3. Agora você pode importar e usar os models
from procedure.models import ProcedureModel

# 1. OCI AVALIAÇÃO DIAGNÓSTICA INICIAL DE CÂNCER DE MAMA AQUI
main_mama = ProcedureModel.objects.create(
    code="0901010014",
    name="OCI AVALIAÇÃO DIAGNÓSTICA INICIAL DE CÂNCER DE MAMA"
)

ProcedureModel.objects.create(
    code="0301010072",
    name="CONSULTA E/OU TELECONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
    parent=main_mama,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0204030030",
    name="MAMOGRAFIA",
    parent=main_mama,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0205020097",
    name="ULTRASSONOGRAFIA BILATERAL",
    parent=main_mama,
    mandatory=False
)

# 2. OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE CÂNCER DE MAMA - I
# main_mama_i = ProcedureModel.objects.create(
#     code="0901010090",
#     name="OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE CÂNCER DE MAMA - I"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA E/OU TELECONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_mama_i,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0201010585",
#     name="PUNÇÃO ASPIRATIVA DE MAMA POR AGULHA FINA",
#     parent=main_mama_i,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0203010043",
#     name="CITOPATOLÓGICO DE MAMA OCI",
#     parent=main_mama_i,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0201010569",
#     name="BIOPSIA/EXERESE DE MAMA",
#     parent=main_mama_i,
#     mandatory=False
# )

# 3. OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE CÂNCER DE MAMA-II
# main_mama_ii = ProcedureModel.objects.create(
#     code="0901010103",
#     name="OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE CÂNCER DE MAMA-II"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA E/OU TELECONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_mama_ii,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0201010607",
#     name="PUNÇÃO DE MAMA POR AGULHA GROSSA",
#     parent=main_mama_ii,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0201010569",
#     name="BIOPSIA/EXERESE DE MAMA",
#     parent=main_mama_ii,
#     mandatory=False
# )

# 4. OCI INVESTIGAÇÃO DIAGNÓSTICA DE CÂNCER DE COLO DE ÚTERO
# main_utero = ProcedureModel.objects.create(
#     code="0901010057",
#     name="OCI INVESTIGAÇÃO DIAGNÓSTICA DE CÂNCER DE COLO DE ÚTERO"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_utero,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0201010606",
#     name="BIÓPSIA DO COLO UTERINO",
#     parent=main_utero,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0203020065",
#     name="EXAME ANATOMOPATOLÓGICO DE MAMA",
#     parent=main_utero,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211040029",
#     name="COLPOSCOPIA",
#     parent=main_utero,
#     mandatory=False
# )

# 5. OCI AVALIAÇÃO DIAGNÓSTICA E TERAPÊUTICA DE CÂNCER DE COLO DO ÚTERO-I
# main_utero_i = ProcedureModel.objects.create(
#     code="0901010111",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA E TERAPÊUTICA DE CÂNCER DE COLO DO ÚTERO-I"
# )

# ProcedureModel.objects.create(
#     code="0203020081",
#     name="EXAME ANATOMO-PATOLÓGICO DO COLO UTERINO-BIÓPSIA",
#     parent=main_utero_i,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_utero_i,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0409060089",
#     name="EXCISÃO TIPO I DO COLO UTERINO",
#     parent=main_utero_i,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211040029",
#     name="COLPOSCOPIA",
#     parent=main_utero_i,
#     mandatory=False
# )

# # 6. OCI AVALIAÇÃO DIAGNÓSTICA E TERAPÊUTICA DE CÂNCER DE COLO DO ÚTERO-II
# main_utero_ii = ProcedureModel.objects.create(
#     code="0901010120",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA E TERAPÊUTICA DE CÂNCER DE COLO DO ÚTERO-II"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_utero_ii,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0409060305",
#     name="EXCISÃO TIPO 2 DO COLO UTERINO",
#     parent=main_utero_ii,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0203020022",
#     name="EXAME ANATOMOPATOLÓGICO DO COLO UTERINO - PEÇA CIRÚRGICA",
#     parent=main_utero_ii,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211040029",
#     name="COLPOSCOPIA",
#     parent=main_utero_ii,
#     mandatory=False
# )

# 7. OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE CÂNCER DE PRÓSTATA AQUI
main_prostata = ProcedureModel.objects.create(
    code="0901010049",
    name="OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE CÂNCER DE PRÓSTATA"
)

ProcedureModel.objects.create(
    code="0301010072",
    name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
    parent=main_prostata,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0205020110",
    name="ULTRASSONOGRAFIA DE PRÓSTATA VIA TRANSBRETAL",
    parent=main_prostata,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0201010410",
    name="BIÓPSIA DE PRÓSTATA VIA TRANSBRETAL",
    parent=main_prostata,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0203020030",
    name="EXAME ANATOMO-PATOLÓGICO PARA CONGELAMENTO / PARAFINA POR PEÇA CIRÚRGICA OU POR BIÓPSIA (EXCETO COLO UTERINO E MAMA)",
    parent=main_prostata,
    mandatory=True
)

# 8. OCI AVALIAÇÃO DIAGNÓSTICA DE CÂNCER GÁSTRICO
# main_gastrico = ProcedureModel.objects.create(
#     code="0901010073",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA DE CÂNCER GÁSTRICO"
# )

# ProcedureModel.objects.create(
#     code="0203020030",
#     name="EXAME ANATOMO PARA CONGELAMENTO / PARAFINA CIRÚRGICA OU POR BIÓPSIA (EXCETO UTERINO E MAMA)",
#     parent=main_gastrico,
#     mandatory=True
# )

# 9. OCI AVALIAÇÃO DIAGNÓSTICA DE CÂNCER COLORRETAL
# main_colon = ProcedureModel.objects.create(
#     code="0901010081",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA DE CÂNCER COLORRETAL"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_colon,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0209010029",
#     name="COLONOSCOPIA",
#     parent=main_colon,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0203020030",
#     name="EXAME ANATOMO-PATOLÓGICO PARA CONGELAMENTO / PARAFINA POR PEÇA CIRÚRGICA OU POR BIÓPSIA (EXCETO COLO UTERINO E MAMA)",
#     parent=main_colon,
#     mandatory=True
# )

# 10. OCI AVALIAÇÃO DE RISCO CIRÚRGICO  AQUI
main_risco = ProcedureModel.objects.create(
    code="0902010018",
    name="OCI AVALIAÇÃO DE RISCO CIRÚRGICO"
)

ProcedureModel.objects.create(
    code="0301010072",
    name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
    parent=main_risco,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211020036",
    name="ELETROCARDIOGRAMA",
    parent=main_risco,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0204030153",
    name="RADIOGRAFIA DE TÓRAX (PA E PERFIL)",
    parent=main_risco,
    mandatory=True
)

# 11. OCI AVALIAÇÃO CARDIOLÓGICA AQUI
main_cardio = ProcedureModel.objects.create(
    code="0902010026",
    name="OCI AVALIAÇÃO CARDIOLÓGICA"
)

ProcedureModel.objects.create(
    code="0301010072",
    name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
    parent=main_cardio,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211020036",
    name="ELETROCARDIOGRAMA",
    parent=main_cardio,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0204030153",
    name="RADIOGRAFIA DE TÓRAX (PA E PERFIL)",
    parent=main_cardio,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0205010032",
    name="ECOCARDIOGRAFIA TRANSTORÁCICA",
    parent=main_cardio,
    mandatory=True
)

# 12. OCI AVALIAÇÃO DIAGNÓSTICA INICIAL - SÍNDROME CORONARIANA CRÔNICA
# main_coronaria = ProcedureModel.objects.create(
#     code="0902010034",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA INICIAL - SÍNDROME CORONARIANA CRÔNICA"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
#     parent=main_coronaria,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211020036",
#     name="ELETROCARDIOGRAMA",
#     parent=main_coronaria,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211020060",
#     name="TESTE DE ESFORÇO / TESTE ERGOMÉTRICO",
#     parent=main_coronaria,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0205010032",
#     name="ECOCARDIOGRAFIA TRANSTORÁCICA",
#     parent=main_coronaria,
#     mandatory=True
# )

# 13. OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA I – SÍNDROME CORONARIANA CRÔNICA
# main_coronaria_i = ProcedureModel.objects.create(
#     code="0902010042",
#     name="OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA I – SÍNDROME CORONARIANA CRÔNICA"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
#     parent=main_coronaria_i,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0205010016",
#     name="ECOCARDIOGRAFIA DE ESTRESSE",
#     parent=main_coronaria_i,
#     mandatory=True
# )

# 14. OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA II – SÍNDROME CORONARIANA CRÔNICA
# main_coronaria_ii = ProcedureModel.objects.create(
#     code="0902010050",
#     name="OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA II – SÍNDROME CORONARIANA CRÔNICA"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
#     parent=main_coronaria_ii,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0208010033",
#     name="CINTILOGRAFIA DE MIOCÁRDIO PARA AVALIAÇÃO DA PERFUSÃO EM REPOUSO (MÍN. 3 PROJEÇÕES)",
#     parent=main_coronaria_ii,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0208010025",
#     name="CINTILOGRAFIA DE MIOCÁRDIO PARA AVALIAÇÃO DA PERFUSÃO EM ESTRESSE (MÍN. 3 PROJEÇÕES)",
#     parent=main_coronaria_ii,
#     mandatory=True
# )

# 15. OCI AVALIAÇÃO DIAGNÓSTICA - INSUFICIÊNCIA CARDÍACA
# main_insuficiencia = ProcedureModel.objects.create(
#     code="0902010069",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA - INSUFICIÊNCIA CARDÍACA"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
#     parent=main_insuficiencia,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211020036",
#     name="ELETROCARDIOGRAMA",
#     parent=main_insuficiencia,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211020060",
#     name="TESTE DE ESFORÇO / TESTE ERGOMÉTRICO",
#     parent=main_insuficiencia,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211020044",
#     name="MONITORAMENTO HOLTER 24 HS (3 CANAIS)",
#     parent=main_insuficiencia,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0202010791",
#     name="DOSAGEM DE PEPTÍDEOS NATRIURÉTICOS TIPO B (BNP E NT-PROBNP)",
#     parent=main_insuficiencia,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0205010032",
#     name="ECOCARDIOGRAFIA TRANSTORÁCICA",
#     parent=main_insuficiencia,
#     mandatory=True
# )

# 16. OCI AVALIAÇÃO DIAGNÓSTICA EM ORTOPEDIA COM RECURSOS DE RADIOLOGIA AQUI
main_ortopedia = ProcedureModel.objects.create(
    code="0903010011",
    name="OCI AVALIAÇÃO DIAGNÓSTICA EM ORTOPEDIA COM RECURSOS DE RADIOLOGIA"
)

ProcedureModel.objects.create(
    code="0301010072",
    name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
    parent=main_ortopedia,
    mandatory=True
)

# 17. OCI AVALIAÇÃO DIAGNÓSTICA EM ORTOPEDIA COM RECURSOS DE RADIOLOGIA E ULTRASSONOGRAFIA
# main_ortopedia_us = ProcedureModel.objects.create(
#     code="0903010020",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA EM ORTOPEDIA COM RECURSOS DE RADIOLOGIA E ULTRASSONOGRAFIA"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
#     parent=main_ortopedia_us,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0205020062",
#     name="ULTRASSONOGRAFIA DE ARTICULAÇÃO",
#     parent=main_ortopedia_us,
#     mandatory=True
# )

# 18. OCI AVALIAÇÃO DIAGNÓSTICA EM ORTOPEDIA COM RECURSOS DE RADIOLOGIA E TOMOGRAFIA COMPUTADORIZADA
# main_ortografia_tc = ProcedureModel.objects.create(
#     code="0903010038",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA EM ORTOPEDIA COM RECURSOS DE RADIOLOGIA E TOMOGRAFIA COMPUTADORIZADA"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
#     parent=main_ortografia_tc,
#     mandatory=True
# )

# # 19. OCI AVALIAÇÃO DIAGNÓSTICA EM ORTOPEDIA COM RECURSOS DE RADIOLOGIA E RESSONÂNCIA MAGNÉTICA
# main_ortografia_rm = ProcedureModel.objects.create(
#     code="0903010040",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA EM ORTOPEDIA COM RECURSOS DE RADIOLOGIA E RESSONÂNCIA MAGNÉTICA"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA E/OU TELECONSULTA MÉDICA NA ATENÇÃO ESPECIALIZADA",
#     parent=main_ortografia_rm,
#     mandatory=True
# )

# 20. OCI AVALIAÇÃO INICIAL DIAGNÓSTICA DE DÉFICIT AUDITIVO
# main_auditivo = ProcedureModel.objects.create(
#     code="0904010015",
#     name="OCI AVALIAÇÃO INICIAL DIAGNÓSTICA DE DÉFICIT AUDITIVO"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_auditivo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211070041",
#     name="AUDIOMETRIA TONAL LIMIAR (VIA AÉREA/ÓSSEA)",
#     parent=main_auditivo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211070203",
#     name="IMITANCIOMETRIA",
#     parent=main_auditivo,
#     mandatory=True
# )

# 21. OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE DÉFICIT AUDITIVO
# main_auditivo_prog = ProcedureModel.objects.create(
#     code="0904010023",
#     name="OCI PROGRESSÃO DA AVALIAÇÃO DIAGNÓSTICA DE DÉFICIT AUDITIVO"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_auditivo_prog,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211070041",
#     name="AUDIOMETRIA TONAL LIMIAR (VIA AÉREA/ÓSSEA)",
#     parent=main_auditivo_prog,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211070262",
#     name="POTENCIAL EVOCADO AUDITIVO DE CURTA, MÉDIA E LONGA LATÊNCIA",
#     parent=main_auditivo_prog,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211070203",
#     name="IMITANCIOMETRIA",
#     parent=main_auditivo_prog,
#     mandatory=True
# )

# 22. OCI AVALIAÇÃO DIAGNÓSTICA DE NASOFARINGE E DE OROFARINGE
# main_faringe = ProcedureModel.objects.create(
#     code="0904010031",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA DE NASOFARINGE E DE OROFARINGE"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_faringe,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0209040041",
#     name="VIDEOLARINGOSCOPIA",
#     parent=main_faringe,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0209040025",
#     name="LARINGOSCOPIA",
#     parent=main_faringe,
#     mandatory=True
# )

# 23. OCI AVALIAÇÃO INICIAL EM OFTALMOLOGIA - 0 A 8 ANOS
# main_oftalmo_0_8 = ProcedureModel.objects.create(
#     code="0905010019",
#     name="OCI AVALIAÇÃO INICIAL EM OFTALMOLOGIA - 0 A 8 ANOS"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_oftalmo_0_8,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060232",
#     name="TESTE ORTÓPTICO",
#     parent=main_oftalmo_0_8,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060127",
#     name="MAPEAMENTO DE RETINA",
#     parent=main_oftalmo_0_8,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060020",
#     name="BIOMICROSCOPIA DE FUNDO DE OLHO",
#     parent=main_oftalmo_0_8,
#     mandatory=True
# )

# 24. OCI AVALIAÇÃO DE ESTRABISMO
# main_estrabismo = ProcedureModel.objects.create(
#     code="0905010027",
#     name="OCI AVALIAÇÃO DE ESTRABISMO"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_estrabismo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060232",
#     name="TESTE ORTÓPTICO",
#     parent=main_estrabismo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060127",
#     name="MAPEAMENTO DE RETINA",
#     parent=main_estrabismo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060259",
#     name="TONOMETRIA",
#     parent=main_estrabismo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060020",
#     name="BIOMICROSCOPIA DE FUNDO DE OLHO",
#     parent=main_estrabismo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060100",
#     name="FUNDOSCOPIA",
#     parent=main_estrabismo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060178",
#     name="RETINOGRAFIA COLORIDA BINOCULAR",
#     parent=main_estrabismo,
#     mandatory=True
# )

# 25. OCI AVALIAÇÃO INICIAL EM OFTALMOLOGIA - A PARTIR DE 9 ANOS AQUI
main_oftalmo_9 = ProcedureModel.objects.create(
    code="0905010035",
    name="OCI AVALIAÇÃO INICIAL EM OFTALMOLOGIA - A PARTIR DE 9 ANOS"
)

ProcedureModel.objects.create(
    code="0301010072",
    name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
    parent=main_oftalmo_9,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060259",
    name="TONOMETRIA",
    parent=main_oftalmo_9,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060127",
    name="MAPEAMENTO DE RETINA",
    parent=main_oftalmo_9,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060020",
    name="BIOMICROSCOPIA DE FUNDO DE OLHO",
    parent=main_oftalmo_9,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060232",
    name="TESTE ORTÓPTICO",
    parent=main_oftalmo_9,
    mandatory=True
)

# 26. OCI AVALIAÇÃO DE RETINOPATIA DIABÉTICA
main_retinopatia = ProcedureModel.objects.create(
    code="0905010043",
    name="OCI AVALIAÇÃO DE RETINOPATIA DIABÉTICA"
)

ProcedureModel.objects.create(
    code="0301010072",
    name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
    parent=main_retinopatia,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060127",
    name="MAPEAMENTO DE RETINA",
    parent=main_retinopatia,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060178",
    name="RETINOGRAFIA COLORIDA BINOCULAR",
    parent=main_retinopatia,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060020",
    name="BIOMICROSCOPIA DE FUNDO DE OLHO",
    parent=main_retinopatia,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060259",
    name="TONOMETRIA",
    parent=main_retinopatia,
    mandatory=True
)

# 27. OCI AVALIAÇÃO INICIAL PARA ONCOLOGIA OFTALMOLÓGICA AQUI
main_onco_oftalmo = ProcedureModel.objects.create(
    code="0905010051",
    name="OCI AVALIAÇÃO INICIAL PARA ONCOLOGIA OFTALMOLÓGICA"
)

ProcedureModel.objects.create(
    code="0301010072",
    name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
    parent=main_onco_oftalmo,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0205020089",
    name="ULTRASSONOGRAFIA DE GLOBO OCULAR/ÓRBITA (MONOCULAR)",
    parent=main_onco_oftalmo,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060127",
    name="MAPEAMENTO DE RETINA",
    parent=main_onco_oftalmo,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060020",
    name="BIOMICROSCOPIA DE FUNDO DE OLHO",
    parent=main_onco_oftalmo,
    mandatory=True
)

ProcedureModel.objects.create(
    code="0211060259",
    name="TONOMETRIA",
    parent=main_onco_oftalmo,
    mandatory=True
)

# 28. OCI AVALIAÇÃO DIAGNÓSTICA EM NEURO OFTALMOLOGIA
# main_neuro_oftalmo = ProcedureModel.objects.create(
#     code="0905010060",
#     name="OCI AVALIAÇÃO DIAGNÓSTICA EM NEURO OFTALMOLOGIA"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_neuro_oftalmo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060038",
#     name="CAMPIMETRIA COMPUTADORIZADA OU MANUAL COM GRÁFICO",
#     parent=main_neuro_oftalmo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060259",
#     name="TONOMETRIA",
#     parent=main_neuro_oftalmo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060224",
#     name="TESTE DE VISÃO DE CORES",
#     parent=main_neuro_oftalmo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060127",
#     name="MAPEAMENTO DE RETINA",
#     parent=main_neuro_oftalmo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060178",
#     name="RETINOGRAFIA COLORIDA BINOCULAR",
#     parent=main_neuro_oftalmo,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060020",
#     name="BIOMICROSCOPIA DE FUNDO DE OLHO",
#     parent=main_neuro_oftalmo,
#     mandatory=True
# )

# 29. OCI EXAMES OFTALMOLÓGICOS SOB SEDAÇÃO
# main_oftalmo_sedacao = ProcedureModel.objects.create(
#     code="0905010078",
#     name="OCI EXAMES OFTALMOLÓGICOS SOB SEDAÇÃO"
# )

# ProcedureModel.objects.create(
#     code="0301010072",
#     name="CONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
#     parent=main_oftalmo_sedacao,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0417010060",
#     name="SEDAÇÃO",
#     parent=main_oftalmo_sedacao,
#     mandatory=True
# )

# ProcedureModel.objects.create(
#     code="0211060259",
#     name="TONOMETRIA",
#     parent=main_oftalmo_sedacao,
#     mandatory=True
# )