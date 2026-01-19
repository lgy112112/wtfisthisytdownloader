import subprocess
import os

# 刷新 PATH
os.environ['PATH'] = os.environ.get('PATH', '') + r';C:\Users\29724\AppData\Local\Microsoft\WinGet\Packages\DenoLand.Deno_Microsoft.Winget.Source_8wekyb3d8bbwe'

cmd = [
    "yt-dlp",
    "--cookies", "www.youtube.com_cookies.txt",
    "--remote-components", "ejs:github",
    "--list-formats",
    "https://youtu.be/K5zgJ_oWgAE"
]

# 不捕获输出，直接显示
subprocess.run(cmd)

