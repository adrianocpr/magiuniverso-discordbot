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

def salvar_hashes_iniciais():
    hashes = {}
    for root, _, files in os.walk(BASE_DIR):
        for nome_arquivo in files:
            if any(nome_arquivo.endswith(ext) for ext in EXTENSOES_MONITORADAS):
                caminho = Path(root) / nome_arquivo
                hash_val = gerar_hash_arquivo(caminho)
                if hash_val:
                    hashes[str(caminho.relative_to(BASE_DIR))] = hash_val
    with open(HASHES_FILE, "w") as f:
        json.dump(hashes, f, indent=2)

def verificar_integridade():
    if not HASHES_FILE.exists():
        salvar_hashes_iniciais()
        return []

    with open(HASHES_FILE, "r") as f:
        hashes_salvos = json.load(f)

    arquivos_alerta = []
    for root, _, files in os.walk(BASE_DIR):
        for nome_arquivo in files:
            if any(nome_arquivo.endswith(ext) for ext in EXTENSOES_MONITORADAS):
                caminho = Path(root) / nome_arquivo
                caminho_rel = str(caminho.relative_to(BASE_DIR))
                hash_atual = gerar_hash_arquivo(caminho)
                if not hash_atual:
                    continue
                if caminho_rel not in hashes_salvos:
                    arquivos_alerta.append(f"Novo arquivo detectado: {caminho_rel}")
                elif hashes_salvos[caminho_rel] != hash_atual:
                    arquivos_alerta.append(f"Alteração detectada: {caminho_rel}")

    for arquivo_salvo in hashes_salvos.keys():
        if not (BASE_DIR / arquivo_salvo).exists():
            arquivos_alerta.append(f"Arquivo removido: {arquivo_salvo}")

    return arquivos_alerta

if __name__ == "__main__":
    alertas = verificar_integridade()
    if alertas:
        print("Alertas de integridade:")
        for alerta in alertas:
            print(f"- {alerta}")
    else:
        print("Todos os arquivos estão íntegros.")
