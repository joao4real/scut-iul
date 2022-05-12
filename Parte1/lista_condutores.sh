#!/bin/bash

###############################################################################
## ISCTE-IUL: Trabalho prático de Sistemas Operativos 2021/2022
##
## Aluno: Nº: 104669      Nome: João Luís Pereira Macedo
## Nome do Módulo: lista_condutores.sh
## Descrição/Explicação do Módulo: 
##Caso o ficheiro exista, ele vai começar por alterar a ordem das tabelas, de acordo o que é solicitado no ficheiro "condutores.txt"
##Após o comando awk, ele vai inicialmente trocar os espaços "default" por ";", depois troca o primeiro por um -( para juntar o ID ao Nome) e, por fim repete este
##comando para colocar um " " entre o nome e o apelido do condutor.
##Por fim, escreve o contéudo no ficheiro condutores.txt, onde vai ser validado na linha a seguir pelo comando success
##
################################################################################
if [ -f pessoas.txt ]; then
cat pessoas.txt | awk -F [:] '{print "ID"$3"-"$2";"$1";"$4";"$3";"150}'  > condutores.txt
./success 2 condutores.txt
else
./error 1 pessoas.txt
fi
