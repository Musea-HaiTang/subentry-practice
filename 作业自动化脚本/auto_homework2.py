import time
import os
import webbrowser
import tempfile


class AutoHomeworkAssistant:
    def __init__(self):
        self.is_running = False
        self.yuanbao_url = "https://yuanbao.tencent.com/project/4c606a99330c4f33adcfac5656f7314f"
        self.temp_dir = tempfile.gettempdir()


    def take_screenshot(self):
        """使用系统截图功能"""
        print("📸 准备截图...")
        print("0.5秒后启动系统截图，请准备好选择区域")
        time.sleep(0.3)

        try:
            # 尝试使用系统截图工具
            # Windows: Win + Shift + S
            # Mac: Command + Shift + 4
            if os.name == 'nt':  # Windows
                pyautogui.hotkey('win', 'shift', 's')
                print("✅ 已启动Windows截图工具")
                print("🖱️ 请用鼠标选择截图区域")
            else:  # Mac
                pyautogui.hotkey('command', 'shift', '4')
                print("✅ 已启动Mac截图工具")

            # 等待用户完成截图（图片会自动保存到剪贴板）
            print("⏳ 等待截图完成...")
            time.sleep(1)

            return True

        except Exception as e:
            print(f"❌ 系统截图失败: {e}")
            return False

    def capture_and_send(self):
        """主流程：截图并发送"""
        if self.is_running:
            return

        self.is_running = True
        try:
            # 1. 使用系统截图工具
            if not self.take_screenshot():
                print("❌ 截图失败，请重试")
                return

            # 2. 打开腾讯元宝
            print("🌐 正在打开腾讯元宝...")
            webbrowser.open(self.yuanbao_url)
            time.sleep(2)  # 等待页面加载

            # 3. 粘贴图片
            print("📋 正在粘贴图片...")
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'v')  # 粘贴剪贴板中的图片
            time.sleep(3)

            # 4. 发送问题
            print("🚀 正在发送...")
            pyautogui.press('enter')

            print("✅ 已完成！请在腾讯元宝界面查看答案")

        except Exception as e:
            print(f"❌ 出错: {e}")
        finally:
            self.is_running = False

    def run(self):
        """运行助手"""
        print("=" * 50)
        print("🎯 全自动作业助手")
        print("=" * 50)
        print("使用方法:")
        print("1. 按 F8 开始")
        print("2. 使用系统截图工具选择区域")
        print("3. 程序会自动发送到腾讯元宝")
        print("=" * 50)
        print("💡 提示: 截图后图片会自动保存在剪贴板")
        print("=" * 50)

        keyboard.add_hotkey('f8', self.capture_and_send)
        print("✅ 已注册热键 F8")
        print("🛑 按 ESC 退出程序")

        keyboard.wait('esc')
        print("👋 程序已退出")


if __name__ == "__main__":
    try:
        import pyautogui
        import keyboard
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请安装: pip install pyautogui keyboard")
        exit()

    assistant = AutoHomeworkAssistant()
    assistant.run()
