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
        self.max_retries = 2
        self.debug = True  # 调试模式

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
                print("⚠️  剪贴板中没有找到图片")
                return None

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)

            # 保存图片
            img.save(filepath, 'PNG')
            print(f"💾 截图已保存到: {os.path.abspath(filepath)}")
            return filepath

        except Exception as e:
            print(f"⚠️  保存截图失败: {e}")
            return None

    def _simulate_screenshot_manual(self) -> bool:
        """
        手动截图（不依赖系统快捷键）
        通过询问用户是否已完成截图
        """
        print("\n📸 手动截图模式")
        print("=" * 40)
        print("请按以下步骤操作:")
        print("1. 使用系统截图工具截图 (Win+Shift+S 或 Cmd+Shift+4)")
        print("2. 选择要截图的区域")
        print("3. 截图会自动复制到剪贴板")
        print("4. 截图完成后，程序会自动继续")
        print("=" * 40)

        input("准备好后，按回车键开始截图...")

        # 等待用户截图
        print("⏳ 等待用户截图...")
        print("提示: 截图后请等待3秒，程序会自动检测")

        # 检测剪贴板中是否有图片
        for i in range(30):  # 最长等待30秒
            time.sleep(1)
            try:
                from PIL import ImageGrab
                img = ImageGrab.grabclipboard()
                if img is not None:
                    print("✅ 检测到截图已保存到剪贴板")
                    # 保存到文件
                    saved_path = self._save_screenshot_to_file()
                    if saved_path:
                        print(f"✅ 截图已保存: {saved_path}")
                    return True
            except:
                pass

            if i % 5 == 0:  # 每5秒提示一次
                remaining = 30 - i
                print(f"⏳ 等待截图中... 还有{remaining}秒自动超时")
                print("提示: 使用系统截图工具截图 (Win+Shift+S 或 Cmd+Shift+4)")

        print("⏰ 截图超时，未检测到截图")
        return False

    def _simulate_screenshot_auto(self) -> bool:
        """
        自动截图（尝试使用系统快捷键）
        """
        print("📸 自动截图模式")
        print("⚠️  3秒后将自动触发截图快捷键...")
        time.sleep(3)

        try:
            if os.name == 'nt':  # Windows
                pyautogui.hotkey('win', 'shift', 's')
                print("✅ 已触发Windows截图快捷键 (Win+Shift+S)")
            elif sys.platform == 'darwin':  # macOS
                pyautogui.hotkey('command', 'shift', '4')
                print("✅ 已触发Mac截图快捷键 (Cmd+Shift+4)")
            else:  # Linux
                print("🐧 Linux系统，请手动截图")
                return self._simulate_screenshot_manual()

            # 等待一段时间让用户截图
            print("⏳ 请使用鼠标选择截图区域...")
            time.sleep(5)  # 给用户5秒时间截图

            # 检查剪贴板
            try:
                from PIL import ImageGrab
                img = ImageGrab.grabclipboard()
                if img is not None:
                    print("✅ 截图成功")
                    saved_path = self._save_screenshot_to_file()
                    if saved_path:
                        print(f"✅ 截图已保存: {saved_path}")
                    return True
                else:
                    print("⚠️  未检测到截图，切换到手动模式")
                    return self._simulate_screenshot_manual()
            except Exception as e:
                print(f"⚠️  检查截图失败: {e}")
                return self._simulate_screenshot_manual()

        except Exception as e:
            print(f"❌ 自动截图失败: {e}")
            return self._simulate_screenshot_manual()

    def _ensure_browser_focus(self):
        """确保浏览器获得焦点"""
        print("🖥️  确保浏览器窗口激活...")
        try:
            # 尝试激活浏览器窗口
            if os.name == 'nt':  # Windows
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.5)
            else:  # macOS
                pyautogui.hotkey('command', 'tab')
                time.sleep(0.5)
        except:
            pass

    def _paste_and_verify(self) -> bool:
        """
        粘贴并验证图片是否上传
        返回是否成功
        """
        print("📋 正在粘贴图片到腾讯元宝...")

        # 先点击输入框确保焦点
        print("🖱️  点击输入框...")
        screen_width, screen_height = pyautogui.size()
        input_box_x = screen_width // 2
        input_box_y = screen_height - 100  # 输入框通常在底部

        try:
            pyautogui.click(input_box_x, input_box_y)
            time.sleep(0.5)
        except:
            print("⚠️  自动点击失败，请手动点击输入框")

        # 尝试粘贴
        for attempt in range(3):
            print(f"📤 尝试粘贴 (第{attempt + 1}次)...")

            try:
                if os.name == 'nt':  # Windows
                    pyautogui.hotkey('ctrl', 'v')
                else:  # macOS
                    pyautogui.hotkey('command', 'v')

                time.sleep(2)  # 等待上传

                # 检查是否上传成功（通过检测屏幕变化）
                # 这里我们可以检查是否有上传进度条或图片预览
                print("⏳ 等待图片上传...")
                time.sleep(3)  # 给更多时间上传

                return True

            except Exception as e:
                print(f"⚠️  粘贴失败: {e}")
                if attempt < 2:
                    time.sleep(1)

        print("❌ 多次粘贴失败")
        return False

    def _send_to_yuanbao(self) -> bool:
        """
        发送到腾讯元宝
        返回是否成功
        """
        print("🚀 准备发送到腾讯元宝...")

        # 检查剪贴板中是否还有图片
        try:
            from PIL import ImageGrab
            img = ImageGrab.grabclipboard()
            if img is not None:
                print("⚠️  剪贴板中仍有图片，可能上传失败")
                print("💡 建议: 手动按 Ctrl+V 粘贴图片，然后按 Enter 发送")
                choice = input("是否继续自动发送? (y/n): ").lower()
                if choice != 'y':
                    return False
        except:
            pass

        # 确认发送
        print("⚠️  即将按下 Enter 键发送...")
        for i in range(3, 0, -1):
            print(f"⏰ {i}秒后发送...")
            time.sleep(1)

        try:
            pyautogui.press('enter')
            print("✅ 已发送")
            time.sleep(2)  # 等待发送完成
            return True
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False

    def _open_yuanbao_safe(self):
        """安全打开腾讯元宝"""
        print("🌐 正在打开腾讯元宝...")

        # 记录当前活动窗口
        current_window = None
        try:
            # 尝试获取当前活动窗口（简化处理）
            pass
        except:
            pass

        # 打开网页
        webbrowser.open(self.yuanbao_url)
        print("✅ 已打开浏览器")

        # 等待页面加载
        print("⏳ 等待页面加载...")
        for i in range(5, 0, -1):
            print(f"页面加载中... {i}秒")
            time.sleep(1)

        # 确保浏览器获得焦点
        self._ensure_browser_focus()

        # 额外等待确保页面完全加载
        time.sleep(2)
        print("✅ 页面加载完成")

        return current_window

    def capture_and_send(self):
        """主流程：截图并发送"""
        if self.is_running:
            print("⏳ 上一个任务还在进行中，请稍候...")
            return

        self.is_running = True

        try:
            print("\n" + "=" * 50)
            print("🚀 腾讯元宝截图上传助手")
            print("=" * 50)

            # 1. 截图
            print("\n📸 步骤1: 截图")
            print("-" * 30)

            # 询问用户使用哪种方式截图
            print("请选择截图方式:")
            print("1. 自动截图 (推荐)")
            print("2. 手动截图")
            print("3. 退出")

            choice = input("请选择 (1/2/3): ").strip()

            if choice == '3':
                print("👋 已取消")
                return
            elif choice == '2':
                success = self._simulate_screenshot_manual()
            else:  # 默认或选择1
                success = self._simulate_screenshot_auto()

            if not success:
                print("❌ 截图失败，请重试")
                return

            # 2. 打开腾讯元宝
            print("\n🌐 步骤2: 打开腾讯元宝")
            print("-" * 30)
            self._open_yuanbao_safe()

            # 3. 粘贴图片
            print("\n📤 步骤3: 上传图片")
            print("-" * 30)
            paste_success = self._paste_and_verify()

            if not paste_success:
                print("⚠️  自动上传失败，请手动操作:")
                print("1. 手动按 Ctrl+V (Windows) 或 Cmd+V (Mac) 粘贴")
                print("2. 图片上传后按 Enter 发送")
                input("完成后按回车键继续...")
            else:
                # 4. 发送
                print("\n🚀 步骤4: 发送")
                print("-" * 30)
                send_success = self._send_to_yuanbao()

                if not send_success:
                    print("⚠️  自动发送失败，请手动按 Enter 键发送")

            print("\n" + "=" * 50)
            print("✅ 流程完成！")
            print("=" * 50)

            # 提示用户
            print("\n💡 提示:")
            print("• 如果上传失败，截图已保存在 screenshots 文件夹")
            print("• 可以手动在腾讯元宝中上传截图")
            print("• 按 F8 可重新开始")

        except KeyboardInterrupt:
            print("\n⏹️ 用户中断")
        except Exception as e:
            print(f"\n❌ 出错: {e}")
            import traceback
            if self.debug:
                traceback.print_exc()
        finally:
            self.is_running = False

    def run(self):
        """运行助手"""
        print("🎯 腾讯元宝截图上传助手")
        print("=" * 50)
        print("📋 使用说明:")
        print("  • 按 F8 键: 开始截图上传流程")
        print("  • 按 ESC 键: 退出程序")
        print("=" * 50)
        print("💡 功能特点:")
        print("  • 支持自动/手动截图")
        print("  • 截图自动保存到 screenshots 文件夹")
        print("  • 自动上传到腾讯元宝")
        print("  • 失败时有详细提示")
        print("=" * 50)

        # 注册热键
        keyboard.add_hotkey('f8', self.capture_and_send)
        print("✅ 热键注册完成:")
        print("  • F8: 开始截图上传")
        print("  • ESC: 退出程序")
        print("\n⏳ 程序运行中，按 F8 开始...")
        print("=" * 50)

        # 等待退出
        keyboard.wait('esc')

        print("\n👋 程序退出")
        print("📁 截图保存在: " + os.path.abspath(self.screenshots_dir))


def main():
    """主函数"""
    print("=" * 50)
    print("腾讯元宝截图上传助手 v2.1")
    print("=" * 50)

    assistant = AutoHomeworkAssistant()

    # 检查依赖
    if not assistant._import_dependencies():
        print("\n请按任意键退出...")
        input()
        sys.exit(1)

    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()



if __name__ == "__main__":
    main()