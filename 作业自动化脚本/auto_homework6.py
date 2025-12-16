import time
import os
import sys
import webbrowser
from datetime import datetime
from typing import Optional
import tempfile


class AutoHomeworkAssistant:
    def __init__(self):
        self.is_running = False
        self.yuanbao_url = "https://yuanbao.tencent.com/project/4c606a99330c4f33adcfac5656f7314f"
        self.temp_dir = tempfile.gettempdir()
        self.screenshots_dir = "screenshots"  # 截图保存目录
        self.browser_window_active = False

        # 创建截图保存目录
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

    def _import_dependencies(self) -> bool:
        """动态导入依赖"""
        missing_deps = []

        try:
            global pyautogui
            import pyautogui
        except ImportError:
            missing_deps.append("pyautogui")

        try:
            global keyboard
            import keyboard
        except ImportError:
            missing_deps.append("keyboard")

        try:
            global ImageGrab
            from PIL import ImageGrab
        except ImportError:
            missing_deps.append("Pillow")

        if missing_deps:
            print(f"❌ 缺少依赖: {', '.join(missing_deps)}")
            print("请使用以下命令安装:")
            print("pip install pyautogui keyboard pillow")
            return False
        return True

    def _save_screenshot_to_file(self) -> Optional[str]:
        """
        从剪贴板保存截图到文件
        返回保存的文件路径
        """
        try:
            from PIL import ImageGrab

            # 从剪贴板获取图片
            img = ImageGrab.grabclipboard()
            if img is None:
                return None

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)

            # 保存图片
            img.save(filepath, 'PNG')
            return filepath

        except Exception:
            return None

    def _take_screenshot_simple(self) -> bool:
        """
        简化的截图流程
        返回是否成功
        """
        print("\n📸 正在启动系统截图...")
        print("请用鼠标选择截图区域")
        print("提示: 截图会自动保存到剪贴板")

        try:
            # 根据系统触发不同的截图快捷键
            if os.name == 'nt':  # Windows
                pyautogui.hotkey('win', 'shift', 's')
                print("✅ 已启动Windows截图 (Win+Shift+S)")
            elif sys.platform == 'darwin':  # macOS
                pyautogui.hotkey('command', 'shift', '4')
                print("✅ 已启动Mac截图 (Cmd+Shift+4)")
            else:  # Linux
                print("🐧 启动Linux截图")
                pyautogui.hotkey('shift', 'printscreen')

            # 等待用户截图
            print("⏳ 请用鼠标选择截图区域...")
            time.sleep(5)  # 给用户足够时间截图

            # 保存截图到文件
            saved_path = self._save_screenshot_to_file()
            if saved_path:
                print(f"💾 截图已保存到: {os.path.abspath(saved_path)}")

            print("✅ 截图完成")
            return True

        except Exception as e:
            print(f"❌ 截图出错: {e}")
            return False

    def _activate_browser_window_smart(self):
        """
        智能激活浏览器窗口
        使用多种方法确保浏览器窗口被激活
        """
        print("🖥️  正在激活浏览器窗口...")

        # 方法1: 先尝试用快捷键激活浏览器
        try:
            if os.name == 'nt':  # Windows
                # 先按一次Alt+Tab
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.3)
                # 再按一次切换回来
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.3)
            elif sys.platform == 'darwin':  # macOS
                pyautogui.hotkey('command', 'tab')
                time.sleep(0.3)
        except:
            pass

        # 方法2: 点击浏览器窗口区域
        try:
            # 点击屏幕中间位置，假设浏览器窗口是激活的
            screen_width, screen_height = pyautogui.size()
            pyautogui.click(screen_width // 2, screen_height // 2)
            time.sleep(0.5)
        except:
            pass

        # 方法3: 如果以上都失败，提示用户
        print("⚠️  如果浏览器窗口没有激活，请手动点击浏览器窗口")
        time.sleep(1)

        self.browser_window_active = True

    def _find_yuanbao_input_box(self):
        """
        查找并点击腾讯元宝输入框
        根据截图，输入框是底部中央的"在这里提问，新建对话"区域
        位置相对固定：屏幕底部中央
        """
        print("🎯 正在定位腾讯元宝输入框...")

        # 获取屏幕尺寸
        screen_width, screen_height = pyautogui.size()

        # 根据您提供的截图，输入框位置：
        # 在屏幕底部，大约是屏幕底部向上 100-200 像素的位置
        # 我们先尝试几个可能的位置

        # 位置1: 屏幕底部向上150像素（最可能的位置）
        input_box_x = screen_width // 2
        input_box_y = screen_height - 150

        print(f"📍 尝试点击位置: ({input_box_x}, {input_box_y})")
        print("💡 这是'在这里提问，新建对话'输入框的预计位置")

        try:
            # 先移动鼠标到该位置，让用户看到
            pyautogui.moveTo(input_box_x, input_box_y, duration=0.5)
            time.sleep(0.5)

            # 点击输入框
            pyautogui.click(input_box_x, input_box_y)
            time.sleep(0.5)

            print("✅ 已点击输入框")
            return True

        except Exception as e:
            print(f"⚠️  点击失败: {e}")

            # 如果失败，尝试附近位置
            alternative_positions = [
                (input_box_x, screen_height - 100),  # 更低
                (input_box_x, screen_height - 200),  # 更高
                (input_box_x, screen_height - 120),  # 中间位置
            ]

            for i, (x, y) in enumerate(alternative_positions, 1):
                try:
                    print(f"📍 尝试替代位置 {i}: ({x}, {y})")
                    pyautogui.moveTo(x, y, duration=0.3)
                    time.sleep(0.3)
                    pyautogui.click(x, y)
                    time.sleep(0.5)
                    print(f"✅ 已点击替代位置 {i}")
                    return True
                except:
                    continue

            print("❌ 无法找到输入框，请手动点击")
            return False

    def _smart_open_yuanbao(self):
        """
        智能打开腾讯元宝
        尝试重用现有标签页
        """
        print("🌐 正在处理腾讯元宝页面...")

        # 尝试先激活现有窗口
        self._activate_browser_window_smart()
        time.sleep(1)

        # 尝试用 webbrowser.open 打开，浏览器通常会自动切换到已有标签页
        webbrowser.open(self.yuanbao_url)
        print("✅ 已打开/切换至腾讯元宝")

        # 等待页面加载
        print("⏳ 等待页面加载...")
        time.sleep(3)

        # 再次确保窗口激活
        self._activate_browser_window_smart()
        time.sleep(1)

    def _paste_screenshot_to_yuanbao(self) -> bool:
        """
        粘贴截图到腾讯元宝
        简化版，不进行复杂检测
        """
        print("📋 正在粘贴截图...")

        # 等待一下，确保输入框已激活
        time.sleep(1)

        # 尝试粘贴
        try:
            if os.name == 'nt':  # Windows
                pyautogui.hotkey('ctrl', 'v')
            else:  # macOS
                pyautogui.hotkey('command', 'v')

            print("✅ 已粘贴截图")
            time.sleep(2)  # 等待图片上传完成
            return True

        except Exception as e:
            print(f"❌ 粘贴失败: {e}")

            # 如果失败，提示用户手动粘贴
            print("💡 请手动操作:")
            print("   1. 确保点击了'在这里提问，新建对话'输入框")
            print("   2. 按 Ctrl+V (Windows) 或 Cmd+V (Mac) 粘贴")
            print("   3. 按 Enter 发送")
            return False

    def _send_question(self):
        """发送问题"""
        print("🚀 准备发送...")

        # 等待一下确保粘贴完成
        time.sleep(1)

        # 检查是否要取消
        if keyboard.is_pressed('esc'):
            print("⏹️ 用户取消发送")
            return False

        # 发送
        try:
            pyautogui.press('enter')
            print("✅ 已发送")
            time.sleep(1)  # 等待发送完成
            return True
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False

    def capture_and_send(self):
        """主流程：截图并发送"""
        if self.is_running:
            print("⏳ 上一个任务还在进行中，请稍候...")
            return

        self.is_running = True

        try:
            print("\n" + "=" * 50)
            print("🚀 开始截图上传流程")
            print("=" * 50)

            # 1. 截图
            print("\n步骤1: 截图")
            if not self._take_screenshot_simple():
                print("❌ 截图失败，请重试")
                return

            # 2. 打开/激活腾讯元宝
            print("\n步骤2: 打开/激活腾讯元宝")
            self._smart_open_yuanbao()

            # 3. 点击输入框
            print("\n步骤3: 点击输入框")
            input_clicked = self._find_yuanbao_input_box()

            if not input_clicked:
                print("⚠️  自动点击失败，请手动点击'在这里提问，新建对话'输入框")
                print("💡 等待3秒让您手动操作...")
                time.sleep(3)

            # 4. 粘贴截图
            print("\n步骤4: 粘贴截图")
            paste_success = self._paste_screenshot_to_yuanbao()

            if not paste_success:
                print("⏳ 等待5秒，您可以手动粘贴...")
                time.sleep(5)

            # 5. 发送
            print("\n步骤5: 发送")
            self._send_question()

            print("\n" + "=" * 50)
            print("✅ 完成！截图已发送到腾讯元宝")
            print("=" * 50)

        except KeyboardInterrupt:
            print("\n⏹️ 用户中断")
        except Exception as e:
            print(f"\n❌ 出错: {e}")
        finally:
            self.is_running = False
            time.sleep(0.5)

    def run(self):
        """运行助手"""
        print("🎯 腾讯元宝截图上传助手")
        print("=" * 50)
        print("📋 使用说明:")
        print("  • 按 F8 键: 截图并上传到腾讯元宝")
        print("  • 按 ESC 键: 退出程序")
        print("=" * 50)
        print("💡 操作流程:")
        print("  1. 按 F8")
        print("  2. 用鼠标选择截图区域")
        print("  3. 程序会自动:")
        print("     - 保存截图到 screenshots 文件夹")
        print("     - 打开/激活腾讯元宝")
        print("     - 点击'在这里提问，新建对话'输入框")
        print("     - 粘贴截图并发送")
        print("=" * 50)
        print("🎯 特别说明:")
        print("  • 程序会点击屏幕底部中央的输入框")
        print("  • 如果位置不准确，请根据您的屏幕调整")
        print("  • 截图自动保存，可手动重新上传")
        print("=" * 50)

        # 注册热键
        keyboard.add_hotkey('f8', self.capture_and_send)
        print("✅ 热键已注册: F8")
        print("⏳ 程序运行中，按 F8 开始...")
        print("=" * 50)

        # 等待退出
        keyboard.wait('esc')

        print("\n👋 程序退出")
        print(f"📁 截图保存在: {os.path.abspath(self.screenshots_dir)}")


def main():
    """主函数"""
    print("=" * 50)
    print("腾讯元宝截图上传助手 v5.0")
    print("优化: 针对腾讯元宝界面优化点击位置")
    print("=" * 50)


    assistant = AutoHomeworkAssistant()

    # 检查依赖
    if not assistant._import_dependencies():
        print("\n请按任意键退出...")
        input()
        return 1

    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
        return 0
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)