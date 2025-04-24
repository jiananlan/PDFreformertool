import fitz  # PyMuPDF
import T21

n = 0
text_list = []
all_images_info = []


def judge(text, block_position, blockpage):
    global n, text_list

    def conclude(img_block, text_blick):
        if img_block[0] <= text_blick[0] <= img_block[2] or img_block[0] <= text_blick[2] <= img_block[2]:
            if img_block[1] <= text_blick[1] <= img_block[3] or img_block[1] <= text_blick[3] <= img_block[3]:
                return True
        return False

    for item in all_images_info:
        if blockpage == item['page']:
            if conclude(item['bbox'][0], block_position):
                n += 1
                text_list.append(text)
                return False
    return True


def process_pdf(input_pdf, output_pdf):
    # 打开PDF文件
    doc = fitz.open(input_pdf)

    # 遍历每一页
    for page_num, page in enumerate(doc):
        print(f"Processing page {page_num}...")

        # 获取页面的所有字块
        blocks = page.get_text("dict")["blocks"]

        # 遍历每个字块
        for block in blocks:
            if "lines" not in block:  # 有些块可能没有具体内容，跳过
                continue
            for line in block["lines"]:
                for span in line["spans"]:  # 遍历最小的 span 单位
                    span_text = span["text"]  # 获取文本内容
                    print(f'->[{page_num}]{span["bbox"]}')
                    if judge(span_text, span["bbox"], page_num):  # 如果符合 judge 判定
                        span_bbox = fitz.Rect(span["bbox"])
                        page.add_redact_annot(span_bbox, text="")  # 添加涂抹标注

        # 应用所有标注（擦除内容）
        page.apply_redactions()

    # 保存修改后的 PDF
    doc.save(output_pdf)
    print(f"Processed PDF saved as {output_pdf}")


if __name__ == "__main__":
    pdf_path = r"D:\电脑管家迁移文件\微信聊天记录搬家\WeChat Files\wxid_wbjxn8hzlq6w22\FileStorage\File\2024-11\科研入门培养方案\科研入门培养方案\flash4_ug_4p62.pdf"
    output_pdf = "otput.pdf"

    all_images_info = T21.extract_images_info(pdf_path)
    print([item['bbox'][0] for item in all_images_info])
    T21.delete_images_from_pdf(pdf_path, all_images_info, output_pdf)
    process_pdf(output_pdf, 'oo___000___ottput.pdf')
    print(n)
    print(text_list)
    # insert_image_into_pdf
