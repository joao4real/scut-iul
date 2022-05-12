#!/bin/bash

###############################################################################
## ISCTE-IUL: Trabalho prático de Sistemas Operativos 2021/2022
##
## Aluno: Nº: 104669       Nome: João Luís Pereira Macedo 
## Nome do Módulo: stats.sh
## Descrição/Explicação do Módulo: 
##
##
###############################################################################

#!/bin/bash

if [ -z "$1" ]; then																								#argumento1 existe?
./error 2
exit
elif [ $# -gt 2 ]; then																								#o numero total de argumentos é maior que 2?
./error 2
exit
fi

if [ $# -eq 1 ]; then																								#caso o total de args seja 1, pode ser entre "listar" ou #condutores", caso contrario da erro
	if [ "$1" == "listar" ]; then
		 cat portagens.txt | cut -d ':' -f3 | uniq > listar.txt
         ./success 6 listar.txt																						#mostra a lista de todas as AEs que tenham registos de portagens
         rm listar.txt
         exit
	elif [ "$1" == "condutores" ]; then
	 cat relatorio_utilizacao.txt | cut -d ':' -f3 | sort | uniq > x.txt	
                IDS=$( cat x.txt | wc -l)																			#conta o numero de condutores com registos
                    for ((i=1 ; i <= IDS ; i++)); do																#percorrer todos os condutores
                    CURRENT=$( cat x.txt | head -$i | tail -1 )														#id do condutor atual segundo o incremento i
                    CONDUTOR=$( cat condutores.txt | grep "$CURRENT" | cut -d '-' -f2 | cut -d ';' -f1)				#condutor com o respetivo id
				    echo "$CONDUTOR" >> y.txt																		#mostra os condutores com registos de portagens
                    done
				    rm x.txt
				    ./success 6 y.txt
				    rm y.txt
					exit
	elif [ "$1" != "listar" ] && [ "$1" != "condutores" ] && [ "$1" != "registos" ]; then							#caso nao seja nem "listar" nem "condutores" pode ainda ser "registos", mas é inválido
	./error 3 "$1"																									#porque, caso seja "registos" precisa de mais um argumento numerico
	exit
	elif [ "$1" == "registos" ]; then
	./error 2
	exit
	fi
elif [ $# -eq 2 ]; then
	if [ "$1" == "registos" ]; then
		if [[ $2 =~ ^[0-9][0-9]*$ ]]; then																			#é unica e exclusivamente um numero?
		 cat relatorio_utilizacao.txt | cut -d ':' -f2 | uniq > pt.txt
                        LANCOS=$( cat pt.txt | wc -l)																#nº de lanços
                        for (( i=1 ; i <= $LANCOS ; i++ )); do														#percorrer todo os registos
                        REGISTO=$( cat pt.txt | head -$i | tail -1 )												#registo atual segundo o incremeno i
                        COUNTER=$( cat relatorio_utilizacao.txt | grep "$REGISTO" | wc -l )
                            if [ $COUNTER -ge $2 ]; then															#regista todos os lancos que tiverem igual ou mais registos que o argumento2
                            echo "$REGISTO" >> final.txt
                            else
                            echo "" >> final.txt
                            fi
                        done
                        rm pt.txt
                        cat final.txt | sort | uniq >final
                        cat final > final.txt
                        ./success 6 final.txt
                        rm final.txt
                        rm final
						exit
		else 
		./error 3 $2
		exit
		fi
#	else
#	./error 3 "$1"
#	exit
	fi
fi
