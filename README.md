# Magiuniverso Discord Bot com Verificação de Integridade

Este bot do Discord inclui um sistema automático de **verificação de integridade de arquivos** e **alertas em tempo real**.

## Recursos

- ✅ Comando `!ping`
- 🛡️ Verificação de arquivos `.py`, `.json`, `.txt`, `.md`, `.env`
- 🔄 Intervalo de 5 minutos entre verificações
- 📢 Alertas enviados para o canal do Discord (`ID: 1371601665169428501`)
- ♻️ Geração automática de hashes e comparação de integridade

## Configuração

1. Defina a variável de ambiente `DISCORD_TOKEN` com seu token do bot
2. Use o Render como Web Service (não Background Worker)
3. Adicione o bot ao seu servidor com as permissões corretas