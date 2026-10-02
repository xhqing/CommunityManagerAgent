#!/usr/bin/env bash
# ocu.sh —— open-computer-use 调用封装（微信操作用）
#
# 用法：
#   ./ocu.sh get_app_state '{"app":"WeChat"}'   # 打印无障碍元素树 + 保存截图
#   ./ocu.sh <任意工具> '<json 参数>'            # 透传调用，同样保存截图（若返回图片）
#   OUT_PNG=/path/shot.png ./ocu.sh ...          # 自定义截图输出路径
#
# 为什么这么做：微信 Mac 4.x 的界面是自绘的，无障碍元素树里只有窗口框架，
# 真正能用的信息在**截图**里（人眼看图定位坐标）。所以这个脚本的作用就是
# 「一次调用 = 一份元素树 + 一张截图」，后续点击坐标都从这张截图里量。
#
# 截图默认落在 $WX_OPS_DIR（默认 /tmp/wx-ops）——**里面可能有群成员头像、
# 聊天内容等隐私，收尾时记得删掉**，不要放进会被 git 跟踪的目录。
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
DIR="${WX_OPS_DIR:-/tmp/wx-ops}"
mkdir -p "$DIR"
PNG="${OUT_PNG:-$DIR/ocu-shot.png}"
RAW="$DIR/ocu-raw.json"
ERR="$DIR/ocu-err.txt"

if [ $# -eq 0 ]; then
  echo "用法：$0 <tool> '<json-args>'   （例：$0 get_app_state '{\"app\":\"WeChat\"}'）"
  exit 1
fi

tool="$1"
args="${2:-\{\}}"

if ! command -v open-computer-use >/dev/null 2>&1; then
  echo "[错误] 找不到 open-computer-use —— 先安装（npm i -g @qwen-code/open-computer-use），"
  echo "       并用 'open-computer-use doctor' 确认辅助功能 / 屏幕录制权限已授权。"
  exit 1
fi

open-computer-use call "$tool" --args "$args" >"$RAW" 2>"$ERR" || {
  echo "[调用失败] $(head -5 "$ERR" 2>/dev/null)"
  head -c 400 "$RAW" 2>/dev/null
  exit 1
}

python3 - "$RAW" "$PNG" <<'PY'
import base64, json, sys
raw_path, png_path = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(raw_path, encoding='utf-8'))
except Exception as e:
    print("[JSON 解析失败]", e)
    print(open(raw_path, encoding='utf-8').read()[:500])
    sys.exit(0)

items = data if isinstance(data, list) else [data]
for i, item in enumerate(items):
    if len(items) > 1:
        print(f"--- call[{i}] ---")
    for b in (item.get('content') or []):
        if b.get('type') == 'text':
            print(b.get('text', ''))
        elif b.get('type') == 'image':
            open(png_path, 'wb').write(base64.b64decode(b.get('data', '')))
            print(f"[截图已保存] {png_path}")
PY
