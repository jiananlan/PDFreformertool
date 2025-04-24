import fitz  # PyMuPDF


def extract_text_and_font_info(pdf_path):
    # 打开PDF文件
    doc = fitz.open(pdf_path)

    # 遍历每一页
    for page_num in range(89, 91):
        page = doc.load_page(page_num)

        # 获取页面的所有字块（每个字块包括字形、位置等信息）
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            # 只处理包含文字的块
            if block["type"] == 0:
                for line in block["lines"]:
                    print(line)
                    for span in line["spans"]:
                        # 打印文本、位置和字体信息
                        print(f"[{page_num}]Text: {span['text']}")
                        print(
                            f"Position: {span['bbox']}"
                        )  # bbox是字块的矩形框位置 (x0, y0, x1, y1)
                        print(f"Font: {span['font']}")  # 字体信息
                        print(f"Font size: {span['size']}")  # 字体大小
                        print("-" * 40)


# 示例：提取PDF中的所有字块信息
pdf_path = r"C:\Users\anlan\Desktop\科研入门培养方案\flash4_ug_4p62.pdf"  # 替换为你的PDF文件路径
extract_text_and_font_info(pdf_path)
