import time
import os
import sys
from datetime import datetime
from typing import Optional


class AutoHomeworkAssistant:
    def __init__(self):
        self.is_running = False
        self.screenshots_dir = "screenshots"

        # 使用您提供的准确坐标
        self.input_box_x = 770
        self.input_box_y = 930

        # 等待时间设置
        self.after_screenshot_wait = 1
        self.page_activate_wait = 2
        self.page_refresh_wait = 2
        self.after_paste_wait = 3

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
        """保存截图到文件"""
        try:
            from PIL import ImageGrab

            img = ImageGrab.grabclipboard()
            if img is None:
                return None

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)

            img.save(filepath, 'PNG')
            return filepath

        except Exception:
            return None

    def _take_screenshot_simple(self) -> bool:
        """截图功能"""
        print("\n📸 正在启动截图...")
        print("请用鼠标选择截图区域")
        print("截图会自动保存到剪贴板")

        try:
            if os.name == 'nt':  # Windows
                pyautogui.hotkey('win', 'shift', 's')
                print("✅ 已触发 Windows 截图 (Win+Shift+S)")
            elif sys.platform == 'darwin':  # macOS
                pyautogui.hotkey('command', 'shift', '4')
                print("✅ 已触发 Mac 截图 (Cmd+Shift+4)")
            else:  # Linux
                pyautogui.hotkey('shift', 'printscreen')
                print("✅ 已触发 Linux 截图")

            # 等待用户截图
            print("⏳ 请用鼠标选择截图区域...")
            time.sleep(5)  # 给用户5秒时间截图

            # 检查剪贴板是否有图片
            for i in range(5):
                time.sleep(1)
                try:
                    from PIL import ImageGrab
                    img = ImageGrab.grabclipboard()
                    if img is not None:
                        # 保存截图
                        saved_path = self._save_screenshot_to_file()
                        if saved_path:
                            print(f"💾 截图已保存: {saved_path}")
                        print("✅ 截图完成")
                        return True
                except:
                    pass

            print("⚠️  未检测到截图，但继续流程")
            return True

        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return False

    def _activate_browser_window(self):
        """激活浏览器窗口"""
        print("\n🌐 正在激活浏览器窗口...")

        # 等待一下，确保截图已完成
        time.sleep(self.after_screenshot_wait)

        # 先切换到浏览器
        try:
            if os.name == 'nt':  # Windows
                # Alt+Tab 切换到浏览器
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.5)
                print("✅ 已切换到浏览器窗口")
            elif sys.platform == 'darwin':  # macOS
                # Command+Tab 切换到浏览器
                pyautogui.hotkey('command', 'tab')
                time.sleep(0.5)
                print("✅ 已切换到浏览器窗口")
        except Exception as e:
            print(f"⚠️  切换窗口失败: {e}")
            print("💡 请手动点击浏览器窗口")

        # 等待浏览器激活
        time.sleep(self.page_activate_wait)

    def _refresh_yuanbao_page(self):
        """刷新腾讯元宝页面"""
        print("🔄 刷新页面...")

        try:
            # 按F5刷新页面
            pyautogui.press('f5')
            print("✅ 已刷新页面")

            # 等待页面加载
            time.sleep(self.page_refresh_wait)

        except Exception as e:
            print(f"⚠️  刷新页面失败: {e}")

    def _focus_input_box(self):
        """聚焦输入框"""
        print(f"🎯 聚焦输入框 ({self.input_box_x}, {self.input_box_y})...")

        try:
            # 移动鼠标到输入框位置
            pyautogui.moveTo(self.input_box_x, self.input_box_y, duration=0.5)
            time.sleep(0.5)

            # 点击输入框
            pyautogui.click(self.input_box_x, self.input_box_y)
            time.sleep(0.5)

            print("✅ 已点击输入框")
            return True

        except Exception as e:
            print(f"❌ 点击输入框失败: {e}")
            return False

    def _paste_screenshot(self):
        """粘贴截图"""
        print("📋 粘贴截图...")

        try:
            if os.name == 'nt':  # Windows
                pyautogui.hotkey('ctrl', 'v')
            else:  # macOS
                pyautogui.hotkey('command', 'v')

            print("✅ 已粘贴")

            # 等待图片上传
            time.sleep(self.after_paste_wait)

            return True

        except Exception as e:
            print(f"❌ 粘贴失败: {e}")
            return False

    def _send_to_yuanbao(self):
        """发送到腾讯元宝"""
        print("🚀 发送...")

        try:
            pyautogui.press('enter')
            print("✅ 已发送")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False

    def capture_and_send(self):
        """主流程"""
        if self.is_running:
            print("⏳ 上一个任务还在进行中，请稍候...")
            return

        self.is_running = True

        try:
            print("\n" + "=" * 50)
            print("🚀 腾讯元宝截图上传")
            print("=" * 50)

            # 1. 截图
            print("\n步骤1: 截图")
            if not self._take_screenshot_simple():
                print("❌ 截图失败")
                return

            # 2. 激活浏览器窗口
            print("\n步骤2: 激活浏览器窗口")
            self._activate_browser_window()

            # 3. 刷新页面
            self._refresh_yuanbao_page()

            # 4. 点击输入框
            print("\n步骤3: 点击输入框")
            if not self._focus_input_box():
                print("⚠️  点击输入框失败")
                print("💡 请手动点击输入框，然后按F8继续")
                print("⏳ 等待5秒...")
                time.sleep(5)

                # 重试一次
                self._focus_input_box()

            # 5. 粘贴截图
            print("\n步骤4: 粘贴截图")
            if not self._paste_screenshot():
                print("⚠️  粘贴失败")
                print("💡 请手动按 Ctrl+V 或 Cmd+V 粘贴")
                print("⏳ 等待5秒...")
                time.sleep(5)

            # 6. 发送
            print("\n步骤5: 发送")
            self._send_to_yuanbao()

            print("\n" + "=" * 50)
            print("✅ 完成！截图已发送到腾讯元宝")
            print("=" * 50)

        except KeyboardInterrupt:
            print("\n⏹️ 用户中断")
        except Exception as e:
            print(f"\n❌ 出错: {e}")
        finally:
            self.is_running = False

    def run(self):
        """运行助手"""
        print("🎯 腾讯元宝截图上传助手")
        print("=" * 50)
        print("📋 使用说明:")
        print("  1. 确保腾讯元宝页面已在浏览器中打开")
        print("  2. 确保在'111'分组页面")
        print("  3. 按 F8 开始截图上传")
        print("  4. 按 ESC 退出程序")
        print("=" * 50)
        print("💡 流程:")
        print("  F8 → 截图 → 切换窗口 → 刷新 → 点击输入框 → 粘贴 → 发送")
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
    print("腾讯元宝截图上传助手 v9.0")
    print("修复: 跳转网页问题")
    print("=" * 50)
    print("🎯 特别注意:")
    print("  1. 运行前请先打开腾讯元宝页面")
    print("  2. 确保在正确的分组页面")
    print("  3. 程序通过Alt+Tab切换窗口")
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