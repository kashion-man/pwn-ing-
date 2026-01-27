### 一、文件操作（最常用）

|    指令     |           功能描述            |          基础用法           |                     示例                     |
| :---------: | :---------------------------: | :-------------------------: | :------------------------------------------: |
|    `ls`     |   列出目录下的文件 / 文件夹   |     `ls [选项] [目录]`      | `ls -l`（详细列表）、`ls -a`（显示隐藏文件） |
|   `touch`   |  创建空文件或修改文件时间戳   |       `touch 文件名`        |    `touch test.py`（创建空 Python 文件）     |
|    `cat`    |  查看文件内容（适合小文件）   |        `cat 文件名`         |      `cat /etc/passwd`（查看用户配置）       |
| `more/less` |  分页查看文件（适合大文件）   | `more 文件名`/`less 文件名` |    `less /var/log/syslog`（日志文件分页）    |
| `head/tail` |    查看文件开头 / 结尾内容    |    `head -n 行数 文件名`    |      `tail -f app.log`（实时监控日志）       |
|    `cp`     |       复制文件 / 文件夹       |     `cp [选项] 源 目标`     |    `cp test.py ~/Desktop/`（复制到桌面）     |
|    `mv`     |  移动文件 / 文件夹 或 重命名  |        `mv 源 目标`         |        `mv old.txt new.txt`（重命名）        |
|    `rm`     | 删除文件 / 文件夹（谨慎使用） |     `rm [选项] 文件名`      |    `rm -rf temp/`（强制删除文件夹及内容）    |
|    `vim`    |    编辑文件（终端编辑器）     |        `vim 文件名`         |      `vim config.conf`（编辑配置文件）       |
|   `chmod`   |         修改文件权限          |     `chmod 权限 文件名`     |      `chmod +x run.sh`（添加执行权限）       |

### 二、目录操作

|  指令   |             功能描述             |        基础用法         |                    示例                     |
| :-----: | :------------------------------: | :---------------------: | :-----------------------------------------: |
|  `pwd`  |       显示当前所在目录路径       |          `pwd`          |         `pwd`（输出：`/home/user`）         |
|  `cd`   |             切换目录             |      `cd 目录路径`      | `cd ..`（返回上一级）、`cd ~`（回到家目录） |
| `mkdir` |            创建文件夹            | `mkdir [选项] 文件夹名` |  `mkdir -p src/utils`（递归创建多级目录）   |
| `rmdir` |     删除空文件夹（仅空目录）     |    `rmdir 文件夹名`     |             `rmdir empty_dir/`              |
| `tree`  | 以树形结构显示目录内容（需安装） |      `tree [目录]`      |    `tree ~/project/`（查看项目目录结构）    |

### 三、系统管理与进程操作

|    指令    |          功能描述          |        基础用法         |                     示例                      |                                  |
| :--------: | :------------------------: | :---------------------: | :-------------------------------------------: | :------------------------------: |
|   `sudo`   |    以管理员权限执行命令    |       `sudo 指令`       |        `sudo apt update`（更新软件源）        |                                  |
|   `top`    | 实时查看系统进程和资源占用 |          `top`          |           按 `q` 退出，`k` 终止进程           |                                  |
|    `ps`    |      查看当前用户进程      |       `ps [选项]`       |       `ps aux`（查看所有进程）、`ps -ef       | grep python`（查找 Python 进程） |
|   `kill`   |          终止进程          |  `kill [信号] 进程ID`   | `kill -9 1234`（强制终止 PID 为 1234 的进程） |                                  |
|    `df`    |    查看磁盘空间使用情况    | `df -h`（人类可读格式） |         `df -h`（显示各分区剩余空间）         |                                  |
|    `du`    |    查看目录 / 文件大小     |      `du -sh 目录`      |  `du -sh ~/Downloads/`（查看下载文件夹大小）  |                                  |
|   `free`   |      查看内存使用情况      |        `free -h`        |     `free -h`（显示内存 / 交换分区使用）      |                                  |
|  `reboot`  |    重启系统（需 sudo）     |      `sudo reboot`      |                                               |                                  |
| `shutdown` |    关闭系统（需 sudo）     | `sudo shutdown -h now`  |                   立即关机                    |                                  |

### 四、用户与权限管理

|   指令    |       功能描述        |           基础用法            |                       示例                       |
| :-------: | :-------------------: | :---------------------------: | :----------------------------------------------: |
| `whoami`  |  显示当前登录用户名   |           `whoami`            |                   输出：`user`                   |
| `useradd` | 创建新用户（需 sudo） |   `sudo useradd -m 用户名`    | `sudo useradd -m testuser`（创建带家目录的用户） |
| `passwd`  |     修改用户密码      |        `passwd 用户名`        |     `passwd testuser`（修改 testuser 密码）      |
| `userdel` |  删除用户（需 sudo）  |   `sudo userdel -r 用户名`    |  `sudo userdel -r testuser`（删除用户及家目录）  |
|   `su`    |       切换用户        |         `su - 用户名`         |         `su - root`（切换到 root 用户）          |
|  `chown`  | 修改文件 / 目录所有者 | `sudo chown 用户名:组名 目标` | `sudo chown user:user test.py`（修改文件所有者） |
| `groups`  |  查看当前用户所属组   |           `groups`            |    输出：`user sudo`（属于 user 和 sudo 组）     |

