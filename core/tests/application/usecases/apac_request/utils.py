from datetime import date

def get_date_for_token():
    now = date.today()
    try:
        in_a_year = now.replace(year=now.year + 1)
    except ValueError:
        # Caso hoje seja 29 de fevereiro e o ano seguinte não seja bissexto
        in_a_year = now.replace(month=2, day=28, year=now.year + 1)
    return in_a_year