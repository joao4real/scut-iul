#ifndef __UTILS_H__
#define __UTILS_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>

/******************************************************************************
 *  Macros para tratamento de mensagens de DEBUG
 ******************************************************************************/
#define TRUE  1
#define FALSE 0

/**
 *  Impressão de mensagens de DEBUG incluindo o módulo e a linha de código. Para ativar, alterar DEBUG_MODE para 1
 */
#define DEBUG_MODE FALSE  // Se estiver a TRUE, apresentará mensagens de DEBUG, caso contrário, não apresenta

/**
 *  Escreve uma mensagem de debug (parâmetros iguais ao printf) se DEBUG_MODE estiver a TRUE
 */
#define debug(fmt, ...) do { if (DEBUG_MODE) fprintf(stderr, "@@Debug@@:%s:%d:%s(): " fmt "\n", __FILE__, __LINE__, __func__, ## __VA_ARGS__); } while (0)

/******************************************************************************
 *  Macros para impressão de mensagens de sucesso e de erro
 ******************************************************************************/

/**
 *  Valida se uma operação teve sucesso ou não. Se não teve, escreve uma mensagem de erro e sai com erro -1, e mostrando a mensagem de erro,
 *  @param status   resultado da operação anterior. Se < 0 é porque houve erro, e nesse caso afixa a mensagem de erro e sai com status -1
 *  @param errorMsg mensagem de erro a apresentar em caso de erro
 */
#define exit_on_error(status, errorMsg) do { if (status < 0) { perror(errorMsg); exit(-1); } } while (0)

/**
 *  Valida se uma operação teve sucesso ou não. Se não teve, escreve uma mensagem de erro e sai com erro -1, e mostrando a mensagem de erro,
 *  @param status   resultado da operação anterior. Se == NULL é porque houve erro, e nesse caso afixa a mensagem de erro e sai com status -1
 *  @param errorMsg mensagem de erro a apresentar em caso de erro
 */
#define exit_on_null(status, errorMsg) do { if (NULL == status) { perror(errorMsg); exit(-1); } } while (0)

/******************************************************************************
 *  Macros para leitura de Strings de um ficheiro ou do STDIN
 ******************************************************************************/

/**
 *  Macro para leitura de Strings de um ficheiro
 *  Esta macro basicamente efetua a leitura de uma string de um ficheiro, definido um buffer_size. Semelhante a fgets(), mas removendo o '\n' e os caracteres extra.
 *  @param buffer        (char*) buffer onde vai ser depositada a informação
 *  @param buffer_size   (int) tamanho do buffer acima (em bytes)
 *  @param file          (FILE*) handler do ficheiro a ler
 */
#define my_fgets(buffer, buffer_size, file) ({          \
    char* _result = fgets(buffer, buffer_size, file);   \
    if (NULL != _result) {                              \
        if ('\n' == buffer[strlen(buffer) - 1])         \
            buffer[strlen(buffer) - 1] = '\0';          \
        else {                                          \
            int c;                                      \
            do                                          \
                c = getc(file);                         \
            while ('\n' != c && EOF != c);              \
        }                                               \
    }                                                   \
    _result;                                            \
})

/**
 *  Macro para leitura de Strings do STDIN
 *  Esta macro basicamente efetua a leitura de uma string do STDIN, definido um buffer_size. Semelhante a fgets(), mas removendo o '\n' e os caracteres extra.
 *  @param buffer        (char*) buffer onde vai ser depositada a informação
 *  @param buffer_size   (int) tamanho do buffer acima (em bytes)
 */
#define my_gets(buffer, buffer_size) my_fgets(buffer, buffer_size, stdin)

/******************************************************************************
 *  Macros utilitárias
 ******************************************************************************/

#define my_rand() ({         \
    struct timeval tv;       \
    gettimeofday(&tv, NULL); \
    srand(tv.tv_usec);       \
    rand();                  \
})

/******************************************************************************
 *  Macros para impressão de mensagens de sucesso e de erro
 ******************************************************************************/

/**
 *  Escreve uma mensagem de sucesso (parâmetros iguais ao printf), deve ser usado em todas as mensagens "positivas" que a aplicação mostra
 *  @param passo (o passo do enunciado) ... os argumentos são os mesmos que os do printf(), logo recebe uma string de formatação e depois um número variável de argumentos
 */
#define success(passo, fmt, ...) do { printf("@@Success@@ {" passo "} " fmt "\n", ## __VA_ARGS__); } while (0)

/**
 *  Escreve uma mensagem de erro (parâmetros iguais ao printf), deve ser usado em todas as mensagens "de erro" que a aplicação mostra.
 *  Estas mensagens de erro são as "de negócio", e não as de erros referentes a problemas técnicos como abertura de ficheiros, etc. (onde se deve usar perror)
 *  @param passo (o passo do enunciado) ... os argumentos são os mesmos que os do printf(), logo recebe uma string de formatação e depois um número variável de argumentos
 */
#define error(passo, fmt, ...) do { printf("@@Error@@ {" passo "} " fmt "\n", ## __VA_ARGS__); } while (0)

#endif

/****************************************************************************
 * FUNÇÕES UTILITÁRIAS FORNECIDAS PELOS VOSSOS QUERIDOS PROFESSORES DE SO...
 *****************************************************************************/

