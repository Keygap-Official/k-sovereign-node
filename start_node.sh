#!/bin/bash
# --- K-SOVEREIGN ULTRA-STABLE STARTER ---

echo -e "\033[1;33m--- [K-SOVEREIGN] Reset totale processi... ---\033[0m"
# Chiude tutto sulla porta 8100 e ferma i tunnel precedenti
fuser -k 8100/tcp > /dev/null 2>&1
pkill -f lt > /dev/null 2>&1
pkill -f serveo > /dev/null 2>&1
sleep 2

echo -e "\033[1;32m--- [K-SOVEREIGN] Avvio Motore (Bot)... ---\033[0m"
# Avviamo il bot in modo che non possa essere "ucciso" facilmente
nohup python3 -u keygap_bot.py > output.log 2>&1 &

echo -e "\033[1;36m--- [K-SOVEREIGN] Apertura Tunnel SSH (Serveo)... ---\033[0m"
sleep 3

# Avviamo il tunnel tramite SSH. Se ti chiede 'yes/no', scrivi 'yes'
ssh -o ServerAliveInterval=60 -R 80:localhost:8100 serveo.net