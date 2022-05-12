#!/usr/bin/env python3

##########################################################################
# ISCTE-IUL: 1.º - Trabalho prático de Sistemas Operativos 2021/2022
#
# Avaliação automática de 1 trabalho
#
# Versão 0.3.1
##########################################################################

import subprocess
import os
import sys
import argparse

##########################################################################
# Test data
#
##########################################################################
pessoas = \
    "L1234567:Manuel Silva:234580880:961112223", \
    "L1844374:Maria Abreu:215654377:916566777"

portagens = \
    "1:Cartaxo-Santarém:A1:1", \
    "14:Lisboa-Porto:A1:10", \
    "3:Fogueteiro-Coina:A2:3"

utilizacao = \
    "1:Cartaxo-Santarém:ID234580880:12-HT-62:5:21/02/2022", \
    "14:Lisboa-Porto:ID234580880:12-HT-62:10:17/02/2022", \
    "1:Cartaxo-Santarém:ID215654377:00-MV-88:5:15/02/2022", \
    "1:Cartaxo-Santarém:ID215654377:00-MV-88:5:13/02/2022", \
    "14:Lisboa-Porto:ID234580880:12-HT-62:10:05/02/2022"

##########################################################################
# List of questions
#
###########################################################################
enunciado = { 
    "1.1":"Verifica se 'pessoas.txt' existe",
    "1.2.1":"Cria ficheiro 'condutores.txt' correctamente",
    "1.2.2":"Chama './success 2'",
    "2.1.1":"Falha com 0 argumentos", 
    "2.1.2":"Falha com 1 argumentos", 
    "2.1.3":"Falha com 2 argumentos", 
    "2.1.4":"Falha com lanço inválido", 
    "2.1.5":"Falha com auto-estrada inválida", 
    "2.1.6":"Falha com valor taxa inválida", 
    "2.2.1":"(existe ficheiro, novo lanço) Chama 'success 3'",
    "2.2.2":"(existe ficheiro, novo lanço) Chama 'success 4'",
    "2.2.3":"(existe ficheiro, novo lanço) Ficheiro 'portagens.txt' correcto",
    "2.3.1":"(existe ficheiro, lanço existente) Chama 'success 3'",
    "2.3.2":"(existe ficheiro, lanço existente) Chama 'success 4'",
    "2.3.3":"(existe ficheiro, lanço existente) Ficheiro 'portagens.txt' correcto",
    "2.4.1":"(novo ficheiro) Chama 'sucess 3'",
    "2.4.2":"(novo ficheiro) Chama 'success 4'",
    "2.4.3":"(novo ficheiro) Ficheiro 'portagens.txt' correcto",
    "3.1":"Verifica se 'relatorio_utilizacao.txt' existe",
    "3.2.1":"Chama 'success 5'",
    "3.2.2":"Ficheiro 'faturas.txt' correcto",
    "4.1.1":"Falha com 0 argumentos",
    "4.1.2":"Falha com argumento inválido",
    "4.2.1":"Chama 'success 6'",
    "4.2.2":"Lista auto-estradas corretamente",
    "4.3.1":"Falha com registos sem argumentos",
    "4.3.2.a":"Chama 'success 6'",
    "4.3.2.b":"Lista lanços corretamente",
    "4.4.1":"Chama 'success 6'",
    "4.4.2":"Lista condutores corretamente",
    "5.1":"Sai do menu com 0",
    "5.2":"Chama lista_condutores.sh correctamente",
    "5.3":"Chama altera_taxa_portagem.sh correctamente",
    "5.4.1":"Chama stats.sh listar corretamente",
    "5.4.2":"Chama stats.sh registos corretamente",
    "5.4.3":"Chama stats.sh condutores corretamente",
    "5.5":"Chama faturacao.sh corretamente"
}

##########################################################################
# Utility functions
#
###########################################################################

if ( sys.stdout.encoding == "UTF-8" or sys.stdout.encoding == "utf-8" ):
  ok   = u"\u001b[32m✔\u001b[0m"
  fail = u"\u001b[31m✗\u001b[0m"
  warn = u"\u001b[33m⚠️\u001b[0m"
