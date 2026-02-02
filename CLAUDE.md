# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a YouTube video downloader utility built with Python that wraps yt-dlp with an interactive format selection interface. The project consists of two main scripts for downloading YouTube videos with cookie authentication and remote component support.

## Key Commands

### Running the Main Downloader
```bash
# 交互模式（默认URL，下载到 ./downloads/）
python download_yt.py

# 指定URL
python download_yt.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定下载目录
python download_yt.py -o /path/to/save "https://www.youtube.com/watch?v=VIDEO_ID"

# 非交互模式：直接指定格式代码
python download_yt.py -f 137+bestaudio "https://www.youtube.com/watch?v=VIDEO_ID"
```

**CLI 参数:**
- `url` (positional, optional): YouTube 视频 URL，默认使用硬编码 URL
- `-o / --output`: 下载保存目录，默认为项目根目录下的 `downloads/`
- `-f / --format`: 直接指定 yt-dlp 格式代码，跳过交互选择

This launches an interactive prompt that:
1. Lists available video formats with resolution, file size, and type
2. Allows selection of specific quality/format
3. Automatically merges video and audio streams when needed

### Debug/List Formats
```bash
python debug_formats.py
```
Displays raw yt-dlp format list for a hardcoded URL (useful for debugging format parsing).

## Architecture

### Core Components

**download_yt.py** - Main interactive downloader with three key functions:
- `get_formats(url)`: Calls yt-dlp with `--list-formats` to retrieve available formats
- `parse_formats(output)`: Parses yt-dlp output, filters out audio-only/storyboard formats, deduplicates by resolution, and sorts by resolution
- `download_video(url, format_code, output_dir)`: Executes yt-dlp download with optional format code, saves to specified directory (defaults to `./downloads/`)

**debug_formats.py** - Simple format listing tool for debugging

### yt-dlp Integration

All yt-dlp calls use consistent parameters:
- `--cookies www.youtube.com_cookies.txt` - Cookie file for authentication (must exist in working directory)
- `--remote-components ejs:github` - Enables remote component support
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
- Deno added to PATH (C:\Users\29724\AppData\Local\Microsoft\WinGet\Packages\DenoLand.Deno_Microsoft.Winget.Source_8wekyb3d8bbwe)
- Cookie file `www.youtube.com_cookies.txt` in working directory for authenticated downloads

## Important Notes

- The video URL defaults to a hardcoded value but can be overridden via CLI positional argument. debug_formats.py still uses a hardcoded URL.
- The Deno PATH addition (lines 6-7 in download_yt.py, lines 4-5 in debug_formats.py) is user-specific and may need adjustment on different systems.
- Format parsing relies on specific regex patterns that match yt-dlp's output format. Changes to yt-dlp output formatting may break the parser.
