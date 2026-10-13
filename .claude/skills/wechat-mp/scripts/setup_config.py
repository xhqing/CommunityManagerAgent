#!/usr/bin/env python3
"""写入公众号 API 凭证到本机配置文件（不进 git）。

用法：python3 setup_config.py
凭据在公众号后台获取：设置与开发 → 基本配置（AppID / AppSecret）。
写入位置：~/.wechat-mp/config.json（权限 600）
"""

from __future__ import annotations

import getpass
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wx_api import config_path  # noqa: E402


def main() -> None:
    p = config_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    old = {}
    if p.exists():
        old = json.loads(p.read_text(encoding="utf-8"))
        print(f"已存在配置：{p}（直接回车＝保留原值）")

    appid = input(f"AppID（当前 {old.get('appid', '未设置')}）：").strip() or old.get("appid", "")
    secret = getpass.getpass("AppSecret（输入不回显）：").strip() or old.get("appsecret", "")
    if not appid or not secret:
        raise SystemExit("AppID / AppSecret 不能为空")

    cfg = {"appid": appid, "appsecret": secret,
           "use_proxy": bool(old.get("use_proxy", False)),
           "author": old.get("author", "AI+X 实战经验交流群")}
    p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    p.chmod(0o600)
    print(f"已写入 {p}（权限 600，不进 git）")
    print("下一步：把调用机器的公网出口 IP 加进公众号后台「设置与开发 → 基本配置 → IP 白名单」")


if __name__ == "__main__":
    main()
