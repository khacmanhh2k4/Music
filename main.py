# play_from_list.py
import re
import os
import sys
import subprocess
from pathlib import Path
import platform
import webbrowser



script_dir = Path(__file__).parent


def parse_song_line(line):
    """Trích xuất index, title, url từ một dòng."""
    line = line.strip()
    if not line:
        return None

    # tìm URL nếu có
    url_match = re.search(r"https?://\S+", line)
    url = url_match.group(0) if url_match else None

    # tìm số đầu dòng
    num_match = re.match(r"^\s*(\d+)", line)
    index = int(num_match.group(1)) if num_match else None

    # loại bỏ số và url khỏi dòng để lấy title
    title_part = line
    if num_match:
        title_part = re.sub(r"^\s*\d+\s*[.)-]?\s*", "", title_part, count=1)
    if url:
        title_part = title_part.replace(url, "")
    title_part = re.sub(r"[-\|:\t]+", " ", title_part)
    title = title_part.strip(" -|:.\t")

    return (index, title if title else "(untitled)", url)

def load_songs(path):
    """Đọc file và trả về danh sách bài hát."""
    songs = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for lineno, line in enumerate(f, start=1):
            parsed = parse_song_line(line)
            if parsed is None:
                continue
            idx, title, url = parsed
            if idx is None:
                idx = lineno
            songs.append({"index": idx, "title": title, "url": url, "raw": line.strip()})
    songs.sort(key=lambda s: s["index"])
    return songs

def open_in_browser(url):
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(f'start "" "{url}"', shell=True)
        elif "microsoft" in platform.release().lower():  # WSL
            subprocess.run(f'cmd.exe /c start "" "{url}"', shell=True)
        else:
            subprocess.run(["xdg-open", url], check=True)
        return True
    except Exception:
        webbrowser.open(url, new=2)
        return False

def main():
    path = Path(SONG_FILE)
    if not path.exists():
        print(f"Không tìm thấy {SONG_FILE}. Hãy tạo file theo ví dụ và thử lại.")
        sys.exit(1)

    songs = load_songs(path)
    if not songs:
        print("Không có bài nào trong file.")
        sys.exit(1)

    print("Danh sách bài hát:")
    for s in songs:
        print(f"{s['index']}. {s['title']}")

    try:
        choice = input("Nhập số bài muốn phát: ").strip()
        if not choice:
            print("Không nhập gì, thoát.")
            return
        num = int(choice)
    except ValueError:
        print("Vui lòng nhập một số hợp lệ.")
        return

    selected = next((s for s in songs if s["index"] == num), None)
    if not selected:
        print("Không tìm thấy bài có số đó.")
        return

    if not selected["url"]:
        print("Bài này không có URL trong file. Bạn cần thêm link YouTube ở dòng tương ứng.")
        print("Dòng raw:", selected["raw"])
        return

    print(f"Đang mở: {selected['title']}")
    opened = open_in_browser(selected["url"])
    if opened:
        print("Đã mở bài hát bằng trình duyệt hoặc ứng dụng mặc định.")
    else:
        print("Không thể mở bài hát tự động, vui lòng mở thủ công.")

print("---------Menu--------")
print('1. Chill Music')
print('2. Motivational Music')

n = input("Hôm nay tâm trạng của bạn thế nào: ")
if(n == "Sad" or n == "relax" or n == '1'):
    
    SONG_FILE = script_dir / "ChillMusic.txt"
    
    
if(n == "exitement" or n == 'intensity' or n =='2'):
     SONG_FILE = script_dir / "MotivationalMusic.txt"
else:
    exit

if __name__ == "__main__":
    main()
