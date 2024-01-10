import yaml
import sys
import os
# 获取当前脚本的完整路径
script_path = os.path.realpath(__file__)
# 获取当前脚本所在的目录
script_dir = os.path.dirname(script_path)
# 检查是否有至少一个命令行参数
# print(f'name={sys.argv[1]}')
if len(sys.argv) < 2:
    print("Usage: python mount.py [name|*] [proj_dir]")
    sys.exit(1)

# 读取参数
name = sys.argv[1]
proj_dir = sys.argv[2] if len(sys.argv) > 2 else "."  # 如果没有提供第二个参数，则使用假设的环境变量

# 读取 YAML 文件内容
with open(f'{script_dir}/mountLs.yaml', 'r') as file:
    data = yaml.safe_load(file)

# 获取配置选项
option = data['option']
method = option['method']
source_dir = option['sourceDir']
workspace_dir = option['workspaceDir']
tmp_dir = option['tmpDir']

# 定义生成挂载命令的函数
def generate_mount_cmd(fs_key, proj_directory):
    if method == "unionFs":
        layers = data['fs'][fs_key]
        layers = reversed(layers)  # UnionFS 需要倒序，最上层的目录在最前面
        layers_paths = ":".join([f'"{proj_directory}/{source_dir}/{layer}"=RO' for layer in layers])
        # 最上层的目录需要读写权限
        layers_paths = layers_paths.replace('=RO', '=RW', 1)
        return f"unionfs-fuse -o cow,allow_other {layers_paths} \"{proj_directory}/{workspace_dir}/{fs_key}\""
    elif method == "overlayFS":
        lower_dirs = ":".join(reversed([f'"{proj_directory}/{source_dir}/{layer}"' for layer in data['fs'][fs_key][:-1]]))
        upper_dir = f'"{proj_directory}/{source_dir}/{data["fs"][fs_key][-1]}"'
        return (f"sudo mount -t overlay overlay -o "
                 f"lowerdir={lower_dirs},upperdir={upper_dir},workdir=\"{proj_directory}/{tmp_dir}\" "
                 f"\"{proj_directory}/{workspace_dir}/{fs_key}\"")
    else:
        raise ValueError(f"Unsupported method: {method}")

# 根据输入参数生成命令
if name == 'all':
    # 如果参数是 'all'，生成所有有效命令
    for fs_key in option['enable']:
        if fs_key in data['fs']:
            print(generate_mount_cmd(fs_key, proj_dir))
else:
    # 否则，只生成指定参数的命令
    if name not in data['fs']:
        print(f"The name '{name}' is not a valid key under 'fs'.")
        sys.exit(1)
    print(generate_mount_cmd(name, proj_dir))
