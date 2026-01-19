# ytdl-interactive

YouTube 视频下载工具，提供交互式格式选择界面。

## 功能特性

- 🎯 交互式格式选择：列出所有可用的视频格式，包括分辨率、文件大小等信息
- 🔄 自动合并：自动合并视频流和音频流，获得最佳质量
- 🍪 Cookie 支持：支持使用 Cookie 文件进行身份验证
- ⚡ 简单易用：基于强大的 yt-dlp，提供简洁的命令行界面

## 安装

### 从源代码安装

```bash
git clone https://github.com/yourusername/ytdl.git
cd ytdl
pip install -e .
```

### 从 GitHub 安装

```bash
pip install git+https://github.com/yourusername/ytdl.git
```

## 使用方法

### 基本用法

```bash
ytdl "https://www.youtube.com/watch?v=VIDEO_ID"
```

这将显示可用格式列表，让你选择下载哪个格式。

### 使用 Cookie 文件

```bash
ytdl -c cookies.txt "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 指定输出文件名模板

```bash
ytdl -o "%(title)s-%(id)s.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 直接指定格式（跳过交互选择）

```bash
ytdl -f "bestvideo+bestaudio" "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 命令行参数

- `url`: YouTube 视频 URL（必需）
- `-c, --cookies`: Cookie 文件路径
- `-o, --output`: 输出文件名模板
- `-f, --format`: 格式代码（跳过交互式选择）

## 依赖

- Python 3.7+
- yt-dlp

## 许可证

MIT License
