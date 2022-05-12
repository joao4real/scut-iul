#!/bin/bash

# Utilização: ./stats.sh listar | registos <nr_registos> | condutores"

erro=0
case "$1" in
    listar)
        if [ $# -ne 1 ]; then
            echo "[*SO*] erro em stats.sh listar: número de parametros errado"
            erro=1
        else 
            echo "[*SO*] ok stats.sh listar"
        fi

    ;;
    registos)
        if [ $# -ne 2 ]; then
            echo "[*SO*] erro em stats.sh registos: número de parametros errado"
            erro=1
        else 
            echo "[*SO*] ok stats.sh registos '$2'"
        fi
    ;;
    condutores)
        if [ $# -ne 1 ]; then
            echo "[*SO*] erro em stats.sh condutores: número de parametros errado"
            erro=1
        else 
            echo "[*SO*] ok stats.sh condutores"
        fi

    ;;
    *)
        echo "[*SO*] erro em stats.sh: parâmetros inválidos"
        erro=1
    ;;
esac

if [ "$erro" != "0" ]; then
    i=0
    for v in $@; do
        i=$((i+1))
        echo "[*SO*] $i. '$v'"
    done
fi