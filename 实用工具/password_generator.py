import secrets
import string
import random
from datetime import datetime
import os

"""
密码生成器，要求必须含有字母大小写、数字、特殊字符，可选定长度
"""


# 标准标点符号集合定义
PUNCTUATION_CHARS = "!@#$%^&*"
# 密码记录文件名
PASSWORD_LOG_FILE = "generated_passwords.txt"


def get_password_length() -> int | None:
    """获取用户输入的密码长度，支持重复输入直到有效"""
    while True:
        try:
            length = int(input("请输入密码的长度："))
            if length <= 0:
                print("密码长度必须是正整数，请重新输入。")
                continue
            if length > 512:  # 更严格的上限控制以减少资源消耗风险
                print("密码长度不能超过512，请重新输入。")
                continue
            if length < 4:
                print("密码长度至少为4位，以确保包含各类字符，请重新输入。")
                continue
            return length
        except ValueError:
            print("输入无效，请输入一个整数。")
        except KeyboardInterrupt:
            print("\n程序已退出。")
            raise


def generate_password(length: int) -> str:
    """生成指定长度的随机密码，确保包含各类字符"""
    if not isinstance(length, int):
        raise ValueError("密码长度必须是整数")

    # 定义各类字符集合
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = PUNCTUATION_CHARS

    # 确保至少包含每类字符各一个
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(punctuation)
    ]

    # 组合所有字符集合
    all_characters = lowercase + uppercase + digits + punctuation

    # 填充剩余长度
    for _ in range(length - 4):
        password.append(secrets.choice(all_characters))

    # 使用安全随机数源进行洗牌操作
    random.SystemRandom().shuffle(password)

    return ''.join(password)


def save_password_to_file(password: str) -> None:
    """将生成的密码保存到文件中"""
    try:
        # 获取当前时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 追加写入文件
        with open(PASSWORD_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {password}\n")
        print(f"密码已保存到 {PASSWORD_LOG_FILE}")
    except Exception as e:
        print(f"保存密码到文件时发生错误：{e}")


if __name__ == '__main__':
    try:
        length = get_password_length()
        password = generate_password(length)
        print("生成的密码为：", password)
        # 保存密码到文件
        save_password_to_file(password)
        print("文件将保存在:", os.path.abspath(PASSWORD_LOG_FILE))
    except ValueError as e:
        print(f"输入错误：{e}")
    except MemoryError:
        print("密码长度过大，内存不足")
    except SystemExit:
        pass
    except Exception as e:
        print(f"生成密码时发生未知错误：{e}")
