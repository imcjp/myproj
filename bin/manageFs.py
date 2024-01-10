import yaml
import sys
import os
# 获取当前脚本的完整路径
script_path = os.path.realpath(__file__)
# 获取当前脚本所在的目录
script_dir = os.path.dirname(script_path)

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def save_yaml(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

def add_entry(data, name, dirs):
    if name in data['fs']:
        return f"条目 '{name}' 已经存在。"
    data['fs'][name] = [f"{dir}" for  dir in dirs.split(',')]
    return f"条目 '{name}' 已成功添加。"

def remove_entry(data, name):
    if name not in data['fs']:
        return f"条目 '{name}' 不存在。"
    del data['fs'][name]
    if name in data['option']['enable']:
        data['option']['enable'].remove(name)
        return f"条目 '{name}' 及其启用状态已成功删除。"
    return f"条目 '{name}' 已成功删除。"

def enable_entry(data, name):
    if name in data['fs'] and name not in data['option']['enable']:
        data['option']['enable'].append(name)
        return f"条目 '{name}' 已成功启用。"
    return f"条目 '{name}' 不存在或已经启用。"

def disable_entry(data, name):
    if name in data['option']['enable']:
        data['option']['enable'].remove(name)
        return f"条目 '{name}' 已成功禁用。"
    return f"条目 '{name}' 当前未启用或不存在。"

def change_method(data, name):
    if name in data['option']['availMethods']:
        data['option']['method'] = name
        return f"方法已成功更改为 '{name}'。"
    return f"方法 '{name}' 不可用。"

def list_entries(data):
    entries = []
    entries.append(f"当前使用的挂载方法是{data['option']['method']}，挂载项目为如下{len(data['fs'].items())}项，小括号内代表可写层：")
    for name, dirs in data['fs'].items():
        entry = f"    {name}:\t" + ",".join(f"[{i}]{dir}" for i, dir in enumerate(dirs[:-1])) + f",([{len(dirs) - 1}]{dirs[-1]})"
        if name in data['option']['enable']:
            entry += "\t[enable]"
        entries.append(entry)
    return "\n".join(entries)

def main():
    file_path = f'{script_dir}/mountLs.yaml'
    if len(sys.argv) == 1:
        data = load_yaml(file_path)
        print(list_entries(data))
        return

    if len(sys.argv) < 2:
        print("参数不足。使用 '-h' 查看帮助。")
        sys.exit(1)

    command = sys.argv[1]

    if command == '-h':
        print_help()
        return

    name = sys.argv[2]
    dirs = sys.argv[3] if len(sys.argv) > 3 else None

    data = load_yaml(file_path)

    feedback = "无效指令。使用 '-h' 查看帮助。"
    if command == 'add' and dirs:
        feedback = add_entry(data, name, dirs)
    elif command == 'rm':
        feedback = remove_entry(data, name)
    elif command == 'enable':
        feedback = enable_entry(data, name)
    elif command == 'disable':
        feedback = disable_entry(data, name)
    elif command == 'method':
        feedback = change_method(data, name)

    if "已成功" in feedback:
        save_yaml(file_path, data)

    print(feedback)

def print_help():
    help_text = """
用法: python manageFs.py [指令] [参数]

指令:
  (无指令)        列出所有条目
  -h              显示帮助信息
  add [name] [dirs]  添加一个新的条目，dirs 为逗号分隔的目录列表
  rm [name]          删除一个存在的条目
  enable [name]      启用一个条目
  disable [name]     禁用一个条目
  method [name]      更改挂载方法，name 必须在可用方法列表中

例子:
  python script.py
  python script.py add myconfig dir1,dir2,dir3
  python script.py rm myconfig
  python script.py enable myconfig
  python script.py disable myconfig
  python script.py method unionFs
"""
    print(help_text)

if __name__ == "__main__":
    main()
