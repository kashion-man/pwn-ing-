#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/epoll.h>
#include <time.h>

#include "task.h"

#define MAX_TASK 0x10
task *global_task[MAX_TASK];

typedef struct task_queue
{
    int index;
    int time;
    task *t;
    struct task_queue *next;
} task_queue;

void *main_task(void *p)
{
    int epoll_fd, pipe_fd, option = UNUSED, result, wtime, index, i, is_run;
    info local;
    struct epoll_event ev;
    struct epoll_event evs[1];
    task_queue *queue = NULL, *temp, *tail;

    time_t pre, diff;

    pipe_fd = (int)(size_t)p;
    epoll_fd = epoll_create(1);

    ev.events = EPOLLIN | EPOLLET;
    ev.data.fd = pipe_fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, pipe_fd, &ev);

    wtime = NO_TASK;
    is_run = 0;

    while (option != EXIT)
    {
        if (is_run == 1)
        {
            if (queue == NULL)
            {
                is_run = 0;
                wtime = NO_TASK;
            }
            else
            {
                wtime = queue->time;
            }
        }

        pre = time(NULL);
        result = epoll_wait(epoll_fd, evs, 1, wtime);
        diff = time(NULL) - pre;

        if (result < 0)
        {
            exit(EXIT_FAILURE);
        }
        else if (result == 1)
        {
            if (is_run == 1)
            {
                queue->time -= diff;
            }

            read(pipe_fd, &local, sizeof(info));
            option = local.option;
            switch (option)
            {
            case ADD:
                index = -1;
                for (i = 0; i < MAX_TASK; i++)
                {
                    if (!global_task[i])
                    {
                        index = i;
                        break;
                    }
                }
                if (index == -1)
                {
                    exit(EXIT_FAILURE);
                }

                global_task[index] = malloc(sizeof(task));
                global_task[index]->time = local.t.time;
                global_task[index]->message = malloc(local.t.message_size);
                memcpy(global_task[index]->message, local.t.message, local.t.message_size);
                global_task[index]->message_size = local.t.message_size;

                break;
            case RUN:
                is_run = 1;
                for (i = 0; i < MAX_TASK; i++)
                {
                    if (global_task[i])
                    {
                        temp = malloc(sizeof(task_queue));
                        temp->next = NULL;
                        temp->index = i;
                        temp->time = global_task[i]->time;
                        temp->t = global_task[i];

                        if (queue == NULL)
                        {
                            queue = temp;
                        }
                        else
                        {
                            tail = queue;
                            while (tail->next != NULL)
                            {
                                tail = tail->next;
                            }
                            tail->next = temp;
                        }
                    }
                }
                break;
            case EXIT:
                break;
            default:
                exit(EXIT_FAILURE);
            }
        }
        else if (result == 0)
        {
            temp = queue;
            queue = queue->next;
            free(temp->t->message);
            free(global_task[temp->index]);
            global_task[temp->index] = NULL;
            free(temp);
        }
    }
}