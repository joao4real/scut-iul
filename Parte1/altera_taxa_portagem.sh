#!/bin/bash

###############################################################################
## ISCTE-IUL: Trabalho prático de Sistemas Operativos 2021/2022
##
## Aluno: Nº: 104669       Nome: João Luís Pereira Macedo
## Nome do Módulo: altera_taxa_portagem.sh
##  Descrição/Explicação do Módulo: 
##
##
###############################################################################
if [ $# -ne 3 ]; then #total de argumentos valido? (3)
./error 2
exit
#elif [ -z "$1" ]; then #argumento1 existe?
#./error 3 "$1"
#exit
elif !  [[ $1 =~ ^[a-zA-Z][a-zA-Z]*'-'[a-zA-Z][a-zA-Z]*$ ]]; then 		#argumento1 é uma String-String apenas?
./error 3 "$1"
exit
#elif [ -z "$2" ]; then		#argumento 2 existe?
#./error 3 "$2"
#exit
elif ! [[ $3 =~ ^[0-9][0-9]*$ ]]; then	#argumento3 é unica e exclusivamente um numero?
./error 3 "$3"
exit
elif [ $3 -lt 1 ]; then		#argumento3 é menor que 1?
./error 3 "$3"
exit
fi
 
if [ -f portagens.txt ]; then								#portagens.txt existe?	 
LANCO=$(grep -w "$1" ./portagens.txt | cut -d ':' -f2)		#verifica se o lanco ja existe
AE=$(grep -w "$1" ./portagens.txt | cut -d ':' -f3)			#autoestrada correspondente ao lanco, caso exista
		if [ -s portagens.txt ]; then						#portagens.txt tem algo escrito?
			if [ $LANCO ]; then								#se o lanco existir
ID=$(grep -w "$1" portagens.txt | cut -d ':' -f1)			#sacar o id do respetivo lanco
pickline=$(grep -w "$1" portagens.txt)						#vai buscar a linha do lanco
sed -i "s/"$pickline"/$ID:$1:$AE:$3/" portagens.txt			#altera apenas o valor da taxa
./success 3 "$1"											
			else
LASTID=$(cut -d ':' -f1 portagens.txt | sort -n | tail -1)	#vai buscar o ultimo id utilizado para poder incrementar +1
echo "$(($LASTID+1)):"$1":"$2":"$3"" >> portagens.txt		#incrementar
./success 3 "$1"
			fi
		else 
echo "1:"$1":"$2":$3" >> portagens.txt
./success 3 "$1"
		fi
	else
echo "1:"$1":"$2":$3" > portagens.txt
./success 3 "$1"
	fi

cat portagens.txt | sort -t ':' -k2,2 | sort -t ':' -k 3,3 -V -s > temp.txt			#ordenacao das autoestradas primeiramente e , em ultimo recurso (-s) ordena alfabeticamente lancos com a mesma AE
cat temp.txt > portagens.txt														#a virgula serve para limitar a ordenacao exlcusivamente a coluna em questao
rm temp.txt
./success 4 portagens.txt


