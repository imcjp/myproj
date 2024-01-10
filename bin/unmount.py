import yaml
import sys
import os
# 获取当前脚本的完整路径
script_path = os.path.realpath(__file__)
# 获取当前脚本所在的目录
script_dir = os.path.dirname(script_path)

# 检查是否有足够的命令行参数
if len(sys.argv) != 3:
    print("Usage: python unmount.py [name] [proj_dir]")
    sys.exit(1)

# 读取参数
name = sys.argv[1]
proj_dir = sys.argv[2] if len(sys.argv) > 2 else "."  # 如果没有提供第二个参数，则使用假设的环境变量

# 读取 YAML 文件内容
with open(f'{script_dir}/mountLs.yaml', 'r') as file:
    data = yaml.safe_load(file)

# 检查 name 是否在 fs 标签下
if name not in data['fs']:
    print(f"The name '{name}' is not a valid key under 'fs'.")
    sys.exit(1)

# 获取配置选项
option = data['option']
method = option['method']
workspace_dir = option['workspaceDir']

# 生成卸载命令
if method == "unionFs":
    unmount_cmd = f"fusermount -u \"{proj_dir}/{workspace_dir}/{name}\""
elif method == "overlayFS":
    unmount_cmd = f"sudo umount \"{proj_dir}/{workspace_dir}/{name}\""
else:
    print(f"Unsupported method: {method}")
    sys.exit(1)

# 输出卸载命令
print(unmount_cmd)
