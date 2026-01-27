/**
 * Author: Ex
 * Time: 2020-02-15
 * Email: 2462148389@qq.com
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>
#include <unistd.h>
#include <signal.h>

#define LENGTH 0x10
char *ptr[LENGTH];
int ptr_size[LENGTH];
unsigned int is_used[LENGTH];

char *heap_addr;

#define USED 1
#define UNUSED 0

void initial()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    alarm(60);
    heap_addr = malloc(0x18);
}

void welcome()
{
    puts("Heap Challenge - House of Orange");
}

void menu()
{
    puts("1. add");
    puts("2. delete");
    puts("3. show");
    puts("4. exit");
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
    unsigned int size, index = -1, i, result;
    for (i = 0; i < LENGTH; i++)
    {
        if (!ptr[i])
        {
            index = i;
            break;
        }
    }
    if (index == -1)
    {
        puts("Out of space!");
        return;
    }

    printf("Size: ");
    size = get_int();
    if (size > 0x3ff)
    {
        puts("Invalid size!");
        return;
    }

    ptr[index] = malloc(size + 1);
    if(ptr[index] < heap_addr || ptr[index] > heap_addr + 0x21000)
    {
        puts("Invalid address!");
        exit(EXIT_FAILURE);
    }
    printf("Content: ");
    result = read_n(ptr[index], size);
    if (ptr[index][result - 1] == '\n')
    {
        ptr[index][result - 1] = '\0';
    }
    else
    {
        ptr[index][result] = '\0';
    }
    is_used[index] = USED;
}

void delete ()
{
    unsigned int index = -1;
    printf("Index: ");
    index = get_int();
    if (index >= LENGTH || !ptr[index])
    {
        puts("Invalid index!");
        return;
    }
    free(ptr[index]);
    is_used[index] = UNUSED;
}

void show()
{
    unsigned int index = -1;
    printf("Index: ");
    index = get_int();
    if (index < LENGTH && ptr[index] && is_used[index] == USED)
    {
        printf("Content: %s\n", ptr[index]);
    }
    else
    {
        puts("Invalid index!");
    }
}

int main()
{
    unsigned int option = 0;
    initial();
    welcome();

    while (option != 4)
    {
        menu();
        option = get_int();
        switch (option)
        {
        case 1:
            add();
            break;
        case 2:
            delete ();
            break;
        case 3:
            show();
            break;
        case 4:
            break;
        default:
            puts("Invalid choice!");
            break;
        }
        puts("");
    }

    puts("Goodbye!");

    return 0;
}
