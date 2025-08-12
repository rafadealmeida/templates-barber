from pathlib import Path

p = Path("fixtures/groups.json")
# p = Path("fixtures/site_content.json")
b = p.read_bytes()

decoded = None
for enc in ("utf-8", "cp1252", "latin-1"):
    try:
        decoded = b.decode(enc)
        print(f"Decodificado como: {enc}")
        break
    except UnicodeDecodeError:
        pass

if decoded is None:
    raise SystemExit("Não consegui decodificar o arquivo. Me envie o arquivo para eu checar.")

# Grava em UTF-8 (sem BOM)
p.write_text(decoded, encoding="utf-8")
print("Convertido e salvo em UTF-8:", p)