else:
  ok = "\u001b[32m[ ok ]\u001b[0m"
  fail = "\u001b[31m[fail]\u001b[0m"
  warn = "\u001b[33m[warn]\u001b[0m"

def create_file( filename, text ):
    """
    Creates a test file from a list of strings

    Parameters
    ----------
    filename : str
        Name of file to write, will be overriten
    text : list of str
        List of strings to write
    """
    f = open( filename, 'w' )
    for line in text:
        print( line, file = f )
    f.close()

def compare_files( fileA, fileB, skip_blanks = True, verbose = False, trim = True ):
    """
    Compares two text files, optionally skippping blank lines

    Parameters
    ----------
    fileA : str
        Filename of file A
    fileB : str
        Filename of file B
    skip_blanks : logical [optional]
        If set to True (default) blank lines will be skipped in the comparison
    trim : logical [optional]
        If set to True (default) lines will be trimmed (remove leading and 
        trailing blanks) before comparison
    verbose : logical [optional]
        If set to True prints out all different lines between the files. The
        default is not to print different lines.
    
    Returns
    -------
    compare_files : logical
        Returns true if the two files match, false otherwise
    """
    if ( not os.path.exists(fileA) ):
        print("(*error*) compare_files: file A '{}' not found".format(fileA) )
        return False

    if ( not os.path.exists(fileB) ):
        print("(*error*) compare_files: file B '{}' not found".format(fileB) )
        return False
    
    with open( fileA, 'r' ) as f:
        dataA = f.read().splitlines()

    with open( fileB, 'r' ) as f:
        dataB =  f.read().splitlines()

    if ( trim ):
        dataA = [ s.strip() for s in dataA ]
        dataB = [ s.strip() for s in dataB ]

    if ( skip_blanks ):
        dataA = [ s for s in dataA if s != '' ]
        dataB = [ s for s in dataB if s != '' ]
    
    if ( len(dataA) == len(dataB) ):
        equal = ( dataA == dataB )
    else:
        equal = False
    
    if ( not equal ):
        print("\n{} Files {} and {} don't match".format(fail,fileA, fileB))

        if ( verbose ):
            i = 0
            while ( (i < len(dataA)) or (i < len(dataB) ) ):
                if ( (i < len(dataA) ) and (i < len(dataB)) ):
                    if ( dataA[i] != dataB[i] ):
                        print('{:>16}:{} - {}'.format( fileA, i+1, dataA[i]) )
                        print('{:>16}:{} - {}\n'.format( fileB, i+1, dataB[i]) )
                elif ( i < len(dataA) ):
                    print('{:>16}:{} - {}'.format( fileA, i+1, dataA[i]) )
                    print('{:>16}:{} - \n'.format( fileB, i+1 ) )
                else:
                    print('{:>16}:{} - '.format( fileA, i+1 ) )
                    print('{:>16}:{} - {}\n'.format( fileB, i+1, dataB[i]) )

                i = i+1
    
    return equal


def compare_lists( listA, listB, skip_blanks = True, verbose = False, exact = True, trim = True ):
    """
    Compares two list of strings. The comparison may eliminate leading and
    trailing blanks and/or empty strings before comparison. The order of
    elements in the lists is not considered (i.e. lists are sorted before
    comparion). The comparison may consider either equal elements (A == B)
    or the presence of element A in string B (A in B).

    Parameters
    ----------
    listA : list of str
        List A
    listB : list of str
        List B
    exact : logical [optional]
        If set to True (default) the routine will check if the elements in list
        A match exactly the elements in list B. Otherwise the routine will check
        if the elements of list A are present (in) the elements of list B
    skip_blanks : logical [optional]
        If set to True (default) blank elements will be skipped in the comparison
    trim : logical [optional]
        If set to True (default) elements will be trimmed (remove leading and 
        trailing blanks) before comparison
    verbose : logical [optional]
        If set to True prints and the lists are different the routine will print
        the two lists. The default is never to print the lists.
    
    Returns
    -------
    compare_lists : logical
        Returns true if the two lists match, false otherwise
    """

    dataA = listA.copy()
    dataB = listB.copy()

    if ( trim ):
        dataA = [ s.strip() for s in dataA ]
        dataB = [ s.strip() for s in dataB ]

    if ( skip_blanks ):
        dataA = [ s for s in dataA if s != '' ]
        dataB = [ s for s in dataB if s != '' ]
    
    if ( len(dataA) == len(dataB)):
        dataA.sort()
        dataB.sort()
        if ( exact ):
            equal = ( dataA == dataB )
        else:
            equal = True
            i = 0
            for b in dataB:
                if ( not dataA[i] in b):
                    equal = False
                    break
                i = i + 1
    else:
        equal = False
    
    if ( not equal ):
        print( "\n{} Lists don't match".format(fail))

        if ( verbose ):
            print( "Expected: ", listA )
            print( "Got:      ", listB )
            print()
    
    return equal




