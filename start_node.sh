#!/bin/bash
echo "--- [K-SOVEREIGN] Reset Chirurgico (Protezione altri Bot)... ---"

# 1. Chiude SOLO il bot specifico cercando il nome esatto del file
pkill -f "keygap_bot.py" > /dev/null 2>&1

# 2. Chiude SOLO il tunnel specifico legato alla porta 8100
pkill -f "127.0.0.1:8100" > /dev/null 2>&1

# 3. Libera la porta 8100 per evitare errori
fuser -k 8100/tcp > /dev/null 2>&1

sleep 1

echo "--- [K-SOVEREIGN] Avvio Motore e Log in tempo reale... ---"
# Avvia il bot e mostra i log nello stesso terminale
python3 -u keygap_bot.py > output.log 2>&1 &
tail -f output.log &
LOG_PID=$!

echo "--- [K-SOVEREIGN] Apertura Tunnel SSH con Link FISSO ---"
# Chiediamo l'alias fisso. Grazie alla tua chiave SSH, Serveo ora può riconoscerlo
ssh -o ServerAliveInterval=60 -R keygap-sovereign-node:80:127.0.0.1:8100 serveo.net

# Ferma il monitoraggio dei log alla chiusura
kill $LOG_PID