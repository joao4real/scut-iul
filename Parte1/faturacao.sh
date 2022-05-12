#!/bin/bash

###############################################################################
## ISCTE-IUL: Trabalho prático de Sistemas Operativos 2021/2022
##
## Aluno: Nº: 104669       Nome: João Luís Pereira Macedo 
## Nome do Módulo: faturacao.sh
## Descrição/Explicação do Módulo: 
##
##
###############################################################################

if [ -f relatorio_utilizacao.txt ]; then														#o relatorio existe?
	if [ -f faturas.txt ]; then																	# faturas existe?
	rm faturas.txt																				#remove antigas faturas
	./faturacao.sh																				#volta a repetir o script
		elif [ -s relatorio_utilizacao.txt ]; then												#o relatorio tem algo escrito?
		CONDUTORES=$(cat pessoas.txt | wc -l)													#ve o numero de condutores
		for (( i=1 ; i <= $CONDUTORES ; i++ )); do												#vai percorrer todos os condutores
		CONDUTOR=$( cat pessoas.txt | head -$i | tail -1 | cut -d ':' -f2 )						#condutor relativo ao incremento i
		ID=$( cat pessoas.txt | head -$i | tail -1 | cut -d ':' -f3 )							#id relativo ao incremento i
		TOTAL=$( grep "$ID" relatorio_utilizacao.txt | cut -d ':' -f5 | paste -sd "+" | bc)		#o paste-sd passa o que esta em coluna para uma linha e substitui o " " por "+" e o bc faz a conta
		echo "Cliente: $CONDUTOR" >> faturas.txt												
		echo "$( grep "$ID" relatorio_utilizacao.txt )" >> faturas.txt
		echo "Total: $(($TOTAL+0)) créditos" >> faturas.txt
		echo "" >> faturas.txt 
		done 
	./success 5 faturas.txt
		fi
	else 
	./error 1 relatorio_utilizacao.txt
	fi 