def cleanup( files ):
    """Deletes file in list

    Parameters
    ----------
    files : list of str | str
        File or List of files to be deleted
    """
    if ( isinstance( files, str ) ):
        if ( os.path.exists(files) ):
            os.remove( files )
    else:
        for f in files:
            if ( os.path.exists(f) ):
                os.remove( f )

def eval_msg( success, key, test = None ):
    """Prints evaluation message

    Parameters
    ----------
    success : logical
        Set to true if test is working properly
    key : str
        Question number
    test : str or list of str [optional]
        Description of test to print in case of failure
    """
    if ( success ):
        print('{} - {}\t{}'.format( key, enunciado[key],ok))
    else:
        print('{} - {}\t{}'.format( key, enunciado[key],fail))
        if ( test ):
            if ( isinstance( test, str) ):
                msg = test
            else:
                msg = ' '.join(test)
            print('\t({}) test was <{}>'.format( key, msg ))

def run_process( scr, input = None, timeout = 2 ):
    """
    Runs a process and returns the associated CompletedProcess object

    The process has a maximum time of `timeout` seconds to execute, otherwise
    the command returns False.

    Parameters
    ----------
    scr : list
        Command to be run. Actual command invocation is the first list
        member, additional command line parameters are set in the
        remainder list elements
    input : list [optional]
        Input text to be sent to stdin, defaults to None
    timeout : int [optional]
        Timeout time, defaults to 2 (seconds)
    
    Returns
    -------
    process : CompletedProcess | False
        Returns the associated CompletedProcess object on success, and
        False on timeout.
    """
    try:
        proc = subprocess.run( scr, input = input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout )
        
        if ( proc.stderr ):
            stderr = proc.stderr.decode("utf-8").split('\n')
            if ( stderr[0] ):
                print("\n{}  Output on stderr from <{}>:".format(warn,' '.join(scr)))
            
            for l in stderr:
                if (l):
                    print( "{}\t{}".format(warn,l ))
            if ( stderr[0] ):
                print()
        
        return proc
    except subprocess.TimeoutExpired:
        print( "{}\t{}\t(*error*) timedout".format(fail, scr[0]) )
        return None

def check_proc_out( scr, output, input = None, timeout = 2 ):
    """
    Runs a process and checks if the stdout output matches the supplied values

    The process has a maximum time of `timeout` seconds to execute, otherwise
    the command returns False.

    Parameters
    ----------
    scr : list
        Command to be run. Actual command invocation is the first list
        member, additional command line parameters are set in the
        remainder list elements
    output : str
        Expected output
    input : list [optional]
        Input text to be sent to stdin, defaults to None
    timeout : int [optional]
        Timeout time, defaults to 2 (seconds)
    
    Returns
    -------
    check : logical
        Returns true if the required `output` is in the process stdout
    """

    try:
        proc = subprocess.run( scr, input = input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2 )

        if ( proc.stderr ):
            stderr = proc.stderr.decode("utf-8").split('\n')
            if ( stderr[0] ):
                print("\n{}  Output on stderr from <{}>:".format(warn,' '.join(scr)))
            for l in stderr:
                if (l):
                    print( "{}\t{}".format(warn,l ))

            if ( stderr[0] ):
                print()

        if ( output in proc.stdout ):
            return True
        else:
            print( "{}\t{}\t(*error*) got {}".format(fail,scr[0], proc.stdout) )
            return False
    except subprocess.TimeoutExpired:
        print( "{}\t{}\t(*error*) timedout".format(fail, scr[0]) )
        return False


