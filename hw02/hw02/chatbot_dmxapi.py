import os
import sys
from typing import Any

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(errors="replace")

API_URL = os.getenv("DMXAPI_API_URL", "https://www.dmxapi.cn/v1/chat/completions")
MODEL_NAME = os.getenv("DMXAPI_MODEL", "claude-sonnet-4-6")
API_KEY = os.getenv("DMXAPI_API_KEY")
TIMEOUT = 60


def call_dmxapi(user_message: str) -> str:
    if not API_KEY:
        raise RuntimeError(
            "未检测到 DMXAPI_API_KEY。请先设置环境变量，再运行本脚本。"
        )

    payload: dict[str, Any] = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> int:
    print("DMXAPI Chatbot CLI")
    print(f"当前模型：{MODEL_NAME}")
    print("输入问题后回车即可提问，输入 exit 退出。")

    while True:
        try:
            user_message = input("\n你：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n已退出。")
            return 0

        if not user_message:
            continue

        if user_message.lower() in {"exit", "quit"}:
            print("已退出。")
            return 0

        try:
            answer = call_dmxapi(user_message)
        except requests.HTTPError as exc:
            detail = exc.response.text if exc.response is not None else str(exc)
            print(f"\n请求失败：{detail}")
            continue
        except requests.RequestException as exc:
            print(f"\n网络错误：{exc}")
            continue
        except RuntimeError as exc:
            print(f"\n配置错误：{exc}")
            return 1

        print(f"\n模型：{answer}")


if __name__ == "__main__":
    sys.exit(main())
