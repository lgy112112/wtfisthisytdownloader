---
name: "wtfisthisytdownloader"
description: "Download YouTube videos or Shorts with interactive format selection through a bundled yt-dlp wrapper that authenticates from a logged-in browser profile instead of local cookies.txt files. Use when Codex needs to fetch a YouTube URL, list available qualities, resume or retry downloads, or pick a specific format on macOS or Windows."
---

# YouTube Downloader

Use the bundled script instead of reconstructing yt-dlp flags by hand.

## Files

- Run [`scripts/download_yt.py`](scripts/download_yt.py) for all downloads.

## Prerequisites

- Ensure `yt-dlp` is installed and on `PATH`.
- Ensure `ffmpeg` is installed and on `PATH` for formats that need merge/remux support.
- Prefer a logged-in `chrome` profile. Use `edge` or `firefox` when Chrome is unavailable. Use `safari` only on macOS.
- If `node` is installed, leave it available on `PATH`; the script enables it automatically for YouTube challenge solving.

## Happy Path

Run the script from the skill directory or pass an absolute path:

```bash
python3 <skill-path>/scripts/download_yt.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

The script:

- reads browser cookies with `--cookies-from-browser`
- lists visible video formats
- prompts for a quality choice
- downloads into a `downloads/` directory next to the script unless `-o/--output` overrides it

## Common Commands

Default browser (`chrome`):

```bash
python3 <skill-path>/scripts/download_yt.py "<youtube-url>"
```

Pick another browser:

```bash
python3 <skill-path>/scripts/download_yt.py -b edge "<youtube-url>"
python3 <skill-path>/scripts/download_yt.py -b firefox "<youtube-url>"
```

Use Safari on macOS only:

```bash
python3 <skill-path>/scripts/download_yt.py -b safari "<youtube-url>"
```

Skip the interactive picker and force a format id:

```bash
python3 <skill-path>/scripts/download_yt.py -f 18 "<youtube-url>"
```

Write into a specific directory:

```bash
python3 <skill-path>/scripts/download_yt.py -o /abs/output/dir "<youtube-url>"
```

## Failure Handling

- If the listed qualities look too limited, switch from the default browser to another logged-in browser before assuming the video lacks higher formats.
- If YouTube returns challenge or signature errors, ensure `node` is installed; the script already enables it when present.
- If `ffmpeg` errors on macOS with missing `libvpx`, repair Homebrew packages before retrying.
- If Safari cookie access fails, retry with `chrome`, `edge`, or `firefox`; Safari often depends on extra OS permissions.

## Verification

- Confirm the script prints the selected browser source before downloading.
- Confirm the target file appears under the chosen output directory.
- For interrupted large downloads, rerun the same command and allow yt-dlp to resume the `.part` file.
