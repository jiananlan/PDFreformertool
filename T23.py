import fitz  # PyMuPDF

doc = fitz.open(
    r"C:\Users\anlan\Documents\WeChat Files\wxid_wbjxn8hzlq6w22\FileStorage\File\2025-04\PhysRevE.111.035406.pdf"
)  # 打开 PDF 文件
for page_num, page in enumerate(doc):
    text_data = page.get_text("dict")  # 获取文本的字典结构
    for block in text_data["blocks"]:  # 遍历所有文本块
        if "lines" in block:  # 确保是文本块（排除图片等其他块）
            for line in block["lines"]:  # 遍历每一行
                for span in line["spans"]:  # 遍历每个 span（文本段）
                    text = span["text"]  # 文本内容
                    font = span["font"]  # 字体
                    font_size = span["size"]  # 字体大小
                    print(
                        f"Page {page_num} - Block({span["bbox"]}) - Font: {font}, Size: {font_size}, Text: {text}"
                    )