##########################################################################
# Crete Input files from test data
#
###########################################################################

def create_file_condutores( pessoas, filename = 'condutores.txt'):
    """Cria o ficheiro 'condutores.*' a partir da variável `pessoas`

    Parameters
    ----------
    pessoas : list
        List of pessoas
    filename : str [optional]
        Output filename, defaults to 'condutores.txt'
    """
    f = open( filename, 'w')
    for pessoa in pessoas:
        data = pessoa.split(":")
        print( "ID{}-{};{};{};{};150".format(data[2],data[1],data[0],data[3],data[2]), file = f )
    f.close()

def create_file_faturas( utilizacao, pessoas, filename = 'faturas.txt'):
    """Cria o ficheiro 'faturas.*' a partir das variáveis `utilizacao` e `pessoas`

    Parameters
    ----------
    utilização : list
        List of utilização
    pessoas : list
        List of pessoas
    filename : str [optional]
        Output filename, defaults to 'faturas.txt'
    """

    # Get individuals and ids
    people = []

    for p in pessoas:
        data = p.split(":")
        people.append( ["ID"+data[2], data[1] ] )
    
    f = open( filename, 'w' )

    for p in people:
        total = 0
        id = p[0]
        name = p[1]
        
        for use in utilizacao:
            if ( id in use ):
                data = use.split(":")
                total += int(data[4])

        if ( total > 0 ):
            print("Cliente: {}".format(name), file = f )
            for use in utilizacao:
                if ( id in use ):
                    print( use, file = f )
            print( "Total: {} créditos\n".format(total), file = f )
    
    f.close()

def create_test_files():
    """Creates test files
    """
    create_file( 'pessoas.txt', pessoas )
    create_file( 'portagens.txt', portagens )
    create_file( 'relatorio_utilizacao.txt', utilizacao )
    create_file_condutores( pessoas, filename = 'condutores.txt')

def cleanup_test_files():
    """Removes test files
    """
    cleanup ( ['pessoas.txt','portagens.txt','relatorio_utilizacao.txt','condutores.txt'])

##########################################################################
# Parte 1 - lista_condutores.sh
#
##########################################################################

def test_lista_condutores( t ) :
    """Testa o script 'lista_condutores.sh'

    Alíneas 1.1, 1.2.1 e 1.2.2

    Parameters
    ----------
    t : str
        Source directory
    """
    scr = t + "/lista_condutores.sh"

    print( "\n1 - lista_condutores.sh...")

    if (not os.path.exists( scr )):
        print( "1. (*error*) {} not found {}".format(scr,fail) )
        return

    # Alínea 1.1
    cleanup( "pessoas.txt" )
    eval_msg( check_proc_out( scr, b'ERRO: O ficheiro "' ), '1.1', test = scr )
    
    # Alínea 1.2
    create_file( 'pessoas.txt', pessoas )
    create_file_condutores( pessoas, 'condutores.eval')

    try:
        proc = subprocess.run( [scr], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2 )
        # Check if 'condutores.txt' has the proper content
        success = False
        if (os.path.exists("condutores.txt")):
            success = compare_files( "condutores.txt", "condutores.eval", verbose = True )
        eval_msg( success, '1.2.1', test = scr)

        # Check if "success 2" was called
        eval_msg( ( b'SUCESSO: Lista de Condutores:\n' in proc.stdout ), '1.2.2', test = scr)

    except subprocess.TimeoutExpired:
        print( "{}\t{}\t(*error*) ./lista_condutores.sh timedout".format(t,fail) )

    # Cleanup test files
    cleanup( ["pessoas.txt", "condutores.eval", "condutores.txt" ] )

