#!/bin/bash

# Risolvi l'IP del container 'db'
DB_IP=$(getent hosts db | awk '{ print $1 }')

echo "🔧 Mapping localhost -> db ($DB_IP)"

# Aggiungi l'entry in /etc/hosts per mappare localhost al database
echo "$DB_IP localhost" >> /etc/hosts

# Avvia l'applicazione
exec python Task_server.py
