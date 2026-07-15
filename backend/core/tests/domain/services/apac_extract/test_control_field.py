from apac_core.domain.services.apac_extract.control_field import calculate_control_field


def test_soma_zero_cai_no_piso_do_dominio():
    assert calculate_control_field(procedures=[], apac_numbers=[]) == "1111"


def test_resto_zero_volta_ao_piso_do_dominio():
    assert calculate_control_field(procedures=[("1111", 0)], apac_numbers=[]) == "1111"


def test_resto_maximo_atinge_o_teto_do_dominio():
    assert calculate_control_field(procedures=[("1110", 0)], apac_numbers=[]) == "2221"


def test_soma_inclui_codigo_quantidade_e_numero_da_apac():
    # total = 100 (código) + 5 (quantidade) + 6 (número da APAC) = 111
    # resto = 111 % 1111 = 111 -> controle = 111 + 1111 = 1222
    resultado = calculate_control_field(procedures=[("100", 5)], apac_numbers=["6"])
    assert resultado == "1222"


def test_soma_varios_procedimentos_e_varias_apacs():
    resultado = calculate_control_field(
        procedures=[("10", 1), ("20", 2), ("30", 3)],
        apac_numbers=["100", "200"],
    )
    # total = (10+20+30) + (1+2+3) + (100+200) = 60 + 6 + 300 = 366
    # resto = 366 % 1111 = 366 -> controle = 366 + 1111 = 1477
    assert resultado == "1477"


def test_cenario_realista_com_dados_do_golden_file():
    """Códigos e batch_number iguais aos de tests/domain/services/export/fixtures.py
    (cenário 'apac_simples'), só para validar a fórmula com dados reais do domínio —
    não é o valor que o export de produção emite hoje (segue fixo em "1810")."""
    procedimentos = [
        ("0902010026", 1),  # principal — OCI AVALIAÇÃO CARDIOLÓGICA
        ("0301010072", 1),  # CONSULTA MEDICA EM ATENCAO ESPECIALIZADA
        ("0211020036", 1),  # ELETROCARDIOGRAMA
        ("0204030153", 1),  # RADIOGRAFIA DE TORAX (PA E PERFIL)
        ("0205010032", 1),  # ECOCARDIOGRAFIA TRANSTORACICA
    ]
    resultado = calculate_control_field(procedures=procedimentos, apac_numbers=["3325700278201"])
    assert resultado == "1917"
