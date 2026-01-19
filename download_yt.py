import subprocess
import sys
import re
import os

# 添加 deno 到 PATH
os.environ['PATH'] = os.environ.get('PATH', '') + r';C:\Users\29724\AppData\Local\Microsoft\WinGet\Packages\DenoLand.Deno_Microsoft.Winget.Source_8wekyb3d8bbwe'

def get_formats(url):
    """获取所有可用格式"""
    cmd = [
        "yt-dlp",
        "--cookies", "www.youtube.com_cookies.txt",
        "--remote-components", "ejs:github",
        "--list-formats",
        url
    ]
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

def download_video(url, format_code=None):
    """下载视频"""
    cmd = [
        "yt-dlp",
        "--cookies", "www.youtube.com_cookies.txt",
        "--remote-components", "ejs:github",
        "-o", "%(title)s.%(ext)s",
    ]
    if format_code:
        cmd.extend(["-f", format_code])
    cmd.append(url)
    subprocess.run(cmd)

if __name__ == "__main__":
    url = "https://youtu.be/K5zgJ_oWgAE"

    print("正在获取可用格式...\n")
    output = get_formats(url)
    formats = parse_formats(output)

    if not formats:
        print("未找到可用格式，使用默认格式下载...")
        download_video(url)
        sys.exit(0)

    # 显示选项
    print("="*60)
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
        download_video(url)
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(formats):
                fmt = formats[idx]
                print(f"\n下载 {fmt['resolution']}...")
                if fmt['type'] == '仅视频':
                    # 自动合并最佳音频
                    download_video(url, f"{fmt['id']}+bestaudio")
                else:
                    download_video(url, fmt['id'])
            else:
                print("无效选择")
        except ValueError:
            print("无效输入")

