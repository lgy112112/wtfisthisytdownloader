# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a YouTube video downloader utility built with Python that wraps yt-dlp with an interactive format selection interface. The repository is centered on a single script, `download_yt.py`, and is intended to work on both macOS and Windows.

## Key Commands

### Running the Main Downloader
```bash
# 指定URL
python download_yt.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定下载目录
python download_yt.py -o /path/to/save "https://www.youtube.com/watch?v=VIDEO_ID"

# 非交互模式：直接指定格式代码
python download_yt.py -f 137+bestaudio "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定浏览器登录态
python download_yt.py -b chrome "https://www.youtube.com/watch?v=VIDEO_ID"
```

**CLI 参数:**
- `url` (positional, required): YouTube 视频 URL
- `-o / --output`: 下载保存目录，默认为项目根目录下的 `downloads/`
- `-f / --format`: 直接指定 yt-dlp 格式代码，跳过交互选择
- `-b / --browser`: 浏览器登录态来源，默认 `chrome`

This launches an interactive prompt that:
1. Lists available video formats with resolution, file size, and type
2. Allows selection of specific quality/format
3. Automatically merges video and audio streams when needed

## Architecture

### Core Components

**download_yt.py** - Main interactive downloader with three key functions:
- `get_formats(url, browser)`: Calls yt-dlp with `--list-formats` to retrieve available formats
- `parse_formats(output)`: Parses yt-dlp output, filters out audio-only/storyboard formats, deduplicates by resolution, and sorts by resolution
- `download_video(url, format_code, output_dir, browser)`: Executes yt-dlp download with optional format code, saves to specified directory (defaults to `./downloads/`)

### yt-dlp Integration

All yt-dlp calls use consistent parameters:
- `--cookies-from-browser chrome` - Use the browser login session for authentication
- `--remote-components ejs:github` - Enables remote component support
- `--js-runtimes node` - Enabled automatically when `node` is available on PATH
- `-o "%(title)s.%(ext)s"` - Output filename template, files saved to `downloads/` directory by default

### Format Selection Logic

The format parser (download_yt.py:21-61):
1. Filters out storyboard/audio-only formats
2. Extracts format ID, extension, resolution, and file size
3. Distinguishes between video-only and audio+video streams
4. Deduplicates by resolution, preferring audio+video when available
5. Sorts by pixel count (width × height)

When downloading video-only formats, the script automatically appends `+bestaudio` to merge with the best available audio stream.

## Environment Requirements

- Python 3.x
- yt-dlp installed and accessible in PATH
- ffmpeg installed and accessible in PATH
- Browser login session (for example Chrome) for authenticated downloads
- Optional: node installed and accessible in PATH for more reliable YouTube challenge solving

## Important Notes

- There is no hardcoded default URL anymore; the script requires a positional URL argument.
- Safari is only supported as a browser source on macOS.
- Format parsing relies on specific regex patterns that match yt-dlp's output format. Changes to yt-dlp output formatting may break the parser.