##########################################################################
# Parte 2 - altera_taxa_portagem.sh
#
##########################################################################

def test_altera_portagem( t ):
    """Testa o script 'altera_taxa_portagem.sh'

    Alíneas 2.1, 2.2 e 2.3

    Parameters
    ----------
    t : str
        Source directory
    """
    scr = t + "/altera_taxa_portagem.sh"

    print( "\n2 - altera_taxa_portagem.sh...")

    if (not os.path.exists( scr )):
        print( "2. (*error*) {} not found {}".format(scr,fail) )
        return


    # Alínea 2.1

    create_file( 'portagens.txt', portagens )

    eval_msg( check_proc_out( [ scr ],
         b'ERRO: N\xc3\xa3o foram passados argumentos suficientes!\n' ),
        '2.1.1', test = scr )

    test = [ scr, 'A' ]
    eval_msg( check_proc_out( test,
         b'ERRO: N\xc3\xa3o foram passados argumentos suficientes!\n' ),
        '2.1.2', test = test )

    test = [ scr, 'A', 'B' ]
    eval_msg( check_proc_out( test,
         b'ERRO: N\xc3\xa3o foram passados argumentos suficientes!\n' ),
        '2.1.3', test = test )

    test = [ scr, 'A', 'B', 'C' ]
    eval_msg( check_proc_out( test,
         b'ERRO: O formato do argumento "' ),
        '2.1.4', test = test )

    test = [ scr, 'Leiria-Pombal', 'B', 'C' ]
    eval_msg( check_proc_out( test,
         b'ERRO: O formato do argumento "' ),
        '2.1.5', test = test )

    test = [ scr, 'Leiria-Pombal', 'A2', 'C' ]
    eval_msg( check_proc_out( test,
         b'ERRO: O formato do argumento "' ),
        '2.1.6', test = test )

    # Alínea 2.2 (existe ficheiro, lanço novo)
    cleanup( "portagens.txt" )
    create_file( 'portagens.txt', portagens )

    test = [scr, 'Lisboa-Setúbal', 'A2', '5']
    proc = run_process( test )
    if ( proc ):
        eval_msg( ( b'SUCESSO: Atualiza\xc3\xa7\xc3\xa3o da taxa de utiliza\xc3\xa7\xc3\xa3o do Lan\xc3\xa7o "Lisboa-Set\xc3\xbabal"\n'
            in proc.stdout ), '2.2.1' )
        eval_msg( ( b'\n15:Lisboa-Set\xc3\xbabal:A2:5\n' in proc.stdout ), '2.2.2', test = test )

        new = list(portagens)
        new.append("15:Lisboa-Setúbal:A2:5")
        create_file( 'portagens.eval', new )
        eval_msg( compare_files( "portagens.txt", "portagens.eval", verbose = True ), '2.2.3', test = test)
        os.remove( 'portagens.eval')

    else :
        eval_msg( False, '2.2.1', test = test)
        eval_msg( False, '2.2.2', test = test)
        eval_msg( False, '2.2.3', test = test)

    # Alínea 2.3 (existe ficheiro, lanço existente)
    cleanup( "portagens.txt" )
    create_file( 'portagens.txt', portagens )

    test = [scr, 'Lisboa-Porto', 'A1', '15']
    proc = run_process( test )
    if ( proc ):
        eval_msg( ( b'SUCESSO: Atualiza\xc3\xa7\xc3\xa3o da taxa de utiliza\xc3\xa7\xc3\xa3o do Lan\xc3\xa7o "Lisboa-Porto"\n'
            in proc.stdout ), '2.3.1' )
        eval_msg( ( b'\n14:Lisboa-Porto:A1:15\n' in proc.stdout ), '2.3.2', test = test )

        new = list(portagens)
        for i in range( len(new) ):
            if ( 'Lisboa-Porto' in new[i] ):
                new[i] = '14:Lisboa-Porto:A1:15'
                break
        create_file( 'portagens.eval', new )
        eval_msg( compare_files( "portagens.txt", "portagens.eval", verbose = True ), '2.3.3', test = test )
        os.remove( 'portagens.eval')

    else :
        eval_msg( False, '2.3.1', test = test)
        eval_msg( False, '2.3.2', test = test)
        eval_msg( False, '2.3.3', test = test)

    # Alínea 2.4 (não existe ficheiro)
    cleanup( "portagens.txt" )

    test = [scr, 'Lisboa-Porto', 'A1', '15']
    proc = run_process( test )
    if ( proc ):
        eval_msg( ( b'SUCESSO: Atualiza\xc3\xa7\xc3\xa3o da taxa de utiliza\xc3\xa7\xc3\xa3o do Lan\xc3\xa7o "Lisboa-Porto"\n'
            in proc.stdout ), '2.4.1' )
        eval_msg( ( b'\n1:Lisboa-Porto:A1:15\n' in proc.stdout ), '2.4.2', test = test )

        new = ['1:Lisboa-Porto:A1:15']
        create_file( 'portagens.eval', new )
        eval_msg( compare_files( "portagens.txt", "portagens.eval", verbose = True ), '2.4.3', test = test)
        os.remove( 'portagens.eval')
    else :
        eval_msg( False, '2.4.1', test = test)
        eval_msg( False, '2.4.2', test = test)
        eval_msg( False, '2.3.3', test = test)
    
    cleanup( "portagens.txt" )

