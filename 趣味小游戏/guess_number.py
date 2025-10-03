import random

def main():
    secret_number = random.randint(1, 500)
    print("I'm thinking of a number between 1 and 500.")
    print("Type 'quit' or 'exit' to quit the game at any time.")
    attempts = 0
    quit_commands = {'quit', 'exit'}
    while True:
        user_input = input("Take a guess (or 'quit' to exit): ").strip() # 先获取用户输入的字符串

        # 处理空输入
        if not user_input:
            print("Please enter a valid number.")
            continue

        # 处理退出命令
        if user_input.lower() in quit_commands:
            print(f"The number was {secret_number}. Thanks for playing!")
            break

        # 尝试转换为整数
        try:
            guess = int(user_input)
            if guess < 1 or guess > 500:
                print("Please enter a number between 1 and 500.")
                continue

            attempts += 1
            if guess < secret_number:
                print("Your guess is too low.")
            elif guess > secret_number:
                print("Your guess is too high.")
            else:
                print(f"Good job! You guessed my number in {attempts} guesses!")
                break
        except ValueError:
            print("Please enter a valid number.")
            continue



if __name__ == "__main__":
    main()