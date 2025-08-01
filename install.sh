#!/bin/bash
# Vampire Squad - API Finder Installer by VAMPIRE

clear
echo -e "\033[1;31mVampire-API-Finder Installer by VAMPIRE\033[0m"
sleep 1

echo -e "\n[+] Updating packages..."
pkg update -y && pkg upgrade -y

echo -e "\n[+] Installing Python..."
pkg install python -y

echo -e "\n[+] Installing mitmproxy..."
pip install mitmproxy

echo -e "\n✅ All requirements installed!"
echo -e "\n🚀 Run the tool with: \033[1;32mpython3 api_finder.py\033[0m"