##########################################################################
# Parte 3 - faturacao.sh
#
##########################################################################

def test_faturacao( t ):
    """Testa o script 'faturacao.sh'

    Alíneas 3.1, 3.2

    Parameters
    ----------
    t : str
        Source directory
    """

    scr = t + "/faturacao.sh"

    print( "\n3 - faturacao.sh...")


    if (not os.path.exists( scr )):
        print( "3. (*error*) {} not found {}".format(scr,fail) )
        return

    # Alínea 3.1
    cleanup("relatorio_utilizacao.txt")

    eval_msg( check_proc_out( [ scr ],
         b'ERRO: O ficheiro "' ),
        '3.1', test = scr )
    
    # Alínea 3.2
    create_file( 'pessoas.txt', pessoas )
    create_file_condutores( pessoas, 'condutores.txt' )
    create_file( 'relatorio_utilizacao.txt', utilizacao )

    proc = run_process( [scr] )
    if ( proc ):
        eval_msg( ( b'SUCESSO: Lista de Faturas:\n'
            in proc.stdout ), '3.2.1', test = scr )

        create_file_faturas( utilizacao, pessoas, 'faturas.eval' )
        eval_msg( compare_files( "faturas.txt", "faturas.eval", verbose = True ), '3.2.2', test = scr)
        os.remove( "faturas.eval" )
    else:
        eval_msg( False, '3.2.1', test = scr)
        eval_msg( False, '3.2.2', test = scr)

    # Cleanup
    cleanup( [ "relatorio_utilizacao.txt", "pessoas.txt", "condutores.txt", "faturas.txt" ] )

##########################################################################
# Parte 4 - stats.sh
#
##########################################################################

