#!/bin/bash

hdf_init_scp_path="${BASH_SOURCE}"
# 解析软链接，获取脚本的实际物理路径
while [ -h "$hdf_init_scp_path" ]; do
  hdf_scp_dir="$( cd -P "$( dirname "$hdf_init_scp_path" )" && pwd )"
  hdf_init_scp_path="$(readlink "$hdf_init_scp_path")"
  [[ $hdf_init_scp_path != /* ]] && hdf_init_scp_path="$hdf_scp_dir/$hdf_init_scp_path"
done
export hdf_scp_dir="$( cd -P "$( dirname "$hdf_init_scp_path" )" && pwd )"
#“层次开发框架”翻译为 "Hierarchical Development Framework"，缩写为 "HDF"。
hdf() {
  if [ "$1" = "cd" ]; then
    cd $($hdf_scp_dir/main "$@")
  else
    $hdf_scp_dir/main "$@"
  fi
}


