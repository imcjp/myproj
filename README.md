## 层次开发框架（Hierarchical Development Framework，HDF），用于科学地开发项目

部署命令如下：

curl -s https://raw.githubusercontent.com/imcjp/myproj/main/bin/setup.sh | bash -s -- [name]

其中[name]为所要部署的项目名称若为空，则默认为myproj

部署后的配置，设部署后的路径为path=[absPath]/[name]：

1. 配置到当前交互式会话环境，配置后可以使用 **hdf** 命令。将如下命令添加到home目录下的.bashrc文件中即可：
   
   source [absPath]/[name]/bin/init_env.sh
   
3. 配置开机自启动。将如下命令添加到/etc/rc.local文件中即可：
   
   [absPath]/[name]/bin/startup.sh
