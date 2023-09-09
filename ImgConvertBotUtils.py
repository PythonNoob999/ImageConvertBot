from pyrogram.types import InlineKeyboardButton as Button
import subprocess

messages = {
"startup_message": """
Welcome {} 👋

Click on the Convert☢ and send your **PNG** or **JPEG** Image to convert it
**[Bot Maker](tg://user?id=929863209)🃏**
""",
}

keyboards = {
"main": [[Button("Convert☢", callback_data="conv")], [Button("Source Code🎛", url="https://github.com/PythonNoob999/ImageConvertBot")]],
"back": [[Button("Back🔙", callback_data="back")]]
}

def convert_file(file_path: str, wanted_extension: str):
    subprocess.run(f"ffmpeg -i {file_path} {file_path.replace(file_path[-3:], wanted_extension)}", shell=True)
    return file_path.replace(file_path[-3:], wanted_extension)