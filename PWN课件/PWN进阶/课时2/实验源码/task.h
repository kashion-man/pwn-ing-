#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define MAXEPOLL 0x10

typedef struct task
{
    int time;
    int message_size;
    char *message;
} task;

typedef struct info
{
    int option;
    struct task t;
} info;

void *main_task(void *p);

// Option
#define ADD 0
#define RUN 1
#define EXIT 2
#define UNUSED -1

#define NO_TASK -1

#define handle_error_en(en, msg) \
    do                           \
    {                            \
        errno = en;              \
        perror(msg);             \
        exit(EXIT_FAILURE);      \
    } while (0)

#define handle_error(msg)   \
    do                      \
    {                       \
        perror(msg);        \
        exit(EXIT_FAILURE); \
    } while (0)
