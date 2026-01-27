C_FLAGS = -O0
normal: hello_world.c
	gcc $(CC_FLAGS) ./hello_world.c -o hello_world

preprocess: hello_world.c
	gcc $(CC_FLAGS) -E ./hello_world.c -o hello_world.i

compile: hello_world.i
	gcc $(CC_FLAGS) -S ./hello_world.i -o hello_world.s

assembly: hello_world.s
	gcc $(CC_FLAGS) -c ./hello_world.s -o hello_world.o

link: hello_world.o
	gcc $(CC_FLAGS) ./hello_world.o -o hello_world

temps: hello_world.c
	gcc -save-temps $(CC_FLAGS) ./hello_world.c -o hello_world