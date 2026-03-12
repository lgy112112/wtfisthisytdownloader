# wtfisthisytdownloader

这个仓库现在既是一个可直接运行的 YouTube 下载器仓库，也是一个可安装的 Codex skill。

可安装的 skill 目录在 [wtfisthisytdownloader](/Users/davidjam/REPO/wtfisthisytdownloader/wtfisthisytdownloader)，主脚本在 [wtfisthisytdownloader/scripts/download_yt.py](/Users/davidjam/REPO/wtfisthisytdownloader/wtfisthisytdownloader/scripts/download_yt.py)。根目录的 [download_yt.py](/Users/davidjam/REPO/wtfisthisytdownloader/download_yt.py) 只是一个兼容包装器。

默认下载到 skill 目录下的 `downloads/`，默认使用浏览器 `chrome` 登录态。

## 安装成 Skill

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo lgy112112/wtfisthisytdownloader \
  --path wtfisthisytdownloader
```

安装后重启 Codex 以加载新 skill。

## 准备

先安装依赖：

### macOS

```bash
python3 -m pip install yt-dlp
brew install ffmpeg
```

如果你的 `ffmpeg` 已经损坏并报 `libvpx` 动态库缺失，直接修：

```bash
brew reinstall libvpx ffmpeg
```

### Windows

```bash
py -3 -m pip install yt-dlp
winget install Gyan.FFmpeg
```

## 用法

### 直接运行

macOS:

```bash
cd /Users/davidjam/REPO/wtfisthisytdownloader
python3 wtfisthisytdownloader/scripts/download_yt.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Windows:

```bash
cd C:\path\to\wtfisthisytdownloader
py -3 wtfisthisytdownloader\scripts\download_yt.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

脚本默认从 `chrome` 读取登录态。

### 指定浏览器登录态

```bash
python3 wtfisthisytdownloader/scripts/download_yt.py -b chrome "https://www.youtube.com/watch?v=VIDEO_ID"
python3 wtfisthisytdownloader/scripts/download_yt.py -b edge "https://www.youtube.com/watch?v=VIDEO_ID"
python3 wtfisthisytdownloader/scripts/download_yt.py -b firefox "https://www.youtube.com/watch?v=VIDEO_ID"
```

`safari` 仅在 macOS 可用：

```bash
python3 wtfisthisytdownloader/scripts/download_yt.py -b safari "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 直接指定格式，跳过交互

```bash
python3 wtfisthisytdownloader/scripts/download_yt.py -f 18 "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 指定输出目录

```bash
python3 wtfisthisytdownloader/scripts/download_yt.py -o ~/Downloads/youtube "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 参数

- `url`: YouTube 视频或 Shorts 链接
- `-o, --output`: 下载目录，默认是仓库下的 `downloads/`
- `-f, --format`: 直接指定 yt-dlp 格式代码
- `-b, --browser`: 从浏览器读取 Cookie，默认 `chrome`
- 浏览器取值：`chrome`、`edge`、`firefox`
- `safari` 仅在 macOS 可用

## 说明

- 脚本会自动加上 `yt-dlp` 的 EJS 远程组件配置。
- 如果系统里安装了 `node`，脚本会自动启用它，减少 YouTube 签名解析失败。
- Windows 和 macOS 都建议直接使用浏览器登录态，不再支持本地 `cookies.txt` 文件。
