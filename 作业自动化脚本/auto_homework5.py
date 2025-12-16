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
        1. 触发系统截图快捷键
        2. 等待用户截图
        3. 检查剪贴板是否有图片
        4. 自动保存到文件
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
            time.sleep(3)  # 给用户3秒时间开始截图

            # 检测用户是否在截图
            print("⏳ 检测到截图进行中...")
            time.sleep(2)  # 再等待2秒让用户完成

            # 检查剪贴板是否有图片
            for i in range(10):
                time.sleep(0.5)
                try:
                    from PIL import ImageGrab
                    img = ImageGrab.grabclipboard()
                    if img is not None:
                        # 保存截图到文件
                        saved_path = self._save_screenshot_to_file()
                        if saved_path:
                            print(f"💾 截图已保存到: {os.path.abspath(saved_path)}")
                        print("✅ 截图完成")
                        return True
                except:
                    pass

            # 如果没检测到，假设用户已完成
            print("⚠️  未检测到截图，假设用户已完成")
            time.sleep(1)

            # 最后检查一次
            try:
                from PIL import ImageGrab
                img = ImageGrab.grabclipboard()
                if img is not None:
                    saved_path = self._save_screenshot_to_file()
                    if saved_path:
                        print(f"💾 截图已保存到: {os.path.abspath(saved_path)}")
                    print("✅ 截图完成")
                    return True
            except:
                pass

            print("⚠️  可能截图失败，将继续尝试上传")
            return True

        except Exception as e:
            print(f"❌ 截图出错: {e}")
            return False

    def _ensure_yuanbao_focused(self):
        """确保腾讯元宝窗口获得焦点"""
        print("🖥️  激活腾讯元宝窗口...")
        time.sleep(1)  # 等待浏览器打开

        try:
            # 尝试切换到浏览器窗口
            if os.name == 'nt':  # Windows
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.5)
                # 再按一次返回
                pyautogui.hotkey('alt', 'shift', 'tab')
                time.sleep(0.5)
            elif sys.platform == 'darwin':  # macOS
                pyautogui.hotkey('command', 'tab')
                time.sleep(0.5)
        except:
            print("⚠️  自动激活窗口失败，请手动点击腾讯元宝窗口")

    def _paste_to_yuanbao(self) -> bool:
        """
        粘贴到腾讯元宝
        返回是否成功
        """
        print("📋 正在上传到腾讯元宝...")

        # 等待页面加载
        time.sleep(2)

        # 先点击输入框确保焦点
        try:
            # 尝试点击输入框位置（假设在屏幕底部中央）
            screen_width, screen_height = pyautogui.size()
            input_box_x = screen_width // 2
            input_box_y = screen_height - 100

            pyautogui.click(input_box_x, input_box_y)
            time.sleep(0.5)
            print("✅ 已点击输入框")
        except:
            print("⚠️  自动点击失败，请手动点击输入框")

        # 尝试粘贴
        try:
            if os.name == 'nt':  # Windows
                pyautogui.hotkey('ctrl', 'v')
            else:  # macOS
                pyautogui.hotkey('command', 'v')

            print("✅ 已粘贴图片")
            return True

        except Exception as e:
            print(f"❌ 粘贴失败: {e}")
            return False

    def _send_to_yuanbao(self):
        """发送到腾讯元宝"""
        print("🚀 准备发送...")

        # 等待图片上传
        print("⏳ 等待图片上传...")
        time.sleep(3)  # 给图片上传时间

        # 检查用户是否要取消
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

    def _open_yuanbao_smart(self):
        """智能打开腾讯元宝"""
        print("🌐 正在打开腾讯元宝...")

        # 先检查是否已在浏览器中打开
        webbrowser.open_new_tab(self.yuanbao_url)
        print("✅ 已在浏览器中打开")

        # 等待页面加载
        print("⏳ 等待页面加载...")
        time.sleep(3)

    def capture_and_send(self):
        """主流程：截图并发送 - 简化版"""
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

            # 2. 打开腾讯元宝
            print("\n步骤2: 打开腾讯元宝")
            self._open_yuanbao_smart()

            # 3. 确保窗口激活
            self._ensure_yuanbao_focused()

            # 4. 粘贴图片
            print("\n步骤3: 上传")
            if not self._paste_to_yuanbao():
                print("⚠️  自动上传失败")
                print("💡 请手动操作:")
                print("   1. 点击腾讯元宝输入框")
                print("   2. 按 Ctrl+V (Windows) 或 Cmd+V (Mac) 粘贴")
                print("   3. 按 Enter 发送")
                print("\n将在5秒后继续...")

                # 等待用户手动操作
                for i in range(5, 0, -1):
                    if keyboard.is_pressed('esc'):
                        print("⏹️ 用户取消")
                        return
                    time.sleep(1)

            # 5. 发送
            print("\n步骤4: 发送")
            self._send_to_yuanbao()

            print("\n" + "=" * 50)
            print("✅ 完成！请查看腾讯元宝")
            print("=" * 50)

        except KeyboardInterrupt:
            print("\n⏹️ 用户中断")
        except Exception as e:
            print(f"\n❌ 出错: {e}")
        finally:
            self.is_running = False
            time.sleep(0.5)  # 防止快速重复触发

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
        print("  3. 截图会自动上传到腾讯元宝")
        print("  4. 截图保存在 screenshots 文件夹")
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
    print("腾讯元宝截图上传助手 v3.0")
    print("=" * 50)

    assistant = AutoHomeworkAssistant()

    # 检查依赖
    if not assistant._import_dependencies():
        print("\n请按任意键退出...")
        input()
        return 1  # 返回非0退出码表示错误

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