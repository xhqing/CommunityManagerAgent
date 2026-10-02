#!/usr/bin/env bash
# tap.sh —— 拖拽式点击（真实鼠标事件，会移动用户鼠标指针）
#
# 用法：./tap.sh <截图x> <截图y> [偏移像素，默认 2]
#   ./tap.sh 1210 45      # 点主窗口「···」
#   ./tap.sh 200 168 0    # 偏移 0：down/up 同点，更接近"纯点击"
#
# 什么时候用它（而不是 clic.sh）：
#   click 工具走「无障碍元素优先」的路径——遇到微信自绘控件时，工具可能在
#   窗口层面就"点成功了"（实际什么都没发生），永远轮不到真实鼠标事件。
#   drag 路径（本脚本）在开启全局指针兜底后**直接发真实鼠标事件**，能穿过去。
#
# 副作用与注意：
#   - 会移动用户的真实鼠标指针（微信窗口会被 raise 到前台），用户如果在用电脑会看到
#   - 有些控件会把连续的拖拽事件判成"拖拽"而不是"点击"，那样按钮不会响应——
#     这时改用偏移 0（./tap.sh x y 0）再试；还不行就换 clic.sh
set -u

if [ $# -lt 2 ]; then
  echo "用法：$0 <截图x> <截图y> [偏移像素=2]"
  exit 1
fi

X="$1"; Y="$2"; OFF="${3:-2}"
X2=$((X + OFF)); Y2=$((Y + OFF))

# 全局指针兜底开关：没有它，click/drag 在无障碍路径失败时只会报错，不会真点击
OPEN_COMPUTER_USE_ALLOW_GLOBAL_POINTER_FALLBACKS=1 \
  open-computer-use call drag \
  --args "{\"app\":\"${WX_APP:-WeChat}\",\"from_x\":$X,\"from_y\":$Y,\"to_x\":$X2,\"to_y\":$Y2}" \
  >/dev/null 2>&1

echo "已点击 ($X, $Y)（偏移 $OFF）"
