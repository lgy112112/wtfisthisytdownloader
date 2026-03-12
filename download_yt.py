import subprocess
import sys
import re
import os
import argparse
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOWNLOAD_DIR = os.path.join(ROOT_DIR, "downloads")
DEFAULT_BROWSER = "chrome"
COMMON_BROWSERS = ("chrome", "edge", "firefox")
MAC_ONLY_BROWSERS = ("safari",)


def build_base_command(browser=None):
    """构建 yt-dlp 基础命令。"""
    cmd = ["yt-dlp", "--remote-components", "ejs:github"]

    # 如果已安装 node，优先启用，减少 YouTube 签名解析失败。
    if shutil.which("node"):
        cmd.extend(["--js-runtimes", "node"])

    if browser:
        cmd.extend(["--cookies-from-browser", browser])

    return cmd


def get_formats(url, browser=None):
    """获取所有可用格式"""
    cmd = build_base_command(browser)
    cmd.extend(["--list-formats", url])
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result.stdout + result.stderr

def parse_formats(output):
    """解析格式列表，返回可下载的视频格式"""
    formats = []
    lines = output.split('\n')

    for line in lines:
        # 跳过 storyboard、纯音频、表头
        if 'mhtml' in line or 'audio only' in line:
            continue
        if 'EXT' in line or '───' in line or 'storyboard' in line:
            continue

        # 匹配视频格式
        match = re.search(r'^\s*(\d+)\s+(\w+)\s+(\d+x\d+)\s+\d+', line)
        size_match = re.search(r'([\d.]+[MG]iB)', line)
        if match and size_match:
            is_video_only = 'video only' in line
            formats.append({
                'id': match.group(1),
                'ext': match.group(2),
                'resolution': match.group(3),
                'filesize': size_match.group(1),
                'type': '仅视频' if is_video_only else '音视频'
            })

    # 去重（按分辨率），保留文件最大的
    seen = {}
    for fmt in formats:
        res = fmt['resolution']
        if res not in seen or fmt['type'] == '音视频':
            seen[res] = fmt

    formats = list(seen.values())

    # 按分辨率排序
    def res_key(f):
        w, h = f['resolution'].split('x')
        return int(w) * int(h)
    formats.sort(key=res_key)

    return formats

def download_video(url, format_code=None, output_dir=None, browser=None):
    """下载视频到指定目录"""
    if output_dir is None:
        output_dir = DEFAULT_DOWNLOAD_DIR
    os.makedirs(output_dir, exist_ok=True)

    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    cmd = build_base_command(browser)
    cmd.extend(["-o", output_template])
    if format_code:
        cmd.extend(["-f", format_code])
    cmd.append(url)
    return subprocess.run(cmd).returncode


def get_browser_help():
    browsers = ", ".join(COMMON_BROWSERS)
    if sys.platform == "darwin":
        return f"从浏览器读取 Cookie，默认 {DEFAULT_BROWSER}；可选 {browsers}, safari"
    return f"从浏览器读取 Cookie，默认 {DEFAULT_BROWSER}；可选 {browsers}"


def validate_browser(browser):
    allowed = set(COMMON_BROWSERS)
    if sys.platform == "darwin":
        allowed.update(MAC_ONLY_BROWSERS)

    if browser not in allowed:
        if sys.platform == "darwin":
            choices = ", ".join((*COMMON_BROWSERS, *MAC_ONLY_BROWSERS))
        else:
            choices = ", ".join(COMMON_BROWSERS)
        raise ValueError(f"不支持的浏览器: {browser}。当前系统可用值: {choices}")


def main():
    parser = argparse.ArgumentParser(description="YouTube 视频下载器")
    parser.add_argument("url", help="YouTube 视频 URL")
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_DOWNLOAD_DIR,
        help=f"下载保存目录 (默认: {DEFAULT_DOWNLOAD_DIR})",
    )
    parser.add_argument("-f", "--format", default=None, help="直接指定 yt-dlp 格式代码，跳过交互选择")
    parser.add_argument(
        "-b",
        "--browser",
        default=DEFAULT_BROWSER,
        help=get_browser_help(),
    )
    args = parser.parse_args()

    url = args.url
    output_dir = args.output
    browser = args.browser

    try:
        validate_browser(browser)
    except ValueError as exc:
        print(exc)
        sys.exit(2)

    # 非交互模式：直接使用指定格式下载
    if args.format:
        print(f"下载到: {output_dir}")
        print(f"Cookie 来源: 浏览器 {browser} (默认: {DEFAULT_BROWSER})")
        sys.exit(download_video(url, args.format, output_dir, browser))

    print("正在获取可用格式...\n")
    output = get_formats(url, browser)
    formats = parse_formats(output)

    if not formats:
        print("未找到可用格式，使用默认格式下载...")
        sys.exit(download_video(url, output_dir=output_dir, browser=browser))

    # 显示选项
    print("="*60)
    print(f"下载到: {output_dir}")
    print(f"Cookie 来源: 浏览器 {browser} (默认: {DEFAULT_BROWSER})")
    print("可用清晰度:")
    print("="*60)
    for i, fmt in enumerate(formats, 1):
        print(f"  {i}. {fmt['resolution']:>10}  {fmt['ext']:>4}  ~{fmt['filesize']:>10}  ({fmt['type']})")

    print("="*60)
    print(f"  0. 默认最佳格式 (自动合并音视频)")
    print(f"  q. 退出")
    print("="*60)

    choice = input("\n请选择 [0-{}]: ".format(len(formats))).strip()

    if choice.lower() == 'q':
        print("已退出")
    elif choice == "" or choice == "0":
        print("\n使用默认最佳格式下载...")
        sys.exit(download_video(url, output_dir=output_dir, browser=browser))
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(formats):
                fmt = formats[idx]
                print(f"\n下载 {fmt['resolution']}...")
                if fmt['type'] == '仅视频':
                    sys.exit(download_video(url, f"{fmt['id']}+bestaudio", output_dir, browser))
                else:
                    sys.exit(download_video(url, fmt['id'], output_dir, browser))
            else:
                print("无效选择")
        except ValueError:
            print("无效输入")
            sys.exit(1)


if __name__ == "__main__":
    main()
