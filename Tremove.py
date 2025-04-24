import os
import hashlib
from docx import Document


def get_text_from_docx(file_path):
    """提取 Word 文件中的文本"""
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"无法读取 Word 文件 {file_path}，错误: {e}")
        return None


def find_and_remove_duplicates(directory):
    """查找并删除重复的 Word 文件，保留日期最新的一个"""
    text_dict = {}

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".docx"):
                file_text = get_text_from_docx(file_path)

                if file_text is not None:
                    # 计算文本的 MD5 哈希
                    file_hash = hashlib.md5(file_text.encode("utf-8")).hexdigest()
                    # 获取文件的最后修改时间
                    file_mtime = os.path.getmtime(file_path)

                    if file_hash in text_dict:
                        # 比较文件的最后修改时间，保留修改时间最新的文件
                        existing_file, existing_mtime = text_dict[file_hash]
                        if file_mtime > existing_mtime:
                            # 删除旧文件，保留新文件
                            print(f"删除旧文件: {existing_file}😎{file_path}")
                            os.remove(existing_file)
                            text_dict[file_hash] = (file_path, file_mtime)
                        else:
                            # 否则删除当前文件
                            print(f"删除重复文件: {file_path}😎{existing_file}")
                            os.remove(file_path)
                    else:
                        text_dict[file_hash] = (file_path, file_mtime)


if __name__ == "__main__":
    directory = r"D:\PYTHON\new\MATHbuildingMODEL\Output_File"
    find_and_remove_duplicates(directory)