/******************************************************************************
 * FUNÇÕES IPC SEMÁFOROS
 *****************************************************************************/

 /**
  * @brief Função interna, não é para ser utilizada diretamente pelos alunos
  */
 int __semGet( int nrSemaforos, int semFlags ) {
    int id = semget( IPC_KEY, nrSemaforos, semFlags );
    if ( id < 0 ) {
        debug( "Não consegui criar/abrir o grupo de semáforos com key=0x%x", IPC_KEY );
    } else {
        debug( "Estou a usar o grupo de semáforos com key=0x%x e id=%d", IPC_KEY, id );
    }
    return id;
}

/**
 * @brief Cria um grupo de semáforos IPC associado a IPC_KEY com o número de semáforos passado
 * 
 * @param nrSemaforos número de semáforos deste grupo de semáforos
 * @return int em caso de sucesso, retorna o IPC_ID correspondente. Em caso de erro, retorna -1
 */
int semCreate( int nrSemaforos ) {
    return __semGet( nrSemaforos, IPC_CREAT | 0666 );
}

/**
 * @brief "Liga-se" a um grupo de semáforos IPC associado a IPC_KEY
 * 
 * @return int em caso de sucesso, retorna o IPC_ID correspondente. Em caso de erro, retorna -1
 */
int semGet() {
    return __semGet( 0, 0 );
}

/**
 * @brief Remove o grupo de semáforos IPC associado a IPC_KEY
 * 
 * @return int 0 if success, -1 if the semaphore group exists and could not be removed
 */
int semRemove() {
    int id = semGet();
    // Ignore any errors here, as this is only to check if the semaphore group exists and remove it
    if ( id > 0 ) {
        // If the semaphore group with IPC_KEY already exists, remove it.
        int result = semctl( id, 0, IPC_RMID, 0 );
        if ( result < 0) {
            debug( "Não consegui remover este grupo de semáforos" );
        } else {
            debug( "Removi este grupo de semáforos" );
        }
        return result;
    }
    return 0;
}

/**
 * @brief Define o valor do semáforo semNr do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @param semNr índice do semáforo a definir (começando em 0)
 * @param value valor a ser definido no semáforo semNr
 * @return int success
 */
int semNrSetValue( int semNr, int value ) {
    int id = semGet();
    exit_on_error( id, "Erro semget" );
    int result = semctl( id, semNr, SETVAL, value );
    if ( result < 0) {
        debug( "Não consegui definir o valor do semáforo %d deste grupo de semáforos", semNr );
    } else {
        debug( "O semáforo %d deste grupo de semáforos ficou com o valor %d", semNr, value );
    }
    return result;
}

/**
 * @brief Define o valor do semáforo 0 do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @param value valor a ser definido no semáforo 0
 * @return int success
 */
int semSetValue( int value ) {
    return semNrSetValue( 0, value );
}

/**
 * @brief Obtém o valor do semáforo semNr do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @param semNr índice do semáforo cujo valor queremos obter (começando em 0)
 * @return int valor do semáforo, ou -1 em caso de erro
 */
int semNrGetValue( int semNr ) {
    int id = semGet();
    exit_on_error( id, "Erro semget" );
    int result = semctl( id, semNr, GETVAL, 0 );
    if ( result < 0 ) {
        debug( "Não consegui obter o valor do semáforo %d deste grupo de semáforos", semNr );
    } else {
        debug( "O semáforo %d deste grupo de semáforos tem o valor %d", semNr, result );
    }
    return result;
}

/**
 * @brief Obtém o valor do semáforo 0 do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @return int valor do semáforo, ou -1 em caso de erro
 */
int semGetValue() {
    return semNrGetValue( 0 );
}

/**
 * @brief Adiciona um valor ao semáforo semNr do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @param semNr índice do semáforo a adicionar um valor (começando em 0)
 * @param addValue valor a ser adicionado no semáforo semNr
 * @return int success
 */
int semNrAddValue( int semNr, int addValue ) {
    int id = semGet();
    exit_on_error( id, "Erro semget" );
    int result = semctl( id, semNr, GETVAL, 0 );
    exit_on_error( result, "Erro semctl" );
    debug( "O semáforo %d deste grupo de semáforos tinha o valor %d", semNr, result );
  
    struct sembuf operation = { semNr, addValue, 0 };
    result = semop( id, &operation, 1 );

    if ( result < 0 ) {
        debug( "Não consegui adicionar o valor %d ao semáforo %d deste grupo de semáforos", addValue, semNr );
    } else {
        result = semctl( id, semNr, GETVAL, 0 );
        exit_on_error( result, "Erro semctl" );
        debug( "O semáforo %d deste grupo de semáforos passou a ter o valor %d", semNr, result );
    }
    return result;
}

/**
 * @brief Adiciona um valor ao semáforo 0 do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @param addValue valor a ser adicionado no semáforo 0
 * @return int success
 */
int semAddValue( int addValue ) {
    return semNrAddValue( 0, addValue );
}

/**
 * @brief Adiciona 1 ao semáforo semNr do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @param semNr índice do semáforo cujo valor queremos obter (começando em 0)
 * @return int success
 */
int semNrUp( int semNr ) {
    return semNrAddValue( semNr, 1 );
}

/**
 * @brief Adiciona -1 ao semáforo semNr do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @param semNr índice do semáforo cujo valor queremos obter (começando em 0)
 * @return int success
 */
int semNrDown( int semNr ) {
    return semNrAddValue( semNr, -1 );
}

/**
 * @brief Adiciona 1 ao semáforo 0 do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @return int success
 */
int semUp() {
    return semAddValue( 1 );
}

/**
 * @brief Adiciona -1 ao semáforo 0 do grupo de semáforos IPC associado a IPC_KEY
 * 
 * @return int success
 */
int semDown() {
    return semAddValue( -1 );
}