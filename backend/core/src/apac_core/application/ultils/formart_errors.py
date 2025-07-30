def format_validation_errors(errors: list) -> str:
    formatted_errors = []
    for err in errors:
        loc = " → ".join(str(item) for item in err.get("loc", []))
        msg = err.get("msg", "Erro desconhecido")
        input_value = err.get("input", None)
        if input_value is not None:
            formatted_errors.append(f"{loc}: {msg} (valor: {input_value})")
        else:
            formatted_errors.append(f"{loc}: {msg}")
    return "\n".join(formatted_errors)
