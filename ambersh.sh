#!/bin/bash

last_dir=""
while :; do
  echo "amber懒人脚本by damin"
  echo "请输入运行目录（为空则默认上次目录）："
  read -p "目录： " dir
  if [ -z "$dir" ]; then
    if [ -f "last_dir.txt" ]; then
      dir=$(cat last_dir.txt)
    else
      echo "未检测到历史目录，请先指定目录！"
      continue
    fi
  fi
  echo "$dir" > last_dir.txt
  echo "请选择操作："
  echo "0. 下载并解压模型"
  echo "1. 运行模拟"
  echo "2. 继续模拟"
  echo "3. 退出"
  echo "4. 杀死GPU上的amber进程"
  read -p "请输入选项： " option

  case $option in
    0)
      wget https://s3.tebi.io/s3.ag.cn.eu.org/model.zip -O model.zip
      unzip model.zip -d "$dir"
      echo "模型已下载并解压至 $dir"
      ;;
    1)
      echo "请输入模拟运行的段数："
      read -p "段数： " num
      echo "请输入运行模拟的显卡号："
      read -p "显卡号： " gpu_id
      python3 "$dir/2.py" -n $num
      cp amber.sh $dir
      chmod +x "$dir/amber.sh"
      cd $dir
      CUDA_VISIBLE_DEVICES=$gpu_id bash "$dir/amber.sh" > "$dir/amber.log" 2>&1 &
      disown
      nvidia-smi
      ;;
    2)
      echo "请输入模拟的开始段数："
      read -p "开始段数： " start1
      echo "请输入运行的段数："
      read -p "运行段数： " num1
      echo "请输入运行模拟的显卡号："
      read -p "显卡号： " gpu_id
      python3 "$dir/3.py" -s $start1 -n $num1
      cp amber.sh $dir
      chmod +x "$dir/amber.sh"
      cd $dir
      CUDA_VISIBLE_DEVICES=$gpu_id bash "$dir/amber.sh" > "$dir/amber.log" 2>&1 &
      disown
      nvidia-smi
      ;;
    3)
      echo "退出程序..."
      exit 0
      ;;
    4)
      wget https://s3.tebi.io/s3.ag.cn.eu.org/kill_amber.sh -O kill_amber.sh
      chmod +x kill_amber.sh
      echo "请输入要杀死的GPU号："
      read -p "GPU号： " gpu_id
      bash kill_amber.sh $gpu_id
      ;;
    *)
      echo "无效选项，请重新输入！"
      ;;
  esac
done


