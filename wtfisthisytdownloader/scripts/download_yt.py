import argparse
import os
import re
import shutil
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOWNLOAD_DIR = os.path.join(ROOT_DIR, "downloads")
DEFAULT_BROWSER = "chrome"
COMMON_BROWSERS = ("chrome", "edge", "firefox")
MAC_ONLY_BROWSERS = ("safari",)


def build_base_command(browser=None):
    """Construct the common yt-dlp command prefix."""
    cmd = ["yt-dlp", "--remote-components", "ejs:github"]

    if shutil.which("node"):
        cmd.extend(["--js-runtimes", "node"])

    if browser:
        cmd.extend(["--cookies-from-browser", browser])

    return cmd


def get_formats(url, browser=None):
    """Fetch the available formats for a YouTube URL."""
    cmd = build_base_command(browser)
    cmd.extend(["--list-formats", url])
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return result.stdout + result.stderr


def parse_formats(output):
    """Parse yt-dlp format output into simplified choices."""
    formats = []

    for line in output.splitlines():
        if "mhtml" in line or "audio only" in line:
            continue
        if "EXT" in line or "───" in line or "storyboard" in line:
            continue

        match = re.search(r"^\s*(\d+)\s+(\w+)\s+(\d+x\d+)\s+\d+", line)
        size_match = re.search(r"([\d.]+[MG]iB)", line)
        if match and size_match:
            is_video_only = "video only" in line
            formats.append(
                {
                    "id": match.group(1),
                    "ext": match.group(2),
                    "resolution": match.group(3),
                    "filesize": size_match.group(1),
                    "type": "仅视频" if is_video_only else "音视频",
                }
            )

    seen = {}
    for fmt in formats:
        resolution = fmt["resolution"]
        if resolution not in seen or fmt["type"] == "音视频":
            seen[resolution] = fmt

    formats = list(seen.values())

    def res_key(fmt):
        width, height = fmt["resolution"].split("x")
        return int(width) * int(height)

    formats.sort(key=res_key)
    return formats


def download_video(url, format_code=None, output_dir=None, browser=None):
    """Download a YouTube URL into the selected directory."""
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

    print("=" * 60)
    print(f"下载到: {output_dir}")
    print(f"Cookie 来源: 浏览器 {browser} (默认: {DEFAULT_BROWSER})")
    print("可用清晰度:")
    print("=" * 60)
    for index, fmt in enumerate(formats, 1):
        print(f"  {index}. {fmt['resolution']:>10}  {fmt['ext']:>4}  ~{fmt['filesize']:>10}  ({fmt['type']})")

    print("=" * 60)
    print("  0. 默认最佳格式 (自动合并音视频)")
    print("  q. 退出")
    print("=" * 60)

    choice = input(f"\n请选择 [0-{len(formats)}]: ").strip()

    if choice.lower() == "q":
        print("已退出")
        return
    if choice == "" or choice == "0":
        print("\n使用默认最佳格式下载...")
        sys.exit(download_video(url, output_dir=output_dir, browser=browser))

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(formats):
            fmt = formats[idx]
            print(f"\n下载 {fmt['resolution']}...")
            if fmt["type"] == "仅视频":
                sys.exit(download_video(url, f"{fmt['id']}+bestaudio", output_dir, browser))
            sys.exit(download_video(url, fmt["id"], output_dir, browser))
        print("无效选择")
        sys.exit(1)
    except ValueError:
        print("无效输入")
        sys.exit(1)


if __name__ == "__main__":
    main()
