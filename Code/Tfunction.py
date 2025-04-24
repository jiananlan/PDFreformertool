import secrets
import string


def generate_random_filename(length=12, end=".docx"):
    """
    生成一个随机的合法文件名。

    参数:
        length (int): 文件名的长度（至少1个字符）。

    返回:
        str: 随机生成的文件名。

    异常:
        ValueError: 如果长度小于1。
    """
    if length < 1:
        raise ValueError("文件名长度必须至少为1")

    # 允许的字符集：字母、数字、连字符(-)、下划线(_)
    allowed_chars = string.ascii_letters + string.digits + "-_"

    # 确保首字符为字母（避免以数字或符号开头）
    first_char = secrets.choice(string.ascii_letters)
    remaining_chars = "".join(secrets.choice(allowed_chars) for _ in range(length - 1))

    return first_char + remaining_chars + end


# 示例用法
if __name__ == "__main__":
    filename = generate_random_filename()
    print(filename)  # 输出类似 "x3a8K_-9vD2z"
