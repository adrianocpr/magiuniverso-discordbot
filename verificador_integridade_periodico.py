import os
import hashlib
import json
from pathlib import Path

BASE_DIR = Path.cwd()
HASHES_FILE = BASE_DIR / "integridade_hashes.json"
EXTENSOES_MONITORADAS = [".py", ".json", ".env", ".txt", ".md"]

def gerar_hash_arquivo(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def verificar_integridade():
    if not HASHES_FILE.exists():
        return ["⚠️ Arquivo de hash não encontrado. Inicializando..."]

    with open(HASHES_FILE, "r") as f:
        hashes_salvos = json.load(f)

    alertas = []
    for root, _, files in os.walk(BASE_DIR):
        for nome_arquivo in files:
            if any(nome_arquivo.endswith(ext) for ext in EXTENSOES_MONITORADAS):
                caminho = Path(root) / nome_arquivo
                caminho_rel = str(caminho.relative_to(BASE_DIR))
                hash_atual = gerar_hash_arquivo(caminho)
                if not hash_atual:
                    continue
                if caminho_rel not in hashes_salvos:
                    alertas.append(f"📁 Novo arquivo: `{caminho_rel}`")
                elif hashes_salvos[caminho_rel] != hash_atual:
                    alertas.append(f"📝 Alteração: `{caminho_rel}`")

    for arquivo_salvo in hashes_salvos:
        if not (BASE_DIR / arquivo_salvo).exists():
            alertas.append(f"❌ Arquivo removido: `{arquivo_salvo}`")

    return alertas if alertas else ["✅ Todos os arquivos estão íntegros."]
