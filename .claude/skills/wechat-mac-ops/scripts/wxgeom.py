#!/usr/bin/env python3
"""wxgeom.py —— 微信窗口几何与坐标换算（排查"点偏了"时的第一件工具）

用法：
  wxgeom.py geom
      列出微信（WeChat）当前所有窗口的 X / Y / 宽 / 高（屏幕点坐标，左上角为原点）。
      换算公式：全局点 = 窗口原点 + 截图像素 × (窗口尺寸 ÷ 截图尺寸)
  wxgeom.py conv <截图宽> <截图高> <截图x> <截图y> --name <窗口名关键字>
      按窗口名找窗口（例：--name 微信 拿主窗口；--name 群公告 拿公告窗口）。

  wxgeom.py conv <截图宽> <截图高> <截图x> <截图y> <窗口X> <窗口Y> <窗口宽> <窗口高>
      直接给窗口 bounds（从 geom 输出里拷；弹窗请用这条，因为弹窗是另一个窗口）。

  wxgeom.py cursor
      打印当前鼠标指针的屏幕坐标——点一下之后跑它，就能验证"点击实际落在哪"。

为什么需要它：open-computer-use 的 click / drag 收的是**截图像素坐标**，内部按
「该次截图对应的窗口 bounds」换算。主窗口没问题；但**弹窗（确认框 / sheet）是另一个
窗口**，工具可能仍按主窗口的比例算，于是点偏。查清楚弹窗自己的窗口 bounds，就能反推出
应该传什么截图坐标：截图坐标 = (目标全局点 − 弹窗原点) × (截图尺寸 ÷ 弹窗尺寸)。
"""
import sys

import Quartz

OWNER = "WeChat"


def windows():
    # 用 kCGWindowListOptionAll：微信窗口可能不在当前 Space / 已最小化，
    # 用 OnScreenOnly 会漏（实测：切到别的桌面后列表里只剩 Finder）
    info = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionAll | Quartz.kCGWindowListExcludeDesktopElements,
        Quartz.kCGNullWindowID,
    )
    out = []
    for w in info:
        if w.get("kCGWindowOwnerName") == OWNER:
            b = w.get("kCGWindowBounds", {})
            out.append({"name": w.get("kCGWindowName") or "", "bounds": b})
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]

    if cmd == "geom":
        ws = windows()
        if not ws:
            print("没有找到微信窗口——微信没启动？或窗口被隐藏？"
                  "（若确认微信开着，检查「系统设置 → 隐私与安全性 → 屏幕录制」是否已授权给终端 / pi）")
            return
        for i, w in enumerate(ws):
            b = w["bounds"]
            print(f"[{i}] {w['name'] or '(无标题)'}  X={b.get('X')} Y={b.get('Y')} "
                  f"W={b.get('Width')} H={b.get('Height')}")
        print("\n换算：全局点 = 窗口原点 + 截图像素 × (窗口尺寸 ÷ 截图尺寸)")

    elif cmd == "conv":
        if len(sys.argv) < 6:
            print(__doc__)
            return
        sw, sh, sx, sy = map(float, sys.argv[2:6])
        rest = sys.argv[6:]

        # 方式 A：--name <关键字>（取第一个名字包含关键字的窗口）
        if len(rest) == 2 and rest[0] == "--name":
            key = rest[1]
            hit = next((w for w in windows() if key in w["name"]), None)
            if not hit:
                print(f"没找到名字包含「{key}」的窗口，先跑 geom 看看有哪些：")
                for w in windows():
                    if w["name"]:
                        b = w["bounds"]
                        print(f"  {w['name']!r} X={b.get('X')} Y={b.get('Y')} "
                              f"W={b.get('Width')} H={b.get('Height')}")
                return
            b = hit["bounds"]
            print(f"（按名字命中窗口 {hit['name']!r}）")

        # 方式 B：直接给 bounds
        elif len(rest) == 4:
            bx, by, bw, bh = map(float, rest)
            b = {"X": bx, "Y": by, "Width": bw, "Height": bh}

        else:
            print(__doc__)
            return

        gx = b["X"] + sx * b["Width"] / sw
        gy = b["Y"] + sy * b["Height"] / sh
        print(f"截图像素 ({sx:g}, {sy:g}) → 全局点 ({gx:.1f}, {gy:.1f})")

    elif cmd == "cursor":
        loc = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
        print(f"当前鼠标指针：({loc.x:.1f}, {loc.y:.1f})")

    else:
        print(__doc__)


main()
