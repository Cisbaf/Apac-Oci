from apac_core.application.ultils.string import format_field



def test_format_filed():
    assert format_field("Daniel", 8, "") == "Daniel  "