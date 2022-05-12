#!/bin/bash

###############################################################################
## ISCTE-IUL: Trabalho prático de Sistemas Operativos 2021/2022
##
## Aluno: Nº: 104669       Nome: João Luís Pereira Macedo
## Nome do Módulo: menu.sh
## Descrição/Explicação do Módulo: 
##
##
############################################################################### 

while [ true ]; do #MENU							permite ficar em loop ate clicar em "Voltar"
echo ""
echo "MENU"
echo ""
echo -e "1. Lista condutores\n2. Altera taxa de portagem\n3. Stats\n4. Faturação\n0. Sair"
echo ""
echo -n "Opção: " 
read number 
	case $number in
	0)		exit;;																													#sai do script
	1)      echo ""																													
		    echo "Listar os condutores..."																								
		    echo ""																													#lista os condutores
		    ./lista_condutores.sh;;
	2)		echo ""
			echo "Altera taxa de portagem..."
			echo -n "Lanço              :"
			read lanco 
			echo -n "Auto-estrada       :"
			read estrada
			echo -n "Novo valor taxa    :"
			read taxa
			./altera_taxa_portagem.sh $lanco $estrada $taxa;;																		#Adiciona o lanco, AE e Taxa
	3)		 #SUBMENU
				echo ""
				echo "Stats"
				echo ""
				echo -e "1. Nomes de todas as Autoestradas\n2. Registos de utilização\n3. Listagem condutores\n0. Voltar"
				echo ""
				echo -n "Opção: "																									#SUBMENU dentro da 3ºopção do MENU
				read option
					case $option in
						0);;																										#volta ao menu
						1)./stats.sh listar;;																						#lista as AEs
						2)echo -n "Mínimo de registos :"
							read registos								
							./stats.sh registos $registos;;																			#escolhe os registos maiores ou igual que o argumento
						3)./stats.sh condutores;;																					#lista os condutores												
						*)echo "Escolha um dos números propostos";;																	#caso introduza um valor invalido, ele notifica
					esac;;
			
	4)			./faturacao.sh;;																									#NO MENU, imprime a fatura de todos os condutores
	*)		echo "Escolha um dos números propostos";;																				#Caso introduza um valor invalido, ele notifica
	esac
done	








										
