#!/usr/bin/env bash
# clic.sh —— 真点击（open-computer-use 的 click 工具 + 全局指针兜底）
#
# 用法：./clic.sh <截图x> <截图y>
#
# 与 tap.sh 的区别：
#   - 本脚本发的是 down/up（中间没有拖拽位移），是"纯点击"，适合对拖拽敏感的按钮
#   - 但如果目标控件在无障碍树里能被"点中"，工具会走无障碍路径、根本不发鼠标事件
#     （表现：鼠标不动、界面没反应）——这时换 tap.sh
#   - 反过来，tap.sh 的连续拖拽事件有时会被判成拖拽而点不中按钮——这时换本脚本
#   一句话：**两个都试**，以截图上出现预期变化为准。
set -u

if [ $# -lt 2 ]; then
  echo "用法：$0 <截图x> <截图y>"
  exit 1
fi

OPEN_COMPUTER_USE_ALLOW_GLOBAL_POINTER_FALLBACKS=1 \
  open-computer-use call click \
  --args "{\"app\":\"${WX_APP:-WeChat}\",\"x\":$1,\"y\":$2}" \
  >/dev/null 2>&1

echo "已点击 ($1, $2)"