def test_stats( t ):
    """Testa o script 'stats.sh'

    Alíneas 4.1 a 4.4

    Parameters
    ----------
    t : str
        Source directory
    """

    scr = t + "/stats.sh"

    print( "\n4 - stats.sh...")

    if (not os.path.exists( scr )):
        print( "4. (*error*) {} not found {}".format(scr,fail) )
        return
    
    #4.1.1 - Falha com 0 argumentos
    create_file( "portagens.txt", portagens )
    create_file( 'relatorio_utilizacao.txt', utilizacao )

    eval_msg( check_proc_out( [ scr ],
         b'ERRO: N\xc3\xa3o foram passados argumentos suficientes!\n' ),
        '4.1.1', test = scr )

    cleanup( ['relatorio_utilizacao.txt', 'portagens.txt'] )

    #4.1.2 - Falha com argumento inválido
    create_file( "portagens.txt", portagens )
    create_file( 'relatorio_utilizacao.txt', utilizacao )

    test = [ scr, "bad" ]
    eval_msg( check_proc_out( test,
         b'ERRO: O formato do argumento "' ),
        '4.1.2', test = test )

    #4.2   - Lista auto-estradas corretamente
    create_file( "portagens.txt", portagens )
    create_file( 'relatorio_utilizacao.txt', utilizacao )

    test = [scr, 'listar']
    proc = run_process( test )
    if ( proc ):
        res = proc.stdout.split(b'\n')
        if ( b'SUCESSO: Lista de Nomes:\n' in proc.stdout ):
            eval_msg( True, '4.2.1', test = test )
            res.pop(0)
        else:
            eval_msg( False, '4.2.1', test = test )

        # Cleanup command output
        res = [ s.decode("utf-8") for s in res if s != b'' ]

        # Create solution from test data
        eval = [ (s.split(':'))[2] for s in portagens ]
        eval = list(set(eval))
        
        success = compare_lists( eval, res, verbose = True )
        
        eval_msg( success, '4.2.2', test = test)
    else:
        eval_msg( False, '4.2.1', test = test)
        eval_msg( False, '4.2.2', test = test)
    
    cleanup( ['relatorio_utilizacao.txt', 'portagens.txt'] )

    #4.3.1 - Falha com registos sem argumentos
    create_file( 'relatorio_utilizacao.txt', utilizacao )
    
    test = [ scr, "registos" ]
    eval_msg( check_proc_out( test,
         b'ERRO: N\xc3\xa3o foram passados argumentos suficientes!\n' ),
        '4.3.1', test = test )

    #4.3.2 - Lista lanços corretamente
    create_file( 'relatorio_utilizacao.txt', utilizacao )
    create_file( 'portagens.txt', portagens )

    nr_registos = 3

    test = [scr, 'registos', str(nr_registos)]
    proc = run_process( test )
    if ( proc ):
        res = proc.stdout.split(b'\n')
        if ( b'SUCESSO: Lista de Nomes:\n' in proc.stdout ):
            eval_msg( True, '4.3.2.a', test = test )
            res.pop(0)
        else:
            eval_msg( False, '4.3.2.a', test = test )
        
        res = [ s.decode("utf-8") for s in res if s != b'' ]

        lancos = [ (s.split(':'))[1] for s in utilizacao ]
        eval = []
        for l in list(set(lancos)):
            count = lancos.count(l)
            if (count >= nr_registos):
                eval.append( l )

        success = compare_lists( eval, res, exact = False, verbose = True )
        eval_msg( success, '4.3.2.b', test = test)


    else:
        eval_msg( False, '4.3.2.a', test = test)
        eval_msg( False, '4.3.2.b', test = test)
    
    cleanup( ['relatorio_utilizacao.txt', 'portagens.txt'] )

    #4.4   - Lista condutores corretamente
    create_file( "pessoas.txt", pessoas )
    create_file( 'relatorio_utilizacao.txt', utilizacao )
    create_file_condutores( pessoas, filename = 'condutores.txt')

    test = [ scr, 'condutores' ]
    proc = run_process( test )
    if ( proc ):
        res = proc.stdout.split(b'\n')
        if ( b'SUCESSO: Lista de Nomes:\n' in proc.stdout ):
            eval_msg( True, '4.4.1', test = test )
            res.pop(0)
        else:
            eval_msg( False, '4.4.1', test = test )

        # Cleanup command output
        res = [ s.decode("utf-8") for s in res if s != b'' ]

        # Create solution from test data
        eval = [ (s.split(':'))[1] for s in pessoas ]

        success = compare_lists( eval, res, verbose = True )
        eval_msg( success, '4.4.2', test = test)
    else:
        eval_msg( False, '4.4.1', test = test)
        eval_msg( False, '4.4.2', test = test)
    
    cleanup( ["pessoas.txt", "condutores.txt", "relatorio_utilizacao.txt"] )


##########################################################################
# Parte 5 - menu.sh
#
##########################################################################

