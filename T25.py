# Compare 2 PDF

import fitz  # PyMuPDF
import sys


def merge_a4_to_a3(pdf_path1, pdf_path2, output_path):
    doc1 = fitz.open(pdf_path1)
    doc2 = fitz.open(pdf_path2)

    if len(doc1) != len(doc2):
        raise ValueError("两个PDF页数不同！")

    output_pdf = fitz.open()

    for i in range(len(doc1)):
        page1 = doc1[i]
        page2 = doc2[i]

        # 获取 A4 尺寸（一般是 595 x 842 点）
        rect = page1.rect
        a4_width, a4_height = rect.width, rect.height

        # 创建 A3 横向页面（A4 高度，宽度为 2 倍 A4 宽度）
        a3_width = a4_width * 2
        a3_height = a4_height
        a3_page = output_pdf.new_page(width=a3_width, height=a3_height)

        # 将两个 A4 页面分别贴到 A3 的左侧和右侧
        a3_page.show_pdf_page(
            fitz.Rect(0, 0, a4_width, a4_height),
            doc1,
            i
        )
        a3_page.show_pdf_page(
            fitz.Rect(a4_width, 0, a3_width, a4_height),
            doc2,
            i
        )

    output_pdf.save(output_path)
    print(f"合并完成，保存为：{output_path}")


# 使用示例（修改为你自己的文件路径）
merge_a4_to_a3(r"C:\Users\anlan\Desktop\翻译件\XPLANE塞斯纳奖状指南.pdf", r"E:\SteamLibrary\steamapps\common\X-Plane 12\Aircraft\Laminar Research\Cessna Citation X\X-Plane Citation X FMS Manual.pdf"
, "Tmerged_a3.pdf")
