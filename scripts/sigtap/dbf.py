"""Leitor mínimo de arquivos DBF (dBase III / Clipper), sem dependências externas.

As tabelas oficiais do SIGTAP distribuídas com o APAC Magnético são DBF Clipper.
Só precisamos ler; não há escrita aqui de propósito — o SIGTAP é fonte de leitura.
"""
import struct


def read_dbf(path, encoding="latin-1"):
    """Devolve (campos, registros). `campos` é [(nome, tipo, tamanho, decimais)]."""
    with open(path, "rb") as f:
        data = f.read()

    num_records, header_len, record_len = struct.unpack("<IHH", data[4:12])

    fields = []
    pos = 32
    while data[pos] != 0x0D:  # 0x0D encerra o descritor de campos
        raw = data[pos:pos + 32]
        name = raw[0:11].split(b"\x00")[0].decode("ascii", "replace")
        fields.append((name, chr(raw[11]), raw[16], raw[17]))
        pos += 32

    rows = []
    for i in range(num_records):
        offset = header_len + i * record_len
        record = data[offset:offset + record_len]
        if not record or record[0:1] == b"*":  # registro marcado como deletado
            continue
        cursor = 1
        row = {}
        for name, _type, length, _dec in fields:
            row[name] = record[cursor:cursor + length].decode(encoding, "replace").strip()
            cursor += length
        rows.append(row)
    return fields, rows