def test_menu( t ):
    """Testa o script 'menu.sh'

    Alíneas 5.1 a 5.5

    Parameters
    ----------
    t : str
        Source directory
    """

    scr = t + "/menu.sh"

    print( "\n5 - menu.sh...")

    if (not os.path.exists( scr )):
        print( "5. (*error*) {} not found {}".format(scr,fail) )
        return
    
    # Alínea 5.1
    opts = bytes('0\n','ascii')
    proc = run_process( [scr], input = opts )
    if ( proc ):
        eval_msg( True, '5.1')
    else:
        eval_msg( False, '5.1')
        print('{} {}'.format( "Menu fails to exit, manual correction needed",fail))
        return
    
    # Alínea 5.2
    opts = bytes('1\n\n0\n','ascii')
    eval_msg( check_proc_out( [ scr ],
        b'[*SO*] lista_condutores.sh ok\n', input = opts ),
        '5.2' )
    
    # Alínea 5.3
    opts = bytes('2\nAlverca-Tomar\nA2\n120\n\n0\n','ascii')
    eval_msg( check_proc_out( [ scr ],
        b"[*SO*] altera_taxa_portagem.sh 'Alverca-Tomar' 'A2' '120'\n", input = opts ),
        '5.3' )
    
    # Alínea 5.4
    opts = bytes('3\n1\n\n0\n','ascii')
    eval_msg( check_proc_out( [ scr ],
        b"[*SO*] ok stats.sh listar\n", input = opts ),
        '5.4.1' )

    opts = bytes('3\n2\n12\n\n0\n','ascii')
    eval_msg( check_proc_out( [ scr ],
        b"[*SO*] ok stats.sh registos '12'\n", input = opts ),
        '5.4.2' )
    
    opts = bytes('3\n3\n\n0\n','ascii')
    eval_msg( check_proc_out( [ scr ],
        b"[*SO*] ok stats.sh condutores\n", input = opts ),
        '5.4.3' )

    # Alínea 5.5
    opts = bytes('4\n\n0\n','ascii')
    eval_msg( check_proc_out( [ scr ],
        b"[*SO*] faturacao.sh ok\n", input = opts ),
        '5.5' )


##########################################################################
# Main
#
##########################################################################

parser = argparse.ArgumentParser( description="Evaluate test problem",
    usage = '%(prog)s [-h] [-g] [-c] <source>' )

parser.add_argument( "-g","--generate", dest="generate", action='store_true', \
                    help = "Generate test files")

parser.add_argument( "-c","--cleanup", dest="cleanup", action='store_true', \
                    help = "Cleanup test files")

parser.add_argument( 'Source', 
    metavar='source', nargs = '?', default = None,
    type =str, 
    help='Directory with source files to evaluate' )

# Parse command line arguments
args = parser.parse_args()

# If requested generate test files and exit
if ( args.generate ):
    print("Generating test files...")
    create_test_files()
    print("done.")
    exit(0)

# If requested cleanup test files and exit
if ( args.cleanup ):
    print("Cleaning up test files...")
    cleanup_test_files()
    print("done.")
    exit(0)

if ( args.Source is None ):
    print("Source directory not specified")
    parser.print_usage()
    exit(1)

# Get test directory
testdir = args.Source

# Check if directory exists
if (not os.path.exists( testdir )):
    print('(*error*) Directory "{}" does not exist'.format(testdir))
    exit(1)

# Check if it is current directory
if ( os.path.samefile(".", testdir)):
    print('(*error*) Source must not be local (.) directory')
    exit(2)

# Check for additional scripts
scripts = ["error","success",
    "altera_taxa_portagem.sh",
    "faturacao.sh",
    "lista_condutores.sh",
    "stats.sh" ]

for s in scripts:
    if ( not os.path.exists(s)):
        print('(*error*) "{}" script not found'.format(s))
        exit(3)

# Run tests
print("Evaluating directory '{}'...".format(testdir))

test_lista_condutores( testdir )
test_altera_portagem( testdir )
test_faturacao( testdir )
test_stats( testdir )
test_menu( testdir )

print("\ndone.")
