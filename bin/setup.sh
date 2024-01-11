#!/bin/bash

# 接收的参数为目标文件夹的名称
name=${1:-myproj}

# GitHub仓库地址
repo_url="https://github.com/imcjp/myproj.git"

# 克隆GitHub仓库到指定的$name文件夹
git clone $repo_url $name

# 检查git clone命令是否成功执行
if [ $? -ne 0 ]; then
    echo "Git克隆失败。请检查仓库是否存在以及你是否可以访问互联网。"
    exit 1
fi

# 进入克隆的仓库目录
cd $name

# 创建所需的子文件夹
mkdir -p ws tmp projStk/{0source,1env,2dev,3run}

# 进入ws文件夹
cd ws

# 再次创建子文件夹
mkdir -p build dev run

# 回到$name文件夹
cd ..


# 设置bin目录下的脚本为可执行
# 假设bin目录在仓库的根目录下
if [ -d "bin" ]; then
  chmod +x bin/main bin/init_env.sh bin/startup.sh
  echo "仓库已克隆，目录已创建，脚本已设置为可执行，全部操作成功完成。"
  echo "请手动将 'source $(pwd)/bin/init_env.sh' 添加到home目录下的.bashrc文件中并重新连接，以便可以使用 'hdf' 命令"
  echo "请手动将 '$(pwd)/bin/startup.sh' 添加到自启动项，以便开机时挂载目录"
else
  echo "bin目录不存在。"
fi


# 脚本结束
