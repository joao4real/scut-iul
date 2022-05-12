#!/bin/bash

# Utilização: ./altera_taxa_portagem.sh <lanço> <auto-estrada> <novo_valor_taxa>

if [ $# -ne 3 ]; then
    echo "[*SO*] erro em altera_taxa_portagem.sh: número de parametros errado: $#"
    i=0
    for v in "$@"; do
        i=$((i+1))
        echo "$i. '$v'"
    done
else
    echo "[*SO*] altera_taxa_portagem.sh '$1' '$2' '$3'"
fi

