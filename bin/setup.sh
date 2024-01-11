#!/bin/bash

hdf_init_scp_path="${BASH_SOURCE}"
# 解析软链接，获取脚本的实际物理路径
while [ -h "$hdf_init_scp_path" ]; do
  hdf_scp_dir="$( cd -P "$( dirname "$hdf_init_scp_path" )" && pwd )"
  hdf_init_scp_path="$(readlink "$hdf_init_scp_path")"
  [[ $hdf_init_scp_path != /* ]] && hdf_init_scp_path="$hdf_scp_dir/$hdf_init_scp_path"
done
hdf_scp_dir="$( cd -P "$( dirname "$hdf_init_scp_path" )" && pwd )"
projPath="$(dirname "$hdf_scp_dir")"
# 启动脚本
output=$(python "${hdf_scp_dir}/mount.py" all "${projPath}")
status=$?
# 检查Python脚本是否成功执行
if [ $status -eq 0 ]; then
  # 如果Python脚本成功执行，那么执行它的输出
  # eval "$output"
  eval "$output"
else
  # 如果Python脚本执行失败，打印错误消息并退出
  current_date=$(date +"%Y-%m-%d")
  echo "[${current_date}]"
  echo "Python script "${scpPath}/mount.py" exited with status $status" >> err.log
  echo "$output" >> err.log
  exit $status
fi