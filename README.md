

# Hello Shell 个人脚本管理工具

## 一切的开始

作为一名程序猿，每个人都会有一些私家珍藏的脚本，来帮助完成自动化流程。但这些脚本并没有得到很好的管理，导致很多人经常重写一些常用的脚本，浪费了很多时间，最可怕的是，越是不管理的人，可能越是对脚本语言不熟悉的人，所以每次重写，也是重新学习的过程，例如我就是这样。所以，为不让我的工作效率看起来很傻，我想，我可能需要一个脚本管理工具，来方便我管理。

#### 举个例子，每次遇到，就觉得傻到爆  

`ll`  命令，常用但不是系统默认，每次重装系统或换了电脑，都要重新配置，又不是经常操作，忘的快，总不记得 alias 怎么写，就每次的问 google。 😱。

#### 满足简单的需求

1. 可以很方便地创建脚本文件，一步链接到 bin 目录
2. 提供常用的模板，工具，方便脚本开发
3. 可以方便的备份脚本到 github，与恢复脚本。



#### 这里想求大家来帮助，尽可能满足通用的要求

如果你觉得，你的脚本管理的也是一塌糊涂，并且觉得上面的需求你也有，并且更多，那么欢迎你加入到项目开发里。对没有说错，是邀请你来开发。我要承认，我的对写脚本并不是很好，只可算作初学者。所以，如果有你的加入，才能开发出一款真正有效的应用，如果你也是位初学者，也可把它当做是一次学习。



## 帮助文档 (未完待续)

### 安装

#### - 使用 npm

```shell
$ npm install helloshell -g
```



#### - 手动

```shell
$ git clone https://github.com/wl879/HelloShell.git
$ chmod 777 ./HelloShell/main.py
$ ln -s "$(pwd)/HelloShell/main.py" /usr/local/bin/helloshell
```



### 命令参数说明

#### 1. 新建脚本到仓库中

```shell
$ helloshell new name [-l [name]]
```

 新建一个脚本，目前支持 bash/python 模板，参数 `-l, --link` 设置将脚本链接到 `bin` 目录下



#### 2. 对仓库进行管理

```shell
$ helloshell repo [-d file] [-r github] [-b] [-u]
```

* `-d, --dir`           设置本地仓库路径

* `-r, --remote`     设置 github 仓库地址

* `-b, --back `         从 github 仓库恢复到本地

* `-u, --update`     更新 github 仓库

  ​



#### 3. 将脚本安装到系统环境中

```shell
$ helloshell link
```



#### 4. 读写配置文件

```shell
$ helloshell conf <file> [option [= value]] [--prefix name]
```

* `option`               输出选项变量
* `option=value`   设置并输出变量
* `p, --prefix`     设置输出变量名的前缀

**e.g.**

```shell
# 写入配置
$ helloshell conf test.ini name=wang sex=man
name="wang";
sex="man";

# 读取配置
$ helloshell conf test.ini
name="wang";
sex="man";

$ helloshell conf test.ini name
name="wang";

```



#### 5. 解析参数
```shell
$ helloshell args <file> [arguments]
```

解析参数为 shell 语法格式，以`argv_`为前缀

**e.g. **

 将下例代码保存为 `test.sh` 文件,  读取 `<file>` 中以 "# HELP DOCUMENT" 为开始的注释段落

```shell
#!/bin/sh
# HELP DOCUMENT
#
# 参数:
#	-t, --text string	示例
#	-h, --help			查看帮助
#

eval "$(helloshell args $0 $*)"
if [ $? != 0 ]; then
	echo "Argument Error:"
	echo $argv_errors
	exit 1
fi
if [ $argv_help ]; then
	echo "${help_document}"
	exit 1
fi
if [ $argv_text ]; then
	echo $argv_text
fi
```

运行结果如下：

```shell
$ test.sh --help

 参数:
    -t, --text string    示例
    -h, --help            查看帮助
    
```

```shell
$ test.sh -t "haha"
haha
```



#### 6. 彩色输出

```shell
$ helloshell echo "#r[abcd]"

$ echo "#b[abcd]" | helloshell
```

`#r[]` = 红色 / `#g[]` = 绿色 / `#b[]` = 蓝色 / `#c[]` = 蓝绿色 / `#d[]` = 灰色 / `#w[]` = 白色



## 功能设计 (未完待续)

* 管理功能
  - [x] 程序配置
  - [x] shell 仓库配置
        - [x] 设置仓库目录
        - [x] 设置 github 
  - [ ] 新建脚本文件
        - [x] bash    模板支持
        - [x] python 模板支持
        - [ ] nodejs 模板支持
        - [ ] ruby     模板支持
  - [ ] 支持 alias，
        - [ ] 添加
        - [ ] 还原
  - [ ] 备份仓库到 github
        - [x] master 分支，用户提交
        - [ ] history 分支，自动提交
        - [ ] 支持单独脚本提交与恢复
        - [ ] 对各种冲突处理
  - [ ] 链接脚本
        - [ ] 创建自己的环境变量
        - [x] 链接到 bin 目录*（当前版本是链接到 helloshell 命令同目录下）*
              - [ ] 生成日志文件，用与回复配置
        - [ ] 支持解析 nodejs package.json
  - [ ] 提示更新
  - [ ] 支持多平台 （目前只支持 mac os）



* 工具
  - [x] `helloshell args` 参数解析
        - [ ] 以 command 传入字符串参数时，空格会被拆分 bug
  - [ ] `helloshell conf` 生成与读写配置文件
        - [x] 支持 .ini 文件格式
        - [ ] 支持 .yml 文件格式
  - [ ] `helloshell echo` 格式化输出
        - [x] 支持 color 标签
        - [ ] 进度条输出




