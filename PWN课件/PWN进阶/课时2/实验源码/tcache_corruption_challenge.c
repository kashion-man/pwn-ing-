#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/epoll.h>

#include "task.h"

extern void *main_task(void *p);

int fd;

void initial()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    alarm(60);
}

void welcome()
{
    puts("Tcache Corruption");
    printf("Gift: %p\n\n", printf);
}

void menu()
{
    puts("1. add task");
    puts("2. run task");
    puts("3. exit");
    printf("Your choice: ");
}

int read_n(char *buf, int size)
{
    int result;
    result = read(STDIN_FILENO, buf, size);
    if (result <= 0)
    {
        exit(0);
    }
    return result;
}

unsigned int get_int()
{
    char buf[0x10];
    int result;
    result = read_n(buf, sizeof(buf) - 1);
    buf[result] = 0;
    return atoi(buf);
}

void add()
{
    info local;
    int wtime, size, result;

    local.option = ADD;
    printf("Time: ");
    wtime = get_int() / 1000;
    local.t.time = wtime;

    printf("Message size: ");
    size = get_int();
    if (size > 0x400)
    {
        puts("Invalid size!");
        return;
    }

    local.t.message_size = size;
    local.t.message = malloc(size);
    printf("Message: ");
    read_n(local.t.message, size);

    result = write(fd, &local, sizeof(info));
    if (result <= 0)
    {
        exit(EXIT_FAILURE);
    }

    usleep(1000);
}

void run()
{
    info local;
    int result;

    local.option = RUN;

    result = write(fd, &local, sizeof(info));
    if (result <= 0)
    {
        exit(EXIT_FAILURE);
    }
}

void task_exit()
{
    info local;
    int result;

    local.option = EXIT;

    result = write(fd, &local, sizeof(info));
    if (result <= 0)
    {
        exit(EXIT_FAILURE);
    }
}

int main()
{
    int option, result, pipe_fd[2];
    pthread_t thread_task;
    void *res;

    initial();
    welcome();

    pipe(pipe_fd);
    fd = pipe_fd[1];

    result = pthread_create(&thread_task, NULL, main_task, (void *)(size_t)pipe_fd[0]);

    if (result != 0)
    {
        handle_error_en(result, "pthread_create");
    }

    while (option != 3)
    {
        menu();
        option = get_int();
        switch (option)
        {
        case 1:
            add();
            break;
        case 2:
            run();
            break;
        case 3:
            task_exit();
            break;
        default:
            puts("Invalid choice!");
            break;
        }
        puts("");
    }

    result = pthread_join(thread_task, &res);
    if (result != 0)
    {
        handle_error_en(result, "pthread_join");
    }
    close(pipe_fd[0]);
    close(pipe_fd[1]);

    puts("Goodbye!");
}