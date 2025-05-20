import asyncio
import subprocess

async def periodic_integrity_check(interval=300):
    while True:
        print("Executando verificação de integridade...")
        result = subprocess.run(["python", "verificador_integridade.py"], capture_output=True, text=True)
        print(result.stdout)
        await asyncio.sleep(interval)

if __name__ == "__main__":
    try:
        asyncio.run(periodic_integrity_check())
    except KeyboardInterrupt:
        print("Verificador interrompido.")