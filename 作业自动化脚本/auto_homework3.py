import time
import os
import sys
import webbrowser
import tempfile
from typing import Optional
import subprocess


class AutoHomeworkAssistant:
    def __init__(self):
        self.is_running = False
        self.yuanbao_url = "https://yuanbao.tencent.com/chat/naQivTmsDa?projectId=5ff3faf6a751452c99b215fa5aa79a90"
        self.temp_dir = tempfile.gettempdir()
        self.screenshot_timeout = 10  # 截图超时时间(秒)
        self.page_load_delay = 3  # 页面加载等待时间
        self.max_retries = 3  # 最大重试次数

    def _import_dependencies(self) -> bool:
        """动态导入依赖，提供更友好的错误提示"""
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

        if missing_deps:
            print(f"❌ 缺少依赖: {', '.join(missing_deps)}")
            print("请使用以下命令安装:")
            print("pip install pyautogui keyboard pillow")
            return False
        return True

    def _wait_for_screenshot(self, timeout: int = 10) -> bool:
        """
        等待用户完成截图
        通过检测鼠标状态来判断用户是否在截图
        """
        print("⏳ 等待截图完成（支持手动取消）...")
        print("提示: 右键点击或按ESC取消截图")

        start_time = time.time()
        last_mouse_pos = pyautogui.position()
        no_move_count = 0

        while time.time() - start_time < timeout:
            time.sleep(0.5)

            # 检查是否按下ESC键
            if keyboard.is_pressed('esc'):
                print("⏹️ 用户取消截图")
                return False

            # 检测鼠标是否移动（表示用户正在选择区域）
            current_pos = pyautogui.position()
            if current_pos != last_mouse_pos:
                last_mouse_pos = current_pos
                no_move_count = 0
            else:
                no_move_count += 1

            # 如果鼠标一段时间没移动，可能截图已完成
            if no_move_count > 6:  # 3秒没移动
                print("✅ 检测到截图完成")
                time.sleep(0.5)  # 额外等待确保截图保存
                return True

        print("⏰ 截图超时")
        return False

    def _save_screenshot_backup(self, filename: str = "screenshot_backup.png") -> Optional[str]:
        """
        保存截图备份到临时文件
        返回文件路径或None
        """
        try:
            # 尝试从剪贴板获取图片
            import io
            from PIL import Image, ImageGrab

            # 获取剪贴板中的图片
            img = ImageGrab.grabclipboard()
            if img is None:
                return None

            # 保存到临时文件
            filepath = os.path.join(self.temp_dir, filename)
            img.save(filepath, 'PNG')
            print(f"💾 截图已备份到: {filepath}")
            return filepath

        except ImportError:
            print("⚠️  未安装PIL，无法保存截图备份")
            return None
        except Exception as e:
            print(f"⚠️  截图备份失败: {e}")
            return None

    def take_screenshot(self) -> bool:
        """使用系统截图功能"""
        print("=" * 40)
        print("📸 截图助手")
        print("=" * 40)
        print("提示:")
        print("1. 使用鼠标选择截图区域")
        print("2. 右键点击可取消截图")
        print("3. 截图会自动保存到剪贴板")
        print("=" * 40)

        time.sleep(0.5)  # 给用户时间阅读提示

        try:
            # 根据系统使用不同的截图快捷键
            if os.name == 'nt':  # Windows
                print("🖼️  启动Windows截图工具 (Win+Shift+S)")
                pyautogui.hotkey('win', 'shift', 's')
            elif sys.platform == 'darwin':  # macOS
                print("🖼️  启动Mac截图工具 (Cmd+Shift+4)")
                pyautogui.hotkey('command', 'shift', '4')
            else:  # Linux
                print("🐧 尝试Linux截图 (通常为PrintScreen键)")
                # 尝试多种Linux截图方式
                try:
                    pyautogui.hotkey('shift', 'printscreen')
                except:
                    pyautogui.press('printscreen')

            # 等待用户完成截图
            if not self._wait_for_screenshot(self.screenshot_timeout):
                return False

            # 保存截图备份
            self._save_screenshot_backup()

            return True

        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return False

    def _ensure_yuanbao_focused(self) -> bool:
        """
        确保腾讯元宝窗口获得焦点
        返回是否成功
        """
        try:
            # 尝试激活浏览器窗口
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.5)
            return True
        except:
            return False

    def _paste_with_retry(self, max_retries: int = 3) -> bool:
        """
        尝试粘贴图片，支持重试
        返回是否成功
        """
        for attempt in range(max_retries):
            try:
                print(f"📋 尝试粘贴图片 (第{attempt + 1}次)...")

                # 根据系统使用不同的粘贴快捷键
                if os.name == 'nt':  # Windows/Linux
                    pyautogui.hotkey('ctrl', 'v')
                else:  # macOS
                    pyautogui.hotkey('command', 'v')

                time.sleep(1)  # 等待粘贴完成
                return True

            except Exception as e:
                print(f"⚠️  粘贴失败: {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.5)

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
            if not self.take_screenshot():
                print("❌ 截图流程中断")
                return

            # 2. 打开腾讯元宝
            print("\n步骤2: 打开腾讯元宝")
            print(f"🌐 正在打开: {self.yuanbao_url}")

            # 尝试在新标签页打开
            webbrowser.open_new_tab(self.yuanbao_url)
            time.sleep(self.page_load_delay)

            # 3. 确保窗口获得焦点
            print("\n步骤3: 激活窗口")
            if not self._ensure_yuanbao_focused():
                print("⚠️  无法自动激活窗口，请手动点击腾讯元宝窗口")
                time.sleep(1)

            # 4. 粘贴图片
            print("\n步骤4: 粘贴图片")
            if not self._paste_with_retry():
                print("❌ 粘贴失败，请手动粘贴 (Ctrl+V 或 Cmd+V)")
                return

            # 5. 发送
            print("\n步骤5: 发送")
            time.sleep(1)  # 给粘贴一点时间
            pyautogui.press('enter')

            print("\n" + "=" * 50)
            print("✅ 完成！截图已发送到腾讯元宝")
            print("=" * 50)

        except Exception as e:
            print(f"\n❌ 流程出错: {e}")
            print("💡 建议:")
            print("1. 检查网络连接")
            print("2. 确保腾讯元宝页面已加载")
            print("3. 尝试手动操作 (Ctrl+V 粘贴, Enter 发送)")

        finally:
            self.is_running = False
            time.sleep(1)  # 防止快速重复触发

    def _cleanup_temp_files(self):
        """清理临时文件（可选）"""
        try:
            backup_file = os.path.join(self.temp_dir, "screenshot_backup.png")
            if os.path.exists(backup_file):
                os.remove(backup_file)
                print("🧹 已清理临时文件")
        except:
            pass

    def run(self):
        """运行助手"""
        print("🎯 腾讯元宝截图上传助手")
        print("=" * 50)
        print("📋 使用说明:")
        print("  • 按 F8 键: 开始截图上传")
        print("  • 按 ESC 键: 退出程序")
        print("  • 截图时按 ESC 或右键: 取消截图")
        print("=" * 50)
        print("💡 提示:")
        print("  • 截图会自动保存到剪贴板")
        print("  • 失败时会自动重试")
        print("  • 支持 Windows/macOS/Linux")
        print("=" * 50)

        # 注册热键
        keyboard.add_hotkey('f8', self.capture_and_send)
        keyboard.add_hotkey('ctrl+shift+f8', self._cleanup_temp_files)  # 清理热键

        print("✅ 热键注册完成:")
        print("  • F8: 开始截图上传")
        print("  • Ctrl+Shift+F8: 清理临时文件")
        print("  • ESC: 退出程序")
        print("\n⏳ 程序运行中...")

        # 等待退出
        keyboard.wait('esc')

        print("\n" + "=" * 50)
        print("👋 程序退出")
        print("=" * 50)

        # 清理
        self._cleanup_temp_files()


def main():
    """主函数"""
    assistant = AutoHomeworkAssistant()

    # 检查依赖
    if not assistant._import_dependencies():
        sys.exit(1)

    # 显示欢迎信息
    print("=" * 50)
    print("腾讯元宝截图上传助手 v2.0")
    print("=" * 50)

    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        print("请检查:")
        print("1. 是否安装所有依赖")
        print("2. 是否有足够的权限")
        print("3. 是否在其他程序中使用")




if __name__ == "__main__":
    main()