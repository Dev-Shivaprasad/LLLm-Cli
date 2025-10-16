import os
import glob
import subprocess

pathtobin = r"bin"
appname = "yt-dlp.exe"
tempdir = "temp"


def Getsubtitle(ytlink: str):
    subprocess.run([os.path.join(pathtobin, appname), "-U"])
    os.makedirs(tempdir, exist_ok=True)

    # First: try to get user-uploaded English subs
    cmd = [
        os.path.join(pathtobin, appname),
        "--skip-download",
        "--sub-langs",
        "en",  # user-uploaded English only
        "--sub-format",
        "srt",
        "--write-subs",  # try user subs first
        "-o",
        os.path.join(tempdir, "subtitle"),
        ytlink,
    ]
    subprocess.run(cmd)

    subtitles_text = stripubtitiles()
    if subtitles_text:
        print("Usergen Subs")
        return subtitles_text  # ✅ found user-uploaded subtitles

    # If none found → try auto-generated English subs
    cmd = [
        os.path.join(pathtobin, appname),
        "--skip-download",
        "--sub-langs",
        "en",
        "--sub-format",
        "srt",
        "--write-auto-subs",  # fallback to auto
        "-o",
        os.path.join(tempdir, "subtitle"),
        ytlink,
    ]
    subprocess.run(cmd)

    return stripubtitiles()


def stripubtitiles():
    # Find the downloaded .srt file
    srt_files = glob.glob(os.path.join(tempdir, "*.en.srt"))
    subtitles_text = ""

    if srt_files:
        srt_file = srt_files[0]
        with open(srt_file, "r", encoding="utf-8") as f:
            raw_content = f.read()

        # Clean out numbering + timestamps
        cleaned_lines = []
        for line in raw_content.splitlines():
            if line.strip().isdigit():
                continue
            if "-->" in line:
                continue
            if line.strip() == "":
                continue
            cleaned_lines.append(line.strip())

        subtitles_text = " ".join(cleaned_lines)

        # Delete after processing
        os.remove(srt_file)

    return subtitles_text
