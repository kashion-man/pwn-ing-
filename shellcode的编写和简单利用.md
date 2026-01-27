## 一、shellcode的介绍

![image-20260125111632427](./assets/image-20260125111632427.png)

## 二、shellcode的编写

![image-20260125111806790](./assets/image-20260125111806790.png)

### 32位系统shellcode编写

![image-20260125111922068](./assets/image-20260125111922068.png)

![image-20260125112038419](./assets/image-20260125112038419.png)

### 64位系统shellcode编写

![image-20260125112247063](./assets/image-20260125112247063.png)

### pwntools内模块编写shellcode（默认生成32位）

![image-20260125112418064](./assets/image-20260125112418064.png)

## 三、shellcode的利用（ret2shellcode攻击方法）

![image-20260125112541397](./assets/image-20260125112541397.png)

**即NX防御关闭，内存中存在可读可写的段**

**rwx为可读可写可执行**