### 五、网络操作

|    指令    |               功能描述               |       基础用法        |                     示例                     |
| :--------: | :----------------------------------: | :-------------------: | :------------------------------------------: |
|   `ping`   |            测试网络连通性            |  `ping 目标IP/域名`   |      `ping baidu.com`（测试百度连通性）      |
| `ifconfig` | 查看网络接口信息（需安装 net-tools） |      `ifconfig`       |            显示 IP 地址、网卡信息            |
|    `ip`    |     替代 ifconfig 的网络管理工具     | `ip addr`（查看 IP）  |           `ip route`（查看路由表）           |
|   `curl`   |      发送 HTTP 请求 / 下载文件       |  `curl [选项] 网址`   | `curl https://www.baidu.com`（获取百度首页） |
|   `wget`   |       下载文件（支持断点续传）       |    `wget 下载链接`    |     `wget https://github.com/xxx.tar.gz`     |
| `netstat`  | 查看网络连接状态（需安装 net-tools） |    `netstat -tuln`    |           查看监听的 TCP/UDP 端口            |
|   `ssh`    |        远程登录 Linux 服务器         | `ssh 用户名@服务器IP` |           `ssh user@192.168.1.100`           |

### 六、文件搜索与查找

|   指令    |           功能描述           |          基础用法           |                         示例                          |
| :-------: | :--------------------------: | :-------------------------: | :---------------------------------------------------: |
|  `find`   | 按路径 / 名称 / 类型查找文件 |  `find 路径 -name 文件名`   | `find ~ -name "*.py"`（查找家目录下所有 Python 文件） |
|  `grep`   |   搜索文件内容（文本匹配）   | `grep [选项] 关键词 文件名` |   `grep "import" test.py`（查找文件中 import 语句）   |
|  `which`  |      查找指令的执行路径      |        `which 指令`         |      `which python3`（输出：`/usr/bin/python3`）      |
| `whereis` |   查找指令 / 配置文件路径    |        `whereis vim`        |            显示 vim 的执行文件、手册页路径            |

### 七、软件包管理（Ubuntu/Debian 系统）

|       指令       |         功能描述          |         基础用法          |                  示例                   |
| :--------------: | :-----------------------: | :-----------------------: | :-------------------------------------: |
|   `apt update`   | 更新软件源列表（需 sudo） |     `sudo apt update`     |           更新可用软件包信息            |
|  `apt install`   |    安装软件（需 sudo）    | `sudo apt install 软件名` |   `sudo apt install git`（安装 Git）    |
|   `apt remove`   |    卸载软件（需 sudo）    | `sudo apt remove 软件名`  |    `sudo apt remove vim`（卸载 Vim）    |
| `apt autoremove` |  清理无用依赖（需 sudo）  |   `sudo apt autoremove`   |          删除不再需要的依赖包           |
|   `apt search`   |        搜索软件包         |    `apt search 软件名`    | `apt search python3-pip`（搜索 pip 包） |

### 八、压缩与解压

|  指令   |            功能描述             |           基础用法            |                       示例                        |
| :-----: | :-----------------------------: | :---------------------------: | :-----------------------------------------------: |
|  `tar`  | 打包 / 解压 tar.gz/tar.bz2 文件 |   解压：`tar -zxvf 压缩包`    |     `tar -zxvf project.tar.gz`（解压 tar.gz）     |
|         |                                 | 打包：`tar -zcvf 压缩包 目录` | `tar -zcvf docs.tar.gz docs/`（打包 docs 文件夹） |
| `unzip` |     解压 zip 文件（需安装）     |      `unzip 压缩包.zip`       |                 `unzip test.zip`                  |
|  `zip`  |     打包 zip 文件（需安装）     |  `zip 压缩包.zip 文件/目录`   |        `zip files.zip file1.txt file2.py`         |

### 新手必备小技巧

1. **指令补全**：按 `Tab` 键自动补全文件名、目录名、指令（减少输入错误）；
2. **历史指令**：按 `↑`/`↓` 键查看之前执行过的指令，或用 `history` 命令查看所有历史；
3. **帮助文档**：任何指令后加 `--help` 查看用法（如 `ls --help`），或用 `man 指令` 看详细手册（如 `man cp`）；
4. **管道符 `|`**：将前一个指令的输出作为后一个指令的输入，例如 `ls -l | grep ".py"`（筛选 Python 文件）；
5. **通配符 `\*`**：匹配任意字符，例如 `rm *.log`（删除所有.log 文件）。