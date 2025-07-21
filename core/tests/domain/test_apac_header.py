from apac_core.domain.dto.apac_export import ApacHeader
from datetime import date

def test_apac_header():

    header = ApacHeader(
        origin_organization_name="POL SHOPPING NI",
        origin_organization_acronym="UNT",
        provider_cnpj_cpf="4565465",
        destination_organization_name="SECRETARIA DE SAUDE",
        destination_indicator="E",
        layout_version="1",
        competence="202505",
        apac_count=12,
        control_field="1774",
        generation_date=date(2025, 6, 30),
    )
    header_string = header.to_apac_string()
    header_expected = "01#APAC2025050000121774POL SHOPPING NI               UNT   00000004565465SECRETARIA DE SAUDE                     E202506301              "
    assert header_string == header_expected
    